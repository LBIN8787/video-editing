"""움직이는 비유 애니메이션 (style: motion-metaphor) — 2026-11-12 사용자 요청.
"단순히 글로만 정리하는 것이 아니라 애니메이션·움직이는 효과로 편집하는 스타일을 추가" (레퍼런스: AI 자동화 해설 채널의
비유 장면 — 갈라진 화면, 사람·물건이 한쪽으로 몰려가고, '바글바글/휑' 같은 의성어·의태어가 튀어나오고, 손으로 그린 곡선 화살표).
레퍼런스의 그림·캐릭터·문구는 쓰지 않고 '기법'만: 그림은 도형·아이콘으로 직접 그린다 (사용자 선택).

장면 type "metaphor"
  mode "migrate"  무리(사람·돈·데이터)가 한쪽에서 다른 쪽으로 포물선을 그리며 옮겨 감 → 한쪽은 북적, 한쪽은 텅 빔
      {"type":"metaphor","mode":"migrate","title":"...","hl":"강조어",
       "target":{"label":"코어위브","color":"#D9412B","kind":"bus|building|box"},
       "sources":[{"label":"A","color":"#2F6FB3"},...],          # 오른쪽 작은 탈것·건물들 (0~3개)
       "crowd":{"icon":"person|<lucide 이름>","n":36,"start":"right|left","beat":1,"board":0.8},
       "words":[{"text":"바글바글","side":"left","beat":1},{"text":"휑","side":"right","beat":1}],
       "arrow":{"beat":0}, "beats":[...]}
  mode "pop"      가운데 물건이 튀어 들어오고, 꼬리표(숫자)가 올라가며, 의태어가 붙음
      {"type":"metaphor","mode":"pop","object":{"label":"옛 GPU","kind":"box","color":"#5B6B7A"},
       "tag":{"from":"100","to":"+30~50%","beat":1},"words":[...],"title":"...","hl":"..."}
움직임은 장면 안에서 한 번씩만 (v12 차분하게): 등장 → 이동 한 번 → 의태어 → 멈춤.
"""
from __future__ import annotations

import hashlib
import html as H

SKY, SKY2, GROUND, GROUND2 = "#BFE4F6", "#E9F6FC", "#A7B0BA", "#8E98A3"
INK = "#14181F"


def _outline(px: int) -> str:
    """글자 테두리: text-shadow 8방향 (HTML 글자에서 -webkit-text-stroke 는 글자 안쪽을 덮어 뭉개짐)."""
    import math
    return ",".join(f"{px * math.cos(a * math.pi / 8):.1f}px {px * math.sin(a * math.pi / 8):.1f}px 0 {INK}" for a in range(16))
YEL = "#FFD84A"
PEOPLE = ["#2B3446", "#3A4458", "#4A3F35", "#5A6474", "#33405A", "#6B5A4A", "#7D8794"]


def _r(key: str, lo: float, hi: float) -> float:
    v = int(hashlib.md5(key.encode()).hexdigest()[:6], 16) / 0xFFFFFF
    return lo + (hi - lo) * v


def _scenery(D, W, HH):
    D.media.append(f'<div style="position:absolute;inset:0;background:linear-gradient({SKY2},{SKY} 58%,{SKY} 60%)"></div>'
                   f'<div style="position:absolute;left:0;right:0;top:{int(HH * 0.6)}px;bottom:0;background:linear-gradient({GROUND},{GROUND2})"></div>'
                   f'<div style="position:absolute;left:0;right:0;top:{int(HH * 0.6)}px;height:6px;background:rgba(255,255,255,.35)"></div>')


