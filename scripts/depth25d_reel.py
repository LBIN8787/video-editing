"""입체감 있는 2.5D 모션그래픽 견본 (docs/38 §7) — 진짜 CSS 3D(원근 + 깊이 층)로 만든 다섯 가지.

    python scripts/depth25d_reel.py [출력폴더]      # → depth25d.mp4 + sheet.png (기본 .cache/depth25d)

1. 멀티플레인 풍경   — 평면 그림 6층을 서로 다른 깊이에 두고 카메라가 다가감 → 가까운 층일수록 빨리 지나감(시차)
2. 공간 속 카드      — 숫자·차트 카드가 깊이가 다른 자리에 떠 있고 카메라가 카드에서 카드로 날아감, 초점 밖은 흐림
3. 기울인 지도 + 기둥 — 지도를 바닥처럼 눕히고 도시마다 입체 기둥이 솟음, 카메라가 천천히 돎
4. 2.5D 막대 차트    — 바닥 격자 위 입체 막대가 자라고 그림자가 깔림, 카메라 궤도
5. 팝업북           — 종이에 누워 있던 오림판이 차례로 일어섬

모든 숫자는 **예시 데이터**(화면에 표시). 카메라 계열이라 실제 영상에서는 한 편에 몇 번만 (v31).
"""
from __future__ import annotations

import json
import random
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ytflow.stages import hyper  # noqa: E402

W, H, SEG, P = 1920, 1080, 6.0, 1200     # P: 원근 거리(px)


def label(i, name, when, dark=True):
    c, sub = ("#fff", "rgba(255,255,255,.75)") if dark else ("#15171c", "rgba(21,23,28,.65)")
    return (f'<div class="lab" style="color:{c}"><b>{i:02d}</b> {name}'
            f'<div style="font-size:30px;color:{sub};margin-top:10px;font-family:sans">{when}</div></div>')


def layer(z, inner, extra=""):
    """깊이 z 의 층. 멀수록 작게 보이므로 (P-z)/P 배로 키워 화면을 꽉 채움 (그래야 '같은 그림, 다른 깊이')."""
    s = (P - z) / P
    return (f'<div class="ly" style="transform:translateZ({z}px) scale({s:.4f});{extra}">{inner}</div>')


def pillar(pid, x, y, w, h, colors, shadow=True):
    """바닥면(눕힌 평면) 위 (x,y)에 서는 입체 기둥. 바깥 #pid 를 scaleZ 0→1 로 키우면 자람."""
    top, front, side = colors
    f = (f'<div class="fc" style="left:{-w/2}px;top:{-w/2}px;width:{w}px;height:{w}px;background:{top};transform:translateZ({h}px)"></div>'
         f'<div class="fc" style="left:{-w/2}px;top:{w/2 - h}px;width:{w}px;height:{h}px;background:{front};transform-origin:50% 100%;transform:rotateX(-90deg)"></div>'
         f'<div class="fc" style="left:{-w/2}px;top:{-w/2 - h}px;width:{w}px;height:{h}px;background:{front};transform-origin:50% 100%;transform:rotateX(-90deg)"></div>'
         f'<div class="fc" style="left:{w/2 - h}px;top:{-w/2}px;width:{h}px;height:{w}px;background:{side};transform-origin:100% 50%;transform:rotateY(90deg)"></div>'
         f'<div class="fc" style="left:{-w/2 - h}px;top:{-w/2}px;width:{h}px;height:{w}px;background:{side};transform-origin:100% 50%;transform:rotateY(90deg)"></div>')
    sh = (f'<div class="shd" id="{pid}s" style="left:{x - w/2 + 10}px;top:{y - w/2 + 14}px;width:{w + h * 0.35:.0f}px;height:{w}px"></div>' if shadow else "")
    return sh + f'<div class="p3" style="left:{x}px;top:{y}px"><div class="p3" id="{pid}">{f}</div></div>'


