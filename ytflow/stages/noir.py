"""누아르 사건 보드 장면 (docs/57-osint-sixsigma-benchmark.md §4) — 오신트형 '흩어진 사실을 한 질문으로 잇기'의 구조만.

  1. hubweb   질문 허브 관계망: 가운데 질문 원("누가?" 처럼 그 편의 질문)에서 박자마다 가지(사건·인물)가 하나씩 늘어남. 화면을 갈아 치우지 않고 쌓음.
              지금 말하는 가지만 빨강, 앞 박자 가지는 회색으로 물러남. 위쪽 날짜 눈금(ruler)이 있으면 빨간 표시가 그 날짜로 이동.
  2. ledger   두 열 장부: "끌어내리려는 자 / 다시 올리려는 자"처럼 맞서는 두 편을 왼쪽·오른쪽 열에 한 줄씩 적어 감.
              지금 줄만 빨간 막대, 지운 줄(strike)은 빨간 줄로 긋고 흐리게, 마지막에 판정 한 줄(verdict).

스킨은 무엇이든 되지만 누아르(skins/noir)를 기준으로 만듦 — 장면에 "skin": "noir".

대본 예 (02_script/hybrid.json):
  {"type": "hubweb", "skin": "noir", "title": "누가 움직였나",
   "hub": {"label": "누가?", "sub": "이사회 뒤의 손"},
   "ruler": ["11.10", "11.12", "11.14", "11.17"],
   "nodes": [{"id": "a", "label": "대주주 펀드", "sub": "지분 12%", "date": "11.10", "rel": "지분 매각"},
             {"id": "b", "label": "사외이사 2명", "sub": "동시 사임", "date": "11.12"},
             {"id": "c", "label": "경쟁사 대표", "from": "a", "rel": "같은 날 매수", "date": "11.14"}],
   "beats": [{"say": "...", "add": ["a"]}, {"say": "...", "add": ["b"]}, {"say": "...", "add": ["c"], "hi": "a"},
             {"say": "...", "cut": ["b"]}]}
  {"type": "ledger", "skin": "noir", "title": "두 편",
   "left": {"head": "끌어내리려는 자", "sub": "사임 요구"}, "right": {"head": "다시 올리려는 자", "sub": "복귀 요구"},
   "rows": [{"id": "l1", "side": "l", "name": "이사회", "note": "해임 의결", "date": "11.10"},
            {"id": "r1", "side": "r", "name": "직원 700명", "note": "연판장", "date": "11.12"}],
   "beats": [{"say": "...", "add": ["l1"]}, {"say": "...", "add": ["r1"]},
             {"say": "...", "strike": ["l1"], "verdict": "닷새 만에 뒤집힘"}]}
"""
from __future__ import annotations

import html as H
import math

W, HH = 1920, 1080


def _e(s) -> str:
    return H.escape(str(s))


def _pal(D) -> dict:
    return D.skin.get("palette", {}) or {}


def _c(D, k: str, dflt: str) -> str:
    return _pal(D).get(k) or dflt


def _ease_to(D, sel: str, props: str, t: float, d: float = 0.35):
    D.js.append(f'tl.to("{sel}",{{{props},duration:{d},ease:"power2.out"}},{t:.2f});')


