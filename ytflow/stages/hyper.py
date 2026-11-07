"""미주일기(paper) 카드를 HyperFrames(HTML + GSAP → MP4)로 그리는 렌더러.

paper.py 와 같은 종이 배경·폰트·색을 쓰고, 움직임만 HTML 로 만든다:
- 손그림 선(밑줄·상자·동그라미·화살표)은 SVG 경로를 stroke-dashoffset 으로 '그려 나가게'
- 글자는 아래에서 떠오르며 나타나고, 숫자는 0부터 올라간다(GSAP 타임라인에 묶여 프레임마다 같은 결과)
- 배치는 Python 에서 글자 폭을 재서(paper.fit) 정하므로 겹치지 않는다. 렌더 전 `hyperframes check` 가 한 번 더 본다.

지원 카드: text · number_compare · analogy · flow · table · bars · headline. 그 밖(chart·line)은 paper.py 로.
필요: tools/hyperframes 에 고정 버전 설치 (python scripts/install_tools.py). 없으면 paper.py 로 자동 대체.
"""
from __future__ import annotations

import html
import json
import math
import os
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np

from .. import config
from . import paper
from .paper import FT, fit, ellipse_path, rect_path, arrow_path, wobble

TOOLS = config.ROOT / "tools" / "hyperframes"
BIN = TOOLS / "node_modules" / ".bin" / "hyperframes"
GSAP = TOOLS / "node_modules" / "gsap" / "dist" / "gsap.min.js"
ROUGH = TOOLS / "node_modules" / "roughjs" / "bundled" / "rough.cjs.js"   # rough.js (MIT): 손그림 선·빗금 채우기
ROUGH_JS = config.ROOT / "ytflow" / "assets" / "rough_paths.mjs"
SUPPORTED = {"text", "number_compare", "analogy", "flow", "table", "bars", "headline"}


def available() -> bool:
    return BIN.exists() and GSAP.exists() and shutil.which("ffmpeg") is not None


def _env() -> dict:
    env = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1")  # 사용 통계 전송 끔
    shell = next(Path("/opt/pw-browsers").glob("chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell"), None) \
        if Path("/opt/pw-browsers").exists() else None
    if shell and "PRODUCER_HEADLESS_SHELL_PATH" not in env:
        env["PRODUCER_HEADLESS_SHELL_PATH"] = str(shell)
    return env


def _hex(c) -> str:
    return c if isinstance(c, str) else "#%02x%02x%02x" % tuple(c[:3])


def _d(points) -> str:
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points)


