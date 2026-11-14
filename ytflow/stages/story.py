"""이야기 그림판 장면 (`story`) — 호기심 채널: 이야기를 들려주듯, 말하는 순간 종이 위에 그림이 그려진다 (2026-11-13 사용자 요청).

> "호기심 채널은 주로 이야기를 들려주는 방식이기에 이 대본에 맞추어 애니메이션 효과 넣어주세요.
>  주식 채널은 정보를 제공한다 느낌이 있기 때문에 서로 양식이 조금 다를 수밖에 없다." (참고: 미주일기)

주식 채널(정보형)은 '요약판 + 말에 맞춰 생기는 사물'(motion2), 호기심 채널(이야기형)은 이 '그림판':
- 큰 종이 한 장(3840×2160, 화면의 2배)을 지우지 않고, 이야기가 진행되면 카메라가 다음 그림 자리로 옮겨 간다 (미주일기의 한 장 캔버스).
- 사람(막대 인물)·사물(선 아이콘)은 **선이 그려지듯** 나타나고(draw-on), 날짜는 도장, 생각·말은 말풍선, 핵심 낱말은 종이 쪽지 + 형광펜.
- 모든 것은 **그 낱말을 말하는 순간**(받아쓰기 단어 시각) 생긴다. 제자리 흔들림은 없다 (2026-11-13 사용자: 웅웅거림 빼기).

대본 (02_script/hybrid.json):
  {"type": "story", "beats": [
     {"say": "1997년 5월 11일, 미국 뉴욕. 세계 체스 챔피언 카스파로프가 자리에서 일어났습니다.",
      "draw": [
        {"t": "1997년", "do": "stamp", "id": "d", "text": "1997. 5. 11 · 뉴욕", "x": 700, "y": 420, "cam": [1100, 900, 0.8]},
        {"t": "카스파로프", "do": "figure", "id": "k", "pose": "stand", "x": 900, "y": 1100, "label": "카스파로프"},
        {"t": "체스", "do": "draw", "id": "c", "icon": "chess", "x": 1350, "y": 1150, "s": 260},
        {"t": "일어났", "do": "arrow", "a": "k", "b": "c"}]}]}
좌표는 그림판(3840×2160) 기준. cam = [가운데 x, 가운데 y, 확대] (0.5 = 그림판 전체, 1.0 = 화면 1장 크기), "full" = 전체.
do: draw(아이콘·그림) · figure(사람) · chip(종이 쪽지, hl 형광펜) · note(손글씨) · stamp(날짜·장소 도장) · count(숫자 올라감)
    · bubble(말·생각 풍선, to=가리킬 id) · arrow(a→b 또는 from/to) · line(선) · circle · cross · check · hl · dim · cam(카메라만)
"""
from __future__ import annotations

import html as H
import math
import re

CW, CH = 3840, 2160
W, H_ = 1920, 1080
INK, RED, CARD, MARK, BLUE, OK = "#22304D", "#C4452F", "#FBF8F1", "#F3D36B", "#2F5D8C", "#2E7D4F"