def _vehicle(D, x, y, w, label, color, kind="bus", at=0.2, big=False):
    """도형으로 그린 탈것·건물·상자 + 이름표. 반환: 요소 id (흔들기용)."""
    i = D._id()
    h = int(w * (0.52 if kind == "bus" else 0.8 if kind == "building" else 0.62))
    fs = 46 if big else 28
    if kind == "bus":
        win = "".join(f'<span style="position:absolute;top:{int(h * 0.16)}px;left:{int(w * (0.08 + k * 0.15))}px;width:{int(w * 0.12)}px;height:{int(h * 0.26)}px;'
                      f'background:#1C2633;border-radius:6px;opacity:.85"></span>' for k in range(5))
        wheels = "".join(f'<span style="position:absolute;bottom:-{int(h * 0.12)}px;left:{int(w * p)}px;width:{int(h * 0.26)}px;height:{int(h * 0.26)}px;'
                         f'background:#20252D;border-radius:50%;border:5px solid #59606A"></span>' for p in (0.14, 0.72))
        body = (f'<div style="position:absolute;inset:0;background:{color};border-radius:{int(h * 0.18)}px {int(h * 0.3)}px {int(h * 0.12)}px {int(h * 0.12)}px;'
                f'box-shadow:inset 0 -{int(h * 0.12)}px 0 rgba(0,0,0,.18),0 12px 24px rgba(0,0,0,.25)">{win}{wheels}</div>')
        tag_top = int(h * 0.5)
    elif kind == "building":
        win = "".join(f'<span style="position:absolute;top:{int(h * (0.12 + r * 0.2))}px;left:{int(w * (0.12 + c * 0.27))}px;width:{int(w * 0.18)}px;height:{int(h * 0.11)}px;'
                      f'background:#DDEBF5;opacity:.8"></span>' for r in range(3) for c in range(3))
        body = (f'<div style="position:absolute;inset:0;background:{color};border-radius:8px;box-shadow:inset -{int(w * 0.1)}px 0 0 rgba(0,0,0,.15),0 12px 24px rgba(0,0,0,.25)">{win}</div>')
        tag_top = int(h * 0.74)
    else:   # box (상자·서버·칩)
        body = (f'<div style="position:absolute;inset:0;background:{color};border-radius:14px;box-shadow:inset 0 -{int(h * 0.14)}px 0 rgba(0,0,0,.2),0 12px 24px rgba(0,0,0,.25)">'
                + "".join(f'<span style="position:absolute;left:{int(w * 0.1)}px;right:{int(w * 0.1)}px;top:{int(h * (0.16 + r * 0.18))}px;height:6px;background:rgba(255,255,255,.35);border-radius:3px"></span>' for r in range(3))
                + '</div>')
        tag_top = int(h * 0.62)
    tag = (f'<div style="position:absolute;left:50%;top:{tag_top}px;transform:translate(-50%,-50%);background:#fff;color:{INK};font-family:sans-x;font-size:{fs}px;'
           f'padding:{6 if not big else 10}px {14 if not big else 22}px;border-radius:10px;white-space:nowrap;box-shadow:0 3px 8px rgba(0,0,0,.2)">{H.escape(label)}</div>')
    D.items.append(f'<div id="{i}" style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h:.0f}px;width:{w}px;height:{h}px;transform-origin:50% 100%">{body}{tag}</div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.5,ease:"back.out(1.6)"}},{at:.2f});')
    return i, h


def _person(D, key, x, y, s, color):
    i = D._id()
    D.items.append(f'<div id="{i}" class="mm-p" style="position:absolute;left:{x - s / 2:.0f}px;top:{y - s * 1.6:.0f}px;width:{s:.0f}px;height:{s * 1.6:.0f}px">'
                   f'<span style="position:absolute;left:{s * 0.22:.0f}px;top:0;width:{s * 0.56:.0f}px;height:{s * 0.56:.0f}px;border-radius:50%;background:{color}"></span>'
                   f'<span style="position:absolute;left:0;top:{s * 0.6:.0f}px;width:{s:.0f}px;height:{s:.0f}px;border-radius:{s * 0.45:.0f}px {s * 0.45:.0f}px 6px 6px;background:{color}"></span></div>')
    return i


def _word(D, text, x, y, at, color=YEL, rot=-8, size=88):
    i = D._id()
    D.items.append(f'<div id="{i}" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;transform:translate(-50%,-50%) rotate({rot}deg);font-family:sans-x;font-size:{size}px;'
                   f'color:{color};text-shadow:{_outline(6)},6px 8px 0 {INK};white-space:nowrap;letter-spacing:2px">{H.escape(text)}</div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(2.6)"}},{at:.2f});')
    D.sfx.append(("pop", at))


def _title(D, W, title, hl, at):
    if not title:
        return
    from .paper import FT, fit
    i = D._id()
    parts = H.escape(title)
    if hl and hl in title:
        a, b = title.split(hl, 1)
        parts = f'{H.escape(a)}<span style="background:{YEL};color:{INK};text-shadow:none;padding:0 14px;border-radius:6px;box-shadow:0 0 0 5px {INK}">{H.escape(hl)}</span>{H.escape(b)}'
    D.items.append(f'<div id="{i}" style="position:absolute;left:50%;top:70px;transform:translateX(-50%);font-family:sans-x;font-size:64px;color:#fff;'
                   f'text-shadow:{_outline(5)};white-space:nowrap">{parts}</div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{at:.2f});')


