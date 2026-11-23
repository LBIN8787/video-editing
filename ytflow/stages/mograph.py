"""모션그래픽 사물 — '말에 맞춰 생기는 사물'(motion2)에 더하는 움직이는 그림 (2026-11-23 사용자: "편집방식을 모션그래픽을
좀 잘쓰고싶습니다 적극적으로 많이요").

원칙: 화면(카메라)을 확대·축소하지 않는다(v31). 움직이는 것은 '대본의 동사를 연기하는 사물'이다 —
떨어진다(drop)·돈다(spin)·흔들린다(shake)·시계가 그 시각을 가리킨다(clock)·돈이 들어간다(coins)·
시간 줄 위 지금 위치가 옮겨 간다(dot + move)·감시한다(scan).

박자 대본 (motion 목록에 그대로):
  {"t": "긴급회의", "do": "glyph", "id": "hall", "icon": "landmark", "anim": "draw", "x": 1500, "y": 420, "label": "정부서울청사"}
      anim: pop(기본)·drop·spin·shake·swing·beat·draw     size(150)·color·accent(false 면 글자색)
  {"t": "9시", "do": "clock", "id": "c9", "hour": 9, "minute": 0, "x": 1500, "y": 700, "label": "오늘 09:00"}
  {"t": "증안펀드", "do": "coins", "id": "cn", "into": "pig", "n": 5}            # into: 먼저 놓인 사물 id
  {"t": "코스피는", "do": "dot", "id": "cur", "x": 230, "y": 560}                # 커서 점
  {"t": "정규장은", "do": "move", "on": "cur", "to": [1690, 560]}               # 사물 옮기기
  {"t": "감시", "do": "scan", "id": "sc", "x": 1500, "y": 560, "w": 420}
"""
from __future__ import annotations

import html as H
import math
import re
from pathlib import Path

ICONS = Path(__file__).resolve().parent.parent / "assets" / "icons"
KINDS = ("glyph", "clock", "coins", "dot", "scan")


def _e(s) -> str:
    return H.escape(str(s))


def glyph_svg(name: str, size: float, color: str, sw: float = 2.0, gid: str = "") -> str:
    f = ICONS / f"{name}.svg"
    raw = f.read_text(encoding="utf-8") if f.exists() else \
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/></svg>'
    raw = re.sub(r'width="[^"]*"', f'width="{size:.0f}"', raw, count=1)
    raw = re.sub(r'height="[^"]*"', f'height="{size:.0f}"', raw, count=1)
    raw = raw.replace("currentColor", color).replace('stroke-width="2"', f'stroke-width="{sw}"')
    if gid:
        raw = raw.replace("<svg", f'<svg id="{gid}" style="overflow:visible"', 1)
    return raw


def _label(st, did: str, x, y, h, lab: str, t: float, light: bool):
    if not lab:
        return
    col = "#2A2E36" if light else "#E8EEF6"
    st.items.append(f'<div id="{did}_lb" style="position:absolute;left:{x - 300:.0f}px;top:{y + h / 2 + 10:.0f}px;width:600px;text-align:center;'
                    f'font-family:gr,sans;font-size:34px;color:{col};white-space:nowrap;opacity:0;z-index:6">{_e(lab)}</div>')
    st.js.append(f'tl.fromTo("#{did}_lb",{{opacity:0,y:8}},{{opacity:1,y:0,duration:0.3}},{t + 0.2:.3f});')


def move(st, m: dict, t: float) -> None:
    """이미 놓인 사물을 to=[x, y] 로 옮김 (GSAP x·y 는 처음 자리 기준)."""
    on = m.get("on")
    if on not in st.pos:
        return
    if not hasattr(st, "_origin"):
        st._origin = {}
    x0, y0 = st._origin.setdefault(on, st.pos[on][:2])
    tx, ty = m["to"]
    st.js.append(f'tl.to("#{st.p}_{on}",{{x:{tx - x0:.0f},y:{ty - y0:.0f},duration:{m.get("dur", 0.6)},ease:"power2.inOut"}},{t:.3f});')
    st.pos[on] = (tx, ty) + tuple(st.pos[on][2:])
    st.sfx.append(("whoosh-short", t))