# ---------------------------------------------------------------- 1. 멀티플레인 풍경
def multiplane(t0, js):
    rnd = random.Random(7)

    def skyline(n, y0, hmin, hmax, col, win=None, width=2600):
        out, x = [], -340
        while x < width - 300:
            bw, bh = rnd.randint(90, 220), rnd.randint(hmin, hmax)
            out.append(f'<rect x="{x}" y="{y0 - bh}" width="{bw}" height="{bh + 400}" fill="{col}"/>')
            if win:
                for wy in range(y0 - bh + 24, y0, 34):
                    for wx in range(x + 14, x + bw - 20, 30):
                        if rnd.random() < 0.28:
                            out.append(f'<rect x="{wx}" y="{wy}" width="12" height="16" fill="{win}" opacity="{rnd.uniform(.5, 1):.2f}"/>')
            if rnd.random() < 0.25:   # 첨탑
                out.append(f'<rect x="{x + bw / 2 - 6}" y="{y0 - bh - 70}" width="12" height="70" fill="{col}"/>')
            x += bw + rnd.randint(-10, 30)
        return f'<svg width="2600" height="1500" style="position:absolute;left:-340px;top:-200px">{"".join(out)}</svg>'

    sky = (f'<div style="position:absolute;left:-600px;top:-400px;width:3100px;height:1900px;'
           f'background:linear-gradient(#0b1d3a 0%,#2b3d6b 45%,#e48f6a 78%,#f7c59f 100%)"></div>')
    sun = '<div style="position:absolute;left:1180px;top:430px;width:230px;height:230px;border-radius:50%;background:#ffe0b0;box-shadow:0 0 120px 40px rgba(255,200,140,.55)"></div>'
    fog = lambda o: f'<div style="position:absolute;left:-600px;top:600px;width:3100px;height:900px;background:linear-gradient(rgba(247,197,159,0),rgba(247,197,159,{o}))"></div>'
    lamp = ('<svg width="1920" height="1080" style="position:absolute;left:0;top:0">'
            '<rect x="1580" y="180" width="26" height="1000" fill="#0a0f1c"/><rect x="1500" y="170" width="170" height="22" rx="8" fill="#0a0f1c"/>'
            '<ellipse cx="1520" cy="205" rx="40" ry="18" fill="#ffd27a"/><circle cx="1520" cy="215" r="90" fill="#ffd27a" opacity=".18"/>'
            '<rect x="-100" y="930" width="2200" height="16" fill="#0a0f1c"/>'
            + "".join(f'<rect x="{x}" y="930" width="12" height="200" fill="#0a0f1c"/>' for x in range(-100, 2100, 70)) + '</svg>')
    dust = "".join(f'<div class="dust" style="left:{rnd.randint(0, 1900)}px;top:{rnd.randint(100, 1000)}px;'
                   f'transform:translateZ({rnd.randint(-600, 300)}px)"></div>' for _ in range(40))
    html = (layer(-2600, sky) + layer(-2200, sun) + layer(-1600, skyline(0, 900, 120, 300, "#5a6a96") + fog(.55))
            + layer(-900, skyline(0, 1000, 150, 340, "#2f3a63", "#ffd27a") + fog(.3))
            + layer(-350, skyline(0, 1120, 120, 300, "#161d38", "#ffcf6b")) + dust
            + layer(260, lamp, "filter:blur(3px)"))
    js.append(f'tl.fromTo("#w1",{{z:-60,x:60,rotationY:-2}},{{z:420,x:-140,rotationY:2.5,duration:{SEG},ease:"sine.inOut"}},{t0:.2f});')
    js.append(f'tl.fromTo("#w1 .dust",{{y:0}},{{y:-60,duration:{SEG},ease:"none"}},{t0:.2f});')
    stamp = ('<div id="stamp1" style="position:absolute;left:120px;bottom:120px;font-family:mono;font-size:44px;color:#fff;letter-spacing:4px;'
             'text-shadow:0 2px 10px rgba(0,0,0,.6)">1929 · 뉴욕 · 새벽</div>')
    js.append(f'tl.fromTo("#stamp1",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:1.0,ease:"steps(12)"}},{t0 + 1.2:.2f});')
    return (f'<div class="stage"><div class="world" id="w1">{html}</div></div>{stamp}',
            ("멀티플레인 풍경 (층 시차)", "평면 그림 6층을 깊이만 다르게 — 카메라가 다가가면 가까운 층이 빨리 지나감. 장면 열기·시대·장소"))


