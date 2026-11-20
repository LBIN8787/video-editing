"""새 화풍 3종 시안 — 같은 내용(물건이 집 앞까지 오는 길: 공장 → 물류센터 → 트럭 → 문 앞)을 화풍만 바꿔 렌더.

2026-11-20 사용자: docs/53 §5-3 "새 화풍 후보 셋(아이소메트릭·화이트보드·종이 디오라마)" → "전부 다".
바탕으로 삼은 HyperFrames 블록(이미 설치됨, styles/hyperframes_blocks.yaml):
  whiteboard   ← whiteboard-ink(한 획씩 + 펜촉이 따라감), hw-callout-circle
  isometric    ← exploded-stack(아이소메트릭 층), arc/offset-path-traveler(길 따라 이동)
  paper-diorama← stop-motion-cadence(끊어 움직이기), torn-paper-rip·paper-collage-reveal(종이 질감)
블록 원본을 복사하지 않고, 같은 원리를 우리 글꼴·색으로 다시 씀 (코드로 그린 도형이 '도형 모음'으로 보이는지가 이 시안의 판정 거리 — 05 §0-8).

    python projects/20261120-looks-trial/02_script/render_trial.py [whiteboard isometric paper-diorama]
→ 05_edit/<id>.mp4 (커밋 안 함) + 05_edit/<id>_*.jpg 프레임
"""
from __future__ import annotations

import json
import math
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
ROOT = PROJ.parents[1]
TOOLS = ROOT / "tools" / "hyperframes"
BIN = TOOLS / "node_modules" / ".bin" / "hyperframes"
GSAP = TOOLS / "node_modules" / "gsap" / "dist" / "gsap.min.js"
FONTS = ROOT / "ytflow" / "assets" / "fonts"
W, H, DUR = 1280, 720, 8.0
STOPS = ["공장", "물류센터", "트럭", "문 앞"]
EV: dict[str, list] = {}   # 화풍마다 효과음 사건 (이름, 초) — 짝인 효과음 묶음(assets/sfx/sfx.yaml)으로 섞음
SFX = {"whiteboard": "marker", "isometric": "soft-ui", "paper-diorama": "paper-pencil"}
TITLE = "물건이 집 앞까지 오는 길"