# ---------------------------------------------------------------- 날짜 눈금 (hubweb 의 ruler, 다른 장면에서도 부를 수 있게)
def ruler(D, dates: list, marks: list, y: float = 70, x0: float = 220):
    """화면 위쪽 날짜 눈금. marks: [(시각, 날짜)] — 그 시각에 빨간 표시가 그 날짜로 미끄러져 감."""
    if not dates:
        return
    x1 = W - 220
    xs = {d: (x0 + (x1 - x0) * k / max(1, len(dates) - 1)) if len(dates) > 1 else W / 2 for k, d in enumerate(dates)}
    line, mut = _c(D, "line", "#55534F"), _c(D, "muted_text", "#9C9A96")
    i = D._id()
    D.svg.append(f'<path id="{i}" d="M{x0},{y} L{x1},{y}" stroke="{line}" stroke-width="2" fill="none" pathLength="1" '
                 f'stroke-dasharray="1" stroke-dashoffset="1"/>')
    D.js.append(f'tl.to("#{i}",{{strokeDashoffset:0,duration:.6,ease:"power2.out"}},0.05);')
    for d, x in xs.items():
        j = D._id()
        D.items.append(f'<div id="{j}" style="position:absolute;left:{x - 60:.0f}px;top:{y + 14:.0f}px;width:120px;text-align:center;'
                       f'font-family:sans;font-size:22px;letter-spacing:1px;color:{mut};opacity:0">'
                       f'<div style="width:2px;height:14px;background:{line};margin:-14px auto 6px"></div>{_e(d)}</div>')
        D.js.append(f'tl.to("#{j}",{{opacity:1,duration:.3}},0.25);')
    m = D._id()
    first = next((xs[d] for _, d in marks if d in xs), x0)
    D.items.append(f'<div id="{m}" style="position:absolute;left:{first - 9:.0f}px;top:{y - 9:.0f}px;width:18px;height:18px;'
                   f'border-radius:50%;background:{D.red};box-shadow:0 0 0 6px rgba(214,38,46,.22);opacity:0"></div>')
    shown = False
    for t, d in marks:
        if d not in xs:
            continue
        if not shown:
            D.js.append(f'tl.fromTo("#{m}",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:.35,ease:"power3.in"}},{t:.2f});')
            shown = True
        else:
            _ease_to(D, f"#{m}", f"left:{xs[d] - 9:.0f}", t, 0.55)


# ---------------------------------------------------------------- 1. hubweb
HUB = (W / 2, 640, 118)


def _layout(nodes: list) -> dict:
    """가운데 원 둘레에 1차 가지(타원), 2차 가지는 부모 바깥쪽으로. 직접 준 x·y 가 있으면 그것."""
    hx, hy, _ = HUB
    first = [n for n in nodes if n.get("from", "hub") == "hub"]
    pos = {}
    k = len(first)
    # 위쪽 날짜 눈금·제목을 피해 왼쪽 위에서 시작해 시계 방향으로
    for j, n in enumerate(first):
        a = math.radians(-150) + (math.radians(300) * j / (k - 1) if k > 1 else math.radians(60))
        pos[n["id"]] = (hx + 560 * math.cos(a), hy + 280 * math.sin(a), a)
    # 2차 가지: 부모 둘레 후보 자리 중 화면 안·다른 상자와 안 겹치고·가운데에서 가장 먼 곳 (겹치면 읽히지 않음)
    taken = [(x, y) for x, y, _a in pos.values()] + [(hx, hy)]
    for n in nodes:
        p = n.get("from", "hub")
        if p == "hub" or p not in pos:
            continue
        px, py, a = pos[p]
        best = None
        for dx, dy in ((430, 0), (-430, 0), (0, -175), (0, 175), (400, -170), (-400, -170), (400, 170), (-400, 170)):
            x, y = px + dx, py + dy
            if not (210 <= x <= W - 210 and 300 <= y <= HH - 110):
                continue
            if any(abs(x - qx) < 400 and abs(y - qy) < 150 for qx, qy in taken):
                continue
            if abs(x - hx) < 400 and abs(y - hy) < 200:   # 가운데 질문 원 둘레는 비워 둠
                continue
            score = math.hypot(x - hx, y - hy)
            if best is None or score > best[0]:
                best = (score, x, y)
        x, y = (best[1], best[2]) if best else (px, py + 175)
        pos[n["id"]] = (x, y, a)
        taken.append((x, y))
    out = {}
    for n in nodes:
        x, y, _a = pos.get(n["id"], (hx, hy, 0))
        x, y = n.get("x", x), n.get("y", y)
        out[n["id"]] = (min(W - 200, max(200, x)), min(HH - 110, max(300, y)))
    return out


def _edge_pts(a: tuple, b: tuple, ra: float, rb: tuple) -> tuple:
    """a 중심(반지름 ra 원 또는 rb 상자)에서 b 상자 가장자리까지의 직선."""
    (ax, ay), (bx, by) = a, b
    dx, dy = bx - ax, by - ay
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    sx, sy = ax + ux * ra, ay + uy * ra
    hw, hh = rb
    s = min(hw / abs(ux) if ux else 1e9, hh / abs(uy) if uy else 1e9)
    return (sx, sy), (bx - ux * s, by - uy * s)