# ---------------------------------------------------------------- 2. 공간 속 카드
def cards(t0, js):
    def card(cid, x, y, z, ry, body, w=640, h=400):
        return (f'<div class="cd" id="{cid}" style="left:{960 - w/2 + x}px;top:{540 - h/2 + y}px;width:{w}px;height:{h}px;'
                f'transform:translateZ({z}px) rotateY({ry}deg)">{body}</div>')
    pts = [0.7, 0.62, 0.66, 0.5, 0.42, 0.45, 0.3, 0.22]
    line = " ".join(f"{40 + i * 80},{40 + v * 240:.0f}" for i, v in enumerate(pts))
    c1 = '<div class="ck">매출 (예시)</div><div class="cv">38.2<span>조</span></div><div class="cu">+12% 전년 대비</div>'
    c2 = (f'<div class="ck">재고 개월 수</div><svg width="640" height="300" style="position:absolute;left:0;top:96px">'
          f'<polyline points="{line}" fill="none" stroke="#3ddc97" stroke-width="7" stroke-linejoin="round"/>'
          f'<circle cx="600" cy="{40 + pts[-1] * 240:.0f}" r="12" fill="#3ddc97"/></svg>')
    c3 = '<div class="ck">경영진 발언</div><div style="font-family:sansx;font-size:46px;line-height:1.35;margin-top:30px">"수요는 아직<br>공급보다 큽니다"</div><div class="cu" style="color:#8a909c">— 실적 발표 (예시)</div>'
    floor = (f'<div style="position:absolute;left:-1500px;top:900px;width:5000px;height:5000px;transform-origin:50% 0;transform:rotateX(90deg);'
             f'background-image:linear-gradient(rgba(120,140,200,.18) 2px,transparent 2px),linear-gradient(90deg,rgba(120,140,200,.18) 2px,transparent 2px);background-size:120px 120px"></div>')
    rnd = random.Random(2)
    stars = "".join(f'<div class="dust" style="left:{rnd.randint(-400, 2300)}px;top:{rnd.randint(-100, 900)}px;transform:translateZ({rnd.randint(-2600, 200)}px);background:#9fb4ff"></div>' for _ in range(70))
    html = floor + stars + card("k1", -260, -40, 0, 8, c1) + card("k2", 420, -60, -1100, -14, c2) + card("k3", -380, 0, -2200, 12, c3)
    # 카메라 = 세상을 반대로 움직임. 카드 1 → 2 → 3, 도착할 때 잠깐 머묾
    js.append(f'tl.fromTo("#w2",{{x:200,z:-150,rotationY:-6}},{{x:260,z:80,rotationY:-4,duration:1.4,ease:"power2.out"}},{t0:.2f});')
    js.append(f'tl.to("#w2",{{x:-420,y:30,z:1080,rotationY:10,duration:1.8,ease:"power3.inOut"}},{t0 + 1.6:.2f});')
    js.append(f'tl.to("#w2",{{x:380,y:0,z:2160,rotationY:-8,duration:1.8,ease:"power3.inOut"}},{t0 + 3.6:.2f});')
    # 초점: 지금 보는 카드만 또렷, 나머지는 흐림 (피사계 심도)
    for cid, focus in (("k1", (0, 1.6)), ("k2", (1.6, 3.6)), ("k3", (3.6, 6.0))):
        a, b = focus
        js.append(f'tl.fromTo("#{cid}",{{filter:"blur(7px)",opacity:.55}},{{filter:"blur(0px)",opacity:1,duration:0.9,ease:"power2.out"}},{t0 + max(a - 0.2, 0):.2f});')
        if b < SEG:
            js.append(f'tl.to("#{cid}",{{filter:"blur(8px)",opacity:.35,duration:0.9,ease:"power2.in"}},{t0 + b - 0.1:.2f});')
    return (f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 35%,#1d2340,#080a14 70%)"></div>'
            f'<div class="stage"><div class="world" id="w2">{html}</div></div>',
            ("공간 속 카드 (카메라가 날아감)", "숫자·차트·발언 카드를 깊이가 다른 자리에 — 카메라가 카드에서 카드로, 초점 밖은 흐림. 자료를 엮는 장면"))