def shell(body: str, css: str, js: str, bg: str) -> str:
    fonts = "".join(f"@font-face{{font-family:{n};src:url('assets/{f}')}}" for n, f in
                    (("pen", "NanumPenScript-Regular.ttf"), ("sans", "NanumGothic-Bold.ttf"), ("sansx", "NanumGothic-ExtraBold.ttf")))
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H}">
<script src="assets/gsap.min.js"></script>
<style>{fonts}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{bg}}}
#root{{position:relative;width:100%;height:100%;overflow:hidden}}
{css}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-width="{W}" data-height="{H}">
<div id="layer" class="clip" data-start="0" data-duration="{DUR:.2f}" data-track-index="0" data-layout-allow-overlap>
{body}
</div></div>
<script>
const tl = gsap.timeline({{ paused: true }});
{js}
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>"""


# ---------------------------------------------------------------- 화이트보드
def wobble(pts, rnd, amp=2.2, closed=False, passes=2):
    """손으로 두 번 그은 듯한 선 (점마다 조금씩 어긋남)."""
    out = []
    for p in range(passes):
        ps = pts + ([pts[0]] if closed else [])
        seg = []
        for i, (x, y) in enumerate(ps):
            dx, dy = rnd.uniform(-amp, amp), rnd.uniform(-amp, amp)
            seg.append(f"{'M' if i == 0 else 'L'}{x + dx:.1f} {y + dy:.1f}")
        out.append(" ".join(seg))
    return out


def whiteboard() -> tuple[str, str, str, str]:
    rnd = random.Random(4)
    xs = [190, 500, 800, 1090]
    gy = 400
    icons = []
    # 공장: 톱니 지붕 + 굴뚝
    icons.append([[(120, gy), (120, 330), (165, 300), (165, 330), (210, 300), (210, 330), (255, 300), (255, gy)], [(222, 305), (222, 250), (240, 250), (240, 302)]])
    # 물류센터: 넓은 상자 + 문
    icons.append([[(420, gy), (420, 315), (500, 285), (580, 315), (580, gy)], [(470, gy), (470, 345), (530, 345), (530, gy)]])
    # 트럭
    icons.append([[(730, 385), (730, 320), (835, 320), (835, 385)], [(835, 345), (868, 345), (885, 365), (885, 385), (835, 385)]])
    # 집
    icons.append([[(1035, gy), (1035, 335), (1145, 335), (1145, gy)], [(1020, 340), (1090, 285), (1160, 340)], [(1077, gy), (1077, 362), (1103, 362), (1103, gy)]])
    paths, t = [], 1.3
    for k, ic in enumerate(icons):
        for poly in ic:
            for d in wobble(poly, rnd):
                paths.append((d, "#1d2433", 4.2, t))
                t += 0.16
        t += 0.25
    # 트럭 바퀴 (원)
    for cx in (760, 860):
        pts = [(cx + 13 * math.cos(a / 10 * math.tau), 392 + 13 * math.sin(a / 10 * math.tau)) for a in range(11)]
        paths.append((wobble(pts, rnd, 1.2, passes=1)[0], "#1d2433", 4.2, 3.9))
    # 화살표 (파랑)
    arrows = []
    for a, b in ((270, 405), (595, 715), (900, 1010)):
        mid = (a + b) / 2
        d = f"M{a} 345 Q{mid} {315 + rnd.uniform(-6, 6):.0f} {b} 345"
        head = f"M{b - 16} 333 L{b} 345 L{b - 18} 356"
        arrows += [d, head]
    at = [1.9, 1.9, 2.95, 2.95, 4.05, 4.05]
    for d, tt in zip(arrows, at):
        paths.append((d, "#2459c9", 4.6, tt + 0.55))
    # 빨간 동그라미 (문 앞)
    circ = [(1090 + 105 * math.cos(a / 18 * math.tau + 0.4), 345 + 82 * math.sin(a / 18 * math.tau + 0.4)) for a in range(21)]
    paths.append((wobble(circ, rnd, 3, passes=1)[0], "#d23b2f", 5, 5.6))
    # 지워진 판서 흔적
    ghosts = "".join(f'<path d="{wobble([(rnd.uniform(80, 1200), rnd.uniform(120, 650)) for _ in range(5)], rnd, 8, passes=1)[0]}" class="ghost"/>' for _ in range(7))
    svg = ghosts + "".join(f'<path id="p{i}" d="{d}" stroke="{c}" stroke-width="{w}" class="mk"/>' for i, (d, c, w, _) in enumerate(paths))
    labels = "".join(f'<div class="lb" id="l{k}" style="left:{x - 110}px;top:{gy + 26}px">{s}</div>' for k, (x, s) in enumerate(zip(xs, STOPS)))
    body = (f'<div id="title">{TITLE}</div><div id="tu"></div>'
            f'<div id="stage"><svg id="board" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{svg}</svg>{labels}'
            f'<div id="note">도착!</div><div id="nib"></div></div>')
    css = """
