"""애니메이션 스타일 견본 릴 (docs/38 §6) — 같은 장면(동전이 떨어져 성장 탑이 쌓인다)을 12가지 그림체로.

    python scripts/motion_styles_reel.py [출력폴더]     # → motion_styles.mp4 + sheet.png (기본 .cache/motion_styles)

내용은 같고 '그림체(렌더 스타일)'만 바뀌므로 스타일끼리 비교하기 좋다. 모두 HTML/SVG + GSAP, 외부 그림 없이.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ytflow.stages import hyper  # noqa: E402

W, H, SEG = 1920, 1080, 3.6
G = 830          # 바닥 y
N = 6            # 동전 수


def coin_y(k, h=36):
    return G - (k + 0.5) * h


def label(i, name, when, dark=False):
    c, sub = ("#fff", "rgba(255,255,255,.72)") if dark else ("#15171c", "rgba(21,23,28,.62)")
    return (f'<div class="lab" style="color:{c}"><b>{i:02d}</b> {name}'
            f'<div style="font-size:30px;color:{sub};margin-top:10px;font-family:sans">{when}</div></div>')


def drops(js, sel, t0, n=N, dist=900, fall=0.42, gap=0.3, squash=True, ease="power2.in"):
    for k in range(n):
        t = t0 + 0.35 + k * gap
        js.append(f'tl.fromTo("{sel}{k}",{{y:-{dist}}},{{y:0,duration:{fall},ease:"{ease}"}},{t:.2f});')
        if squash:
            js.append(f'tl.fromTo("{sel}{k}",{{scaleY:0.7,scaleX:1.12}},{{scaleY:1,scaleX:1,duration:0.35,ease:"back.out(2.2)"}},{t + fall:.2f});')


S = []   # (html, js-builder) 차례


def style(fn):
    S.append(fn)
    return fn


# ---------------------------------------------------------------- 1. 플랫 2D
@style
def flat(i, t0, js):
    coins = "".join(f'<g id="f{k}" style="transform-origin:960px {coin_y(k)+18}px"><rect x="870" y="{coin_y(k)-18}" width="180" height="36" rx="6" fill="#e69a28"/>'
                    f'<ellipse cx="960" cy="{coin_y(k)-18}" rx="90" ry="14" fill="#f7c548"/></g>' for k in range(N))
    js.append(f'tl.fromTo("#fman",{{rotation:-8}},{{rotation:8,duration:0.5,yoyo:true,repeat:6,ease:"sine.inOut"}},{t0:.2f});')
    js.append(f'tl.fromTo("#farm",{{rotation:20}},{{rotation:-40,duration:0.35,yoyo:true,repeat:9,ease:"sine.inOut"}},{t0:.2f});')
    drops(js, "#f", t0)
    return (f'<svg width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#f4ead8"/>'
            f'<ellipse cx="400" cy="{G+260}" rx="900" ry="320" fill="#a8d5ba"/><ellipse cx="1600" cy="{G+300}" rx="900" ry="330" fill="#8cc7a6"/>'
            f'<circle cx="1580" cy="230" r="90" fill="#f7c548"/>'
            f'<g id="fman" style="transform-origin:560px {G}px"><rect x="520" y="{G-170}" width="80" height="170" rx="36" fill="#3d5a80"/>'
            f'<circle cx="560" cy="{G-215}" r="48" fill="#f2c9a0"/><rect id="farm" x="590" y="{G-150}" width="90" height="22" rx="11" fill="#3d5a80" style="transform-origin:595px {G-139}px"/></g>'
            f'{coins}</svg>'), ("플랫 2D", "가장 흔한 설명 애니메이션 — 인물·사물을 단순한 면으로, 무엇이든 그릴 수 있음")


# ---------------------------------------------------------------- 2. 라인 아트 (모노라인)
@style
def line(i, t0, js):
    coins = "".join(f'<g id="l{k}"><rect x="870" y="{coin_y(k)-18}" width="180" height="36" rx="6" pathLength="1" class="ln"/>'
                    f'<ellipse cx="960" cy="{coin_y(k)-18}" rx="90" ry="14" pathLength="1" class="ln"/></g>' for k in range(N))
    for k in range(N):
        t = t0 + 0.3 + k * 0.3
        js.append(f'tl.fromTo("#l{k} .ln",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.45,ease:"power1.inOut"}},{t:.2f});')
    js.append(f'tl.fromTo("#larrow",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.9,ease:"power2.inOut"}},{t0 + 2.2:.2f});')
    return (f'<svg width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#fbfbf8"/>'
            f'<style>.ln{{fill:none;stroke:#16181d;stroke-width:5;stroke-dasharray:1;stroke-dashoffset:1;stroke-linecap:round}}</style>'
            f'<line x1="300" y1="{G}" x2="1620" y2="{G}" stroke="#16181d" stroke-width="5"/>{coins}'
            f'<path id="larrow" class="ln" pathLength="1" d="M1120 {G-40} C1250 {G-120} 1300 {G-300} 1330 {G-420} M1290 {G-380} L1330 {G-420} L1360 {G-370}" style="stroke:#e0452f"/>'
            f'</svg>'), ("라인 아트", "선만으로 — 깔끔·지적인 느낌, 기술·개념 설명, 선이 그려지는 과정이 곧 설명")


# ---------------------------------------------------------------- 3. 화이트보드 손그림 (boil)
@style
def board(i, t0, js):
    coins = "".join(f'<g id="w{k}"><rect x="870" y="{coin_y(k)-18}" width="180" height="36" rx="10" pathLength="1" class="wb"/>'
                    f'<ellipse cx="960" cy="{coin_y(k)-18}" rx="90" ry="14" pathLength="1" class="wb"/></g>' for k in range(N))
    for k in range(N):
        js.append(f'tl.fromTo("#w{k} .wb",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.4,ease:"none"}},{t0 + 0.3 + k * 0.3:.2f});')
    for s in range(int(SEG * 8)):   # 초당 8번 선 모양을 바꿔 '살아 있는 선'
        js.append(f'tl.set("#wturb",{{attr:{{seed:{s % 5 + 1}}}}},{t0 + s / 8:.3f});')
    js.append(f'tl.fromTo("#wtxt",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.9,ease:"none"}},{t0 + 2.3:.2f});')
    return (f'<svg width="{W}" height="{H}"><defs><filter id="wrough"><feTurbulence id="wturb" type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="1"/>'
            f'<feDisplacementMap in="SourceGraphic" scale="7"/></filter></defs><rect width="{W}" height="{H}" fill="#f7f7f2"/>'
            f'<style>.wb{{fill:none;stroke:#1d3557;stroke-width:6;stroke-dasharray:1;stroke-dashoffset:1;stroke-linecap:round}}</style>'
            f'<g filter="url(#wrough)"><path d="M320 {G} Q960 {G+8} 1600 {G-4}" stroke="#1d3557" stroke-width="6" fill="none"/>{coins}'
            f'<circle cx="1330" cy="{G-330}" r="95" fill="none" stroke="#e63946" stroke-width="6"/></g>'
            f'</svg><div id="wtxt" style="position:absolute;left:1260px;top:{G-370}px;font-family:pen;font-size:64px;color:#e63946">+200%</div>'),\
        ("화이트보드 손그림", "펜으로 그리는 느낌 — 강의·개념 해설, 긴 영상도 싸게, 선이 떨리는 boil 로 손맛")


# ---------------------------------------------------------------- 4. 아이소메트릭
@style
def iso(i, t0, js):
    def cube(cx, cy, s, top, left, right):
        h = s / 2
        return (f'<polygon points="{cx},{cy - h} {cx + s},{cy} {cx},{cy + h} {cx - s},{cy}" fill="{top}"/>'
                f'<polygon points="{cx - s},{cy} {cx},{cy + h} {cx},{cy + h + s * .55} {cx - s},{cy + s * .55}" fill="{left}"/>'
                f'<polygon points="{cx + s},{cy} {cx},{cy + h} {cx},{cy + h + s * .55} {cx + s},{cy + s * .55}" fill="{right}"/>')
    grid = "".join(f'<line x1="{960 + (k - 8) * 120}" y1="{G - 300}" x2="{960 + (k - 8) * 120 + 600}" y2="{G}" stroke="#d6dbe6" stroke-width="2"/>'
                   f'<line x1="{960 + (k - 8) * 120}" y1="{G - 300}" x2="{960 + (k - 8) * 120 - 600}" y2="{G}" stroke="#d6dbe6" stroke-width="2"/>' for k in range(17))
    blocks = "".join(f'<g id="i{k}">{cube(960, G - 100 - k * 66, 120, "#ffd166", "#f4a261", "#e76f51")}</g>' for k in range(N))
    side = "".join(f'<g id="ib{k}">{cube(x, G - 40, 70, "#a8dadc", "#457b9d", "#1d3557")}</g>' for k, x in enumerate((640, 1280)))
    drops(js, "#i", t0, squash=False, ease="power3.in")
    for k in range(2):
        js.append(f'tl.fromTo("#ib{k}",{{opacity:0,y:-60}},{{opacity:1,y:0,duration:0.4,ease:"expo.out"}},{t0 + 0.1 + k * 0.1:.2f});')
    return (f'<svg width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#eef1f7"/>{grid}{side}{blocks}</svg>'),\
        ("아이소메트릭", "비스듬한 입체 — 공장·도시·데이터센터·공급망 '구조'를 한 화면에, 깔끔한 기술 느낌")


# ---------------------------------------------------------------- 5. 리퀴드 모션
@style
def liquid(i, t0, js):
    drops_ = "".join(f'<circle id="q{k}" cx="960" cy="{G - 140}" r="{70 - k * 4}" fill="url(#qg)"/>' for k in range(N))
    for k in range(N):
        t = t0 + 0.3 + k * 0.3
        js.append(f'tl.fromTo("#q{k}",{{y:-800}},{{y:0,duration:0.45,ease:"power2.in"}},{t:.2f});')
    js.append(f'tl.fromTo("#qpool",{{attr:{{ry:40,rx:200}}}},{{attr:{{ry:150,rx:330}},duration:2.0,ease:"power1.inOut"}},{t0 + 0.6:.2f});')
    js.append(f'tl.fromTo("#qpool",{{y:0}},{{y:-120,duration:2.0,ease:"power1.inOut"}},{t0 + 0.6:.2f});')
    return (f'<svg width="{W}" height="{H}"><defs><linearGradient id="qg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7b2ff7"/><stop offset="1" stop-color="#f107a3"/></linearGradient>'
            f'<filter id="goo"><feGaussianBlur in="SourceGraphic" stdDeviation="22"/><feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 40 -18"/></filter></defs>'
            f'<rect width="{W}" height="{H}" fill="#120c24"/><g filter="url(#goo)"><ellipse id="qpool" cx="960" cy="{G}" rx="200" ry="40" fill="url(#qg)"/>{drops_}</g></svg>'),\
        ("리퀴드 모션", "물방울이 합쳐지고 늘어남 — 흐름·흡수·합병·자금 유입 같은 '섞임', 장 표지·브랜드 느낌")


# ---------------------------------------------------------------- 6. 종이 컷아웃 스톱모션
@style
def paper(i, t0, js):
    import random
    rnd = random.Random(3)
    coins = "".join(f'<g id="p{k}" filter="url(#pshadow)" style="transform-origin:960px {coin_y(k, 40)}px"><g transform="rotate({rnd.uniform(-4, 4):.1f} 960 {coin_y(k, 40)})">'
                    f'<rect x="868" y="{coin_y(k, 40)-20}" width="184" height="40" rx="4" fill="{("#e9c46a", "#f4a261")[k % 2]}"/>'
                    f'<rect x="868" y="{coin_y(k, 40)-20}" width="184" height="40" rx="4" fill="url(#pfib)" opacity=".35"/></g></g>' for k in range(N))
    for k in range(N):   # 12fps 처럼 '두 프레임에 한 번' 끊어 움직임 (steps)
        js.append(f'tl.fromTo("#p{k}",{{y:-820,rotation:-12}},{{y:0,rotation:0,duration:0.5,ease:"steps(6)"}},{t0 + 0.3 + k * 0.3:.2f});')
    js.append(f'tl.fromTo("#ptag",{{rotation:-30,scale:0}},{{rotation:-6,scale:1,duration:0.4,ease:"steps(4)"}},{t0 + 2.4:.2f});')
    return (f'<svg width="{W}" height="{H}"><defs><filter id="pshadow"><feDropShadow dx="6" dy="9" stdDeviation="5" flood-opacity=".35"/></filter>'
            f'<pattern id="pfib" width="200" height="200" patternUnits="userSpaceOnUse"><rect width="200" height="200" fill="#fff"/>'
            f'<path d="M0 30 L200 34 M0 90 L200 86 M0 150 L200 155" stroke="#000" stroke-width="1" opacity=".3"/></pattern></defs>'
            f'<rect width="{W}" height="{H}" fill="#d8c3a5"/><rect width="{W}" height="{H}" fill="url(#pfib)" opacity=".18"/>'
            f'<path filter="url(#pshadow)" d="M0 {G} L300 {G - 12} L700 {G + 6} L1100 {G - 8} L1500 {G + 10} L1920 {G - 4} L1920 1080 L0 1080Z" fill="#6b9080"/>'
            f'{coins}<g id="ptag" filter="url(#pshadow)" style="transform-origin:1320px {G - 380}px"><rect x="1190" y="{G - 440}" width="260" height="120" fill="#e63946"/>'
            f'<text x="1320" y="{G - 362}" text-anchor="middle" font-family="sansx" font-size="64" fill="#fff">UP!</text></g></svg>'),\
        ("종이 컷아웃 (스톱모션)", "종이를 오려 붙인 질감 + 두 프레임에 한 번 끊는 움직임 — 따뜻한 이야기·옛 사례, 시사의 손맛")


# ---------------------------------------------------------------- 7. 2.5D 시차
@style
def parallax(i, t0, js):
    layers = [("#ffd6a5", 0.15, f"M0 560 L300 380 L620 520 L980 330 L1400 500 L1800 360 L2400 520 L2400 1080 L0 1080Z"),
              ("#e5989b", 0.35, f"M-200 650 L200 480 L600 620 L1000 470 L1500 640 L1900 500 L2400 640 L2400 1080 L-200 1080Z"),
              ("#b5838d", 0.65, f"M-300 760 L300 600 L800 740 L1300 590 L1800 760 L2400 620 L2400 1080 L-300 1080Z")]
    html = "".join(f'<g id="x{k}"><path d="{d}" fill="{c}"/></g>' for k, (c, _, d) in enumerate(layers))
    for k, (_, f, _) in enumerate(layers):
        js.append(f'tl.fromTo("#x{k}",{{x:0}},{{x:{-260 * f:.0f},duration:{SEG},ease:"sine.inOut"}},{t0:.2f});')
    coins = "".join(f'<g id="xc{k}" style="transform-origin:1100px {coin_y(k)+18}px"><rect x="1010" y="{coin_y(k)-18}" width="180" height="36" rx="6" fill="#6d597a"/>'
                    f'<ellipse cx="1100" cy="{coin_y(k)-18}" rx="90" ry="14" fill="#ffcdb2"/></g>' for k in range(N))
    js.append(f'tl.fromTo("#xfront",{{x:0}},{{x:-260,duration:{SEG},ease:"sine.inOut"}},{t0:.2f});')
    drops(js, "#xc", t0)
    return (f'<svg width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#fff1e6"/><circle cx="1500" cy="250" r="110" fill="#ffb4a2"/>{html}'
            f'<g id="xfront"><rect x="0" y="{G}" width="2400" height="300" fill="#6d6875"/>{coins}</g></svg>'),\
        ("2.5D 시차", "평면 그림을 층으로 나눠 카메라가 움직이면 깊이가 생김 — 장면 열기·풍경·사진에 공간감, 3D 보다 쌈")


# ---------------------------------------------------------------- 8. 픽셀 / 8비트
@style
def pixel(i, t0, js):
    # 96×54 격자 위에 그리고 20배 키움 (crispEdges) — 움직임도 칸 단위(steps)
    coins = "".join(f'<g id="x8{k}"><rect x="42" y="{40 - k * 2}" width="12" height="2" fill="#ffcc00"/><rect x="42" y="{40 - k * 2}" width="12" height="1" fill="#fff38a"/></g>' for k in range(N))
    for k in range(N):
        js.append(f'tl.fromTo("#x8{k}",{{y:-42}},{{y:0,duration:0.42,ease:"steps(14)"}},{t0 + 0.3 + k * 0.3:.2f});')
    js.append(f'tl.fromTo("#x8hero",{{x:0}},{{x:20,duration:2.4,ease:"steps(20)"}},{t0:.2f});')
    js.append(f'tl.fromTo("#x8hero",{{y:0}},{{y:-3,duration:0.15,yoyo:true,repeat:15,ease:"steps(1)"}},{t0:.2f});')
    js.append(f'tl.fromTo("#x8sc",{{opacity:0}},{{opacity:1,duration:0.01}},{t0 + 2.3:.2f});')
    hero = '<g id="x8hero"><rect x="14" y="34" width="6" height="8" fill="#e43b44"/><rect x="15" y="30" width="4" height="4" fill="#f6d6bd"/><rect x="14" y="42" width="2" height="2" fill="#3e2731"/><rect x="18" y="42" width="2" height="2" fill="#3e2731"/></g>'
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 96 54" shape-rendering="crispEdges"><rect width="96" height="54" fill="#5fcde4"/>'
            f'<rect y="44" width="96" height="10" fill="#6abe30"/><rect y="44" width="96" height="1" fill="#99e550"/>'
            f'<rect x="70" y="8" width="10" height="3" fill="#fff"/><rect x="68" y="9" width="14" height="2" fill="#fff"/>'
            f'{hero}{coins}<text id="x8sc" x="60" y="22" font-family="monospace" font-size="5" fill="#fff">+600</text></svg>'),\
        ("픽셀 / 8비트", "게임 화면 문법 — 레트로·게임·가벼운 쇼츠, 칸 단위로 끊는 움직임이 핵심 (매끄럽게 하면 어색)")


# ---------------------------------------------------------------- 9. 네온 글로우
@style
def neon(i, t0, js):
    coins = "".join(f'<g id="n{k}"><rect x="870" y="{coin_y(k)-18}" width="180" height="36" rx="18" class="ne" stroke="{("#00f5ff", "#ff2bd6")[k % 2]}"/></g>' for k in range(N))
    for k in range(N):
        t = t0 + 0.3 + k * 0.3
        js.append(f'tl.fromTo("#n{k}",{{y:-700,opacity:0}},{{y:0,opacity:1,duration:0.4,ease:"power3.in"}},{t:.2f});')
        js.append(f'tl.fromTo("#n{k}",{{opacity:0.3}},{{opacity:1,duration:0.12,repeat:2,yoyo:true,ease:"steps(1)"}},{t + 0.4:.2f});')
    js.append(f'tl.fromTo("#nline",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:1.2,ease:"power2.inOut"}},{t0 + 0.2:.2f});')
    return (f'<svg width="{W}" height="{H}"><defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
            f'<rect width="{W}" height="{H}" fill="#07060f"/><style>.ne{{fill:none;stroke-width:6}}</style><g filter="url(#glow)">'
            f'<path id="nline" d="M260 {G} L1660 {G}" stroke="#7df9ff" stroke-width="5" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>{coins}</g></svg>'),\
        ("네온 글로우", "어둠 속 빛나는 선 — AI·테크·밤 분위기, 데이터 흐름. 정보 많은 화면엔 눈이 피곤")


# ---------------------------------------------------------------- 10. 하프톤 레트로 인쇄
@style
def halftone(i, t0, js):
    def stack(dx, dy, fill, op):
        return "".join(f'<g class="hs{k}"><rect x="{870 + dx}" y="{coin_y(k)-15 + dy}" width="180" height="30" fill="{fill}" opacity="{op}"/></g>' for k in range(N))
    for k in range(N):
        js.append(f'tl.fromTo(".hs{k}",{{y:-800}},{{y:0,duration:0.42,ease:"power2.in"}},{t0 + 0.3 + k * 0.3:.2f});')
    js.append(f'tl.fromTo("#hhead",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:"expo.out"}},{t0 + 0.2:.2f});')
    return (f'<svg width="{W}" height="{H}"><defs><pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<circle cx="8" cy="8" r="5" fill="#1b998b"/></pattern><pattern id="dots2" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(15)">'
            f'<circle cx="8" cy="8" r="4" fill="#ff5e5b"/></pattern></defs><rect width="{W}" height="{H}" fill="#f3ead3"/>'
            f'<circle cx="960" cy="540" r="320" fill="url(#dots2)" opacity=".55"/>'
            f'<g style="mix-blend-mode:multiply">{stack(-7, 4, "#00a6ed", .85)}{stack(6, -3, "#ff5e5b", .85)}{stack(0, 0, "url(#dots)", 1)}</g>'
            f'<rect x="0" y="{G}" width="{W}" height="12" fill="#1d1d1d"/>'
            f'<text id="hhead" x="1440" y="560" text-anchor="middle" font-family="sansx" font-size="110" fill="#1d1d1d" letter-spacing="8">BOOM</text></svg>'),\
        ("하프톤 레트로 인쇄", "망점·색 어긋남 — 옛날 신문·만화·잡지 느낌, 역사·경제사, 시대를 표시할 때")


# ---------------------------------------------------------------- 11. CSS 3D 블록
@style
def css3d(i, t0, js):
    s = 150
    # 바깥을 향한 면만 보이게(backface-visibility), 쌓인 블록 사이의 위·아래 면은 빼서 비침 방지
    faces = lambda c, top=False: "".join(f'<div class="fc" style="background:{c[j % 3]};transform:{tr}"></div>' for j, tr in enumerate(
        (f"translateZ({s/2}px)", f"rotateY(180deg) translateZ({s/2}px)", f"rotateY(90deg) translateZ({s/2}px)",
         f"rotateY(-90deg) translateZ({s/2}px)") + ((f"rotateX(90deg) translateZ({s/2}px)",) if top else ())))
    # 위치는 바깥 div(left/top), 움직임은 GSAP 가 transform 전부를 맡음 (인라인 transform 과 섞으면 면이 비뚤어짐)
    cubes = "".join(f'<div class="cb" style="left:{-s/2}px;top:{-(k + 1) * s}px"><div class="cb" id="c3{k}" style="left:0;top:0">{faces(("#4361ee", "#3a0ca3", "#4cc9f0"), k == 3)}</div></div>' for k in range(4))
    for k in range(4):
        js.append(f'tl.fromTo("#c3{k}",{{y:-900}},{{y:0,duration:0.45,ease:"power3.in"}},{t0 + 0.3 + k * 0.4:.2f});')
    js.append(f'tl.fromTo("#c3rig",{{rotationY:-20}},{{rotationY:160,duration:{SEG},ease:"none"}},{t0:.2f});')   # 안쪽: 세로축 회전
    return (f'<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,#2b2d42,#0b0c16)"></div>'
            f'<div style="position:absolute;left:960px;top:{G}px;perspective:1800px;perspective-origin:0 -{2 * s}px">'
            f'<div style="position:absolute;left:0;top:0;transform-style:preserve-3d;transform-origin:0 -{2 * s}px;transform:rotateX(-16deg)">'   # 바깥: 카메라 기울기 (고정)
            f'<div id="c3rig" style="position:absolute;left:0;top:0;transform-style:preserve-3d">{cubes}</div></div></div>'
            f'<style>.cb{{position:absolute;width:{s}px;height:{s}px;transform-style:preserve-3d}}.fc{{position:absolute;inset:0;border:2px solid rgba(255,255,255,.35);backface-visibility:hidden}}</style>'),\
        ("3D (CSS 입체)", "진짜 입체가 회전 — 제품·물체·데이터 구조를 돌려 보기, 스튜디오 3D 의 가벼운 판")


# ---------------------------------------------------------------- 12. 클레이 (말랑한 입체감)
@style
def clay(i, t0, js):
    coins = "".join(f'<div class="cl" id="k{k}" style="left:870px;top:{coin_y(k, 48)-24}px;width:180px;height:48px;'
                    f'background:radial-gradient(ellipse at 35% 25%,#ffe29a,#f6a93b 60%,#d9822b);transform-origin:50% 100%"></div>' for k in range(N))
    for k in range(N):
        t = t0 + 0.3 + k * 0.3
        js.append(f'tl.fromTo("#k{k}",{{y:-800,scaleY:1.25,scaleX:0.85}},{{y:0,scaleY:1.25,scaleX:0.85,duration:0.4,ease:"power2.in"}},{t:.2f});')
        js.append(f'tl.to("#k{k}",{{scaleY:0.6,scaleX:1.3,duration:0.08,ease:"power1.out"}},{t + 0.4:.2f});')
        js.append(f'tl.to("#k{k}",{{scaleY:1,scaleX:1,duration:0.5,ease:"elastic.out(1,0.45)"}},{t + 0.48:.2f});')
    js.append(f'tl.fromTo("#kface",{{scale:0}},{{scale:1,duration:0.6,ease:"elastic.out(1,0.5)"}},{t0 + 2.3:.2f});')
    return (f'<div style="position:absolute;inset:0;background:#cdeaf3"></div><div style="position:absolute;left:0;top:{G}px;width:{W}px;height:300px;background:#9ccfb0;'
            f'box-shadow:inset 0 14px 22px rgba(255,255,255,.4)"></div>'
            f'<style>.cl{{position:absolute;border-radius:30px;box-shadow:0 10px 18px rgba(0,0,0,.18),inset -8px -10px 16px rgba(0,0,0,.12),inset 8px 8px 14px rgba(255,255,255,.5)}}</style>'
            f'{coins}<div id="kface" class="cl" style="left:1240px;top:{G-420}px;width:200px;height:200px;border-radius:50%;'
            f'background:radial-gradient(circle at 35% 30%,#ffb3c6,#ff6f91);display:flex;align-items:center;justify-content:center;font-size:90px;font-family:sansx;color:#fff">^^</div>'),\
        ("클레이 (말랑한 입체)", "찰흙처럼 눌리고 튕김(스쿼시·스트레치) — 친근·귀여움, 어린이·생활·호기심, 캐릭터 감정")


def build(work: Path) -> Path:
    a = work / "assets"
    (a / "fonts").mkdir(parents=True, exist_ok=True)
    shutil.copy(hyper.GSAP, a / "gsap.min.js")
    for f in ("NanumGothic-Bold.ttf", "NanumGothic-ExtraBold.ttf", "NanumPenScript-Regular.ttf"):
        shutil.copy(ROOT / "ytflow/assets/fonts" / f, a / "fonts" / f)
    js, secs = [], []
    dark = {"liquid", "neon", "css3d"}
    for i, fn in enumerate(S):
        t0 = i * SEG
        body, (name, when) = fn(i + 1, t0, js)
        secs.append(f'<div class="sec" id="sec{i}">{body}{label(i + 1, name, when, fn.__name__ in dark)}</div>')
        js.append(f'tl.set("#sec{i}",{{visibility:"visible"}},{t0:.2f});tl.set("#sec{i}",{{visibility:"hidden"}},{t0 + SEG:.2f});')
        js.append(f'tl.fromTo("#sec{i} .lab",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.35,ease:"expo.out"}},{t0 + 0.05:.2f});')
    dur = SEG * len(S)
    html = f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H}">
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:sans;src:url('assets/fonts/NanumGothic-Bold.ttf')}}
@font-face{{font-family:sansx;src:url('assets/fonts/NanumGothic-ExtraBold.ttf')}}
@font-face{{font-family:pen;src:url('assets/fonts/NanumPenScript-Regular.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.sec{{position:absolute;inset:0;visibility:hidden;overflow:hidden}}
.sec>svg{{position:absolute;inset:0}}
.lab{{position:absolute;left:70px;top:56px;font-family:sansx;font-size:58px;max-width:1100px;line-height:1.2}}
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


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / ".cache" / "motion_styles"
    work = build(out / "hf")
    mp4 = (out / "motion_styles.mp4").resolve()
    r = subprocess.run([str(hyper.BIN), "render", "--quality", "looks", "--fps", "30", "-o", str(mp4)], cwd=work, env=hyper._env(),
                       capture_output=True, text=True, timeout=1800)
    if r.returncode:
        print((r.stdout + r.stderr)[-1500:])
        sys.exit(1)
    # 견본 한 장: 스타일마다 끝나기 직전 프레임
    sel = "+".join(f"eq(n\\,{int((k + 1) * SEG * 30) - 8})" for k in range(len(S)))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf", f"select='{sel}',scale=640:-1,tile=3x4", "-frames:v", "1",
                    str(out / "sheet.png")], check=True)
    print("→", mp4, "·", out / "sheet.png")


if __name__ == "__main__":
    main()