# ---------------------------------------------------------------- 3. 기울인 지도 + 기둥
def map3d(t0, js):
    MW, MH = 2600, 1700
    pts = {"서울": [126.98, 37.57], "도쿄": [139.69, 35.69], "상하이": [121.47, 31.23], "타이베이": [121.56, 25.03], "홍콩": [114.17, 22.32]}
    q = {"W": MW, "H": MH, "points": pts, "projection": "mercator", "center": [124, 32], "scale": 5.2}
    nm = ROOT / "tools" / "hyperframes" / "node_modules"
    r = subprocess.run(["node", str(ROOT / "ytflow/assets/world_map.mjs"), str(nm)], input=json.dumps(q), capture_output=True, text=True, check=True)
    m = json.loads(r.stdout)
    focus = {"South Korea", "Japan", "China", "Taiwan", "North Korea"}
    paths = "".join(f'<path d="{c["d"]}" fill="{"#2c3e66" if c["name"] in focus else "#1c2742"}" stroke="#5b74b3" stroke-width="2"/>' for c in m["countries"])
    vals = {"서울": 0.95, "타이베이": 1.0, "도쿄": 0.55, "상하이": 0.7, "홍콩": 0.35}
    bars, labs = [], []
    for k, (name, (x, y)) in enumerate(m["points"].items()):
        h = 70 + 260 * vals[name]
        bars.append(pillar(f"mp{k}", x, y, 56, h, ("#ffe08a", "#f4b740", "#c98a1c"), shadow=False))
        labs.append(f'<div class="p3" style="left:{x}px;top:{y}px"><div class="mlab" id="ml{k}" style="transform:translateZ({h + 40}px) rotateX(-90deg)">{name}</div></div>')
        t = t0 + 0.9 + k * 0.22
        js.append(f'tl.fromTo("#mp{k}",{{scaleZ:0.001}},{{scaleZ:1,duration:0.9,ease:"expo.out"}},{t:.2f});')
        js.append(f'tl.fromTo("#ml{k}",{{opacity:0}},{{opacity:1,duration:0.3}},{t + 0.5:.2f});')
    plane = (f'<div class="plane" id="mplane" style="left:{960 - MW/2}px;top:{540 - MH/2}px;width:{MW}px;height:{MH}px">'
             f'<svg width="{MW}" height="{MH}" style="position:absolute;inset:0"><rect width="{MW}" height="{MH}" fill="#0e1530"/>'
             f'<path d="{m["graticule"]}" stroke="#22305a" stroke-width="1.5" fill="none"/>{paths}</svg>{"".join(bars)}{"".join(labs)}</div>')
    js.append(f'tl.fromTo("#mplane",{{rotationX:40,rotationZ:-12,y:60,z:-500}},{{rotationX:54,rotationZ:6,y:120,z:-250,duration:{SEG},ease:"sine.inOut"}},{t0:.2f});')
    note = '<div style="position:absolute;right:80px;bottom:70px;font-family:sans;font-size:28px;color:rgba(255,255,255,.6)">예시 데이터 · 높이 = 반도체 수출 비중</div>'
    return (f'<div style="position:absolute;inset:0;background:#070b18"></div><div class="stage" style="perspective:2400px;perspective-origin:50% 35%">'
            f'<div class="world">{plane}</div></div>{note}',
            ("기울인 지도 + 솟는 기둥", "지도를 바닥처럼 눕히고 도시마다 입체 기둥 — '어디에 얼마나'를 한 장면에. 시사·공급망·지역 비교"))


