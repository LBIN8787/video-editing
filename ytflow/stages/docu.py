"""다큐 개념 장면 `docu` — 방송 다큐의 개념 설명 그래픽 문법 (docs/65, 2026-11-24 사용자:
"전문 방송국들이나 편집방식처럼 모션그래픽과 연출 편집방법을 나도 이런 퀄리티로 제작하고싶어 / 내 시장채널도 이런 다큐멘터리 편집법을 활용하고싶어").

레퍼런스(EBS 다큐프라임 어텐션 장면)에서 가져온 것 — 구조·움직임만:
  · 같은 물건이 끝까지 산다: 칩(회사·개념)이 장면 안에서 지워지지 않고 이어지고·옮겨지고·줄을 선다
  · 관계 = 선: 곡선이 그려지며 잇고, 세기는 굵기·밝기 (경쟁·약한 관계는 회색 점선)
  · 판 기울기(tilt): 구조 전체를 한 번 기울여 '판 위의 관계'로 보여 줌 — 카메라 움직임은 **개념 설명 장면에서만**
    (2026-11-24 사용자: v31 확대·축소 금지는 "쓰지 말아야 할 상황에서 남용했기 때문" — 차트·숫자·뉴스 장면은 계속 고정)
  · 신호가 퍼짐(pulse): 가운데에서 빛 점이 선을 타고 퍼지고, 닿은 칩의 숫자가 그때 오른다
  · 재배치(arrange: rank): 관계도의 칩이 그대로 한 줄로 옮겨 서고 아래에서 막대가 자라 순위가 됨 (그물 → 줄)

hybrid.json 장면:
  {"type": "docu", "title": "...", "label": "근거 ...", "panel": "판 이름(선택)",
   "nodes": {"nv": {"label": "엔비디아", "role": "가운데", "x": 960, "y": 560, "value": "+31.48%", "hub": true},
             "amd": {"label": "AMD", "role": "경쟁", "x": 1480, "y": 800, "value": "+6.85%", "tone": "rival"}, ...},
   "links": {"l1": {"from": "nv", "to": "mu", "label": "약정 3,900억 달러", "w": "strong"},
             "r1": {"from": "nv", "to": "amd", "kind": "rival"}},
   "beats": [{"say": "...", "do": [{"show": "nv", "t": "가운데에"}, {"link": ["l1"], "t": "메모리"},
                                     {"tilt": true, "t": "..."}, {"pulse": "nv", "t": "돌아오자"},
                                     {"focus": "mu", "t": "..."}, {"arrange": "rank", "t": "가까울수록", "headline": "가까울수록 더 올랐다"}]}]}
  "t" 는 그 박자 대사 속 낱말 — 그 말이 들리는 순간 (없으면 박자 시작부터 차례로).
숫자는 대본·팩트시트에 있는 값만 씁니다(사실 규칙). 관계 세기(w)는 '공급·고객·경쟁' 같은 종류 표시이지 계산값이 아닙니다.
"""
from __future__ import annotations

import html as H
import math
import re

W, HH = 1920, 1080
BG_CHIP = "linear-gradient(180deg,#22303A,#18222A)"
TEAL, TEAL_HI = "#5FC4AE", "#A8F0DC"
GOLD = "#F0BE5A"
GRAY = "#7C8590"
INKL = "#EEF3F1"
UP, DOWN = "#4FCB86", "#F0706A"
SAFE_BOTTOM = 925


def _measure(text: str, size: int) -> float:
    from PIL import ImageFont
    from .explain import HEAVY
    try:
        return ImageFont.truetype(str(HEAVY), size).getlength(text)
    except Exception:  # noqa: BLE001
        return len(text) * size * 0.9


def _num(v: str) -> float | None:
    m = re.search(r"[-+−]?\d[\d,]*(?:\.\d+)?", v or "")
    return float(m.group().replace(",", "").replace("−", "-")) if m else None


def _when(sc: dict, k: int, b: dict, t0: float, d: float, word: str | None, fallback: float) -> float:
    if word and sc.get("_project_dir"):
        from . import motion2
        try:
            t = motion2.row_time(sc, k, b, t0, d, word)
            if t is not None:
                return max(t0, t - 0.1)
        except Exception:  # noqa: BLE001
            pass
    return fallback


