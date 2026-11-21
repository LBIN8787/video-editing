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