# ---------------------------------------------------------------- 4. 2.5D 막대 차트
def bars3d(t0, js):
    PW = 1600
    data = [("1분기", .38), ("2분기", .52), ("3분기", .61), ("4분기", .95)]
    items = []
    for k, (q, v) in enumerate(data):
        x, y = 360 + k * 300, 800
        last = k == len(data) - 1
        cols = ("#ffcf3f", "#e8a810", "#b98407") if last else ("#8fa3d6", "#5d74b3", "#3d5191")
        items.append(pillar(f"bp{k}", x, y, 150, 60 + 380 * v, cols))
        items.append(f'<div class="blab" style="left:{x - 100}px;top:{y + 110}px">{q}</div>')
        t = t0 + 0.6 + k * 0.25
        js.append(f'tl.fromTo("#bp{k}",{{scaleZ:0.001}},{{scaleZ:1,duration:{1.1 if last else 0.8},ease:"{"back.out(1.4)" if last else "expo.out"}"}},{t:.2f});')
        js.append(f'tl.fromTo("#bp{k}s",{{opacity:0,scaleX:0.2}},{{opacity:1,scaleX:1,duration:0.8,ease:"expo.out"}},{t:.2f});')
    grid = (f'background-color:#eef1f8;background-image:linear-gradient(#d3d9e8 2px,transparent 2px),linear-gradient(90deg,#d3d9e8 2px,transparent 2px);background-size:100px 100px')
    plane = f'<div class="plane" id="bplane" style="left:{960 - PW/2}px;top:{540 - 480}px;width:{PW}px;height:1200px;{grid}">{"".join(items)}</div>'
    js.append(f'tl.fromTo("#bplane",{{rotationX:58,rotationZ:-38,z:-250}},{{rotationX:60,rotationZ:-16,z:-80,duration:{SEG},ease:"sine.inOut"}},{t0:.2f});')
    tag = '<div id="btag" style="position:absolute;left:110px;top:300px;font-family:sansx;font-size:96px;color:#e8a810">+60%<div style="font-size:30px;color:#8a909c;font-family:sans">4분기, 예시 데이터</div></div>'
    js.append(f'tl.fromTo("#btag",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.5,ease:"expo.out"}},{t0 + 2.2:.2f});')
    return (f'<div style="position:absolute;inset:0;background:linear-gradient(#f7f9fd,#dfe5f1)"></div>'
            f'<div class="stage" style="perspective:1700px;perspective-origin:50% 0%"><div class="world">{plane}</div></div>{tag}',
            ("2.5D 막대 차트", "격자 바닥 위 입체 막대가 자라고 그림자가 깔림, 카메라가 천천히 돎 — 평면 막대보다 '규모'가 느껴짐"))