#stage{position:absolute;inset:0;transform-origin:640px 380px;transform:translate(0,95px) scale(1.12)}
#board{position:absolute;inset:0}
.mk{fill:none;stroke-linecap:round;stroke-linejoin:round;opacity:.92}
.ghost{fill:none;stroke:#8b93a3;stroke-width:5;opacity:.05;stroke-linecap:round}
#title{position:absolute;left:0;width:100%;top:92px;text-align:center;font:84px pen;color:#1d2433;clip-path:inset(0 100% 0 0)}
#tu{position:absolute;left:390px;top:196px;width:500px;height:7px;border-radius:4px;background:#2459c9;transform-origin:left;transform:scaleX(0);opacity:.85}
.lb{position:absolute;width:220px;text-align:center;font:52px pen;color:#1d2433;opacity:0}
#note{position:absolute;left:1045px;top:188px;font:60px pen;color:#d23b2f;opacity:0;transform:rotate(-6deg)}
#nib{position:absolute;left:0;top:0;width:16px;height:46px;border-radius:5px 5px 8px 8px;background:linear-gradient(#2c3442,#11151d);
  box-shadow:3px 6px 10px rgba(0,0,0,.18);transform-origin:50% 100%;opacity:0}
"""
    js = ["const nib=document.getElementById('nib');",
          "function follow(p,f){const L=p.getTotalLength(),pt=p.getPointAtLength(L*f);nib.style.transform=`translate(${pt.x-8}px,${pt.y-46}px) rotate(18deg)`;}",
          "tl.to('#title',{clipPath:'inset(0 0% 0 0)',duration:1.0,ease:'none'},0.15);",
          "tl.to('#tu',{scaleX:1,duration:0.45,ease:'power2.out'},1.05);"]
    for i, (_, _, _, tt) in enumerate(paths):
        dur = 0.32 if i < len(paths) - 1 else 0.8
        js.append(f"(function(){{const p=document.getElementById('p{i}');const L=p.getTotalLength()+2;p.style.strokeDasharray=L;p.style.strokeDashoffset=L;"
                  f"const o={{f:0}};tl.to(o,{{f:1,duration:{dur},ease:'power1.inOut',onUpdate:()=>{{p.style.strokeDashoffset=L*(1-o.f);follow(p,o.f);}}}},{tt:.2f});}})();")
    EV["whiteboard"] = [("pencil", tt) for i, (_, _, _, tt) in enumerate(paths) if i % 2 == 0] + [("pop", t) for t in (2.0, 3.05, 4.15, 5.05, 6.3)]
    js.append("tl.set(nib,{opacity:1},1.28);tl.to(nib,{opacity:0,duration:0.3},6.6);")
    for k in range(4):
        js.append(f"tl.to('#l{k}',{{opacity:1,duration:0.35}},{[2.0, 3.05, 4.15, 5.05][k]});")
    js.append("tl.to('#note',{opacity:1,duration:0.3},6.3);")
    return body, css, "\n".join(js), "radial-gradient(ellipse at 30% 18%,#ffffff 0%,#f4f6f8 45%,#e6e9ee 100%)"


# ---------------------------------------------------------------- 아이소메트릭
C30, S30 = math.cos(math.pi / 6), math.sin(math.pi / 6)
UNIT, CX, CY = 46, 640, 250


def iso(x, y, z=0.0):
    return CX + (x - y) * C30 * UNIT, CY + (x + y) * S30 * UNIT - z * UNIT


def poly(pts, fill, extra=""):
    return f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{fill}" {extra}/>'


def box(x, y, w, d, h, top, left, right, z=0):
    """x,y 바닥 모서리에서 w(x방향)·d(y방향)·h 높이 상자: 보이는 세 면."""
    P = lambda a, b, c: iso(x + a, y + b, z + c)
    return (poly([P(0, d, 0), P(w, d, 0), P(w, d, h), P(0, d, h)], left)
            + poly([P(w, 0, 0), P(w, d, 0), P(w, d, h), P(w, 0, h)], right)
            + poly([P(0, 0, h), P(w, 0, h), P(w, d, h), P(0, d, h)], top))


def isometric() -> tuple[str, str, str, str]:
    global CX, CY, UNIT
    navy = ("#3d4f7a", "#2b3a5e", "#22304f")
    teal = ("#5fb3a8", "#3f8f86", "#2f7069")
    sand = ("#f1d9a7", "#d9b97c", "#c29e5e")
    coral = ("#f08a6c", "#d06a4e", "#b0553d")
    UNIT = 50
    # 정거장: 오른쪽으로 펼쳐지도록 x 는 늘고 y 는 줄임 → 화면에서 거의 가로로
    st = [dict(x=0.0, y=0.0, w=2.4, d=2.0), dict(x=3.6, y=-1.9, w=2.8, d=2.0), dict(x=7.3, y=-3.3, w=1.7, d=0.8), dict(x=10.0, y=-5.6, w=1.5, d=1.6)]
    rd = [(q["x"] + q["w"] / 2, q["y"] + q["d"] + 0.8) for q in st]
    rd[2] = (st[2]["x"] + 0.8, st[2]["y"] + 0.4)   # 트럭은 길 위
    route = [rd[0]]
    for a_, b_ in zip(rd, rd[1:]):
        route += [(b_[0], a_[1]), b_]
    # 화면 가운데 맞추기
    CX = CY = 0
    pts = [iso(q["x"] + dx, q["y"] + dy, z) for q in st for dx in (0, q["w"]) for dy in (0, q["d"]) for z in (0, 2.6)] + [iso(x, y) for x, y in route]
    xs_, ys_ = [p[0] for p in pts], [p[1] for p in pts]
    CX, CY = 640 - (min(xs_) + max(xs_)) / 2, 410 - (min(ys_) + max(ys_)) / 2
    gx0, gx1, gy0, gy1 = -1.5, 12.5, -7.5, 4.5
    ground = poly([iso(gx0, gy0), iso(gx1, gy0), iso(gx1, gy1), iso(gx0, gy1)], "#e3e8ef", 'class="ground"')
    tiles = "".join(poly([iso(i, j), iso(i + 1, j), iso(i + 1, j + 1), iso(i, j + 1)], "none", 'class="grid"')
                    for i in range(int(gx0), int(gx1)) for j in range(int(gy0), int(gy1)))
    road = ""
    for (x0, y0), (x1, y1) in zip(route, route[1:]):
        if abs(y1 - y0) < 1e-6:   # x 방향
            lo, hi = min(x0, x1) - 0.4, max(x0, x1) + 0.4
            road += poly([iso(lo, y0 - 0.4), iso(hi, y0 - 0.4), iso(hi, y0 + 0.4), iso(lo, y0 + 0.4)], "#c9d1dc", 'class="road"')
        else:
            lo, hi = min(y0, y1) - 0.4, max(y0, y1) + 0.4
            road += poly([iso(x0 - 0.4, lo), iso(x0 + 0.4, lo), iso(x0 + 0.4, hi), iso(x0 - 0.4, hi)], "#c9d1dc", 'class="road"')
    lane = "M" + " L".join(f"{iso(x, y)[0]:.1f} {iso(x, y)[1]:.1f}" for x, y in route)
    q0, q1, q2, q3 = st
    b = []
    b.append('<g class="bd" id="b0">' + box(q0["x"], q0["y"], q0["w"], q0["d"], 1.4, *navy) + box(q0["x"] + 1.7, q0["y"] + 0.2, 0.45, 0.45, 2.6, *navy) + "</g>")
    b.append('<g class="bd" id="b1">' + box(q1["x"], q1["y"], q1["w"], q1["d"], 1.1, *teal)
             + box(q1["x"] + 0.9, q1["y"] + q1["d"] - 0.04, 1.0, 0.08, 0.7, "#e8f4f2", "#e8f4f2", "#cfe3df") + "</g>")
    b.append('<g class="bd" id="b2">' + box(q2["x"], q2["y"], 1.2, 0.8, 0.75, *sand) + box(q2["x"] + 1.2, q2["y"] + 0.05, 0.45, 0.7, 0.55, *coral) + "</g>")
    x3, y3 = q3["x"], q3["y"]
    roof = (poly([iso(x3 - 0.1, y3 - 0.05, 1.0), iso(x3 + 1.6, y3 - 0.05, 1.0), iso(x3 + 1.6, y3 + 0.8, 1.7), iso(x3 - 0.1, y3 + 0.8, 1.7)], coral[0])
            + poly([iso(x3 + 1.6, y3 - 0.05, 1.0), iso(x3 + 1.6, y3 + 1.65, 1.0), iso(x3 + 1.6, y3 + 0.8, 1.7)], coral[2])
            + poly([iso(x3 - 0.1, y3 + 0.8, 1.7), iso(x3 + 1.6, y3 + 0.8, 1.7), iso(x3 + 1.6, y3 + 1.65, 1.0), iso(x3 - 0.1, y3 + 1.65, 1.0)], coral[1]))
    b.append('<g class="bd" id="b3">' + box(x3, y3, q3["w"], q3["d"], 1.0, "#f6efe4", "#e2d6c3", "#cdbfa9") + roof + "</g>")
    tops = [iso(q["x"] + q["w"] / 2, q["y"] + q["d"] / 2, hz) for q, hz in zip(st, (2.6, 1.1, 0.75, 1.7))]
    pk = box(-0.2, -0.2, 0.4, 0.4, 0.4, "#ffd166", "#e6b24a", "#c9962f")
    sroute = [iso(x, y, 0) for x, y in route]
    labels = "".join(f'<div class="lb" id="l{k}" style="left:{x - 90:.0f}px;top:{y - 86:.0f}px">{s}</div>' for k, ((x, y), s) in enumerate(zip(tops, STOPS)))
    body = (f'<div id="title">{TITLE}</div><div id="cam"><svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{ground}{tiles}{road}'
            f'<path id="lane" d="{lane}" class="lane"/>{"".join(b)}<g id="pk">{pk}</g></svg>{labels}</div>')
    css = """
#cam{position:absolute;inset:0;transform-origin:50% 58%}
.grid{stroke:#cfd6e0;stroke-width:1}
.lane{stroke:#fff;stroke-width:3;stroke-dasharray:14 12;fill:none}
.bd polygon{stroke:rgba(20,28,45,.25);stroke-width:1;stroke-linejoin:round}
#title{position:absolute;left:70px;top:58px;font:46px sansx;color:#22304f;letter-spacing:-1px}
.lb{position:absolute;width:180px;text-align:center;font:30px sansx;color:#22304f;opacity:0}
.lb::after{content:'';display:block;margin:6px auto 0;width:2px;height:24px;background:#22304f;opacity:.5}
"""
    js = ["tl.from('#title',{y:20,opacity:0,duration:0.6,ease:'power2.out'},0.1);",
          "tl.from('.ground,.grid',{opacity:0,duration:0.6},0.1);",
          "tl.from('.road,#lane',{opacity:0,duration:0.4},0.5);",
          "tl.fromTo('#cam',{scale:1.0},{scale:1.06,duration:8,ease:'none'},0);"]
    for k in range(4):
        t0 = 0.8 + k * 0.45
        js.append(f"tl.from('#b{k}',{{y:60,opacity:0,duration:0.7,ease:'back.out(1.6)'}},{t0:.2f});")
        js.append(f"tl.to('#l{k}',{{opacity:1,duration:0.35}},{t0 + 0.5:.2f});")
    pts = json.dumps([[round(a, 1), round(c, 1)] for a, c in sroute])
    js.append(f"""(function(){{const R={pts};const g=document.getElementById('pk');const o={{f:0}};
const seg=[];let T=0;for(let i=0;i<R.length-1;i++){{const l=Math.hypot(R[i+1][0]-R[i][0],R[i+1][1]-R[i][1]);seg.push(l);T+=l;}}
function at(f){{let d=f*T;for(let i=0;i<seg.length;i++){{if(d<=seg[i]||i==seg.length-1){{const u=Math.min(1,d/seg[i]);return [R[i][0]+(R[i+1][0]-R[i][0])*u,R[i][1]+(R[i+1][1]-R[i][1])*u];}}d-=seg[i];}}}}
const put=()=>{{const p=at(o.f);g.setAttribute('transform',`translate(${{p[0]-{CX:.1f}}},${{p[1]-{CY:.1f}}})`);}};put();
tl.from(g,{{opacity:0,duration:0.3}},3.0);tl.to(o,{{f:1,duration:3.6,ease:'power1.inOut',onUpdate:put}},3.2);}})();""")
    js.append("tl.to('#l3',{color:'#d06a4e',scale:1.12,duration:0.3},6.8);")
    EV["isometric"] = [("pop", 0.8 + k * 0.45) for k in range(4)] + [("whoosh-short", 3.2), ("chime", 6.8)]
    return body, css, "\n".join(js), "#eef1f5"


# ---------------------------------------------------------------- 종이 디오라마
def torn(y, rnd, amp=7, step=26, x0=-120, x1=W + 320, wave=0.0, ph=0.0):
    pts, x = [], x0
    while x <= x1:
        pts.append((x, y + wave * math.sin(x / 210 + ph) + rnd.uniform(-amp, amp)))
        x += step * rnd.uniform(0.6, 1.3)
    d = "M" + " L".join(f"{a:.0f} {b:.0f}" for a, b in pts) + f" L{x1} {H + 60} L{x0} {H + 60} Z"
    return d


def paper_diorama() -> tuple[str, str, str, str]:
    rnd = random.Random(9)
    layers = [("far", torn(330, rnd, 6, wave=38, ph=0.3), "#b8cfc3", -28),
              ("mid", torn(420, rnd, 7, wave=24, ph=2.0), "#8fb39e", -60),
              ("road", torn(530, rnd, 5, wave=4), "#d8c3a0", -95),
              ("front", torn(625, rnd, 8, wave=12, ph=1.1), "#6f9a7f", -140)]
    defs = """<defs><filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="5"/>
<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .09 0"/><feComposite in2="SourceGraphic" operator="in"/><feBlend in="SourceGraphic" mode="multiply"/></filter></defs>"""
    lay = "".join(f'<svg class="ly" id="{n}" width="{W + 400}" height="{H}" viewBox="-100 0 {W + 400} {H}">{defs}<path d="{d}" fill="{c}" filter="url(#grain)"/></svg>'
                  for n, d, c, _ in layers)
    # 종이 건물: 평평하게 누워 있다가 세워짐 (팝업북)
    def cut(svg_inner, x, y, w, h, i):
        return (f'<div class="pop" id="pp{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
                f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{svg_inner}</svg></div>')
    factory = ('<path d="M4 176 V70 L52 40 V70 L100 40 V70 L148 40 V176 Z" fill="#7d8aa6"/><rect x="118" y="6" width="20" height="60" fill="#6b7792"/>'
               '<rect x="24" y="110" width="26" height="30" fill="#f4e6c8"/><rect x="74" y="110" width="26" height="30" fill="#f4e6c8"/>')
    ware = '<path d="M4 150 V64 L110 18 L216 64 V150 Z" fill="#c98b5a"/><rect x="80" y="86" width="56" height="64" fill="#8a5a36"/>'
    house = ('<path d="M10 70 L80 8 L150 70 Z" fill="#d0645a"/><rect x="22" y="66" width="116" height="94" fill="#f2e5cf"/>'
             '<rect x="66" y="104" width="30" height="56" fill="#8a5a36"/><rect x="36" y="86" width="22" height="22" fill="#9cc3d5"/>')
    pops = cut(factory, 120, 286, 152, 180, 0) + cut(ware, 410, 316, 220, 154, 1) + cut(house, 1020, 350, 160, 162, 2)
    truck = ('<div id="truck"><svg width="170" height="96" viewBox="0 0 170 96"><rect x="4" y="10" width="104" height="60" rx="4" fill="#f2c14e"/>'
             '<path d="M108 30 H140 L162 52 V70 H108 Z" fill="#e07a5f"/><rect x="118" y="36" width="20" height="16" fill="#cfe6f0"/>'
             '<circle cx="34" cy="76" r="14" fill="#3b3b3b"/><circle cx="132" cy="76" r="14" fill="#3b3b3b"/>'
             '<circle cx="34" cy="76" r="5" fill="#d9d9d9"/><circle cx="132" cy="76" r="5" fill="#d9d9d9"/></svg></div>')
    tg = lambda k, s, x, y, r: f'<div class="tag" id="t{k}" style="left:{x}px;top:{y}px;transform:rotate({r}deg)">{s}</div>'
    tags = "".join(tg(k, STOPS[k], x, y, r) for k, (x, y, r) in ((0, (135, 236, -4)), (1, (455, 262, 3)), (3, (1030, 296, 4))))
    truck = truck.replace('</svg></div>', '</svg>' + tg(2, STOPS[2], 30, -50, -3) + '</div>')
    clouds = "".join(f'<div class="cloud" style="left:{x}px;top:{y}px;width:{w}px;height:{w * .42:.0f}px"></div>' for x, y, w in ((180, 140, 150), (820, 110, 190), (1090, 190, 120)))
    body = (f'<div id="sky"></div><div id="sun"></div><div id="clouds">{clouds}</div>{lay}'
            f'<div id="props">{pops}{truck}</div>{tags}<div id="title"><span>{TITLE}</span></div><div id="tape"></div>')
    css = """
#sky{position:absolute;inset:0;background:linear-gradient(#f6ead2,#efdcbc)}
#sun{position:absolute;left:960px;top:70px;width:110px;height:110px;border-radius:50%;background:#f3a95b;box-shadow:4px 6px 0 rgba(90,60,30,.18)}
.cloud{position:absolute;border-radius:60px;background:#fffaf0;box-shadow:3px 5px 0 rgba(90,60,30,.12)}
.ly{position:absolute;left:-100px;top:0;filter:drop-shadow(0 -3px 0 rgba(255,255,255,.35)) drop-shadow(0 6px 6px rgba(60,40,20,.28))}
#props{position:absolute;inset:0;perspective:900px}
.pop{position:absolute;transform-origin:50% 100%;filter:drop-shadow(5px 8px 4px rgba(60,40,20,.3))}
#truck{position:absolute;left:150px;top:470px;filter:drop-shadow(5px 7px 3px rgba(60,40,20,.3))}
.tag{position:absolute;background:#fffaf0;padding:6px 18px;font:34px sansx;color:#4b3a2a;box-shadow:3px 4px 0 rgba(60,40,20,.2);opacity:0}
#title{position:absolute;left:0;width:100%;top:34px;text-align:center}
#title span{display:inline-block;background:#fffaf0;padding:10px 30px;font:50px sansx;color:#4b3a2a;transform:rotate(-1.5deg);box-shadow:4px 6px 0 rgba(60,40,20,.18)}
#tape{position:absolute;left:330px;top:24px;width:90px;height:28px;background:rgba(240,220,160,.75);transform:rotate(-6deg)}
"""
    js = ["tl.from('#title span,#tape',{y:-80,duration:0.6,ease:'back.out(1.4)'},0.1);"]
    # 층이 아래에서 올라옴 + 카메라(시차): 층마다 다르게 옆으로
    for k, (n, _, _, dx) in enumerate(layers):
        js.append(f"tl.from('#{n}',{{y:220,duration:0.7,ease:'power3.out'}},{0.2 + k * 0.12:.2f});")
        js.append(f"tl.to('#{n}',{{x:{dx},duration:7.2,ease:'none'}},0.8);")
    js.append("tl.to('#clouds',{x:-14,duration:7.2,ease:'none'},0.8);tl.to('#props',{x:-80,duration:7.2,ease:'none'},0.8);")
    for k, t0 in enumerate((1.0, 1.5, 2.0)):
        js.append(f"tl.fromTo('#pp{k}',{{rotationX:-88}},{{rotationX:0,duration:0.8,ease:'back.out(1.7)'}},{t0});")
    for k, t0 in enumerate((1.6, 2.1, 3.0, 2.6)):
        js.append(f"tl.to('#t{k}',{{opacity:1,duration:0.01}},{t0});tl.from('#t{k}',{{y:-30,duration:0.4,ease:'back.out(2)'}},{t0});")
    # 트럭: 끊어 움직이기 (stop-motion — 초당 12장 느낌), 살짝 들썩
    js.append("tl.from('#truck',{opacity:0,duration:0.2},2.8);tl.to('#truck',{x:760,duration:3.6,ease:'steps(40)'},3.0);"
              "tl.to('#truck',{y:-4,duration:0.25,ease:'steps(2)',yoyo:true,repeat:13},3.0);")
    js.append("tl.to('#t3',{scale:1.15,duration:0.3,ease:'back.out(2)'},6.7);")
    EV["paper-diorama"] = [("whoosh-short", 0.2), ("pop", 1.0), ("pop", 1.5), ("pop", 2.0), ("whoosh-short", 3.0), ("pop", 6.7)]
    return body, css, "\n".join(js), "#efdcbc"


def _add_sfx(lid: str, out: Path) -> None:
    """짝인 효과음 묶음으로 사건 소리를 섞어 넣음 (ytflow hybrid.sfx_files 와 같은 묶음 규칙)."""
    sys.path.insert(0, str(ROOT))
    from ytflow.stages import hybrid, looks
    pal = looks.sfx_palettes()[SFX[lid]]
    base = hybrid.sfx_files()
    mp = pal.get("map") or {}
    ins, flt = [], []
    for k, (ev, t) in enumerate(EV.get(lid, [])):
        tgt = mp.get(ev, ev) if ev in mp else ev
        if tgt is None:
            continue
        f = base.get(str(tgt).removeprefix("synth:"))
        if not f:
            continue
        ins += ["-i", str(f)]
        vol = {"pencil": 0.5, "pop": 0.45, "whoosh-short": 0.4, "chime": 0.35}.get(ev, 0.4) * float(pal.get("gain", 1))
        flt.append(f"[{len(ins) // 2}:a]atrim=0:{1.2 if ev == 'pencil' else 2.0},volume={vol:.2f},adelay={int(t * 1000)}|{int(t * 1000)}[s{k}]")
    if not flt:
        return
    lab = "".join(f.rsplit("[", 1)[1].join(["[", ""]) for f in flt)
    tmp = out.with_suffix(".sfx.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out), *ins, "-filter_complex",
                    ";".join(flt) + f";{lab}amix=inputs={len(flt)}:normalize=0,apad[a]", "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", str(tmp)], check=True)
    tmp.replace(out)


LOOKS = {"whiteboard": whiteboard, "isometric": isometric, "paper-diorama": paper_diorama}


def render(lid: str) -> Path:
    work = PROJ / "05_edit" / "work" / lid
    (work / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy(GSAP, work / "assets" / "gsap.min.js")
    for f in ("NanumPenScript-Regular.ttf", "NanumGothic-Bold.ttf", "NanumGothic-ExtraBold.ttf"):
        shutil.copy(FONTS / f, work / "assets" / f)
    body, css, js, bg = LOOKS[lid]()
    (work / "index.html").write_text(shell(body, css, js, bg), encoding="utf-8")
    (work / "hyperframes.json").write_text(json.dumps({"name": lid}), encoding="utf-8")
    env = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1")
    shellbin = next(Path("/opt/pw-browsers").glob("chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell"), None) \
        if Path("/opt/pw-browsers").exists() else None
    if shellbin:
        env.setdefault("PRODUCER_HEADLESS_SHELL_PATH", str(shellbin))
    out = PROJ / "05_edit" / f"{lid}.mp4"
    r = subprocess.run([str(BIN), "render", "--quality", "looks", "-o", str(out)], cwd=work, env=env, capture_output=True, text=True, timeout=900)
    if r.returncode or not out.exists():
        raise SystemExit(f"[{lid}] 렌더 실패: {(r.stderr or r.stdout)[-600:]}")
    _add_sfx(lid, out)
    for t in (1.5, 3.5, 5.0, 7.6):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(out), "-frames:v", "1", "-q:v", "3",
                        str(PROJ / "05_edit" / f"{lid}_{t:.1f}.jpg")], check=True)
    return out


if __name__ == "__main__":
    for lid in sys.argv[1:] or list(LOOKS):
        print(lid, "→", render(lid))
