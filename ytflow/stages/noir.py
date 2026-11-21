"""누아르 사건 보드 (noirboard 장면) — 2026-11-21 사용자: "누아르사건보드 연출 이런걸 한번 사용해주세요".

어두운 방, 스탠드 불빛 한 줄기 아래 검은 보드. 흑백 사진(폴라로이드·테이프)과 타자 친 메모 카드가 박자마다 꽂히고,
붉은 실이 핀에서 핀으로 이어진다. 카메라는 장면 내내 천천히 다가가고, 지금 말하는 카드 쪽으로 불빛이 옮겨 간다.
대본 문법은 map_causal 과 같다(reveal·draw·active) — 증거판(코르크, identity.s_board)의 어두운 변형.

    {"type": "noirboard", "title": "사건: …",
     "nodes": {"p": {"kind": "photo", "img": "04_assets/footage/raw/x.jpg", "cap": "…", "date": "2026.2.27", "x": 960, "y": 300, "w": 250},
               "a": {"kind": "note", "title": "…", "text": "…", "date": "2022", "x": 260, "y": 700, "stamp": "쉼"}},
     "edges": [["a", "b"], …],
     "beats": [{"say": "…", "reveal": ["a"], "draw": [["a", "b"]], "active": "a"}]}

강조는 덜어 냄(2026-11-21 사용자: "강조연출이 너무 많고") — 동그라미·형광펜 없이 불빛과 실로만.
"""
from __future__ import annotations

import html as H

INK = "#1E1A16"
PAPER = "#E9E2D2"
RED = "#B0261E"


def _h(key: str, lo: float, hi: float) -> float:
    v = sum(ord(c) * (i + 3) for i, c in enumerate(key)) % 1000 / 1000
    return lo + (hi - lo) * v


def _asset(D, sc, src):
    from .explain import _asset as a
    return a(D, sc, src)


def _node_size(nd: dict) -> tuple[float, float]:
    if nd.get("kind") == "photo":
        w = nd.get("w", 250)
        return w, w * 1.34
    return nd.get("w", 320), nd.get("h", 190)