# 아이콘에 없는 이야기용 그림 (24 격자, Lucide 와 같은 선 굵기 규칙 — 직접 그림)
SHAPES = {
    "shirt": ['<path d="M8 3 L3.5 5.5 L1.5 10 L5.5 11.6 L6.2 10.2 V21 H17.8 V10.2 L18.5 11.6 L22.5 10 L20.5 5.5 L16 3 C15 5.2 9 5.2 8 3 Z"/>'],
    "chess": ['<path d="M12 1.5v4"/>', '<path d="M10 3.5h4"/>', '<path d="M8.5 7.5h7l-1.8 7.5h-3.4z"/>', '<path d="M7.5 15h9l1 3h-11z"/>',
              '<path d="M5.5 18h13v3h-13z"/>'],
    "board": ['<rect x="2" y="2" width="20" height="20"/>', '<path d="M7 2v20M12 2v20M17 2v20M2 7h20M2 12h20M2 17h20"/>'],
    "cloth": ['<path d="M3 9c2-4 5-6 8-4s4-2 7 0 4 5 2 8-1 5-4 6-5-1-8 0-5-1-5-4 0-4 0-6z"/>', '<path d="M8 10c2 1 3 3 2 5"/>', '<path d="M14 8c1 2 3 3 5 3"/>'],
    "pile": ['<path d="M2 20c1-3 3-4 5-4s3-2 5-2 4 1 6 1 4 2 4 5z"/>', '<path d="M5 16c1-2 3-3 5-3s3-1 5-1 3 1 4 3"/>', '<path d="M8 13c1-1 2-2 4-2s3 0 4 1"/>'],
    "hand": ['<path d="M7 11V5a1.5 1.5 0 0 1 3 0v5"/>', '<path d="M10 9V3.5a1.5 1.5 0 0 1 3 0V9"/>', '<path d="M13 9V5a1.5 1.5 0 0 1 3 0v5"/>',
             '<path d="M16 10V8a1.5 1.5 0 0 1 3 0v6c0 4-3 7-7 7s-6-2-7.5-5L3 12.5a1.5 1.5 0 0 1 2.5-1.5L7 13"/>'],
    "book": ['<path d="M2 4h7a3 3 0 0 1 3 3v14a2 2 0 0 0-2-2H2z"/>', '<path d="M22 4h-7a3 3 0 0 0-3 3v14a2 2 0 0 1 2-2h8z"/>'],
    "eye2": ['<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/>', '<circle cx="12" cy="12" r="3"/>'],
}
POSES = {   # 막대 인물: 머리·몸·팔·다리 (24 격자)
    "stand": ['<circle cx="12" cy="4.5" r="2.6"/>', '<path d="M12 7.2v7.3"/>', '<path d="M7.5 12.5 12 9.5l4.5 3"/>', '<path d="M12 14.5l-3.5 7M12 14.5l3.5 7"/>'],
    "cheer": ['<circle cx="12" cy="4.5" r="2.6"/>', '<path d="M12 7.2v7.3"/>', '<path d="M7 4.5 12 9.5l5-5"/>', '<path d="M12 14.5l-3.5 7M12 14.5l3.5 7"/>'],
    "slump": ['<circle cx="11" cy="6" r="2.6"/>', '<path d="M11.5 8.6 12.5 15"/>', '<path d="M9 16 12 10.5l3 5.5"/>', '<path d="M12.5 15l-3 6.5M12.5 15l3.5 6.5"/>'],
    "point": ['<circle cx="12" cy="4.5" r="2.6"/>', '<path d="M12 7.2v7.3"/>', '<path d="M8 13 12 9.5l7-2"/>', '<path d="M12 14.5l-3.5 7M12 14.5l3.5 7"/>'],
    "think": ['<circle cx="12" cy="4.5" r="2.6"/>', '<path d="M12 7.2v7.3"/>', '<path d="M8 13 12 9.5l2 2.5 0-4.5"/>', '<path d="M12 14.5l-3.5 7M12 14.5l3.5 7"/>'],
    "baby": ['<circle cx="12" cy="8" r="4.2"/>', '<path d="M12 12.2v4.3"/>', '<path d="M8.5 14.5 12 13.5l3.5 1"/>', '<path d="M12 16.5l-2.5 4.5M12 16.5l2.5 4.5"/>'],
    "walk": ['<circle cx="13" cy="4.5" r="2.6"/>', '<path d="M12.5 7.2 11.5 14.5"/>', '<path d="M8 11l4-2 4 3"/>', '<path d="M11.5 14.5 8 21M11.5 14.5l4.5 6.5"/>'],
}


def _e(s) -> str:
    return H.escape(str(s))


def _children(name: str) -> list[str]:
    if name.startswith("pose:"):
        return POSES.get(name[5:], POSES["stand"])
    if name in SHAPES:
        return SHAPES[name]
    from .icons import ICON_DIR
    f = ICON_DIR / f"{name}.svg"
    if not f.exists():
        return SHAPES["cloth"]
    body = f.read_text(encoding="utf-8")
    return re.findall(r"<(?:path|circle|rect|line|polyline|polygon|ellipse)\b[^>]*/>", body)


def _dash(el: str, cls: str) -> str:
    return el.replace("/>", f' class="{cls}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>', 1)