def _arrow(D, x1, y1, x2, y2, at):
    i = D._id()
    mx, my = (x1 + x2) / 2, max(260, min(y1, y2) - 170)   # 위쪽 제목(70~150px)과 겹치지 않게
    loop = f"C {mx + 120:.0f},{my - 40:.0f} {mx + 60:.0f},{my + 90:.0f} {mx:.0f},{my + 20:.0f}"   # 손으로 그린 듯 작은 고리
    d = f"M{x1:.0f},{y1:.0f} Q{(x1 + mx) / 2 + 60:.0f},{my - 10:.0f} {mx + 40:.0f},{my + 10:.0f} {loop} Q{(mx + x2) / 2 - 40:.0f},{my - 30:.0f} {x2:.0f},{y2:.0f}"
    ang_x, ang_y = x2 - (mx + x2) / 2 + 40, y2 - (my - 30)
    import math
    a = math.atan2(ang_y, ang_x)
    hx1, hy1 = x2 - 46 * math.cos(a - 0.5), y2 - 46 * math.sin(a - 0.5)
    hx2, hy2 = x2 - 46 * math.cos(a + 0.5), y2 - 46 * math.sin(a + 0.5)
    D.items.append(f'<svg data-layout-ignore style="position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible">'
                   f'<path id="{i}" d="{d}" fill="none" stroke="{YEL}" stroke-width="14" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" '
                   f'style="filter:drop-shadow(0 0 0 {INK}) drop-shadow(3px 3px 0 {INK})"/>'
                   f'<path id="{i}h" d="M{hx1:.0f},{hy1:.0f} L{x2:.0f},{y2:.0f} L{hx2:.0f},{hy2:.0f}" fill="none" stroke="{YEL}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" style="opacity:0;filter:drop-shadow(3px 3px 0 {INK})"/></svg>')
    D.js.append(f'tl.to("#{i}",{{strokeDashoffset:0,duration:0.8,ease:"power1.inOut"}},{at:.2f});tl.to("#{i}h",{{opacity:1,duration:0.15}},{at + 0.75:.2f});')
    D.sfx.append(("pencil", at))