def s_noirboard(D, sc: dict, bt: list, dur: float):
    nodes, edges = sc["nodes"], sc.get("edges", [])
    D.label(sc.get("label", ""), dark=True)
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    p = D._id()
    when, strings, active = {}, [], []
    for b, (t0, d) in zip(sc["beats"], bt):
        for k_i, k in enumerate(b.get("reveal", [])):
            when.setdefault(k, t0 + 0.3 + 0.35 * k_i)
        for e_i, e in enumerate(b.get("draw", [])):
            strings.append((tuple(e), t0 + 0.8 + 0.5 * e_i))
        if b.get("active"):
            active.append((b["active"], t0 + 0.2))

    # 방: 거의 검은 바탕 + 위에서 떨어지는 스탠드 불빛 + 결 + 가장자리 어둡게
    D.items.append(
        f'<div data-layout-ignore style="position:absolute;inset:0;background:#0B0B0D;z-index:0"></div>'
        f'<div id="{p}_glow" data-layout-ignore style="position:absolute;inset:0;z-index:0;'
        f'background:radial-gradient(ellipse 62% 70% at 50% 34%,rgba(255,214,160,.20),rgba(255,214,160,.06) 45%,rgba(0,0,0,0) 72%)"></div>')
    D.js.append(f'tl.fromTo("#{p}_glow",{{opacity:0}},{{opacity:1,duration:0.25}},0.05);'
                f'tl.to("#{p}_glow",{{opacity:0.55,duration:0.06}},0.32);tl.to("#{p}_glow",{{opacity:1,duration:0.08}},0.40);')

    inner = []
    # 실 (카드 아래)
    paths, sjs = [], []
    for (a, b2), at in strings:
        na, nb = nodes[a], nodes[b2]
        _, ha = _node_size(na)
        _, hb = _node_size(nb)
        x1, y1, x2, y2 = na["x"], na["y"] - ha / 2 + 14, nb["x"], nb["y"] - hb / 2 + 14
        mx, my = (x1 + x2) / 2, max(y1, y2) + 34
        i = D._id()
        paths.append(f'<path id="{i}" d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" fill="none" stroke="{RED}" stroke-width="3.2" '
                     f'stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" style="filter:drop-shadow(2px 5px 3px rgba(0,0,0,.7))"/>')
        sjs.append(f'tl.to("#{i}",{{strokeDashoffset:0,duration:0.6,ease:"power1.inOut"}},{at:.2f});')
        D.sfx.append(("pencil", at))
    inner.append(f'<svg data-layout-ignore style="position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible;z-index:1">{"".join(paths)}</svg>')

    cjs = []
    for k, at in when.items():
        nd = nodes[k]
        w, h = _node_size(nd)
        x, y = nd["x"], nd["y"]
        rot = nd.get("rot", _h(k, -4.0, 4.0))
        c = f"{p}_{k}"
        date = H.escape(nd.get("date", ""))
        if nd.get("kind") == "photo":
            src = _asset(D, sc, nd.get("img", ""))
            img = (f'<div style="position:absolute;left:12px;top:12px;width:{w - 24:.0f}px;height:{w - 24:.0f}px;background:#222 url({src}) center/cover;'
                   f'filter:grayscale(1) contrast(1.25) brightness(.92)"></div>') if src else ""
            cap = H.escape(nd.get("cap", ""))
            body = (img + f'<div style="position:absolute;left:12px;right:12px;top:{w - 2:.0f}px;font-family:pen,sans;font-size:24px;line-height:1.2;color:{INK};'
                    f'text-align:center">{cap}</div>'
                    f'<div style="position:absolute;left:50%;top:-14px;width:110px;height:30px;margin-left:-55px;background:rgba(220,210,180,.55);transform:rotate(-3deg)"></div>')
            bg = "#F3EFE6"
        else:
            title, text = H.escape(nd.get("title", "")), H.escape(nd.get("text", ""))
            body = (f'<div style="position:absolute;left:18px;right:18px;top:16px;height:3px;background:{RED};opacity:.75"></div>'
                    f'<div style="position:absolute;left:20px;right:20px;top:34px;font-family:sans-x,sans;font-size:30px;line-height:1.2;color:{INK}">{title}</div>'
                    f'<div style="position:absolute;left:20px;right:20px;top:{34 + 44 * max(1, round(len(nd.get("title", "")) / 11)):.0f}px;font-family:sans,sans;'
                    f'font-size:24px;line-height:1.3;color:#3A332B">{text}</div>')
            bg = PAPER
        if date and nd.get("kind") == "photo":   # 사진은 날짜를 사진 귀퉁이에 (설명 글과 겹치지 않게)
            body += (f'<div style="position:absolute;right:20px;top:20px;padding:1px 8px;background:rgba(243,239,230,.92);font-family:gx,sans-x;font-size:24px;'
                     f'color:{RED};letter-spacing:.04em">{date}</div>')
        elif date:
            body += (f'<div style="position:absolute;right:14px;bottom:10px;font-family:gx,sans-x;font-size:26px;color:{RED};letter-spacing:.04em;'
                     f'transform:rotate(-4deg)">{date}</div>')
        if nd.get("stamp"):
            body += (f'<div style="position:absolute;right:10px;top:22px;padding:2px 12px;border:3px solid {RED};color:{RED};font-family:gx,sans-x;'
                     f'font-size:30px;transform:rotate(8deg);opacity:.85">{H.escape(nd["stamp"])}</div>')
        inner.append(f'<div id="{c}" style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;width:{w:.0f}px;height:{h:.0f}px;background:{bg};'
                     f'box-shadow:0 14px 30px rgba(0,0,0,.75);transform:rotate({rot:.1f}deg);opacity:0;z-index:2;filter:brightness(.72)">{body}</div>')
        cjs.append(f'tl.fromTo("#{c}",{{opacity:0,y:-18,scale:1.04}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"power2.out"}},{at:.2f});')
        D.sfx.append(("click-soft", at))
        if nd.get("kind") != "photo":   # 메모는 핀, 사진은 테이프
            pi = D._id()
            inner.append(f'<div id="{pi}" data-layout-ignore style="position:absolute;left:{x - 13:.0f}px;top:{y - h / 2 + 1:.0f}px;width:26px;height:26px;border-radius:50%;'
                         f'background:radial-gradient(circle at 35% 35%,#E2685A,#7E1810 72%);box-shadow:3px 6px 7px rgba(0,0,0,.7);opacity:0;z-index:3"></div>')
            cjs.append(f'tl.to("#{pi}",{{opacity:1,duration:0.2}},{at + 0.3:.2f});')

    # 지금 말하는 카드: 불빛이 옮겨 가고 그 카드만 밝아짐 (동그라미 없이)
    spot = f"{p}_spot"
    inner.append(f'<div id="{spot}" data-layout-ignore style="position:absolute;left:0;top:0;width:760px;height:760px;margin:-380px 0 0 -380px;z-index:4;pointer-events:none;'
                 f'background:radial-gradient(circle,rgba(255,226,180,.16),rgba(255,226,180,0) 62%);opacity:0;mix-blend-mode:screen"></div>')
    lit = None
    for k, at in active:
        nd = nodes[k]
        cjs.append(f'tl.to("#{spot}",{{left:{nd["x"]},top:{nd["y"]},opacity:1,duration:0.7,ease:"power2.inOut"}},{at:.2f});')
        if lit:
            cjs.append(f'tl.to("#{p}_{lit}",{{filter:"brightness(.72)",duration:0.5}},{at:.2f});')
        cjs.append(f'tl.to("#{p}_{k}",{{filter:"brightness(1)",duration:0.5}},{at:.2f});')
        lit = k
    if sc.get("title"):
        inner.append(f'<div id="{p}_t" style="position:absolute;left:0;right:0;top:96px;text-align:center;font-family:serif-x,heavy;font-size:50px;'
                     f'color:#EDE5D4;letter-spacing:.02em;text-shadow:0 3px 18px rgba(0,0,0,.8);opacity:0;z-index:5">{H.escape(sc["title"])}</div>')
        cjs.append(f'tl.to("#{p}_t",{{opacity:1,duration:0.6}},0.35);')

    # 카메라: 장면 내내 천천히 다가감 (자막 자리는 그대로)
    D.items.append(f'<div id="{p}_cam" style="position:absolute;inset:0;transform-origin:50% 45%;z-index:1">{"".join(inner)}</div>')
    D.js.append(f'tl.fromTo("#{p}_cam",{{scale:1.0}},{{scale:1.06,duration:{max(dur, 1):.2f},ease:"none"}},0);')
    # 결·가장자리 어둡게 (맨 위)
    D.items.append(f'<div data-layout-ignore style="position:absolute;inset:0;z-index:6;pointer-events:none;box-shadow:inset 0 0 260px 90px rgba(0,0,0,.85)"></div>')
    D.js.extend(sjs + cjs)