def s_hubweb(D, sc: dict, bt: list, dur: float):
    from .hybrid import FT, fit
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    ink, mut, line, card = _c(D, "ink", "#E9E5DC"), _c(D, "muted_text", "#9C9A96"), _c(D, "line", "#55534F"), _c(D, "card", "#18181B")
    red = D.red
    nodes = sc.get("nodes", [])[:8]
    N = {n["id"]: n for n in nodes}
    P = _layout(nodes)
    hx, hy, hr = HUB
    if sc.get("title"):
        D.text(160, 158 if sc.get("ruler") else 120, sc["title"], FT("title"), 40, mut, at=0.1, anchor="lm")
    # 가운데 질문 원
    hub = sc.get("hub") or {"label": "?"}
    i = D._id()
    D.items.append(f'<div id="{i}" style="position:absolute;left:{hx - hr:.0f}px;top:{hy - hr:.0f}px;width:{2 * hr}px;height:{2 * hr}px;'
                   f'border-radius:50%;border:4px solid {red};background:{card};opacity:0;display:flex;flex-direction:column;'
                   f'align-items:center;justify-content:center">'
                   f'<div style="font-family:serif-b;font-size:{fit(FT("value"), hub.get("label", ""), 52, 2 * hr - 30).size}px;color:{ink}">{_e(hub.get("label", ""))}</div>'
                   + (f'<div style="font-family:sans;font-size:22px;color:{mut};margin-top:6px">{_e(hub["sub"])}</div>' if hub.get("sub") else "")
                   + '</div>')
    t0 = bt[0][0]
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:.5,ease:"power3.out"}},{t0 + 0.1:.2f});')
    D.js.append(f'tl.to("#{i}",{{boxShadow:"0 0 0 14px rgba(214,38,46,.10)",duration:1.6,yoyo:true,repeat:{max(1, int(dur / 1.6))},ease:"sine.inOut"}},{t0 + 0.6:.2f});')
    D.sfx.append(("pop", t0 + 0.15))
    BOX = (190, 62)   # 상자 반폭·반높이
    ids: dict = {}
    live: list = []    # 지금 빨강인 것 (다음 박자에 회색으로)
    marks = []

    def node_html(n, x, y):
        k = D._id()
        f = fit(FT("title"), n.get("label", ""), 34, 2 * BOX[0] - 36)
        date = (f'<div style="position:absolute;left:14px;top:-30px;font-family:sans;font-size:20px;letter-spacing:1px;color:{mut}">{_e(n["date"])}</div>'
                if n.get("date") else "")
        sub = (f'<div style="font-family:sans;font-size:22px;color:{mut};margin-top:4px">{_e(n["sub"])}</div>' if n.get("sub") else "")
        D.items.append(f'<div id="{k}" style="position:absolute;left:{x - BOX[0]:.0f}px;top:{y - BOX[1]:.0f}px;width:{2 * BOX[0]}px;height:{2 * BOX[1]}px;'
                       f'box-sizing:border-box;border:3px solid {red};background:{card};opacity:0;display:flex;flex-direction:column;'
                       f'align-items:center;justify-content:center;box-shadow:0 14px 30px rgba(0,0,0,.45)">{date}'
                       f'<div id="{k}t" style="font-family:sans-x;font-size:{f.size}px;color:{ink}">{_e(n.get("label", ""))}</div>{sub}</div>')
        return k

    for b, (tb, d) in zip(sc["beats"], bt):
        # 앞 박자의 빨강 → 회색
        for kind, el in live:
            if kind == "box":
                _ease_to(D, f"#{el}", f'borderColor:"{line}"', tb + 0.05)
            else:
                _ease_to(D, f"#{el}", f'stroke:"{line}"', tb + 0.05)
        live = []
        for j, nid in enumerate(b.get("add", [])):
            if nid not in N or nid in ids:
                continue
            n = N[nid]
            ta = tb + 0.2 + 0.55 * j
            x, y = P[nid]
            par = n.get("from", "hub")
            if par == "hub":
                (sx, sy), (ex, ey) = _edge_pts((hx, hy), (x, y), hr, BOX)
            else:
                px, py = P.get(par, (hx, hy))
                _, (sx, sy) = _edge_pts((x, y), (px, py), 0, BOX)   # 부모 상자 가장자리에서
                _, (ex, ey) = _edge_pts((px, py), (x, y), 0, BOX)   # 자식 상자 가장자리까지
            e = D._id()
            D.svg.append(f'<path id="{e}" d="M{sx:.0f},{sy:.0f} L{ex:.0f},{ey:.0f}" stroke="{red}" stroke-width="4" fill="none" '
                         f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
            D.js.append(f'tl.to("#{e}",{{strokeDashoffset:0,duration:.45,ease:"power2.inOut"}},{ta:.2f});')
            if n.get("rel"):
                r = D._id()
                mx, my = (sx + ex) / 2, (sy + ey) / 2
                D.items.append(f'<div id="{r}" style="position:absolute;left:{mx:.0f}px;top:{my:.0f}px;transform:translate(-50%,-50%);'
                               f'padding:4px 12px;background:{_c(D, "base", "#0E0E10")};font-family:sans;font-size:22px;color:{ink};'
                               f'white-space:nowrap;opacity:0">{_e(n["rel"])}</div>')
                D.js.append(f'tl.to("#{r}",{{opacity:1,duration:.3}},{ta + 0.35:.2f});')
            k = node_html(n, x, y)
            D.js.append(f'tl.fromTo("#{k}",{{opacity:0,scale:.85}},{{opacity:1,scale:1,duration:.35,ease:"back.out(1.6)"}},{ta + 0.35:.2f});')
            D.sfx.append(("pop", ta + 0.4))
            ids[nid] = (k, e)
            live += [("box", k), ("edge", e)]
            if n.get("date"):
                marks.append((ta + 0.3, n["date"]))
        if b.get("date"):
            marks.append((tb + 0.2, b["date"]))
        hi = b.get("hi")
        for nid in ([hi] if isinstance(hi, str) else (hi or [])):
            if nid in ids:
                k, e = ids[nid]
                _ease_to(D, f"#{k}", f'borderColor:"{red}"', tb + 0.3)
                _ease_to(D, f"#{e}", f'stroke:"{red}"', tb + 0.3)
                D.js.append(f'tl.fromTo("#{k}",{{scale:1}},{{scale:1.08,duration:.25,yoyo:true,repeat:1}},{tb + 0.35:.2f});')
                live += [("box", k), ("edge", e)]
        for j, nid in enumerate(b.get("cut", [])):
            if nid in ids:
                k, e = ids[nid]
                tc = tb + 0.4 + 0.3 * j
                x, y = P[nid]
                s = D._id()
                D.items.append(f'<div id="{s}" style="position:absolute;left:{x - BOX[0] - 14:.0f}px;top:{y - 3:.0f}px;width:{2 * BOX[0] + 28}px;'
                               f'height:6px;background:{red};transform-origin:left center;transform:scaleX(0) rotate(-6deg)"></div>')
                D.js.append(f'tl.to("#{s}",{{scaleX:1,duration:.3,ease:"power3.in"}},{tc:.2f});')
                _ease_to(D, f"#{k}", "opacity:.38", tc + 0.3)
                _ease_to(D, f"#{e}", "opacity:.25", tc + 0.3)
                D.sfx.append(("pop", tc + 0.3))
    if sc.get("ruler"):
        ruler(D, sc["ruler"], sorted(marks), x0=640 if sc.get("_chnum") else 220)   # 왼쪽 위 장 꼬리표를 비켜서
    # 천천히 다가가는 카메라 (쌓이는 화면이 정지해 보이지 않게)
    D.js.append(f'tl.fromTo("#root",{{scale:1}},{{scale:1.035,duration:{max(1.0, dur):.2f},ease:"none"}},0);')


# ---------------------------------------------------------------- 2. ledger
def s_ledger(D, sc: dict, bt: list, dur: float):
    from .hybrid import FT, fit
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    ink, mut, line = _c(D, "ink", "#E9E5DC"), _c(D, "muted_text", "#9C9A96"), _c(D, "line", "#55534F")
    red = D.red
    t0 = bt[0][0]
    top = 170
    if sc.get("title"):
        D.text(W / 2, 110, sc["title"], FT("title"), 40, mut, at=0.1)
        top = 200
    cols = {"l": (130, 900), "r": (1020, 1790)}
    for side, key in (("l", "left"), ("r", "right")):
        x0, x1 = cols[side]
        hd = sc.get(key) or {}
        f = fit(FT("title"), hd.get("head", ""), 54, x1 - x0)
        D.text(x0, top + 40, hd.get("head", ""), FT("title"), f.size, ink, at=t0 + 0.1 + (0.3 if side == "r" else 0), anchor="lm")
        if hd.get("sub"):
            D.text(x0, top + 100, hd["sub"], FT("label"), 26, mut, at=t0 + 0.3 + (0.3 if side == "r" else 0), anchor="lm")
        u = D._id()
        D.svg.append(f'<path id="{u}" d="M{x0},{top + 140} L{x1},{top + 140}" stroke="{red}" stroke-width="4" fill="none" '
                     f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
        D.js.append(f'tl.to("#{u}",{{strokeDashoffset:0,duration:.5,ease:"power2.out"}},{t0 + 0.35 + (0.3 if side == "r" else 0):.2f});')
    v = D._id()
    D.svg.append(f'<path id="{v}" d="M{W / 2:.0f},{top + 10} L{W / 2:.0f},{HH - 150}" stroke="{line}" stroke-width="2" fill="none" '
                 f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
    D.js.append(f'tl.to("#{v}",{{strokeDashoffset:0,duration:.7,ease:"power2.out"}},{t0 + 0.2:.2f});')
    D.sfx.append(("pencil", t0 + 0.3))
    rows = {r["id"]: r for r in sc.get("rows", [])}
    count = {"l": 0, "r": 0}
    ids: dict = {}
    live: list = []
    RH = 118
    for b, (tb, d) in zip(sc["beats"], bt):
        for el in live:
            _ease_to(D, f"#{el}b", f'background:"{line}"', tb + 0.05)
        live = []
        for j, rid in enumerate(b.get("add", [])):
            if rid not in rows or rid in ids:
                continue
            r = rows[rid]
            side = "r" if str(r.get("side", "l")).startswith("r") else "l"
            if count[side] >= 5:
                continue
            x0, x1 = cols[side]
            y = top + 175 + count[side] * RH
            count[side] += 1
            ta = tb + 0.2 + 0.45 * j
            k = D._id()
            fn = fit(FT("title"), r.get("name", ""), 40, x1 - x0 - 190)
            date = (f'<div style="position:absolute;left:28px;top:12px;font-family:sans;font-size:22px;letter-spacing:1px;color:{mut}">{_e(r["date"])}</div>'
                    if r.get("date") else "")
            D.items.append(f'<div id="{k}" style="position:absolute;left:{x0}px;top:{y}px;width:{x1 - x0}px;height:{RH - 18}px;opacity:0">'
                           f'<div id="{k}b" style="position:absolute;left:0;top:6px;width:8px;height:{RH - 30}px;background:{red}"></div>{date}'
                           f'<div style="position:absolute;left:{150 if r.get("date") else 28}px;top:2px;font-family:sans-x;font-size:{fn.size}px;color:{ink};white-space:nowrap">{_e(r.get("name", ""))}</div>'
                           f'<div style="position:absolute;left:{150 if r.get("date") else 28}px;top:{fn.size + 14}px;font-family:sans;font-size:25px;color:{mut};white-space:nowrap">{_e(r.get("note", ""))}</div>'
                           f'<div style="position:absolute;left:0;right:0;bottom:0;height:1px;background:{_c(D, "line2", "#3D3C39")}"></div></div>')
            D.js.append(f'tl.fromTo("#{k}",{{opacity:0,x:{-30 if side == "l" else 30}}},{{opacity:1,x:0,duration:.4,ease:"power3.out"}},{ta:.2f});')
            D.sfx.append(("pop", ta + 0.05))
            ids[rid] = (k, x1 - x0, y)
            live.append(k)
        for nid in ([b["hi"]] if isinstance(b.get("hi"), str) else (b.get("hi") or [])):
            if nid in ids:
                k = ids[nid][0]
                _ease_to(D, f"#{k}b", f'background:"{red}"', tb + 0.3)
                D.js.append(f'tl.fromTo("#{k}",{{x:0}},{{x:12,duration:.18,yoyo:true,repeat:1}},{tb + 0.3:.2f});')
                live.append(k)
        for j, rid in enumerate(b.get("strike", [])):
            if rid in ids:
                k, w, y = ids[rid]
                tc = tb + 0.4 + 0.3 * j
                s = D._id()
                x0 = cols["r" if str(rows[rid].get("side", "l")).startswith("r") else "l"][0]
                D.items.append(f'<div id="{s}l" style="position:absolute;left:{x0 + 20}px;top:{y + 44}px;width:{w - 40}px;height:5px;background:{red};'
                               f'transform-origin:left center;transform:scaleX(0)"></div>')
                D.js.append(f'tl.to("#{s}l",{{scaleX:1,duration:.32,ease:"power3.in"}},{tc:.2f});')
                _ease_to(D, f"#{k}", "opacity:.4", tc + 0.3)
                D.sfx.append(("pop", tc + 0.3))
        if b.get("verdict"):
            vv = D._id()
            f = fit(FT("value"), b["verdict"], 56, W - 400)
            D.items.append(f'<div id="{vv}" style="position:absolute;left:0;right:0;top:{HH - 128}px;text-align:center;opacity:0">'
                           f'<span style="font-family:serif-b;font-size:{f.size}px;color:{ink};border-bottom:5px solid {red};padding:0 10px 6px">'
                           f'{_e(b["verdict"])}</span></div>')
            D.js.append(f'tl.fromTo("#{vv}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.5,ease:"power2.out"}},{tb + 0.4:.2f});')
            D.sfx.append(("pop", tb + 0.45))


# ---------------------------------------------------------------- 3. 누아르 장 표지 (스킨이 noir 이고 look 을 따로 안 정했을 때)
def s_chapter_noir(D, sc: dict, bt: list, dur: float):
    """빨간 전면 대신: 검은 바탕 + 작은 빨간 줄(날짜·번호 kicker) + 큰 회백색 명조 제목 + 짧은 빨간 선 (빨강은 한 곳만)."""
    from .hybrid import FT, fit
    ink, mut = _c(D, "ink", "#E9E5DC"), _c(D, "muted_text", "#9C9A96")
    kick = sc.get("kicker") or sc.get("date") or (f"{sc['num']}" if sc.get("num") else "")
    if kick:
        k = D._id()
        D.items.append(f'<div id="{k}" style="position:absolute;left:0;right:0;top:390px;text-align:center;font-family:sans-x;font-size:34px;'
                       f'letter-spacing:6px;color:{D.red};opacity:0">{_e(kick)}</div>')
        D.js.append(f'tl.fromTo("#{k}",{{opacity:0,letterSpacing:"18px"}},{{opacity:1,letterSpacing:"6px",duration:.7,ease:"power2.out"}},0.15);')
    f = fit(FT("value"), sc.get("title", ""), 104, W - 320)
    D.text(W / 2, 540, sc.get("title", ""), FT("value"), f.size, ink, at=0.45, dur=0.7)
    w = min(f.getlength(sc.get("title", "")), W - 320)
    u = D._id()
    D.svg.append(f'<path id="{u}" d="M{W / 2 - w / 4:.0f},630 L{W / 2 + w / 4:.0f},630" stroke="{D.red}" stroke-width="5" fill="none" '
                 f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
    D.js.append(f'tl.to("#{u}",{{strokeDashoffset:0,duration:.5,ease:"power2.out"}},1.0);')
    if sc.get("sub"):
        D.text(W / 2, 700, sc["sub"], FT("label"), 30, mut, at=1.2)
    D.js.append(f'tl.fromTo("#root",{{scale:1.04}},{{scale:1,duration:{max(1.0, dur):.2f},ease:"power1.out"}},0);')
    D.sfx.append(("whoosh", 0.1))


# ---------------------------------------------------------------- 등록
def register():
    from . import hybrid
    hybrid.RENDER["hubweb"] = s_hubweb
    hybrid.RENDER["ledger"] = s_ledger
    orig = hybrid.RENDER["chapter"]

    def chapter(D, sc, bt, dur):
        if sc.get("look") == "noir" or (D.skin.get("id") == "noir" and not sc.get("look")):
            return s_chapter_noir(D, sc, bt, dur)
        return orig(D, sc, bt, dur)
    hybrid.RENDER["chapter"] = chapter