class Board:
    def __init__(self, D, prefix: str):
        self.D, self.p = D, prefix
        self.pos: dict = {}
        self.svg: list = []      # 그림판 좌표의 선 (흔들리는 손 선 필터)
        self.html: list = []     # 쪽지·글씨
        self.js: list = []
        self.n = 0
        self.cam = "full"   # 기본: 이 장면에 그린 것 전체에 맞춤
        self.cam_events: list = []
        self.layers = {0: [], 1: [], 2: []}   # v2: 뒤·가운데·앞 (패럴랙스, story_kit)
        self.last_in = ""
        self.bg_events: list = []
        self.credits: list = []
        self.rots: dict = {}
        self.cuts: dict = {}      # 그림 조각(자세 바꾸기용)
        self.puppets: dict = {}   # 관절 인형

    def layer(self, z: int) -> list:
        return self.layers[max(0, min(2, int(z)))]

    def asset(self, src: str) -> str:
        """04_assets/story/<src> → 장면 assets (하드링크)."""
        import os
        import shutil
        from pathlib import Path
        f = Path(self.D._proj) / "04_assets" / "story" / src
        name = "story_" + src.replace("/", "_")
        dst = Path(self.D._work) / "assets" / name
        if f.exists() and not dst.exists():
            try:
                os.link(f, dst)
            except OSError:
                shutil.copy(f, dst)
        if not f.exists():
            self.D.qa.append(f"story/missing: 04_assets/story/{src}")
        return name

    def html_label(self, x, y, text, t):
        from .story_kit import tag
        i = self._id()
        self.layers[2].append(f'<div id="{i}" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;opacity:0">{tag(text, 50)}</div>')
        self.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.35}},{t:.2f});')

    def js_html_into_cut(self, on, html):   # 그림 조각 안에 새 자세 그림 추가
        key = f'<div id="{self.p}_{on}_mv" style="position:absolute;inset:0">'
        for L in self.layers.values():
            for i, h in enumerate(L):
                if key in h:
                    L[i] = h.replace(key, key + html, 1)
                    return

    def js_html_into(self, on, html):   # 문서 위 형광펜: 같은 자리·같은 기울기의 투명 상자 안에
        x, y, w, h = self.pos[on]
        r = self.rots.get(on, 0)
        self.layers[1].append(f'<div style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;width:{w}px;height:{h}px;'
                              f'transform:rotate({r}deg);pointer-events:none">{html}</div>')

    def _id(self):
        self.n += 1
        return f"{self.p}{self.n}"

    def _sfx(self, name, t):
        self.D.sfx.append((name, t))

    # ---- 그림 (선이 그려짐)
    def _drawn(self, did, children, x, y, s, t, col, sw, dur=0.9):
        k = s / 24
        g = "".join(_dash(c, f"{did}l") for c in children)
        self.svg.append(f'<g id="{did}" opacity="0" transform="translate({x - s / 2:.0f},{y - s / 2:.0f}) scale({k:.3f})" fill="none" stroke="{col}" '
                        f'stroke-width="{sw / k:.2f}" stroke-linecap="round" stroke-linejoin="round">{g}</g>')
        n = max(len(children), 1)
        self.js.append(f'tl.set("#{did}",{{opacity:1}},{t:.2f});')   # 그리기 전에는 숨김 (둥근 선 끝의 점이 미리 보이지 않게)
        self.js.append(f'tl.to(".{did}l",{{strokeDashoffset:0,duration:{dur / n * 1.6:.2f},stagger:{dur / n * 0.7:.2f},ease:"power1.inOut"}},{t:.2f});')
        self._sfx("pencil", t)

    def _label(self, x, y, text, t, fs=64, col=INK, font="pen"):
        if not text:
            return
        i = self._id()
        from .story_kit import tag
        inner = tag(text, fs, col) if font == "pen" else _e(text)
        self.html.append(f'<div id="{i}" style="position:absolute;left:{x - 700}px;top:{y}px;width:1400px;text-align:center;font-family:{font};'
                         f'font-size:{fs}px;color:{col};white-space:nowrap;opacity:0">{inner}</div>')
        self.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.35}},{t:.2f});')

    def add(self, m: dict, t: float):
        do = m["do"]
        x, y = m.get("x", CW / 2), m.get("y", CH / 2)
        mid = m.get("id") or self._id()
        if m.get("cam"):
            c = m["cam"]
            self.cam_events.append((max(t - 0.15, 0), c if c == "full" else tuple(c)))
        from . import story_kit
        if do in ("photo", "doc", "mark", "sticker", "card", "big", "bg", "cut", "pose", "move", "shake", "puppet", "act"):
            if do in ("doc", "photo", "card"):
                self.rots[mid] = m.get("rot", story_kit._rot(mid))
            story_kit.kit(self, m, t, mid, x, y, self.asset)
            return
        if do == "draw":
            s = m.get("s", 260)
            self._drawn(f"{self.p}_{mid}", _children(m["icon"]), x, y, s, t, m.get("color", INK), m.get("sw", 9))
            self._label(x, y + s / 2 + 18, m.get("label", ""), t + 0.5, m.get("lfs", 66))
            self.pos[mid] = (x, y, s, s)
        elif do == "figure":
            s = m.get("s", 420)
            self._drawn(f"{self.p}_{mid}", POSES.get(m.get("pose", "stand"), POSES["stand"]), x, y, s, t, m.get("color", INK), m.get("sw", 10), 0.8)
            self._label(x, y + s / 2 + 10, m.get("label", ""), t + 0.45, m.get("lfs", 70))
            if m.get("sub"):
                self._label(x, y + s / 2 + 96, m["sub"], t + 0.6, 44, "#5a5f6a", "sans")
            self.pos[mid] = (x, y, s * 0.6, s)
        elif do in ("chip", "note"):
            fs = m.get("fs", 84 if do == "chip" else 72)
            rot = m.get("rot", -1.5 if do == "chip" else -3)
            text = m.get("text", "")
            wch = sum(1.0 if ord(ch) > 0x2E80 else 0.62 for ch in text) * fs * 1.08 + (110 if do == "chip" else 40)
            hh = fs * 1.55
            dark = m.get("tone") == "dark"
            did = f"{self.p}_{mid}"
            if do == "chip":
                bg = "#22304D" if dark else CARD
                col = "#FBF8F1" if dark else INK
                self.html.append(
                    f'<div id="{did}" style="position:absolute;left:{x - wch / 2:.0f}px;top:{y - hh / 2:.0f}px;width:{wch:.0f}px;height:{hh:.0f}px;'
                    f'background:{bg};box-shadow:0 14px 34px rgba(0,0,0,.22);transform:rotate({rot}deg);opacity:0">'
                    f'<div id="{did}m" style="position:absolute;left:34px;right:34px;top:{hh * 0.52:.0f}px;height:{fs * 0.42:.0f}px;background:{MARK};opacity:.85;'
                    f'transform-origin:left center"></div>'
                    f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:{m.get("font", "serif-x")};'
                    f'font-size:{fs}px;color:{col};white-space:nowrap">{_e(text)}</div></div>')
                self.js.append(f'tl.fromTo("#{did}",{{opacity:0,y:-30,rotation:{rot - 5}}},{{opacity:1,y:0,rotation:{rot},duration:0.45,ease:"back.out(1.6)"}},{t:.2f});')
                self._sfx("pop", t)
                self.js.append(f'tl.set("#{did}m",{{scaleX:0}},0);')   # 형광펜: 처음엔 0 (CSS transform 대신 GSAP 로 — 충돌 방지)
                if m.get("hl"):
                    self.js.append(f'tl.to("#{did}m",{{scaleX:1,duration:0.45,ease:"power1.inOut"}},{t + 0.45:.2f});')
            else:
                self.html.append(f'<div id="{did}" style="position:absolute;left:{x - wch / 2:.0f}px;top:{y - hh / 2:.0f}px;width:{wch:.0f}px;text-align:center;'
                                 f'font-family:pen;font-size:{fs}px;color:{m.get("color", RED)};white-space:nowrap;transform:rotate({rot}deg);opacity:0">{_e(text)}</div>')
                self.js.append(f'tl.fromTo("#{did}",{{opacity:0,clipPath:"inset(0 100% 0 0)"}},{{opacity:1,clipPath:"inset(0 0% 0 0)",duration:0.6,ease:"none"}},{t:.2f});')
                self._sfx("pencil", t)
            self.pos[mid] = (x, y, wch, hh)
        elif do == "stamp":
            text = m.get("text", "")
            fs = m.get("fs", 72)
            wch = sum(1.0 if ord(ch) > 0x2E80 else 0.6 for ch in text) * fs + 110
            did = f"{self.p}_{mid}"
            self.html.append(f'<div id="{did}" style="position:absolute;left:{x - wch / 2:.0f}px;top:{y - 75}px;width:{wch:.0f}px;height:150px;'
                             f'border:9px double {RED};border-radius:14px;color:{RED};font-family:serif-x;font-size:{fs}px;line-height:1;display:flex;align-items:center;'
                             f'justify-content:center;white-space:nowrap;transform:rotate({m.get("rot", -6)}deg);background:rgba(251,248,241,.96);box-shadow:0 0 0 14px rgba(251,248,241,.96),0 10px 26px rgba(0,0,0,.25);opacity:0">{_e(text)}</div>')
            self.js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:1.7}},{{opacity:1,scale:1,duration:0.26,ease:"power4.in"}},{t:.2f});')
            self._sfx("click-soft", t + 0.24)
            self.pos[mid] = (x, y, wch, 150)
        elif do == "count":
            val = str(m.get("value", ""))
            fs = m.get("fs", 230)
            did = f"{self.p}_{mid}"
            self.html.append(f'<div id="{did}" style="position:absolute;left:{x - 600}px;top:{y - fs * 0.75:.0f}px;width:1200px;text-align:center;opacity:0">'
                             f'<div id="{did}n" style="font-family:serif-x;font-size:{fs}px;line-height:1.1;color:{m.get("color", RED)};white-space:nowrap;'
                             + (f'display:inline-block;background:{CARD};padding:6px 40px 14px;box-shadow:0 14px 30px rgba(0,0,0,.28);transform:rotate(-1.5deg)' if m.get("card") else "")
                             + f'">{_e(val)}</div>'
                             + (f'<div style="margin-top:6px">{__import__("ytflow.stages.story_kit", fromlist=["tag"]).tag(m["label"], m.get("lfs", 62))}</div>' if m.get("label") else "") + '</div>')
            self.js.append(f'tl.fromTo("#{did}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{t:.2f});')
            mm = re.search(r"\d[\d,]*(\.\d+)?", val)
            if mm:
                core = mm.group(0)
                pre, post = val[:mm.start()], val[mm.end():]
                numv = core.replace(",", "")
                fmt = 'Math.round(o.v).toLocaleString("en-US")' if "," in core else "Math.round(o.v)"
                self.js.append(f'(function(){{var o={{v:0}};tl.to(o,{{v:{numv},duration:0.9,ease:"power2.out",onUpdate:function(){{'
                               f'document.getElementById("{did}n").textContent="{_e(pre)}"+{fmt}+"{_e(post)}";}}}},{t + 0.05:.2f});}})();')
            self._sfx("pop", t)
            self.pos[mid] = (x, y, 900, fs)
        elif do == "bubble":
            text = m.get("text", "")
            fs = m.get("fs", 66)
            lines = text.split("\n")
            wch = max(sum(1.0 if ord(ch) > 0x2E80 else 0.58 for ch in ln) for ln in lines) * fs + 140
            hh = len(lines) * fs * 1.35 + 90
            did = f"{self.p}_{mid}"
            tail = ""
            if m.get("to") in self.pos:   # 꼬리: 말하는 사람 쪽으로 작은 동그라미 둘
                tx, ty = self.pos[m["to"]][0], self.pos[m["to"]][1] - self.pos[m["to"]][3] / 2
                for f_, r_ in ((0.62, 34), (0.82, 22)):
                    cx_, cy_ = x + (tx - x) * f_, y + (ty - y) * f_
                    tail += (f'<div style="position:absolute;left:{cx_ - x + wch / 2 - r_:.0f}px;top:{cy_ - y + hh / 2 - r_:.0f}px;width:{2 * r_}px;height:{2 * r_}px;'
                             f'border-radius:50%;background:{CARD};border:5px solid {INK}"></div>')
            self.html.append(f'<div id="{did}" style="position:absolute;left:{x - wch / 2:.0f}px;top:{y - hh / 2:.0f}px;width:{wch:.0f}px;height:{hh:.0f}px;opacity:0">{tail}'
                             f'<div style="position:absolute;inset:0;background:{CARD};border:5px solid {INK};border-radius:{min(hh / 2, 90):.0f}px;'
                             f'box-shadow:0 12px 30px rgba(0,0,0,.18);display:flex;align-items:center;justify-content:center;text-align:center;'
                             f'font-family:pen;font-size:{fs}px;line-height:1.3;color:{INK};white-space:pre">{_e(text)}</div></div>')
            self.js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.42,ease:"back.out(2)"}},{t:.2f});')
            self._sfx("pop", t)
            self.pos[mid] = (x, y, wch, hh)
        elif do in ("arrow", "line"):
            if do == "arrow" and m.get("a") in self.pos and m.get("b") in self.pos:
                a, b = self.pos[m["a"]], self.pos[m["b"]]
                dx, dy = b[0] - a[0], b[1] - a[1]
                L = math.hypot(dx, dy) or 1
                ra = min(a[2], a[3]) / 2 + 40
                rb = min(b[2], b[3]) / 2 + 50
                x1, y1, x2, y2 = a[0] + dx / L * ra, a[1] + dy / L * ra, b[0] - dx / L * rb, b[1] - dy / L * rb
            else:
                (x1, y1), (x2, y2) = m["from"], m["to"]
            dx, dy = x2 - x1, y2 - y1
            L = math.hypot(dx, dy) or 1
            bend = m.get("bend", min(140, L * 0.18)) if do == "arrow" else 0
            cx, cy = (x1 + x2) / 2 - dy / L * bend, (y1 + y2) / 2 + dx / L * bend
            col = m.get("color", RED if do == "arrow" else INK)
            aid = f"{self.p}_{mid}"
            self.svg.append(f'<path id="{aid}" d="M{x1:.0f},{y1:.0f} Q{cx:.0f},{cy:.0f} {x2:.0f},{y2:.0f}" fill="none" stroke="{col}" stroke-width="{m.get("sw", 11)}" '
                            f'stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" opacity="0"/>')
            d_ = m.get("dur", 0.5)
            self.js.append(f'tl.set("#{aid}",{{opacity:1}},{t:.2f});tl.to("#{aid}",{{strokeDashoffset:0,duration:{d_},ease:"power2.inOut"}},{t:.2f});')
            if do == "arrow":   # 화살촉은 선이 다 그려진 뒤 (docs/25 §8-1)
                ang = math.atan2(y2 - cy, x2 - cx)
                pts = [(x2 + 52 * math.cos(ang + s_), y2 + 52 * math.sin(ang + s_)) for s_ in (2.55, -2.55)]
                self.svg.append(f'<path id="{aid}h" d="M{pts[0][0]:.0f},{pts[0][1]:.0f} L{x2:.0f},{y2:.0f} L{pts[1][0]:.0f},{pts[1][1]:.0f}" fill="none" '
                                f'stroke="{col}" stroke-width="{m.get("sw", 11)}" stroke-linecap="round" stroke-linejoin="round" opacity="0"/>')
                self.js.append(f'tl.to("#{aid}h",{{opacity:1,duration:0.08}},{t + d_ - 0.04:.2f});')
                self._sfx("whoosh-short", t)
            else:
                self._sfx("pencil", t)
        elif do in ("circle", "cross", "check"):
            on = self.pos.get(m.get("on"))
            if on:
                ox, oy, ow, oh = on
            else:
                ox, oy = m.get("at", (x, y))
                ow, oh = m.get("size", (400, 300))
            cid = f"{self.p}_{mid}{do}"
            if do == "circle":   # 한 번에 그린 듯 살짝 겹쳐 끝나는 타원
                rx, ry = ow / 2 + m.get("pad", 60), oh / 2 + m.get("pad", 60)
                pts = []
                for k in range(0, 41):
                    a_ = -2.2 + k / 40 * (2 * math.pi + 0.35)
                    r_ = 1 + 0.035 * math.sin(k * 0.9)
                    pts.append((ox + rx * r_ * math.cos(a_), oy + ry * r_ * math.sin(a_)))
                d = "M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts)
                self.svg.append(f'<path id="{cid}" d="{d}" fill="none" stroke="{m.get("color", RED)}" stroke-width="10" stroke-linecap="round" '
                                f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" opacity="0"/>')
                self.js.append(f'tl.set("#{cid}",{{opacity:1}},{t:.2f});tl.to("#{cid}",{{strokeDashoffset:0,duration:0.6,ease:"power1.inOut"}},{t:.2f});')
                self._sfx("pencil", t)
            elif do == "cross":
                r = min(ow, oh) / 2 + 30
                for k, (a1, b1, a2, b2) in enumerate(((-1, -1, 1, 1), (1, -1, -1, 1))):
                    self.svg.append(f'<path id="{cid}{k}" d="M{ox + a1 * r:.0f},{oy + b1 * r:.0f} L{ox + a2 * r:.0f},{oy + b2 * r:.0f}" stroke="{RED}" stroke-width="16" '
                                    f'stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" opacity="0"/>')
                    self.js.append(f'tl.set("#{cid}{k}",{{opacity:1}},{t + k * 0.25:.2f});tl.to("#{cid}{k}",{{strokeDashoffset:0,duration:0.22,ease:"power2.in"}},{t + k * 0.25:.2f});')
                self._sfx("pencil", t)
            else:
                cx_, cy_ = ox + ow / 2 + 10, oy - oh / 2 + 10
                self.svg.append(f'<path id="{cid}" d="M{cx_ - 60:.0f},{cy_:.0f} L{cx_ - 15:.0f},{cy_ + 50:.0f} L{cx_ + 70:.0f},{cy_ - 70:.0f}" fill="none" stroke="{OK}" '
                                f'stroke-width="18" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" opacity="0"/>')
                self.js.append(f'tl.set("#{cid}",{{opacity:1}},{t:.2f});tl.to("#{cid}",{{strokeDashoffset:0,duration:0.35,ease:"power2.out"}},{t:.2f});')
                self._sfx("pop", t + 0.3)
        elif do == "hl" and m.get("on") in self.pos:
            self.js.append(f'tl.to("#{self.p}_{m["on"]}m",{{scaleX:1,duration:0.45,ease:"power1.inOut"}},{t:.2f});')
        elif do == "dim" and m.get("on") in self.pos:
            self.js.append(f'tl.to("#{self.p}_{m["on"]}",{{opacity:{m.get("to", 0.28)},duration:0.4}},{t:.2f});')
        elif do == "undim" and m.get("on") in self.pos:
            self.js.append(f'tl.to("#{self.p}_{m["on"]}",{{opacity:1,duration:0.4}},{t:.2f});')

    def finish(self, dur: float, fade: bool = True):
        D = self.D
        cv = f"{self.p}cv"
        wob = f"{self.p}wob"
        PAR = {0: 0.92, 1: 1.0, 2: 1.07}   # 2.5D: 뒤는 느리게, 앞은 빠르게 (카메라가 움직일 때만 차이가 보임)
        # 배경 (화면 기준, 그림판 아래): 어두운 종이 · 사진 전체
        for k, (t, mode, src, credit) in enumerate(self.bg_events):
            bid = f"{self.p}bg{k}"
            if mode == "dark":
                inner = (f'<div style="position:absolute;inset:0;background:#2C2E34"></div>'   # 어두운 종이: 구김 결이 보이게 (검정 단색 금지)
                         f'<img src="assets/{D.bg_name}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;'
                         f'mix-blend-mode:overlay;opacity:.55;filter:grayscale(1) contrast(1.9)">'
                         f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%,rgba(255,255,255,.06) 0%,rgba(0,0,0,.35) 100%)"></div>')
            elif mode == "photo" and src:
                inner = (f'<img src="assets/{src}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(.35) sepia(.25) brightness(.62) contrast(1.1)">'
                         f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 30%,rgba(0,0,0,.5) 100%)"></div>')
            else:
                inner = ""
            D.items.append(f'<div id="{bid}" style="position:absolute;inset:0;opacity:0">{inner}</div>')
            D.js.append(f'tl.to("#{bid}",{{opacity:1,duration:0.7,ease:"power1.inOut"}},{max(t - 0.2, 0):.2f});')
            for j in range(k):   # 앞 배경은 끔
                D.js.append(f'tl.to("#{self.p}bg{j}",{{opacity:0,duration:0.7}},{max(t - 0.2, 0):.2f});')
            if credit:
                self.credits.append(credit)
        lay = {0: "".join(self.layers[0]),
               1: (f'<svg width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}" style="position:absolute;inset:0;overflow:visible">'
                   f'<filter id="{wob}"><feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="2" seed="3"/>'
                   f'<feDisplacementMap in="SourceGraphic" scale="7"/></filter><g filter="url(#{wob})">{"".join(self.svg)}</g></svg>'
                   + "".join(self.layers[1]) + "".join(self.html)),
               2: "".join(self.layers[2])}
        D.items.append(f'<div style="position:absolute;inset:0;overflow:hidden" data-layout-allow-overflow>'   # 카메라가 다른 곳을 볼 때 화면 밖 그림은 의도된 것
                       + "".join(f'<div id="{cv}{k}" data-layout-allow-overflow style="position:absolute;left:0;top:0;width:{CW}px;height:{CH}px;'
                                 f'transform-origin:0 0">{lay[k]}</div>' for k in (0, 1, 2) if lay[k]) + '</div>')
        used = [k for k in (0, 1, 2) if lay[k]]

        def fit():   # 장면에 그린 것 전체를 감싸는 카메라 (여백 120, 아래 15% 자막 자리 비움)
            if not self.pos:
                return (CW / 2, CH / 2, 0.5)
            x0 = min(p[0] - p[2] / 2 for p in self.pos.values()) - 120
            x1 = max(p[0] + p[2] / 2 for p in self.pos.values()) + 120
            y0 = min(p[1] - p[3] / 2 for p in self.pos.values()) - 120
            y1 = max(p[1] + p[3] / 2 for p in self.pos.values()) + 200   # 이름표
            z = max(0.5, min(1.0, W / (x1 - x0), H_ * 0.84 / (y1 - y0)))
            return ((x0 + x1) / 2, (y0 + y1) / 2 + (540 - 455) / z, z)

        def cam_of(c):
            if c == "full":
                c = fit()
            cx, cy, z = c
            tx = min(0.0, max(W - CW * z, W / 2 - cx * z))
            ty = min(0.0, max(H_ - CH * z, H_ / 2 - cy * z))
            return ((W / 2 - tx) / z, (H_ / 2 - ty) / z, z)   # 실제로 보이는 가운데

        def setv(c, k):
            cx, cy, z = c
            zk = z * PAR[k]
            return f'scale:{zk:.4f},x:{W / 2 - cx * zk:.1f},y:{H_ / 2 - cy * zk:.1f}'

        cur = cam_of(self.cam)
        evs = sorted(self.cam_events)
        if evs and evs[0][0] <= 0.3:   # 첫 카메라는 처음부터
            cur = cam_of(evs[0][1])
            evs = evs[1:]
        for k in used:
            D.js.append(f'tl.set("#{cv}{k}",{{{setv(cur, k)}}},0);')
        marks = [t for t, _ in evs] + [dur]
        t_free = 0.0
        for i, (t, c) in enumerate(evs + [(dur, None)]):
            if t - t_free > 1.0:   # 머무는 동안 아주 천천히 당김 (멈춘 화면 방지, 흔들림 아님)
                drift = (cur[0], cur[1], cur[2] * (1 + 0.012 * min(t - t_free, 6)))
                for k in used:
                    D.js.append(f'tl.to("#{cv}{k}",{{{setv(drift, k)}, duration:{t - t_free:.2f},ease:"none"}},{t_free:.2f});')
                cur = drift
            if c is None:
                break
            nxt = cam_of(c)
            for k in used:
                D.js.append(f'tl.to("#{cv}{k}",{{{setv(nxt, k)}, duration:0.95,ease:"power2.inOut"}},{t:.2f});')
            cur, t_free = nxt, t + 0.95
        _ = marks
        D.js.extend(self.js)
        if fade:   # 단락 사이: 검은 화면을 거쳐 밝아짐 (미주일기·다큐 전환)
            fid = f"{self.p}fade"
            D.items.append(f'<div id="{fid}" style="position:absolute;inset:0;background:#000;opacity:1;pointer-events:none"></div>')
            D.js.append(f'tl.to("#{fid}",{{opacity:0,duration:0.45,ease:"power1.out"}},0.05);')
        if self.credits:
            D.label(" · ".join(dict.fromkeys(self.credits))[:150])


def s_story(D, sc: dict, bt: list, dur: float):
    from pathlib import Path
    from . import align
    from .motion2 import word_time
    D._proj = sc["_project_dir"]
    B = Board(D, f"st{sc['id']}")
    if sc.get("cam"):
        B.cam = "full" if sc["cam"] == "full" else tuple(sc["cam"])
    for k, (b, (t0, d)) in enumerate(zip(sc["beats"], bt)):
        if not b.get("draw"):
            continue
        wav = Path(sc["_project_dir"]) / "03_voice" / f"hb_{sc['id']:03d}_{k}.wav"
        try:
            ws = align.transcribe(wav, "ko")
        except Exception:  # noqa: BLE001
            ws = []
        for m in b["draw"]:
            tt = t0 + (word_time(ws, b["say"], m["t"], d) if m.get("t") else 0.05) + m.get("delay", 0.0)
            B.add(m, max(tt, 0.05))
    low = [k for k, (x, y, w, h) in B.pos.items() if y + h / 2 > 1860]
    if low:   # 그림판 맨 아래는 넓게 볼 때 자막과 겹침
        D.qa.append(f"story/caption_zone: {low} 가 그림판 아래쪽(y>1860) — 위로 옮기세요")
    B.finish(dur)
    dark0 = any(t < 1.0 and mode in ("dark", "photo") for t, mode, _s, _c in B.bg_events)   # 어두운 배경으로 시작하면 장 꼬리표도 밝게
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""), dark=dark0)
    if sc.get("credit"):
        D.label(sc.get("credit", ""))
    kinds = [m["do"] for b in sc["beats"] for m in b.get("draw", []) if m["do"] in ("photo", "doc", "sticker", "card", "draw", "figure", "chip", "note", "count", "big", "stamp")]
    if len(kinds) >= 6:   # 그림 패턴 반복 점검 (2026-11-13 사용자: "그림 패턴도 너무 매번 똑같다")
        top = max(set(kinds), key=kinds.count)
        if kinds.count(top) / len(kinds) > 0.5:
            D.qa.append(f"story/repetitive: '{top}' 가 그림의 {kinds.count(top) / len(kinds):.0%} — 재료를 섞으세요 (사진·문서·스티커·카드·큰 글자)")


def register():
    from . import hybrid
    hybrid.RENDER["story"] = s_story