def register():
    from . import hybrid
    hybrid.RENDER["noirboard"] = s_noirboard
    _register_v2()


# ================================================================ 누아르 사건 보드 v2 — 레퍼런스(2026-11-21 사용자 제공 noir-case-board-demo.mp4)
# 거의 검은 바탕 + 고운 결, 가는 붉은 선, 명조 제목. 세 장면:
#   noirtitle  작은 붉은 머리말 + 큰 명조 제목 + 붉은 밑줄이 그어짐 + 작은 설명
#   noircase   위쪽 가는 시간선(눈금·이름, 붉은 점이 지금 칸으로 이동) + 가운데 붉은 동그라미 + 박자마다 생기는 상자,
#              상자와 동그라미를 잇는 선(지금 것은 붉게, 지난 것은 회색으로), 지난 상자는 흐려짐
#   noirsides  '엇갈린 두 편': 두 칸(머리말·붉은 줄), 박자마다 줄이 쌓이고(왼쪽 붉은 막대), 뒤집힌 줄은 그어 지움
# 강조는 이것뿐 — 튀는 등장·효과음·형광펜 없음 (2026-11-21 사용자: "차분하고 깔끔한")
BG2, TXT, MUT, RED2, BOX, LINE = "#0C0C0E", "#ECEAE6", "#8E8E93", "#D42A2F", "#151517", "#55555B"


def _room(D):
    f = "NanumGothic-ExtraBold.ttf" if getattr(D, "calm", False) else "NanumMyeongjo-ExtraBold.ttf"   # 차분한 모드는 나눔고딕 한 계열
    D.css.append(f"@font-face{{font-family:noirserif;src:url(fonts/{f})}}")
    D.items.append(
        f'<div data-layout-ignore style="position:absolute;inset:0;background:{BG2};z-index:0"></div>'
        '<svg data-layout-ignore style="position:absolute;inset:0;width:1920px;height:1080px;z-index:0;opacity:.10">'
        '<filter id="nz"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/></filter>'
        '<rect width="100%" height="100%" filter="url(#nz)"/></svg>'
        '<div data-layout-ignore style="position:absolute;inset:0;z-index:0;box-shadow:inset 0 0 300px 80px rgba(0,0,0,.6)"></div>')


def _fade(D, el, at, dur=0.6, dy=10):
    D.js.append(f'tl.fromTo("#{el}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur},ease:"power2.out"}},{at:.2f});')