def add(st, m: dict, do: str, x: float, y: float, t: float, lab: str) -> None:
    light = bool(st.th.get("light_bg"))
    acc = m.get("color") or st.th.get("accent", st.th["arrow"])
    ink = "#20242C" if light else "#E8EEF6"
    did = f"{st.p}_{m['id']}"
    if do == "glyph":
        sz = m.get("size", 150)
        col = acc if m.get("accent", True) else ink
        st.items.append(f'<div id="{did}" style="position:absolute;left:{x - sz / 2:.0f}px;top:{y - sz / 2:.0f}px;width:{sz}px;height:{sz}px;opacity:0;z-index:5">'
                        f'{glyph_svg(m.get("icon", "circle"), sz, col, m.get("sw", 1.8), did + "_g")}</div>')
        st.pos[m["id"]] = (x, y, sz, sz)
        a = m.get("anim", "pop")
        if a == "drop":
            st.js.append(f'tl.fromTo("#{did}",{{opacity:0,y:-260}},{{opacity:1,y:0,duration:0.6,ease:"bounce.out"}},{t:.3f});')
        elif a == "draw":   # 선이 그려지며 나타남
            st.js.append(f'tl.set("#{did}",{{opacity:1}},{t:.3f});'
                         f'tl.fromTo("#{did}_g > *",{{strokeDasharray:90,strokeDashoffset:90}},{{strokeDashoffset:0,duration:0.8,stagger:0.07,ease:"power2.inOut"}},{t:.3f});')
        else:
            st.js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(2.2)"}},{t:.3f});')
        if a == "spin":
            st.js.append(f'tl.to("#{did}_g",{{rotation:360,transformOrigin:"50% 50%",duration:1.2,ease:"power2.inOut"}},{t + 0.35:.3f});')
        elif a == "shake":
            st.js.append(f'tl.to("#{did}_g",{{rotation:14,transformOrigin:"50% 15%",duration:0.08,yoyo:true,repeat:7,ease:"sine.inOut"}},{t + 0.35:.3f});')
        elif a == "swing":
            st.js.append(f'tl.fromTo("#{did}_g",{{rotation:-20}},{{rotation:0,transformOrigin:"50% 0%",duration:1.0,ease:"elastic.out(1,0.35)"}},{t + 0.2:.3f});')
        elif a == "beat":
            st.js.append(f'tl.to("#{did}_g",{{scale:1.15,transformOrigin:"50% 50%",duration:0.18,yoyo:true,repeat:3,ease:"power1.inOut"}},{t + 0.4:.3f});')
        _label(st, did, x, y, sz, lab, t, light)
        st.sfx.append(("pop", t))
    elif do == "clock":   # 시계 바늘이 그 시각으로 돈다
        r = m.get("r", 90)
        hh, mi = float(m.get("hour", 9)), float(m.get("minute", 0))
        ticks = "".join(f'<line x1="{r + (r - 12) * math.sin(k * math.pi / 6):.1f}" y1="{r - (r - 12) * math.cos(k * math.pi / 6):.1f}" '
                        f'x2="{r + (r - 24) * math.sin(k * math.pi / 6):.1f}" y2="{r - (r - 24) * math.cos(k * math.pi / 6):.1f}" stroke="{ink}" stroke-width="4"/>'
                        for k in range(12))
        st.items.append(
            f'<div id="{did}" style="position:absolute;left:{x - r:.0f}px;top:{y - r:.0f}px;width:{2 * r}px;height:{2 * r}px;opacity:0;z-index:5">'
            f'<svg width="{2 * r}" height="{2 * r}" viewBox="0 0 {2 * r} {2 * r}"><circle cx="{r}" cy="{r}" r="{r - 4}" fill="none" stroke="{acc}" stroke-width="6"/>{ticks}'
            f'<line id="{did}_h" x1="{r}" y1="{r}" x2="{r}" y2="{r * 0.48:.0f}" stroke="{ink}" stroke-width="9" stroke-linecap="round"/>'
            f'<line id="{did}_m" x1="{r}" y1="{r}" x2="{r}" y2="{r * 0.24:.0f}" stroke="{acc}" stroke-width="5" stroke-linecap="round"/>'
            f'<circle cx="{r}" cy="{r}" r="8" fill="{acc}"/></svg></div>')
        st.pos[m["id"]] = (x, y, 2 * r, 2 * r)
        st.js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{t:.3f});'
                     f'tl.fromTo("#{did}_h",{{rotation:0}},{{rotation:{(hh % 12) * 30 + mi * 0.5 + 360:.0f},svgOrigin:"{r} {r}",duration:1.2,ease:"power3.out"}},{t + 0.2:.3f});'
                     f'tl.fromTo("#{did}_m",{{rotation:0}},{{rotation:{mi * 6 + 720:.0f},svgOrigin:"{r} {r}",duration:1.2,ease:"power3.out"}},{t + 0.2:.3f});')
        _label(st, did, x, y, 2 * r, lab, t, light)
        st.sfx.append(("click-soft", t))
    elif do == "coins":   # 동전이 위에서 떨어져 목표 사물(into) 속으로
        n = int(m.get("n", 5))
        tx, ty = st.pos[m["into"]][:2] if m.get("into") in st.pos else (x, y)
        for k in range(n):
            cid = f"{did}_{k}"
            ox = tx + (k - (n - 1) / 2) * 22
            st.items.append(f'<div id="{cid}" style="position:absolute;left:{ox - 22:.0f}px;top:{ty - 60:.0f}px;width:44px;height:44px;border-radius:50%;'
                            f'background:#F2C14E;border:4px solid #B98A1C;opacity:0;z-index:7;box-shadow:0 4px 10px rgba(0,0,0,.3)" data-layout-ignore></div>')
            st.js.append(f'tl.set("#{cid}",{{opacity:1}},{t + k * 0.13:.3f});'
                         f'tl.fromTo("#{cid}",{{y:-280,x:{(k % 2 * 2 - 1) * 36}}},{{y:0,x:0,duration:0.5,ease:"power2.in"}},{t + k * 0.13:.3f});'
                         f'tl.to("#{cid}",{{opacity:0,scale:0.4,y:24,duration:0.15}},{t + k * 0.13 + 0.5:.3f});')
        if m.get("into") in st.pos:
            st.js.append(f'tl.to("#{st.p}_{m["into"]}",{{scale:1.08,duration:0.12,yoyo:true,repeat:{2 * n - 1},ease:"power1.inOut"}},{t + 0.5:.3f});')
        st.sfx.append(("click-soft", t + 0.5))
    elif do == "dot":   # 커서 점 (move 로 옮김)
        r = m.get("r", 16)
        st.items.append(f'<div id="{did}" style="position:absolute;left:{x - r:.0f}px;top:{y - r:.0f}px;width:{2 * r}px;height:{2 * r}px;border-radius:50%;'
                        f'background:{acc};box-shadow:0 0 0 10px {acc}40;opacity:0;z-index:8"></div>')
        st.pos[m["id"]] = (x, y, 2 * r, 2 * r)
        st.js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(3)"}},{t:.3f});')
    elif do == "scan":   # 돋보기가 넓이 w 를 한 번 훑음
        sz, w, d = m.get("size", 120), m.get("w", 500), m.get("dur", 1.4)
        st.items.append(f'<div id="{did}" style="position:absolute;left:{x - w / 2 - sz / 2:.0f}px;top:{y - sz / 2:.0f}px;width:{sz}px;height:{sz}px;opacity:0;z-index:7">'
                        f'{glyph_svg("search", sz, acc, 2.2)}</div>')
        st.js.append(f'tl.set("#{did}",{{opacity:1}},{t:.3f});tl.fromTo("#{did}",{{x:0}},{{x:{w:.0f},duration:{d},ease:"sine.inOut"}},{t:.3f});'
                     f'tl.to("#{did}",{{opacity:0,duration:0.25}},{t + d:.3f});')
        st.sfx.append(("whoosh-short", t))