def s_docu(D, sc: dict, bt: list, dur: float):
    from . import explain
    sc = dict(sc)
    sc.setdefault("theme", "dark")
    explain._setup(D, sc, title=False)
    if sc.get("title"):
        tid = D._id()
        D.items.append(f'<div id="{tid}" style="position:absolute;left:150px;top:86px;font-family:heavy;font-size:44px;color:#E9EEF0;'
                       f'letter-spacing:-0.5px;opacity:0">{H.escape(sc["title"])}</div>')
        D.js.append(f'tl.fromTo("#{tid}",{{opacity:0,x:-18}},{{opacity:1,x:0,duration:.45,ease:"power2.out"}},0.15);')

    nodes = sc.get("nodes", {})
    links = sc.get("links", {})
    # 무대: 판 하나 — 기울기·재배치를 한꺼번에 받는 그릇
    stage, plate, svg_id = D._id(), D._id(), D._id()
    box = {}
    chips_html = []
    for key, nd in nodes.items():
        hub = bool(nd.get("hub"))
        size = 50 if hub else 40
        lab, role, val = nd.get("label", key), nd.get("role", ""), nd.get("value", "")
        w = max(_measure(lab, size), _measure(val, size - 4) if val else 0, _measure(role, 24) * 0.92) + 64
        w = max(w, 210 if hub else 180)
        h = 22 + (30 if role else 0) + size * 1.15 + ((size - 4) * 1.15 + 6 if val else 0) + 20
        x, y = nd["x"], nd["y"]
        y = min(y, SAFE_BOTTOM - h / 2)
        i = D._id()
        rival = nd.get("tone") == "rival"
        bord = GOLD if hub else (GRAY if rival else TEAL)
        vn = _num(val)
        vcol = (UP if (vn or 0) > 0 else DOWN if (vn or 0) < 0 else INKL)
        chips_html.append(
            f'<div id="{i}" style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;width:{w:.0f}px;height:{h:.0f}px;'
            f'box-sizing:border-box;border-radius:18px;background:{BG_CHIP};border:3px solid {bord};opacity:0;'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;'
            f'box-shadow:0 0 0 rgba(0,0,0,0),0 10px 30px rgba(0,0,0,.45)">'
            + (f'<div style="font-family:sans-x;font-size:24px;color:{"#9AA6AE" if rival else "#8FD9C6"}">{H.escape(role)}</div>' if role else "")
            + f'<div style="font-family:heavy;font-size:{size}px;color:{"#C9D0D5" if rival else INKL};line-height:1.1">{H.escape(lab)}</div>'
            + (f'<div id="{i}v" style="font-family:heavy;font-size:{size - 4}px;color:{vcol};line-height:1.1;opacity:0">{H.escape(val)}</div>' if val else "")
            + "</div>")
        box[key] = {"id": i, "x": x, "y": y, "w": w, "h": h, "val": val, "vn": vn, "hub": hub, "rival": rival, "bord": bord}

    # 선: 판 안의 svg 에 (판과 함께 기울어짐)
    paths = []
    lk = {}
    for key, ln in links.items():
        a, b = box.get(ln["from"]), box.get(ln["to"])
        if not a or not b:
            continue
        dx, dy = b["x"] - a["x"], b["y"] - a["y"]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        ra = min(abs(ux) * a["w"] / 2 + abs(uy) * a["h"] / 2, math.hypot(a["w"], a["h"]) / 2) + 14
        rb = min(abs(ux) * b["w"] / 2 + abs(uy) * b["h"] / 2, math.hypot(b["w"], b["h"]) / 2) + 14
        sx, sy, ex, ey = a["x"] + ux * ra, a["y"] + uy * ra, b["x"] - ux * rb, b["y"] - uy * rb
        bend = ln.get("bend", 0.14)
        cx, cy = (sx + ex) / 2 - uy * L * bend, (sy + ey) / 2 + ux * L * bend
        d = f"M{sx:.0f} {sy:.0f} Q{cx:.0f} {cy:.0f} {ex:.0f} {ey:.0f}"
        rival = ln.get("kind") == "rival"
        strong = ln.get("w") == "strong"
        col = GRAY if rival else TEAL
        wd = 3 if rival else (7 if strong else 4.5)
        pid = D._id()
        dash = ' stroke-dasharray="10 12"' if rival else ' pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"'
        glow = "" if rival else f' style="filter:drop-shadow(0 0 {8 if strong else 5}px {TEAL})"'
        paths.append(f'<path id="{pid}" d="{d}" fill="none" stroke="{col}" stroke-width="{wd}" stroke-linecap="round"{dash} opacity="0"{glow}/>')
        dot = D._id()
        paths.append(f'<path id="{dot}" d="{d}" fill="none" stroke="#FFF6D8" stroke-width="{wd + 7}" stroke-linecap="round" pathLength="1" '
                     f'stroke-dasharray="0.05 2" stroke-dashoffset="0.05" opacity="0" style="filter:drop-shadow(0 0 12px {GOLD})"/>')
        lab_id = None
        if ln.get("label"):
            mx, my = 0.25 * sx + 0.5 * cx + 0.25 * ex, 0.25 * sy + 0.5 * cy + 0.25 * ey
            sgn = -1 if bend >= 0 else 1
            lx, ly = mx + uy * 34 * sgn, my - ux * 34 * sgn
            lab_id = D._id()
            chips_html.append(f'<div id="{lab_id}" style="position:absolute;left:{lx:.0f}px;top:{ly:.0f}px;transform:translate(-50%,-50%);'
                              f'font-family:sans-x;font-size:28px;color:#FFE3A6;background:rgba(14,18,21,.82);padding:4px 12px;border-radius:8px;'
                              f'white-space:nowrap;opacity:0">{H.escape(ln["label"])}</div>')
        lk[key] = {"path": pid, "dot": dot, "label": lab_id, "rival": rival, "from": ln["from"], "to": ln["to"]}

    plate_html = ""
    if sc.get("panel"):
        plate_html = (f'<div id="{plate}" style="position:absolute;left:110px;top:150px;width:1700px;height:800px;border-radius:26px;'
                      f'border:2px dashed rgba(120,190,255,.0);background:rgba(40,80,130,0)">'
                      f'<div id="{plate}l" style="position:absolute;right:26px;top:14px;font-family:sans-x;font-size:24px;color:#86B6E6;opacity:0">{H.escape(sc["panel"])}</div></div>')
    D.items.append(
        f'<div style="position:absolute;left:0;top:0;width:{W}px;height:{HH}px;perspective:2000px;perspective-origin:50% 45%">'
        f'<div id="{stage}" style="position:absolute;left:0;top:0;width:{W}px;height:{HH}px;transform-style:preserve-3d;transform-origin:50% 60%">'
        f'{plate_html}<svg id="{svg_id}" width="{W}" height="{HH}" style="position:absolute;left:0;top:0;overflow:visible">{"".join(paths)}</svg>'
        f'{"".join(chips_html)}</div></div>')

    js = D.js
    shown, linked, counted = set(), set(), set()

    def show(key, t):
        bx = box.get(key)
        if not bx or key in shown:
            return
        shown.add(key)
        js.append(f'tl.fromTo("#{bx["id"]}",{{opacity:0,y:26,scale:.88}},{{opacity:1,y:0,scale:1,duration:.42,ease:"back.out(1.8)"}},{t:.2f});')
        D.sfx.append(("click-soft", t))
        if bx["val"] and (bx["hub"] or bx["rival"] or not has_pulse):
            count(key, t + 0.25)

    def count(key, t):
        bx = box[key]
        if key in counted or not bx["val"]:
            return
        counted.add(key)
        js.append(f'tl.to("#{bx["id"]}v",{{opacity:1,duration:.2}},{t:.2f});')
        n = bx["vn"]
        m = re.search(r"[-+−]?\d[\d,]*(?:\.\d+)?", bx["val"])
        if n is not None and m:
            dec = len(m.group().split(".")[1]) if "." in m.group() else 0
            pre, post = bx["val"][:m.start()], bx["val"][m.end():]
            sign = "+" if m.group().startswith("+") else ""
            js.append(f'(function(){{const o={{v:0}},el=document.getElementById("{bx["id"]}v");'
                      f'tl.to(o,{{v:{abs(n)},duration:.8,ease:"power2.out",onUpdate:()=>{{el.textContent={H.escape(pre)!r}+"{sign}"+'
                      f'o.v.toFixed({dec})+{H.escape(post)!r};}}}},{t:.2f});}})();')

    def glow(key, t, on=True, col=None):
        bx = box[key]
        c = col or (GOLD if bx["hub"] else TEAL_HI)
        if on:
            js.append(f'tl.to("#{bx["id"]}",{{boxShadow:"0 0 34px {c}, 0 10px 30px rgba(0,0,0,.45)",borderColor:"{c}",duration:.25}},{t:.2f});')
        else:
            js.append(f'tl.to("#{bx["id"]}",{{boxShadow:"0 0 0px rgba(0,0,0,0), 0 10px 30px rgba(0,0,0,.45)",borderColor:"{bx["bord"]}",duration:.35}},{t:.2f});')

    def link(key, t):
        L_ = lk.get(key)
        if not L_ or key in linked:
            return
        linked.add(key)
        js.append(f'tl.set("#{L_["path"]}",{{opacity:{0.75 if L_["rival"] else 1}}},{t:.2f});')
        if not L_["rival"]:
            js.append(f'tl.to("#{L_["path"]}",{{strokeDashoffset:0,duration:.6,ease:"power2.inOut"}},{t:.2f});')
        else:
            js.append(f'tl.fromTo("#{L_["path"]}",{{opacity:0}},{{opacity:.75,duration:.5}},{t:.2f});')
        if L_["label"]:
            js.append(f'tl.fromTo("#{L_["label"]}",{{opacity:0,y:8}},{{opacity:1,y:0,duration:.3}},{t + 0.45:.2f});')
        D.sfx.append(("pencil", t))

    has_pulse = any(isinstance(a, dict) and "pulse" in a for b in sc.get("beats", []) for a in (b.get("do") or []))
    tilted = False
    for k, (b, (t0, d)) in enumerate(zip(sc.get("beats", []), bt)):
        seq = t0 + 0.2
        for act in b.get("do") or []:
            if isinstance(act, str):
                act = {"show": act}
            t = _when(sc, k, b, t0, d, act.get("t"), seq)
            seq = max(seq, t) + 0.45
            if "show" in act:
                for j, key in enumerate(act["show"] if isinstance(act["show"], list) else [act["show"]]):
                    show(key, t + j * 0.18)
            if "link" in act:
                for j, key in enumerate(act["link"] if isinstance(act["link"], list) else [act["link"]]):
                    link(key, t + j * 0.2)
            if act.get("tilt") and not tilted:   # 개념 설명 장면에서만 쓰는 판 기울기 — 한 번, 천천히
                tilted = True
                js.append(f'tl.to("#{stage}",{{rotationX:18,y:-30,scale:.96,duration:1.4,ease:"power2.inOut"}},{t:.2f});')
                if sc.get("panel"):
                    js.append(f'tl.to("#{plate}",{{background:"rgba(40,80,130,.20)",borderColor:"rgba(120,190,255,.5)",duration:.8}},{t:.2f});'
                              f'tl.to("#{plate}l",{{opacity:1,duration:.5}},{t + 0.4:.2f});')
            if "pulse" in act:   # 가운데에서 빛 점이 선을 타고 퍼짐 → 닿으면 그 칩의 숫자가 오름
                src = act["pulse"]
                glow(src, t)
                count(src, t)
                for key, L_ in lk.items():
                    if L_["rival"] or L_["from"] != src or key not in linked:
                        continue
                    js.append(f'tl.set("#{L_["dot"]}",{{opacity:1,strokeDashoffset:0.05}},{t + 0.15:.2f});'
                              f'tl.to("#{L_["dot"]}",{{strokeDashoffset:-1,duration:.9,ease:"power1.in"}},{t + 0.15:.2f});'
                              f'tl.set("#{L_["dot"]}",{{opacity:0}},{t + 1.05:.2f});')
                    glow(L_["to"], t + 1.0)
                    count(L_["to"], t + 1.0)
                    glow(L_["to"], t + 2.2, on=False)
                D.sfx.append(("pop", t + 1.0))
            if "focus" in act:
                key = act["focus"]
                glow(key, t)
                for o in box:
                    if o != key and o in shown:
                        js.append(f'tl.to("#{box[o]["id"]}",{{opacity:.35,duration:.3}},{t:.2f});')
                back = ",".join("#" + box[o]["id"] for o in box if o != key and o in shown)
                if back:
                    js.append(f'tl.to("{back}",{{opacity:1,duration:.3}},{t + act.get("hold", 2.4):.2f});')
                glow(key, t + act.get("hold", 2.4), on=False)
            if act.get("arrange") == "rank":   # 그물 → 줄: 같은 칩이 값 순서대로 한 줄에 서고, 아래에서 막대가 자람
                order = sorted([k_ for k_ in box if box[k_]["vn"] is not None], key=lambda k_: -box[k_]["vn"])
                if tilted:
                    js.append(f'tl.to("#{stage}",{{rotationX:0,y:0,scale:1,duration:1.0,ease:"power2.inOut"}},{t:.2f});')
                for L_ in lk.values():
                    js.append(f'tl.to("{",".join("#" + x for x in (L_["path"], L_["label"]) if x)}",{{opacity:0,duration:.35}},{t:.2f});')
                if sc.get("panel"):
                    js.append(f'tl.to("#{plate}",{{opacity:0,duration:.4}},{t:.2f});')
                n = len(order)
                gapx = min(250, 1640 / max(n, 1))
                x0 = 960 - gapx * (n - 1) / 2
                yrow = 800
                vmax = max(abs(box[k_]["vn"]) for k_ in order) or 1
                for j, key in enumerate(order):
                    bx = box[key]
                    tx, ty = x0 + j * gapx, yrow
                    sc_ = min(1.0, (gapx - 26) / bx["w"])
                    count(key, t)
                    js.append(f'tl.to("#{bx["id"]}",{{x:{tx - bx["x"]:.0f},y:{ty - bx["y"]:.0f},scale:{sc_:.2f},opacity:1,duration:1.0,ease:"power3.inOut"}},{t + j * 0.05:.2f});')
                    hbar = 380 * abs(bx["vn"]) / vmax
                    bid = D._id()
                    top_chip = ty - bx["h"] * sc_ / 2 - 12
                    col = GOLD if bx["hub"] else (GRAY if bx["rival"] else TEAL)
                    D.items.append(f'<div id="{bid}" style="position:absolute;left:{tx - 46:.0f}px;top:{top_chip - hbar:.0f}px;width:92px;height:{hbar:.0f}px;'
                                   f'border-radius:10px 10px 4px 4px;background:linear-gradient(180deg,{col},{col}55);transform-origin:50% 100%;'
                                   f'transform:scaleY(0);box-shadow:0 0 18px {col}66"></div>')
                    js.append(f'tl.to("#{bid}",{{scaleY:1,duration:.7,ease:"power2.out"}},{t + 1.0 + j * 0.12:.2f});')
                if act.get("headline"):
                    hid = D._id()
                    D.items.append(f'<div id="{hid}" style="position:absolute;left:960px;top:230px;transform:translate(-50%,-50%);font-family:heavy;'
                                   f'font-size:60px;color:{GOLD};opacity:0;white-space:nowrap">{H.escape(act["headline"])}</div>')
                    js.append(f'tl.fromTo("#{hid}",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.5,ease:"power2.out"}},{t + 1.6:.2f});')
                D.sfx.append(("whoosh-short", t))
    # 대사보다 먼저 끝나 멈춰 있는 칩이 없게 — 보이지 않은 칩은 마지막 박자 끝에 남은 채로 둠(QA 에서 확인)
    missing = [k_ for k_ in box if k_ not in shown]
    if missing:
        D.qa.append(f"다큐 장면 {sc.get('id')}: 박자에서 보이지 않은 칩 — {', '.join(missing)}")


def register():
    from . import hybrid
    from . import explain
    hybrid.RENDER["docu"] = explain._themed(s_docu)   # 어두운 무대 공통 색 변환(근거 라벨·장 표시 밝게)