def s_noirtitle(D, sc, bt, dur):
    _room(D)
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    p = D._id()
    t0 = bt[0][0]
    title = H.escape(sc.get("title", ""))
    D.items.append(
        f'<div id="{p}k" style="position:absolute;left:0;right:0;top:330px;text-align:center;font-family:sans,sans;font-size:30px;letter-spacing:.12em;color:{RED2};opacity:0;z-index:2">{H.escape(sc.get("kicker", ""))}</div>'
        f'<div id="{p}t" style="position:absolute;left:0;right:0;top:390px;text-align:center;font-family:noirserif,serif;font-size:{sc.get("size", 92)}px;color:{TXT};opacity:0;z-index:2">{title}</div>'
        f'<div id="{p}u" style="position:absolute;left:50%;top:{390 + sc.get("size", 92) * 1.35:.0f}px;width:{sc.get("rule", 520)}px;margin-left:-{sc.get("rule", 520) / 2:.0f}px;height:3px;background:{RED2};transform-origin:left;z-index:2"></div>'
        f'<div id="{p}s" style="position:absolute;left:0;right:0;top:{430 + sc.get("size", 92) * 1.45:.0f}px;text-align:center;font-family:sans,sans;font-size:28px;color:{MUT};opacity:0;z-index:2">{H.escape(sc.get("sub", ""))}</div>')
    _fade(D, f"{p}k", t0 + 0.2)
    _fade(D, f"{p}t", t0 + 0.45, 0.9, 14)
    D.js.append(f'tl.fromTo("#{p}u",{{scaleX:0}},{{scaleX:1,duration:0.9,ease:"power2.inOut"}},{t0 + 1.1:.2f});')
    _fade(D, f"{p}s", t0 + 1.6)