class Doc:
    """요소를 순서대로 쌓는다. 각 요소는 (html, gsap 문장)."""

    def __init__(self, seed: int):
        c = paper.cfg()
        self.W, self.H, self.c = c["W"], c["H"], c
        self.ink, self.red = c["ink"], c["red"]
        m = np.array(paper._rgb(c["ink"])) * 0.72 + np.array(paper._rgb(c["base"])) * 0.28  # 대비 3:1 이상
        self.muted = _hex(tuple(int(v) for v in m))
        self.rng = np.random.default_rng(seed)
        self.seed = seed
        self.items, self.svg, self.js, self.t, self.n = [], [], [], 0.25, 0
        self.rq = []  # rough.js 도형 대기열: html() 때 node 로 한 번에 경로를 만든다
        e = config.load("pipeline").get("edit", {})
        self.use_rough = bool(e.get("rough", True)) and ROUGH.exists() and shutil.which("node") is not None

    def _id(self):
        self.n += 1
        return f"e{self.n}"

    def at(self, at, gap):
        t = self.t if at is None else at
        self.t = t + gap
        return t

    def text(self, x, y, s, font_path, size, color, at=None, gap=0.12, dur=0.45, anchor="mm", counter=False):
        i = self._id()
        fam = {paper.SERIF: "serif-x", paper.SERIF_B: "serif-b", paper.PEN: "pen", paper.SANS: "sans",
               paper.SANS_X: "sans-x"}.get(Path(font_path), "sans")
        ax = {"m": "-50%", "l": "0", "r": "-100%"}[anchor[0]]
        style = (f"left:{x:.0f}px;top:{y:.0f}px;font-family:{fam};font-size:{size:.0f}px;color:{color};"
                 f"transform:translate({ax},-50%)")
        self.items.append(f'<div id="{i}w" class="t" style="{style}"><span id="{i}">{html.escape(s)}</span></div>')
        t = self.at(at, gap)
        self.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:18}},{{opacity:1,y:0,duration:{dur},ease:"power2.out"}},{t:.2f});')
        m = re.search(r"\d[\d,]*(?:\.\d+)?", s)
        if counter and m and len(re.findall(r"\d[\d,]*(?:\.\d+)?", s)) == 1:
            num, dec = float(m.group().replace(",", "")), len(m.group().split(".")[1]) if "." in m.group() else 0
            pre, post = json.dumps(s[:m.start()]), json.dumps(s[m.end():])
            self.js.append(
                f'(function(){{const o={{v:0}},el=document.getElementById("{i}");'
                f'tl.to(o,{{v:{num},duration:0.9,ease:"power2.out",onUpdate:()=>{{el.textContent={pre}+'
                f'o.v.toLocaleString("en-US",{{minimumFractionDigits:{dec},maximumFractionDigits:{dec},useGrouping:{str("," in m.group()).lower()}}})+{post};}}}},{t:.2f});'
                f'tl.set(o,{{v:{num}}},{t + 0.9:.2f});}})();')
        return t

    def stroke(self, points, color, width=4, at=None, gap=0.1, dur=0.5):
        i = self._id()
        self.svg.append(f'<path id="{i}" d="{_d(points)}" fill="none" stroke="{color}" stroke-width="{width}" '
                        f'stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
        t = self.at(at, gap)
        self.js.append(f'tl.to("#{i}",{{strokeDashoffset:0,duration:{dur},ease:"power1.inOut"}},{t:.2f});')
        return t

    def rough(self, kind, args, color, width=3, fill=None, at=None, gap=0.1, dur=0.5, roughness=1.3):
        """rough.js 도형 하나 (선 + 빗금 채우기). 모든 선이 펜으로 그려지듯 나타난다."""
        k = len(self.rq)
        opts = {"seed": int(self.seed * 97 + k + 1), "roughness": roughness, "bowing": 1.2, "stroke": color, "strokeWidth": width}
        if fill:
            opts.update({"fill": fill, "fillStyle": "hachure", "hachureGap": 9, "hachureAngle": -41, "fillWeight": 2.2})
        if getattr(self, "rough_hook", None):  # 그래픽 스킨: 선 질감(거칠기·채우기 방식)
            opts = self.rough_hook(opts)
        self.rq.append({"type": kind, "args": args, "opts": opts})
        self.svg.append(f"@@ROUGH{k}@@")
        t = self.at(at, gap)
        self.js.append(f'tl.to(".r{k}",{{strokeDashoffset:0,duration:{dur},ease:"power1.inOut",stagger:{min(0.04, dur / 12):.3f}}},{t:.2f});')
        if fill and opts.get("fillStyle") == "solid":
            self.js.append(f'tl.to(".r{k}f",{{opacity:1,duration:{max(dur, 0.2):.2f},ease:"power1.out"}},{t:.2f});')
        return t

    def _rough_svg(self, svg: str) -> str:
        if not self.rq:
            return svg
        r = subprocess.run(["node", str(ROUGH_JS), str(ROUGH)], input=json.dumps(self.rq), capture_output=True, text=True, timeout=60)
        shapes = json.loads(r.stdout)
        for k, paths in enumerate(shapes):
            el = "".join(
                (f'<path class="r{k}f" d="{p["d"]}" fill="{p["fill"]}" stroke="none" style="opacity:0"/>'   # 면 채우기(solid): 서서히 나타남
                 if p.get("fill") and p["fill"] != "none" else
                 f'<path class="r{k}" d="{p["d"]}" fill="none" stroke="{p["stroke"]}" stroke-width="{p["w"]}" '
                 f'stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>') for p in paths)
            svg = svg.replace(f"@@ROUGH{k}@@", el)
        return svg

    def underline(self, x0, x1, y, at=None):
        if self.use_rough:
            return self.rough("line", [x0, y, x1, y + self.rng.uniform(-3, 3)], self.red, 3.5, at=at, dur=0.35, roughness=1.0)
        return self.stroke(wobble([(x0, y), (x1, y + self.rng.uniform(-3, 3))], self.rng, amp=1.6), self.red, 4, at, 0.1, 0.35)

    def box(self, x0, y0, x1, y1, color, width=4, at=None, fill=None):
        if self.use_rough:
            return self.rough("rectangle", [x0, y0, x1 - x0, y1 - y0], color, width - 0.5, fill=fill, at=at, dur=0.5)
        return self.stroke(rect_path(x0, y0, x1, y1, self.rng), color, width, at, 0.1, 0.45)

    def circle(self, cx, cy, rx, ry, at=None):
        if self.use_rough:
            return self.rough("ellipse", [cx, cy, rx * 2, ry * 2], self.red, 3.5, at=at, dur=0.55, roughness=1.6)
        return self.stroke(ellipse_path(cx, cy, rx, ry, self.rng), self.red, 4, at, 0.1, 0.55)

    def arrow(self, x0, y0, x1, y1, color, at=None):
        body, head = arrow_path(x0, y0, x1, y1, self.rng)
        if self.use_rough:
            t = self.rough("line", [x0, y0, x1, y1], color, 3.5, at=at, gap=0.05, dur=0.35, roughness=0.9)
            self.rough("linearPath", [[list(p) for p in head]], color, 3.5, at=t + 0.3, dur=0.15, roughness=0.6)
            return t
        t = self.stroke(body, color, 4, at, 0.05, 0.35)
        self.stroke(head, color, 4, t + 0.3, 0.1, 0.15)
        return t

    def marker(self, x0, cy, w, h, at=None, index=None):
        """형광펜: 왼쪽에서 오른쪽으로 칠해지는 반투명 노란 띠 (글자 뒤)."""
        i = self._id()
        el = (f'<div id="{i}" style="position:absolute;left:{x0:.0f}px;top:{cy - h / 2:.0f}px;width:{w:.0f}px;height:{h:.0f}px;'
              f'background:#F3D36B;opacity:.5;border-radius:6px;transform-origin:left center"></div>')
        self.items.insert(index if index is not None else 0, el)
        t = self.at(at, 0.1)
        self.js.append(f'tl.fromTo("#{i}",{{scaleX:0}},{{scaleX:1,duration:0.55,ease:"power1.inOut"}},{t:.2f});')
        return t

    def icon(self, name, cx, cy, size, color, at=None, gap=0.1):
        from .icons import svg_markup
        mk = svg_markup(name, size, color) if name else None
        if not mk:
            return self.t
        i = self._id()
        self.items.append(f'<div id="{i}" class="i" style="left:{cx - size / 2:.0f}px;top:{cy - size / 2:.0f}px">{mk}</div>')
        t = self.at(at, gap)
        self.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"}},{t:.2f});')
        return t

    def html(self, duration: float, bg_name: str) -> str:
        fonts = "".join(f"@font-face{{font-family:{n};src:url('assets/fonts/{p.name}')}}" for n, p in
                        (("serif-x", paper.SERIF), ("serif-b", paper.SERIF_B), ("pen", paper.PEN),
                         ("sans", paper.SANS), ("sans-x", paper.SANS_X)))
        return f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width={self.W}, height={self.H}">
<script src="assets/gsap.min.js"></script>
<style>{fonts}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{self.W}px;height:{self.H}px;overflow:hidden;background:{self.c['base']}}}
#root{{position:relative;width:100%;height:100%}}
#bg{{position:absolute;inset:0;width:100%;height:100%}}
.t{{position:absolute;white-space:nowrap;line-height:1.15}}
.t span{{display:inline-block}}
.i{{position:absolute}}
svg#ink{{position:absolute;inset:0}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{duration:.2f}" data-width="{self.W}" data-height="{self.H}">
<img id="bg" src="assets/{bg_name}" class="clip" data-start="0" data-duration="{duration:.2f}" data-track-index="0">
<div id="layer" class="clip" data-start="0" data-duration="{duration:.2f}" data-track-index="1" data-layout-allow-overlap>
<svg id="ink" width="{self.W}" height="{self.H}" viewBox="0 0 {self.W} {self.H}">{self._rough_svg(''.join(self.svg))}</svg>
{''.join(self.items)}
</div></div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(self.js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>"""


# ---------------------------------------------------------------- 카드 배치 (paper.py 와 같은 자리)
def _title(D: Doc, card):
    t = card.get("title")
    if not t:
        return
    f = fit(FT("title"), t, 60, D.W - 300)
    D.text(D.W / 2, 130, t, FT("title"), f.size, D.ink, at=0.15)
    w = f.getlength(t)
    D.underline(D.W / 2 - w / 2, D.W / 2 + w / 2, 174)


def _note(D: Doc, card, y=None):
    if card.get("note"):
        f = fit(FT("note"), card["note"], 46, D.W - 400)
        D.text(D.W / 2, y or D.H * 0.76, card["note"], FT("note"), f.size, D.red)


def h_text(D, card):
    t = card.get("title", "")
    y = D.H * 0.43
    if card.get("icon"):
        D.icon(card["icon"], D.W / 2, D.H * 0.26, 150, D.red if card.get("highlight") else D.ink)
        y = D.H * 0.50
    f = fit(FT("title"), t, 104, D.W - 300)
    D.text(D.W / 2, y, t, FT("title"), f.size, D.red if card.get("highlight") else D.ink, dur=0.6)
    w = f.getlength(t)
    D.underline(D.W / 2 - w / 2, D.W / 2 + w / 2, y + 70)
    for i, it in enumerate(card.get("items", [])[:3]):
        s = it.get("label", "")
        D.text(D.W / 2, y + D.H * 0.14 + i * 64, s, FT("note"), fit(FT("note"), s, 52, D.W - 300).size, D.ink)


def h_number_compare(D, card):
    _title(D, card)
    items = card.get("items", [])[:3]
    n = max(len(items), 1)
    has_icon = any(it.get("icon") for it in items)
    base = D.H * (0.50 if has_icon else 0.47)
    for i, it in enumerate(items):
        x = D.W * (i + 0.5) / n
        col = D.red if it.get("highlight") else D.ink
        if it.get("icon"):
            D.icon(it["icon"], x, D.H * 0.27, 96, col)
        if it.get("label"):
            D.text(x, base - D.H * 0.13, it["label"], FT("label"), fit(FT("label"), it["label"], 36, D.W / n - 80).size, D.muted)
        v = it.get("value", "")
        f = fit(FT("value"), v, 128, D.W / n - 220)
        t = D.text(x, base, v, FT("value"), f.size, col, counter=True)
        if it.get("highlight"):  # 빨간 펜 동그라미: 글자에 닿지 않게 넉넉히
            w = f.getlength(v)
            D.circle(x, base + 4, w / 2 + 105, min(f.size * 0.8, D.H * 0.105), at=t + 0.9)
        if it.get("sub"):
            D.text(x, base + D.H * 0.14, it["sub"], FT("note"), fit(FT("note"), it["sub"], 50, D.W / n - 120).size, D.ink)
    _note(D, card)


def h_analogy(D, card):
    items = card.get("items", [])[:2]
    if len(items) < 2:
        return h_text(D, card)
    _title(D, card)
    for i, (x, it) in enumerate(zip((D.W * 0.27, D.W * 0.73), items)):
        col = D.red if (it.get("highlight") or i == 1) else D.ink
        at = 0.35 + i * 1.0
        D.t = at
        if it.get("icon"):
            D.icon(it["icon"], x, D.H * 0.32, 120, col)
        if it.get("label"):
            D.text(x, D.H * 0.46, it["label"], FT("label"), fit(FT("label"), it["label"], 40, D.W * 0.36).size, D.muted)
        if it.get("value"):
            D.text(x, D.H * 0.57, it["value"], FT("value"), fit(FT("value"), it["value"], 104, D.W * 0.36).size, col, counter=True)
        if it.get("sub"):
            D.text(x, D.H * 0.68, it["sub"], FT("note"), fit(FT("note"), it["sub"], 44, D.W * 0.38).size, D.ink)
        if i == 0:  # 가운데 '≈' 는 직접 그린다 (두 물결선)
            for k, dy in enumerate((-14, 14)):
                pts = [(D.W / 2 - 42 + j * 6, D.H * 0.56 + dy + 9 * math.sin(j * 0.42)) for j in range(15)]
                D.stroke(pts, D.red, 7, at=1.05 + k * 0.12, dur=0.3)
    D.t = max(D.t, 2.3)
    _note(D, card, D.H * 0.79)


def h_flow(D, card):
    items = card.get("items", [])[:6]
    if len(items) < 2:
        it = items[0] if items else {}
        return h_text(D, {"title": card.get("title", ""), "icon": it.get("icon", ""),
                          "items": [{"label": " · ".join(x for x in (it.get("label", ""), it.get("sub", "")) if x)}]})
    _title(D, card)
    n = len(items)
    bw = min(330, (D.W - 160) / n - 70)
    gap = min((D.W - 160 - bw * n) / max(n - 1, 1), 230)  # 상자가 적으면 가운데로 모은다
    left = (D.W - (bw * n + gap * (n - 1))) / 2
    y = D.H * 0.48
    has_icon, has_val = any(it.get("icon") for it in items), any(it.get("value") for it in items)
    h = 150 + (50 if has_icon else 0) + (40 if has_val else 0)  # 아이콘·값이 있으면 상자를 키워 글자끼리 띄운다
    for i, it in enumerate(items):
        x0 = left + i * (bw + gap)
        col = D.red if it.get("highlight") else D.ink
        t = D.box(x0, y - h / 2, x0 + bw, y + h / 2, col, 5 if it.get("highlight") else 4,
                  fill="rgba(140,44,61,0.18)" if it.get("highlight") and D.use_rough else None)
        top = y - h / 2 + 18
        if it.get("icon"):
            D.icon(it["icon"], x0 + bw / 2, top + 26, 52, col, at=t + 0.25)
            top += 60
        lab = it.get("label", "")
        f = fit(FT("box"), lab, 40, bw - 30)
        bottom = y + h / 2 - (48 if has_val else 0)
        D.text(x0 + bw / 2, (top + bottom) / 2, lab, FT("box"), f.size, col)
        if it.get("value"):
            D.text(x0 + bw / 2, y + h / 2 - 28, it["value"], FT("label"), fit(FT("label"), it["value"], 28, bw - 30).size, D.muted)
        if it.get("sub"):
            D.text(x0 + bw / 2, y + h / 2 + 44, it["sub"], FT("note"), fit(FT("note"), it["sub"], 40, bw + gap - 20).size, D.ink)
        if i < n - 1:
            D.arrow(x0 + bw + 12, y, x0 + bw + gap - 12, y, D.ink)
    _note(D, card)


def h_table(D, card):
    _title(D, card)
    items = card.get("items", [])[:6]
    n = max(len(items), 1)
    y0, rh = D.H * 0.30, min(96, (D.H * 0.44) / n)
    cols = (D.W * 0.20, D.W * 0.45, D.W * 0.70)
    for i, it in enumerate(items):
        y = y0 + i * rh
        col = D.red if it.get("highlight") else D.ink
        D.t = 0.5 + i * 0.35
        if it.get("icon"):
            D.icon(it["icon"], cols[0] - 50, y, 40, col, gap=0.05)
        D.text(cols[0], y, it.get("label", ""), FT("label"), fit(FT("label"), it.get("label", ""), 36, D.W * 0.22).size, D.muted, anchor="lm")
        f = fit(FT("value"), it.get("value", ""), 52, D.W * 0.24)
        D.text(cols[1], y, it.get("value", ""), FT("value"), f.size, col, anchor="lm")
        if it.get("sub"):
            D.text(cols[2], y, it["sub"], FT("note"), fit(FT("note"), it["sub"], 40, D.W * 0.26).size, D.ink, anchor="lm")
        if i < n - 1:
            D.stroke(wobble([(cols[0] - 80, y + rh / 2), (D.W * 0.92, y + rh / 2)], D.rng, amp=1.2), D.muted, 2, dur=0.3)
        if it.get("highlight"):  # 형광펜으로 그 줄을 칠한다
            D.marker(cols[0] - 20, y, D.W * 0.92 - cols[0] + 20, rh * 0.62, at=D.t + 0.3)
    _note(D, card, y0 + n * rh + 60)


def h_bars(D, card):
    items = [it for it in card.get("items", [])[:8] if paper.numeric(it.get("value"))]
    if len(items) < 2:
        return h_number_compare(D, card)
    _title(D, card)
    vals = [abs(float(str(it["value"]).replace(",", ""))) for it in items]
    top = max(vals) or 1
    n = len(items)
    y0, rh = D.H * 0.28, min(86, (D.H * 0.46) / n)
    x0, wmax = D.W * 0.30, D.W * 0.52
    for i, (it, v) in enumerate(zip(items, vals)):
        y = y0 + i * rh
        col = D.red if it.get("highlight") else D.ink
        D.t = 0.45 + i * 0.22
        D.text(x0 - 30, y, it.get("label", ""), FT("label"), fit(FT("label"), it.get("label", ""), 34, D.W * 0.24).size, D.muted, anchor="rm", gap=0.02)
        w = max(wmax * v / top, 8)
        if D.use_rough:  # 손으로 빗금을 그어 칠한 막대
            D.rough("rectangle", [x0, y - rh * 0.28, w, rh * 0.56], col, 2.5, fill=col, at=D.t, dur=0.8)
        else:
            bid = D._id()
            D.items.append(f'<div id="{bid}" style="position:absolute;left:{x0:.0f}px;top:{y - rh * 0.28:.0f}px;width:{w:.0f}px;'
                           f'height:{rh * 0.56:.0f}px;background:{col};opacity:.88;transform-origin:left center"></div>')
            D.js.append(f'tl.fromTo("#{bid}",{{scaleX:0}},{{scaleX:1,duration:0.7,ease:"power2.out"}},{D.t:.2f});')
        lab = f"{it['value']}" + (f" {it['sub']}" if it.get("sub") else "")
        D.text(x0 + w + 20, y, lab, FT("value"), fit(FT("value"), lab, 40, D.W * 0.95 - x0 - w).size, col, anchor="lm", at=D.t + 0.5)
    _note(D, card, y0 + n * rh + 50)


def h_headline(D, card):
    """종이 쪽지 위 기사 제목 + 형광펜."""
    pid = D._id()
    D.items.append(f'<div id="{pid}" style="position:absolute;left:{D.W * 0.17:.0f}px;top:{D.H * 0.24:.0f}px;width:{D.W * 0.66:.0f}px;'
                   f'height:{D.H * 0.44:.0f}px;background:#FBF8F1;box-shadow:0 10px 30px rgba(0,0,0,.18);transform:rotate(-1.2deg)"></div>')
    D.js.append(f'tl.fromTo("#{pid}",{{opacity:0,y:40,rotation:-4}},{{opacity:1,y:0,rotation:-1.2,duration:0.6,ease:"power2.out"}},0.1);')
    D.t = 0.6
    t = card.get("title", "")
    lines = [t]
    if fit(FT("title"), t, 64, D.W * 0.58).size < 46 and " " in t:  # 길면 두 줄로 (가운데 가까운 띄어쓰기에서)
        sp = [i for i, ch in enumerate(t) if ch == " "]
        cut = min(sp, key=lambda i: abs(i - len(t) / 2))
        lines = [t[:cut], t[cut + 1:]]
    size = min(fit(FT("title"), ln, 64, D.W * 0.58).size for ln in lines)
    f = paper.F(FT("title"), size)
    y0 = D.H * (0.36 if len(lines) == 1 else 0.33)
    for k, ln in enumerate(lines):
        y = y0 + k * size * 1.35
        D.text(D.W * 0.21, y, ln, FT("title"), size, D.ink, anchor="lm")
        D.marker(D.W * 0.205, y + size * 0.12, f.getlength(ln) + 20, size * 0.5, at=1.1 + k * 0.4, index=1)
    D.t = 1.5 + 0.4 * (len(lines) - 1)
    for k, it in enumerate(card.get("items", [])[:2]):
        s = " · ".join(x for x in (it.get("label", ""), it.get("value", ""), it.get("sub", "")) if x)
        D.text(D.W * 0.21, D.H * (0.47 if len(lines) == 1 else 0.50) + k * 60, s, FT("label"), fit(FT("label"), s, 34, D.W * 0.58).size, D.muted, anchor="lm")
    _note(D, card, D.H * 0.76)


LAYOUT = {"text": h_text, "number_compare": h_number_compare, "analogy": h_analogy, "flow": h_flow,
          "table": h_table, "bars": h_bars, "headline": h_headline}


def build(card: dict, work: Path, duration: float, seed: int = 1) -> Path:
    """카드 → HyperFrames 프로젝트 폴더 (index.html + assets/)."""
    work.mkdir(parents=True, exist_ok=True)
    a = work / "assets"
    (a / "fonts").mkdir(parents=True, exist_ok=True)
    for p in (paper.SERIF, paper.SERIF_B, paper.PEN, paper.SANS, paper.SANS_X):
        if not (a / "fonts" / p.name).exists():  # 폰트는 카드마다 복사하지 않고 링크 (카드 80장 × 14MB 절약)
            try:
                os.link(p, a / "fonts" / p.name)
            except OSError:
                shutil.copy(p, a / "fonts" / p.name)
    shutil.copy(GSAP, a / "gsap.min.js")
    D = Doc(seed)
    bg = paper.paper_bg(D.W, D.H, seed=7)
    bg.save(a / "paper.jpg", quality=92)
    LAYOUT[card.get("type", "text")](D, card)
    duration = max(duration, D.t + 0.6)
    (work / "index.html").write_text(D.html(duration, "paper.jpg"), encoding="utf-8")
    (work / "hyperframes.json").write_text(json.dumps({"name": work.name}), encoding="utf-8")
    return work


def check(work: Path) -> list[str]:
    """hyperframes check: 레이아웃(겹침·잘림)·대비 점검. 문제 문장 목록."""
    r = subprocess.run([str(BIN), "check", "--json"], cwd=work, env=_env(), capture_output=True, text=True, timeout=300)
    try:
        data = json.loads(r.stdout[r.stdout.find("{"):])
    except Exception:
        return [f"check 실행 실패: {(r.stderr or r.stdout)[-200:]}"] if r.returncode else []
    out = []
    for sec in ("lint", "runtime", "layout", "contrast"):  # craft(연출 권고)는 내레이션 길이가 정하므로 제외
        for f in (data.get(sec) or {}).get("findings") or []:
            if f.get("severity") == "error":
                out.append(f"{sec}/{f.get('code', '')}: {(f.get('message') or '')[:120]}")
    return out


def render_card(card: dict, out: Path, duration: float, seed: int = 1, work: Path | None = None) -> list:
    """paper.render_card 와 같은 모양. 지원하지 않는 카드나 도구가 없으면 paper.py 로 그린다."""
    if card.get("type") not in SUPPORTED or not available():
        return paper.render_card(card, out, duration, seed)
    work = work or out.parent / "hf" / out.stem
    build(card, work, duration, seed)
    issues = check(work)
    r = subprocess.run([str(BIN), "render", "--quality", "looks", "-o", str(out.resolve())], cwd=work, env=_env(),
                       capture_output=True, text=True, timeout=900)
    if r.returncode or not out.exists() or out.stat().st_size < 1000:
        print(f"  ! HyperFrames 렌더 실패 → paper 로 대체: {(r.stderr or r.stdout)[-160:]}")
        return paper.render_card(card, out, duration, seed) + issues
    return issues