def s_metaphor(D, sc, bt, dur):
    from .hybrid import W, HH
    _scenery(D, W, HH)
    D.label(sc.get("label", ""), dark=True)
    beat_t = lambda k: bt[min(k, len(bt) - 1)][0] if bt else 0.0
    ground = HH * 0.6 + 120
    mode = sc.get("mode", "migrate")
    if mode == "pop":
        ob = sc.get("object", {})
        vid, h = _vehicle(D, W / 2, ground + 40, 640, ob.get("label", ""), ob.get("color", "#5B6B7A"), ob.get("kind", "box"), at=beat_t(0) + 0.2, big=True)
        D.js.append(f'tl.fromTo("#{vid}",{{scaleY:0.9}},{{scaleY:1,duration:0.35,ease:"back.out(3)"}},{beat_t(0) + 0.6:.2f});')
        tg = sc.get("tag")
        if tg:
            t1 = beat_t(tg.get("beat", 1)) + 0.2
            i = D._id()
            D.items.append(f'<div id="{i}" style="position:absolute;left:{W / 2 + 300:.0f}px;top:{ground - h - 40:.0f}px;transform:rotate(8deg);background:#fff;border:6px solid {INK};'
                           f'border-radius:16px;padding:14px 30px;font-family:sans-x;font-size:84px;color:#C8322A;white-space:nowrap">{H.escape(tg.get("to", ""))}</div>')
            D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:-160,rotation:-20}},{{opacity:1,y:0,rotation:8,duration:0.6,ease:"bounce.out"}},{t1:.2f});')
            D.sfx.append(("pop", t1 + 0.4))
        for k, w in enumerate(sc.get("words", [])):
            x = W / 2 + (-520 if w.get("side") == "left" else 520 if w.get("side") == "right" else 0)
            _word(D, w["text"], x, ground - h - 150 + 40 * k, beat_t(w.get("beat", 1)) + 0.5, w.get("color", YEL), -8 if k % 2 == 0 else 6)
        _title(D, W, sc.get("title", ""), sc.get("hl", ""), beat_t(0) + 0.1)
        return
    # migrate: 왼쪽 큰 대상, 오른쪽 작은 출발지들, 가운데 칸막이, 무리가 포물선으로 옮겨 감
    tg = sc.get("target", {})
    lx = W * 0.27
    divider = D._id()
    D.items.append(f'<div id="{divider}" style="position:absolute;left:{W / 2 - 4:.0f}px;top:0;width:8px;height:{HH}px;background:#fff;opacity:.9"></div>')
    D.js.append(f'tl.fromTo("#{divider}",{{scaleY:0}},{{scaleY:1,duration:0.5,ease:"power2.out"}},{beat_t(0):.2f});')
    tid, th = _vehicle(D, lx, ground, 620, tg.get("label", ""), tg.get("color", "#D9412B"), tg.get("kind", "bus"), at=beat_t(0) + 0.2, big=True)
    srcs = sc.get("sources", [])
    sx = [W * 0.62 + k * (W * 0.32 / max(1, len(srcs) - 1 or 1)) for k in range(len(srcs))] if len(srcs) > 1 else [W * 0.76] * len(srcs)
    for k, s in enumerate(srcs):
        _vehicle(D, sx[k], ground - 20, 260, s.get("label", ""), s.get("color", "#2F6FB3"), s.get("kind", "bus"), at=beat_t(0) + 0.4 + 0.15 * k)
    cr = sc.get("crowd", {})
    n = int(cr.get("n", 30))
    start_right = cr.get("start", "right") == "right"
    move_at = beat_t(cr.get("beat", 1)) + 0.3
    board = float(cr.get("board", 0.8))
    icon = cr.get("icon", "person")
    for k in range(n):
        key = f"{sc.get('id', 0)}_{k}"
        # 출발 자리: 오른쪽(또는 왼쪽) 아래에 흩어져 서 있음
        bx = (W * 0.58 if start_right else W * 0.08) + _r(key + "x", 0, W * 0.36)
        by = ground + 30 + _r(key + "y", 0, 150)
        s = _r(key + "s", 34, 52) * (1 + (by - ground) / 400)
        col = PEOPLE[k % len(PEOPLE)]
        if icon == "person":
            pid = _person(D, key, bx, by, s, col)
        else:
            from .icons import svg_markup
            pid = D._id()
            D.items.append(f'<div id="{pid}" style="position:absolute;left:{bx - s / 2:.0f}px;top:{by - s:.0f}px">{svg_markup(icon, int(s * 1.7), cr.get("color", "#E0A82E"), 2.8) or ""}</div>')
        D.js.append(f'tl.fromTo("#{pid}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{beat_t(0) + 0.3 + 0.01 * k:.2f});')
        if k < n * board:   # 옮겨 가는 사람 — 대상 문 앞 무리로 (포물선: x 는 고르게, y 는 위로 갔다 내려옴)
            tx = lx + _r(key + "tx", -280, 300)
            ty = ground + 30 + _r(key + "ty", 0, 150)
            dx, dy = tx - bx, ty - by
            at = move_at + _r(key + "t", 0, 1.4)
            d = 0.9
            D.js.append(f'tl.to("#{pid}",{{x:{dx:.0f},duration:{d},ease:"power1.inOut"}},{at:.2f});'
                        f'tl.to("#{pid}",{{y:{dy / 2 - 120:.0f},duration:{d / 2:.2f},ease:"sine.out"}},{at:.2f});'
                        f'tl.to("#{pid}",{{y:{dy:.0f},duration:{d / 2:.2f},ease:"sine.in"}},{at + d / 2:.2f});')
    D.js.append(f'tl.to("#{tid}",{{scaleY:0.96,duration:0.18,yoyo:true,repeat:3,ease:"sine.inOut"}},{move_at + 1.4:.2f});')   # 사람이 몰려 타며 출렁
    if sc.get("arrow"):
        _arrow(D, W * 0.72, ground - 330, lx + 200, ground - th - 60, beat_t(sc["arrow"].get("beat", 0)) + 0.6)
    for k, w in enumerate(sc.get("words", [])):
        x = W * (0.12 if w.get("side") == "left" else 0.86)
        y = ground - th - 120 if w.get("side") == "left" else ground - 470
        _word(D, w["text"], x, y, beat_t(w.get("beat", 1)) + (2.0 if w.get("side") == "left" else 1.0), w.get("color", YEL if w.get("side") == "left" else "#7EF0D8"),
              -10 if w.get("side") == "left" else 8)
    _title(D, W, sc.get("title", ""), sc.get("hl", ""), beat_t(0) + 0.1)


def register():
    from . import hybrid
    hybrid.RENDER["metaphor"] = s_metaphor