# ---------------------------------------------------------------- 5. 팝업북
def popup(t0, js):
    PW, PH = 1700, 1000

    def cut(cid, x, y, w, h, svg):
        return (f'<div class="cut" id="{cid}" style="left:{x - w/2}px;top:{y - h}px;width:{w}px;height:{h}px">'
                f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="overflow:visible">{svg}</svg></div>')
    house = ('<path d="M20 170 L150 50 L280 170 L280 330 L20 330 Z" fill="#f2e3c6" stroke="#fff" stroke-width="12" stroke-linejoin="round"/>'
             '<path d="M0 180 L150 30 L300 180" fill="none" stroke="#c0503a" stroke-width="34" stroke-linejoin="round"/>'
             '<rect x="120" y="230" width="60" height="100" fill="#7b4b2a"/><rect x="200" y="200" width="50" height="45" fill="#8fc1e3"/>')
    tree = ('<rect x="95" y="230" width="30" height="120" fill="#7b4b2a" stroke="#fff" stroke-width="8"/>'
            '<circle cx="110" cy="150" r="105" fill="#5f9e6e" stroke="#fff" stroke-width="12"/>')
    person = ('<circle cx="60" cy="40" r="34" fill="#f2c9a0" stroke="#fff" stroke-width="8"/>'
              '<path d="M14 230 L20 100 Q60 75 100 100 L106 230 Z" fill="#3d5a80" stroke="#fff" stroke-width="10" stroke-linejoin="round"/>')
    sign = ('<rect x="10" y="10" width="260" height="120" rx="10" fill="#fff8e6" stroke="#fff" stroke-width="10"/>'
            '<text x="140" y="95" text-anchor="middle" font-family="sansx" font-size="64" fill="#c0503a">1997</text>'
            '<rect x="130" y="130" width="20" height="120" fill="#7b4b2a"/>')
    spots = [(520, 700, 300, 340, house), (900, 560, 220, 350, tree), (1080, 790, 120, 240, person), (1350, 650, 280, 250, sign)]
    # 바닥에 닿는 그림자: 일어서는 동안 진해짐 → '서 있다'가 읽힘
    cuts = "".join(f'<div class="cshd" id="us{k}" style="left:{x - w * .55:.0f}px;top:{y - 30}px;width:{w * 1.1:.0f}px;height:{max(60, h * .35):.0f}px"></div>'
                   for k, (x, y, w, h, _) in enumerate(spots))
    cuts += "".join(cut(f"u{k}", x, y, w, h, svg) for k, (x, y, w, h, svg) in enumerate(spots))
    for k in range(4):
        js.append(f'tl.fromTo("#u{k}",{{rotationX:0}},{{rotationX:-90,duration:0.9,ease:"back.out(1.3)"}},{t0 + 0.7 + k * 0.45:.2f});')
        js.append(f'tl.fromTo("#us{k}",{{opacity:0}},{{opacity:1,duration:0.9,ease:"power2.out"}},{t0 + 0.7 + k * 0.45:.2f});')
    paper = (f'background:#efe4cc;background-image:radial-gradient(rgba(0,0,0,.05) 1px,transparent 1px);background-size:6px 6px;'
             f'box-shadow:0 40px 80px rgba(0,0,0,.35)')
    plane = (f'<div class="plane" id="uplane" style="left:{960 - PW/2}px;top:{540 - PH/2 + 80}px;width:{PW}px;height:{PH}px;{paper}">'
             f'<div style="position:absolute;left:{PW/2 - 3}px;top:0;width:6px;height:{PH}px;background:rgba(0,0,0,.12)"></div>{cuts}</div>')
    js.append(f'tl.fromTo("#uplane",{{rotationX:62,rotationZ:-6,z:-200}},{{rotationX:52,rotationZ:4,z:60,duration:{SEG},ease:"sine.inOut"}},{t0:.2f});')
    return (f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 30%,#5b4636,#2a1f17 75%)"></div>'
            f'<div class="stage" style="perspective:1600px;perspective-origin:50% 10%"><div class="world">{plane}</div></div>',
            ("팝업북 (종이가 일어섬)", "책장에 누워 있던 오림판이 차례로 일어섬 — 이야기·옛 사례·호기심, 손으로 만든 따뜻한 입체"))


SCENES = [multiplane, cards, map3d, bars3d, popup]


def build(work: Path) -> Path:
    a = work / "assets"
    (a / "fonts").mkdir(parents=True, exist_ok=True)
    shutil.copy(hyper.GSAP, a / "gsap.min.js")
    for f in ("NanumGothic-Bold.ttf", "NanumGothic-ExtraBold.ttf"):
        shutil.copy(ROOT / "ytflow/assets/fonts" / f, a / "fonts" / f)
    js, secs = [], []
    for i, fn in enumerate(SCENES):
        t0 = i * SEG
        body, (name, when) = fn(t0, js)
        secs.append(f'<div class="sec" id="sec{i}">{body}{label(i + 1, name, when, fn is not bars3d)}</div>')
        js.append(f'tl.set("#sec{i}",{{visibility:"visible"}},{t0:.2f});tl.set("#sec{i}",{{visibility:"hidden"}},{t0 + SEG:.2f});')
        js.append(f'tl.fromTo("#sec{i} .lab",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.35,ease:"expo.out"}},{t0 + 0.1:.2f});')
    dur = SEG * len(SCENES)
    html = f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H}">
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:sans;src:url('assets/fonts/NanumGothic-Bold.ttf')}}
@font-face{{font-family:sansx;src:url('assets/fonts/NanumGothic-ExtraBold.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.sec{{position:absolute;inset:0;visibility:hidden;overflow:hidden}}
.stage{{position:absolute;inset:0;perspective:{P}px;perspective-origin:50% 50%}}
.world{{position:absolute;inset:0;transform-style:preserve-3d}}
.ly{{position:absolute;inset:0;transform-style:preserve-3d}}
.plane{{position:absolute;transform-style:preserve-3d}}
.p3{{position:absolute;width:0;height:0;transform-style:preserve-3d}}
.fc{{position:absolute;outline:1px solid rgba(255,255,255,.08)}}
.shd{{position:absolute;background:rgba(20,30,60,.22);filter:blur(10px);transform-origin:0 50%}}
.cut{{position:absolute;transform-origin:50% 100%;filter:drop-shadow(0 6px 4px rgba(0,0,0,.25))}}
.cshd{{position:absolute;border-radius:50%;background:radial-gradient(ellipse at 50% 70%,rgba(60,40,20,.45),rgba(60,40,20,0) 70%)}}
.dust{{position:absolute;width:6px;height:6px;border-radius:50%;background:#ffe3b8;opacity:.7}}
.cd{{position:absolute;border-radius:28px;background:rgba(22,27,44,.92);border:2px solid #2d3555;padding:36px 44px;color:#f2f2ee;
     box-shadow:0 30px 60px rgba(0,0,0,.5)}}
.ck{{font-family:sans;font-size:32px;color:#8a909c}}
.cv{{font-family:sansx;font-size:150px;margin-top:20px}} .cv span{{font-size:54px;color:#8a909c;margin-left:10px}}
.cu{{font-family:sans;font-size:34px;color:#3ddc97;margin-top:10px}}
.mlab{{position:absolute;left:-100px;width:200px;text-align:center;font-family:sansx;font-size:40px;color:#fff;transform-origin:50% 100%;
       text-shadow:0 2px 8px rgba(0,0,0,.8)}}
.blab{{position:absolute;width:200px;text-align:center;font-family:sansx;font-size:44px;color:#5d6b8f}}
.lab{{position:absolute;left:70px;top:56px;font-family:sansx;font-size:58px;max-width:1300px;line-height:1.2;z-index:5}}
.lab b{{display:inline-block;min-width:80px;opacity:.5}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur:.2f}" data-width="{W}" data-height="{H}" data-motion-blur="on">
<div id="layer" class="clip" data-start="0" data-duration="{dur:.2f}" data-track-index="0" data-layout-allow-overlap>
{''.join(secs)}
</div></div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>"""
    (work / "index.html").write_text(html, encoding="utf-8")
    return work


def render(work: Path, mp4: Path, quality="looks") -> None:
    r = subprocess.run([str(hyper.BIN), "render", "--quality", quality, "--fps", "30", "-o", str(mp4.resolve())], cwd=work, env=hyper._env(),
                       capture_output=True, text=True, timeout=2400)
    if r.returncode:
        print((r.stdout + r.stderr)[-1500:])
        sys.exit(1)


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / ".cache" / "depth25d"
    work = build(out / "hf")
    mp4 = out / "depth25d.mp4"
    render(work, mp4)
    sel = "+".join(f"eq(n\\,{int(k * SEG * 30) + o})" for k in range(len(SCENES)) for o in (60, 165))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf", f"select='{sel}',scale=640:-1,tile=2x{len(SCENES)}", "-frames:v", "1",
                    str(out / "sheet.png")], check=True)
    print("→", mp4, "·", out / "sheet.png")


if __name__ == "__main__":
    main()