def s_noircase(D, sc, bt, dur):
    _room(D)
    D.label(sc.get("label", ""), dark=True)
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    p = D._id()
    steps = sc.get("steps", [])
    x0, x1, ty = 640, 1720, 118
    sx = [x0 + (x1 - x0) * i / max(1, len(steps) - 1) for i in range(len(steps))]
    parts = [f'<div style="position:absolute;left:{x0}px;top:{ty}px;width:{x1 - x0}px;height:2px;background:#4A4A50"></div>']
    for i, (x, s) in enumerate(zip(sx, steps)):
        parts.append(f'<div style="position:absolute;left:{x - 1:.0f}px;top:{ty - 6}px;width:2px;height:14px;background:#6A6A70"></div>'
                     f'<div style="position:absolute;left:{x - 80:.0f}px;width:160px;top:{ty + 16}px;text-align:center;font-family:sans,sans;font-size:24px;color:{MUT}">{H.escape(s)}</div>')
    parts.append(f'<div id="{p}dot" style="position:absolute;left:{x0 - 11}px;top:{ty - 10}px;width:22px;height:22px;border-radius:50%;background:{RED2};'
                 f'box-shadow:0 0 14px rgba(212,42,47,.8);opacity:0"></div>')
    D.items.append(f'<div id="{p}tl" style="position:absolute;inset:0;z-index:2;opacity:0">{"".join(parts)}</div>')
    D.js.append(f'tl.to("#{p}tl",{{opacity:1,duration:0.6}},0.2);')
    if sc.get("title"):
        D.items.append(f'<div id="{p}h" style="position:absolute;left:144px;top:180px;font-family:sans-x,sans;font-size:46px;color:#A9A9AE;opacity:0;z-index:2">{H.escape(sc["title"])}</div>')
        _fade(D, f"{p}h", 0.35)
    c = sc["center"]
    cx, cy, r = c.get("x", 960), c.get("y", 600), c.get("r", 118)
    D.items.append(f'<div id="{p}c" style="position:absolute;left:{cx - r}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px;border-radius:50%;border:4px solid {RED2};'
                   f'background:{BOX};box-sizing:border-box;z-index:4;opacity:0;display:flex;flex-direction:column;align-items:center;justify-content:center">'
                   f'<div style="font-family:noirserif,serif;font-size:{c.get("size", 58)}px;color:{TXT};line-height:1.1">{H.escape(c.get("title", ""))}</div>'
                   f'<div style="margin-top:12px;font-family:sans,sans;font-size:24px;color:{MUT}">{H.escape(c.get("sub", ""))}</div></div>')
    D.js.append(f'tl.fromTo("#{p}c",{{opacity:0,scale:0.96}},{{opacity:1,scale:1,duration:0.8,ease:"power2.out"}},{bt[0][0] + 0.3:.2f});')
    boxes = sc["boxes"]
    lines = []
    shown, live = [], None
    for b, (t0, d) in zip(sc["beats"], bt):
        if b.get("step") is not None and steps:
            D.js.append(f'tl.to("#{p}dot",{{opacity:1,x:{sx[b["step"]] - x0:.0f},duration:0.7,ease:"power2.inOut"}},{t0 + 0.1:.2f});')
        for k in b.get("reveal", []):
            bx = boxes[k]
            w, h = bx.get("w", 380), bx.get("h", 124)
            x, y = bx["x"], bx["y"]
            bid = f"{p}_{k}"
            D.items.append(
                f'<div id="{bid}" style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;width:{w}px;height:{h}px;z-index:4;opacity:0">'
                f'<div style="position:absolute;left:0;top:-34px;font-family:sans,sans;font-size:22px;color:{MUT}">{H.escape(bx.get("tag", ""))}</div>'
                f'<div id="{bid}b" style="position:absolute;inset:0;border:3px solid {RED2};background:{BOX};box-sizing:border-box;display:flex;flex-direction:column;'
                f'align-items:center;justify-content:center"><div style="font-family:sans-x,sans;font-size:{bx.get("size", 38)}px;color:{TXT};white-space:nowrap">{H.escape(bx.get("title", ""))}</div>'
                f'<div style="margin-top:6px;font-family:sans,sans;font-size:24px;color:{MUT};white-space:nowrap">{H.escape(bx.get("sub", ""))}</div></div></div>')
            D.js.append(f'tl.fromTo("#{bid}",{{opacity:0}},{{opacity:1,duration:0.6,ease:"power2.out"}},{t0 + 0.3:.2f});')
            # 상자 → 동그라미 선 (상자 가장자리에서 동그라미 가장자리까지)
            import math
            dx, dy = cx - x, cy - y
            L = math.hypot(dx, dy) or 1
            ux, uy = dx / L, dy / L
            ra = min(abs(ux) * w / 2 + abs(uy) * h / 2, math.hypot(w, h) / 2)
            ax, ay = x + ux * ra, y + uy * ra
            bxx, byy = cx - ux * (r + 2), cy - uy * (r + 2)
            lid = f"{bid}l"
            lines.append(f'<line id="{lid}" x1="{ax:.0f}" y1="{ay:.0f}" x2="{bxx:.0f}" y2="{byy:.0f}" stroke="{RED2}" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
            D.js.append(f'tl.to("#{lid}",{{strokeDashoffset:0,duration:0.7,ease:"power1.inOut"}},{t0 + 0.7:.2f});')
            if bx.get("edge"):
                mx, my = (ax + bxx) / 2, (ay + byy) / 2
                D.items.append(f'<div id="{lid}t" style="position:absolute;left:{mx - 120:.0f}px;width:240px;top:{my - 34:.0f}px;text-align:center;font-family:sans-x,sans;'
                               f'font-size:24px;color:{TXT};opacity:0;z-index:5"><span style="background:{BG2};padding:2px 8px">{H.escape(bx["edge"])}</span></div>')
                D.js.append(f'tl.to("#{lid}t",{{opacity:1,duration:0.4}},{t0 + 1.2:.2f});')
            # 지난 상자·선은 회색으로
            for old in shown:
                D.js.append(f'tl.to("#{p}_{old}b",{{borderColor:"{LINE}",duration:0.5}},{t0 + 0.3:.2f});'
                            f'tl.to("#{p}_{old}l",{{stroke:"{LINE}",duration:0.5}},{t0 + 0.3:.2f});')
            shown.append(k)
        for k in b.get("dim", []):
            D.js.append(f'tl.to("#{p}_{k}",{{opacity:0.28,duration:0.6}},{t0 + 0.4:.2f});tl.to("#{p}_{k}l",{{opacity:0.25,duration:0.6}},{t0 + 0.4:.2f});')
    D.items.insert(len(D.items) - 0, f'<svg data-layout-ignore style="position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:3">{"".join(lines)}</svg>')


def s_noirsides(D, sc, bt, dur):
    _room(D)
    D.label(sc.get("label", ""), dark=True)
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    p = D._id()
    if sc.get("title"):
        D.items.append(f'<div id="{p}h" style="position:absolute;left:0;right:0;top:110px;text-align:center;font-family:sans-x,sans;font-size:44px;color:#A9A9AE;opacity:0;z-index:2">{H.escape(sc["title"])}</div>')
        _fade(D, f"{p}h", 0.2)
    D.items.append(f'<div id="{p}v" style="position:absolute;left:959px;top:210px;width:2px;height:720px;background:#38383D;transform-origin:top;z-index:2"></div>')
    D.js.append(f'tl.fromTo("#{p}v",{{scaleY:0}},{{scaleY:1,duration:0.8,ease:"power2.inOut"}},0.3);')
    cols = sc["sides"]
    X = [122, 1020]
    for i, s in enumerate(cols):
        x = X[i]
        D.items.append(f'<div id="{p}s{i}" style="position:absolute;left:{x}px;top:200px;width:778px;opacity:0;z-index:2">'
                       f'<div style="font-family:sans-x,sans;font-size:58px;color:{TXT};white-space:nowrap">{H.escape(s.get("head", ""))}</div>'
                       f'<div style="margin-top:6px;font-family:sans,sans;font-size:26px;color:{MUT}">{H.escape(s.get("sub", ""))}</div>'
                       f'<div id="{p}r{i}" style="margin-top:24px;height:3px;background:{RED2};transform-origin:left"></div></div>')
        _fade(D, f"{p}s{i}", 0.5 + 0.3 * i)
        D.js.append(f'tl.fromTo("#{p}r{i}",{{scaleX:0}},{{scaleX:1,duration:0.8,ease:"power2.inOut"}},{0.9 + 0.3 * i:.2f});')
    n = [0, 0]
    rid = {}
    last = None
    for b, (t0, d) in zip(sc["beats"], bt):
        for j, it in enumerate(b.get("add", [])):
            si = it["side"]
            k = n[si]
            n[si] += 1
            x, y = X[si], 375 + k * 120
            e = f"{p}i{si}_{k}"
            rid[(si, k)] = e
            D.items.append(
                f'<div id="{e}" style="position:absolute;left:{x}px;top:{y}px;width:778px;height:110px;opacity:0;z-index:2;border-bottom:1px solid #2A2A2E">'
                f'<div id="{e}m" style="position:absolute;left:0;top:6px;width:7px;height:90px;background:{RED2}"></div>'
                f'<div style="position:absolute;left:28px;top:14px;font-family:sans,sans;font-size:22px;color:{MUT}">{H.escape(it.get("tag", ""))}</div>'
                f'<div id="{e}t" style="position:absolute;left:152px;top:2px;font-family:sans-x,sans;font-size:42px;color:{TXT};white-space:nowrap">{H.escape(it.get("title", ""))}</div>'
                f'<div style="position:absolute;left:152px;top:58px;font-family:sans,sans;font-size:26px;color:{MUT};white-space:nowrap">{H.escape(it.get("sub", ""))}</div>'
                f'<div id="{e}x" style="position:absolute;left:146px;top:30px;width:{min(620, 36 * len(it.get("title", "")) + 16)}px;height:3px;background:{RED2};transform-origin:left"></div></div>')
            at = t0 + 0.3 + 0.4 * j
            D.js.append(f'tl.fromTo("#{e}",{{opacity:0,x:-12}},{{opacity:1,x:0,duration:0.6,ease:"power2.out"}},{at:.2f});')
            if last:
                D.js.append(f'tl.to("#{last}m",{{background:"#4A4A50",duration:0.5}},{at:.2f});')
            last = e
        for (si, k) in b.get("strike", []):
            e = rid.get((si, k))
            if e:
                D.js.append(f'tl.fromTo("#{e}x",{{scaleX:0}},{{scaleX:1,duration:0.6,ease:"power2.inOut"}},{t0 + 0.8:.2f});'
                            f'tl.to("#{e}",{{opacity:0.45,duration:0.6}},{t0 + 1.2:.2f});')


def _register_v2():
    from . import hybrid
    orig = hybrid.RENDER["chapter"]

    def chapter(D, sc, bt, dur):   # 장 표지에 "look": "noir" 면 누아르 제목 카드
        if sc.get("look") == "noir":
            return s_noirtitle(D, dict(sc, _chnum="", _chtitle=""), bt, dur)
        return orig(D, sc, bt, dur)
    hybrid.RENDER["chapter"] = chapter
    hybrid.RENDER["noirtitle"] = s_noirtitle
    hybrid.RENDER["noircase"] = s_noircase
    hybrid.RENDER["noirsides"] = s_noirsides
