"""문장을 연기하는 설명 장면 두 가지 — 설명 다큐 문법(docs/68 E1~E8)으로 다시 만든 시범.

`pricewalk` — 주가 선이 주인공(E2). 말하는 날짜·값에 점·괄호·기준선이 붙는다(E4). 상징 그림 없음(E1).
  do: {"line": "2026-11-20", "t": "계산해"}            처음부터 그 날짜까지 선을 그림 (회색)
      {"seg": ["2026-11-20","2026-11-23"], "tone": "up|down", "label": "...", "t": "165.05"}  구간을 색으로 덧그림
      {"dot": "2026-11-20", "label": "11/20(금) 125.53", "side": "below|above|left", "t": "금요일"}
      {"bracket": [125.53, 165.05], "label": "+39.52달러", "sub": "+31.5%", "tone": "up|down", "t": "39"}
      {"level": "2026-11-11", "label": "...", "t": "직전"}   그 날 값의 점선 기준선 (오른쪽 끝까지)
      {"calc": "39.52달러 × 241.86억 주", "value": "≈ 9,560억 달러", "t": "곱하면"}  {"calcval": true, "t": "9,560억"}
      {"note": "...", "t": "..."}  {"clear": "calc", "t": "..."}  {"addline": "...", "to": "level:2026-11-11", "t": "95"}

`standoff` — 회사마다 '감산' 손잡이(E6: '먼저 줄인다'를 손잡이를 당기는 동작으로). 점유율 막대·고객 점이 실제로 옮겨 간다.
  do: {"lean": "a"} 손잡이를 반쯤, {"pull": ["a"]} 당김, {"reset": true}, {"flow": "a", "to": ["b","c"]} 고객 점 이동,
      {"invest": ["b","c"]} 동전 → 다음 공장, {"wait": true} 셋 다 손을 올린 채 떨림·시계,
      {"chicken": "치킨 게임"} 마주 달리는 두 차, {"together": true} 함께 당김·묶는 선, {"stamp": "담합"},
      {"fine": "삼성전자", "value": 3.0, "text": "3억 달러"} 같은 축척 막대, {"total": 7.3, "text": "7억 3,000만 달러 넘음"}
"""
from __future__ import annotations

import html as H
from datetime import date

from .docu import _when

CREAM, MUTED, GOLD, UP, DOWN, LINE = "#EDE6D6", "#9AA6AE", "#F0BE5A", "#4FCB86", "#F06A5A", "#C9D0D5"


def _title(D, sc):
    if sc.get("title"):
        tid = D._id()
        D.items.append(f'<div id="{tid}" style="position:absolute;left:150px;top:86px;font-family:heavy;font-size:44px;color:#E9EEF0;opacity:0">'
                       f'{H.escape(sc["title"])}</div>')
        D.js.append(f'tl.fromTo("#{tid}",{{opacity:0,x:-18}},{{opacity:1,x:0,duration:.45}},0.15);')


def _txt(D, x, y, s, size=30, color=CREAM, font="sans-x", anchor="l", extra=""):
    i = D._id()
    tr = {"l": "", "r": "transform:translateX(-100%);", "c": "transform:translateX(-50%);"}[anchor]
    D.items.append(f'<div id="{i}" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;{tr}font-family:{font};font-size:{size}px;'
                   f'color:{color};white-space:nowrap;opacity:0;{extra}">{s}</div>')
    return i


def _show(D, i, t, dy=10):
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:.4,ease:"power2.out"}},{t:.2f});')


# ── pricewalk ────────────────────────────────────────────────────────────────
def s_pricewalk(D, sc: dict, bt: list, dur: float):
    from . import explain, marketdata
    sc = dict(sc)
    sc.setdefault("theme", "dark")
    explain._setup(D, sc, title=False)
    _title(D, sc)
    rows = marketdata.fetch(sc["ticker"], sc.get("period", "3mo"), sc["_prices"])
    rows = [r for r in rows if sc.get("from", "") <= r["date"] <= sc.get("to", "9999")]
    x0, x1, y0, y1 = 230, 1490, 300, 860
    lo, hi = sc.get("lo", min(r["close"] for r in rows) * 0.85), sc.get("hi", max(r["close"] for r in rows) * 1.04)
    idx = {r["date"]: i for i, r in enumerate(rows)}
    X = lambda i: x0 + (x1 - x0) * i / (len(rows) - 1)
    Y = lambda v: y1 - (y1 - y0) * (v - lo) / (hi - lo)
    P = lambda d: (X(idx[d]), Y(rows[idx[d]]["close"]))
    # 눈금 (왼쪽) · 날짜 (아래)
    for k in range(5):
        v = lo + (hi - lo) * k / 4
        D.svg.append(f'<line x1="{x0}" y1="{Y(v):.0f}" x2="{x1}" y2="{Y(v):.0f}" stroke="#3A434A" stroke-width="1"/>')
        D.items.append(f'<div style="position:absolute;left:{x0 - 20}px;top:{Y(v) - 15:.0f}px;transform:translateX(-100%);font-family:sans;font-size:24px;color:#7C8590">{v:,.0f}</div>')
    for r in rows:
        dd = date.fromisoformat(r["date"])
        if dd.day <= 3 and (idx[r["date"]] == 0 or date.fromisoformat(rows[idx[r["date"]] - 1]["date"]).month != dd.month):
            D.items.append(f'<div style="position:absolute;left:{X(idx[r["date"]]):.0f}px;top:{y1 + 16}px;font-family:sans;font-size:24px;color:#7C8590">{dd.month}월</div>')

    def path(a, b):
        ia, ib = idx[a], idx[b]
        return " ".join(f'{"M" if j == ia else "L"}{X(j):.1f},{Y(rows[j]["close"]):.1f}' for j in range(ia, ib + 1))

    def draw(a, b, color, width, t, d):
        i = D._id()
        D.svg.append(f'<path id="{i}" d="{path(a, b)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
                     f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
        D.js.append(f'tl.to("#{i}",{{strokeDashoffset:0,duration:{d},ease:"power1.inOut"}},{t:.2f});')
        return i

    groups: dict[str, list[str]] = {}
    for k, (b, (t0, d)) in enumerate(zip(sc.get("beats", []), bt)):
        seq = t0 + 0.2
        for act in b.get("do") or []:
            t = _when(sc, k, b, t0, d, act.get("t"), seq)
            seq = max(seq, t) + 0.6
            g = groups.setdefault(act.get("group", "_"), [])
            if "line" in act:
                draw(rows[0]["date"], act["line"], LINE, 4, t, act.get("dur", 2.0))
                D.sfx.append(("pencil", t))
            if "seg" in act:
                a, z = act["seg"]
                col = UP if act.get("tone") == "up" else DOWN
                g.append(draw(a, z, col, 9, t, 0.7))
                if act.get("label"):
                    mx, my = P(a)[0] * .5 + P(z)[0] * .5, min(P(a)[1], P(z)[1])
                    i = _txt(D, mx, my - 70, H.escape(act["label"]), 30, col, anchor="c")
                    g.append(i); _show(D, i, t + 0.4)
            if "dot" in act:
                x, y = P(act["dot"])
                i = D._id()
                D.items.append(f'<div id="{i}" style="position:absolute;left:{x - 11:.0f}px;top:{y - 11:.0f}px;width:22px;height:22px;border-radius:50%;'
                               f'background:{act.get("color", GOLD)};box-shadow:0 0 0 6px rgba(240,190,90,.18);transform:scale(0)"></div>')
                D.js.append(f'tl.to("#{i}",{{scale:1,duration:.35,ease:"back.out(2.4)"}},{t:.2f});')
                side = act.get("side", "above")
                lx, ly, an = {"above": (x, y - 78, "c"), "below": (x, y + 26, "c"), "left": (x - 26, y - 22, "r"),
                              "right": (x + 26, y - 22, "l")}[side]
                lab = H.escape(act.get("label", ""))
                if "|" in lab:
                    a1, a2 = lab.split("|", 1)
                    lab = f'<span style="font-family:sans-x;font-size:24px;color:{MUTED}">{a1}</span><br><span style="font-family:heavy;font-size:40px;color:{CREAM}">{a2}</span>'
                j = _txt(D, lx, ly, lab, 30, CREAM, anchor=an, extra="text-align:center;line-height:1.15")
                _show(D, j, t + 0.15)
                g += [i, j]
                D.sfx.append(("pop", t))
            if "level" in act:
                x, y = P(act["level"])
                i = D._id()
                D.svg.append(f'<line id="{i}" x1="{x:.0f}" y1="{y:.0f}" x2="{x1 + 40}" y2="{y:.0f}" stroke="{act.get("color", MUTED)}" '
                             f'stroke-width="2.5" stroke-dasharray="10 9" opacity="0"/>')
                D.js.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:.9,duration:.5}},{t:.2f});')
                j = _txt(D, x1 + 60, y - 20, H.escape(act.get("label", "")), 28, act.get("color", MUTED))
                _show(D, j, t + 0.2, 0)
                groups[f'level:{act["level"]}'] = [j]
                g += [i, j]
            if "addline" in act:
                host = groups.get(act.get("to", ""), [None])[0]
                if host:
                    i = D._id()
                    D.items.append(f'<div id="{i}" style="opacity:0;font-family:heavy;font-size:34px;color:{GOLD};margin-top:4px">{H.escape(act["addline"])}</div>')
                    D.js.append(f'(function(){{var h=document.getElementById("{host}"),c=document.getElementById("{i}");if(h&&c)h.appendChild(c);}})();')
                    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:8}},{{opacity:1,y:0,duration:.4}},{t:.2f});')
            if "bracket" in act:
                va, vb = act["bracket"]
                ya, yb = Y(va), Y(vb)
                bx = x1 + 34
                col = UP if act.get("tone") == "up" else DOWN
                i = D._id()
                D.svg.append(f'<path id="{i}" d="M{bx - 14},{ya:.0f} L{bx},{ya:.0f} L{bx},{yb:.0f} L{bx - 14},{yb:.0f}" fill="none" stroke="{col}" '
                             f'stroke-width="5" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
                D.js.append(f'tl.to("#{i}",{{strokeDashoffset:0,duration:.6,ease:"power2.out"}},{t:.2f});')
                band = D._id()   # 그 폭만큼 칠해 '늘어난 값'이 크기로 보이게
                D.svg.append(f'<rect id="{band}" x="{x0}" y="{min(ya, yb):.0f}" width="{x1 - x0}" height="{abs(ya - yb):.0f}" fill="{col}" opacity="0"/>')
                D.js.append(f'tl.to("#{band}",{{opacity:.10,duration:.6}},{t + 0.2:.2f});')
                lab = f'<span style="font-family:heavy;font-size:46px;color:{col}">{H.escape(act.get("label", ""))}</span>'
                if act.get("sub"):
                    lab += f'<br><span style="font-family:sans-x;font-size:26px;color:{MUTED}">{H.escape(act["sub"])}</span>'
                j = _txt(D, bx + 26, (ya + yb) / 2 - 36, lab, 30, col, extra="line-height:1.15")
                _show(D, j, t + 0.3, 0)
                g += [i, band, j]
                D.sfx.append(("click-soft", t))
            if "calc" in act:
                i = D._id()
                D.items.append(f'<div id="{i}" style="position:absolute;left:270px;top:{act.get("y", 640)}px;width:640px;padding:22px 28px;border-radius:12px;'
                               f'background:rgba(10,12,13,.72);border:1px solid #3A434A;opacity:0">'
                               f'<div style="font-family:sans-x;font-size:30px;color:{LINE}">{H.escape(act["calc"])}</div>'
                               f'<div id="{i}v" style="font-family:heavy;font-size:60px;color:{GOLD};margin-top:8px;opacity:0">{H.escape(act.get("value", ""))}</div>'
                               f'<div id="{i}n" style="font-family:sans-x;font-size:26px;color:{MUTED};margin-top:6px;opacity:0">{H.escape(act.get("tag", ""))}</div></div>')
                _show(D, i, t)
                groups["calc"] = [i]
                D.sfx.append(("pop", t))
            if act.get("calcval") and groups.get("calc"):
                D.js.append(f'tl.fromTo("#{groups["calc"][0]}v",{{opacity:0,scale:.9}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2)"}},{t:.2f});')
                D.sfx.append(("pop", t))
            if act.get("calctag") and groups.get("calc"):
                D.js.append(f'tl.to("#{groups["calc"][0]}n",{{opacity:1,duration:.4}},{t:.2f});')
            if "clear" in act:
                for e in groups.pop(act["clear"], []):
                    D.js.append(f'tl.to("#{e}",{{opacity:0,duration:.35}},{t:.2f});')
            if "dim" in act:
                for e in groups.get(act["dim"], []):
                    D.js.append(f'tl.to("#{e}",{{opacity:.25,duration:.4}},{t:.2f});')
            if "pre" in act:   # 종가가 아닌 장 전 거래 값: 점선 + 속이 빈 점 (종가 선과 구별)
                xa, ya = P(act["from"])
                xb, yb2 = X(idx[act["pre"]]), Y(act["value"])
                i = D._id()
                D.svg.append(f'<path id="{i}" d="M{xa:.1f},{ya:.1f} L{xb:.1f},{yb2:.1f}" fill="none" stroke="{UP}" stroke-width="5" stroke-dasharray="10 9" opacity="0"/>')
                D.js.append(f'tl.to("#{i}",{{opacity:1,duration:.5}},{t:.2f});')
                j = D._id()
                D.items.append(f'<div id="{j}" style="position:absolute;left:{xb - 13:.0f}px;top:{yb2 - 13:.0f}px;width:26px;height:26px;border-radius:50%;border:4px solid {UP};background:#14181B;transform:scale(0)"></div>')
                D.js.append(f'tl.to("#{j}",{{scale:1,duration:.35,ease:"back.out(2.4)"}},{t + .3:.2f});')
                k2 = _txt(D, act.get("lx", xb - 26), act.get("ly", yb2 - 74), H.escape(act.get("label", "")), 28, UP, font="heavy", anchor=act.get("anchor", "r"))
                _show(D, k2, t + .4)
                g += [i, j, k2]
            if "note" in act:
                i = _txt(D, act.get("x", 1860), act.get("y", 250), H.escape(act["note"]), 28, MUTED, anchor="r")
                _show(D, i, t, 0)
                g.append(i)


# ── standoff ─────────────────────────────────────────────────────────────────
def _lever(D, cx, y, cid):
    """'감산' 손잡이: 받침 + 막대(위가 기본, 당기면 아래로 눕는다) + 손."""
    return (f'<div style="position:absolute;left:{cx - 70}px;top:{y}px;width:140px;height:150px">'
            f'<div style="position:absolute;left:30px;bottom:0;width:80px;height:34px;border-radius:8px;background:#2B3238;border:2px solid #4A535A"></div>'
            f'<div id="{cid}L" style="position:absolute;left:64px;bottom:26px;width:12px;height:110px;border-radius:6px;background:#9AA6AE;'
            f'transform-origin:50% 100%;transform:rotate(-28deg)">'
            f'<div style="position:absolute;left:-14px;top:-26px;width:40px;height:40px;border-radius:50%;background:{DOWN}"></div></div>'
            f'<div style="position:absolute;left:0;right:0;bottom:-38px;text-align:center;font-family:sans-x;font-size:24px;color:{MUTED}">감산</div></div>')


def s_standoff(D, sc: dict, bt: list, dur: float):
    from . import explain
    sc = dict(sc)
    sc.setdefault("theme", "dark")
    explain._setup(D, sc, title=False)
    _title(D, sc)
    cos = sc["companies"]            # {"a": {"label":..., "x":...}, ...}
    keys = list(cos)
    share_w = 1200
    # 점유율 막대 (위) — 회사마다 같은 몫에서 시작
    bx0, by = 360, 210
    seg = {}
    for j, k in enumerate(keys):
        i = D._id()
        w = share_w / len(keys)
        col = ["#5C7FA6", "#7A8F6B", "#9B7A55"][j % 3]
        D.items.append(f'<div id="{i}" style="position:absolute;left:{bx0 + j * w:.0f}px;top:{by}px;width:{w - 4:.0f}px;height:44px;background:{col};'
                       f'border-radius:6px;opacity:0;display:flex;align-items:center;justify-content:center;font-family:sans-x;font-size:22px;color:#F2F2F2;overflow:hidden">{H.escape(cos[k]["label"])}</div>')
        seg[k] = (i, col)
    cap = _txt(D, bx0, by - 40, "점유율", 24, MUTED)
    # 회사 + 손잡이 + 고객 점
    yc = 470
    for k in keys:
        c = cos[k]
        D.items.append(f'<div id="co{k}" style="position:absolute;left:{c["x"] - 130}px;top:{yc}px;width:260px;padding:16px 0;border-radius:12px;'
                       f'background:linear-gradient(180deg,#232A30,#161B1F);border:1px solid #3A434A;text-align:center;opacity:0">'
                       f'<div style="font-family:heavy;font-size:36px;color:{CREAM}">{H.escape(c["label"])}</div>'
                       f'<div style="font-family:sans-x;font-size:22px;color:{MUTED}">{H.escape(c.get("role", ""))}</div></div>')
        D.items.append(f'<div id="lv{k}" style="opacity:0">{_lever(D, c["x"], yc + 120, "lv" + k)}</div>')
        D.items.append(f'<div id="th{k}" style="position:absolute;left:{c["x"]}px;top:{yc - 64}px;transform:translateX(-50%);padding:8px 18px;border-radius:24px;'
                       f'background:{CREAM};color:#1A1D20;font-family:sans-x;font-size:26px;white-space:nowrap;opacity:0">{H.escape(c.get("think", ""))}</div>')
        for m in range(4):   # 고객 점
            D.items.append(f'<div id="cu{k}{m}" style="position:absolute;left:{c["x"] - 66 + m * 40}px;top:{yc + 330}px;width:24px;height:24px;border-radius:50%;'
                           f'background:#6FA8DC;opacity:0"></div>')
    clock = _txt(D, 1700, 300, "⏱", 64, CREAM, font="sans")
    fines_y = [0]
    extra: list[str] = []   # 함께 당김 선 등 — 무대를 비울 때 같이 지움
    for k_, (b, (t0, d)) in enumerate(zip(sc.get("beats", []), bt)):
        seq = t0 + 0.2
        for act in b.get("do") or []:
            t = _when(sc, k_, b, t0, d, act.get("t"), seq)
            seq = max(seq, t) + 0.6
            if act.get("setup"):
                for j, k in enumerate(keys):
                    D.js.append(f'tl.fromTo("#co{k}",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.4}},{t + j * .15:.2f});')
                    D.js.append(f'tl.to("#lv{k}",{{opacity:1,duration:.4}},{t + .2 + j * .15:.2f});')
                    D.js.append(f'tl.to("#{seg[k][0]}",{{opacity:1,duration:.4}},{t + j * .15:.2f});')
                    for m in range(4):
                        D.js.append(f'tl.to("#cu{k}{m}",{{opacity:1,duration:.25}},{t + .4 + j * .15 + m * .05:.2f});')
                _show(D, cap, t, 0)
            if "lean" in act:
                D.js.append(f'tl.to("#lv{act["lean"]}L",{{rotation:10,duration:.6,ease:"power2.inOut"}},{t:.2f});')
                D.sfx.append(("click-soft", t))
            if "pull" in act:
                for k in act["pull"]:
                    D.js.append(f'tl.to("#lv{k}L",{{rotation:62,duration:.35,ease:"power3.in"}},{t:.2f});')
                D.sfx.append(("click-soft", t))
            if "flow" in act:
                src, dst = act["flow"], act["to"]
                for m in range(4):
                    tgt = cos[dst[m % len(dst)]]
                    dx = tgt["x"] - cos[src]["x"] + (m // len(dst)) * 30
                    D.js.append(f'tl.to("#cu{src}{m}",{{x:{dx},duration:.8,ease:"power2.inOut"}},{t + m * .12:.2f});')
                w = share_w / len(keys)
                D.js.append(f'tl.to("#{seg[src][0]}",{{width:{w * .35:.0f},duration:.8}},{t:.2f});')
                for j, k in enumerate(keys):
                    if k in dst:
                        D.js.append(f'tl.to("#{seg[k][0]}",{{width:{w * (1 + .65 / len(dst)) - 4:.0f},duration:.8}},{t:.2f});')
                # 막대 위치 다시 맞추기
                xs, cx = {}, bx0
                for k in keys:
                    ww = w * .35 if k == src else (w * (1 + .65 / len(dst)) if k in dst else w)
                    xs[k] = cx; cx += ww
                for k in keys:
                    D.js.append(f'tl.to("#{seg[k][0]}",{{left:{xs[k]:.0f},duration:.8}},{t:.2f});')
                D.sfx.append(("whoosh", t))
            if "invest" in act:
                for j, k in enumerate(act["invest"]):
                    c = cos[k]
                    i = _txt(D, c["x"], yc - 70, "＋$ → 다음 공장", 28, GOLD, font="heavy", anchor="c")
                    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.4}},{t + j * .2:.2f});')
                    D.js.append(f'tl.to("#{i}",{{opacity:0,duration:.3}},{t + 2.6:.2f});')
                D.sfx.append(("pop", t))
            if act.get("reset"):
                w = share_w / len(keys)
                for j, k in enumerate(keys):
                    D.js.append(f'tl.to("#lv{k}L",{{rotation:-28,duration:.4}},{t:.2f});')
                    D.js.append(f'tl.to("#{seg[k][0]}",{{width:{w - 4:.0f},left:{bx0 + j * w:.0f},duration:.6}},{t:.2f});')
                    for m in range(4):
                        D.js.append(f'tl.to("#cu{k}{m}",{{x:0,duration:.6}},{t:.2f});')
            if act.get("wait"):
                for j, k in enumerate(keys):
                    D.js.append(f'tl.to("#lv{k}L",{{rotation:-8,duration:.4}},{t + j * .1:.2f});')
                    D.js.append(f'tl.to("#lv{k}L",{{rotation:-14,duration:.22,yoyo:true,repeat:{int(act.get("hold", 4) / .22)},ease:"sine.inOut"}},{t + .5 + j * .1:.2f});')
                    D.js.append(f'tl.fromTo("#th{k}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.35}},{t + .3 + j * .25:.2f});')
                _show(D, clock, t + .2, 0)
                D.js.append(f'tl.to("#{clock}",{{rotation:360,duration:{act.get("hold", 4)},ease:"none"}},{t + .2:.2f});')
            if "chicken" in act:
                rid = D._id()
                D.items.append(f'<div id="{rid}" style="position:absolute;left:520px;top:836px;width:940px;height:100px;opacity:0">'
                               f'<div style="position:absolute;left:0;right:0;top:58px;height:4px;background:repeating-linear-gradient(90deg,#9AA6AE 0 30px,transparent 30px 54px)"></div>'
                               f'<div style="position:absolute;left:0;top:30px"><div id="{rid}a" style="font-size:58px"><span style="display:inline-block;transform:scaleX(-1)">🚗</span></div></div>'
                               f'<div style="position:absolute;right:0;top:30px"><div id="{rid}b" style="font-size:58px">🚗</div></div>'
                               f'<div style="position:absolute;right:100%;margin-right:28px;top:30px;font-family:heavy;font-size:44px;color:{GOLD};white-space:nowrap">{H.escape(act["chicken"])}</div></div>')
                D.js.append(f'tl.to("#{rid}",{{opacity:1,duration:.3}},{t:.2f});')
                D.js.append(f'tl.to("#{rid}a",{{x:380,duration:1.6,ease:"power1.in"}},{t + .2:.2f});')
                D.js.append(f'tl.to("#{rid}b",{{x:-380,duration:1.6,ease:"power1.in"}},{t + .2:.2f});')
                D.js.append(f'tl.to("#{rid}",{{opacity:0,duration:.4}},{bt[k_][0] + bt[k_][1] + .1:.2f});')
                D.sfx.append(("whoosh", t))
            if act.get("together"):
                for k in keys:
                    D.js.append(f'tl.to("#th{k}",{{opacity:0,duration:.3}},{t:.2f});')
                    D.js.append(f'tl.to("#lv{k}L",{{rotation:62,duration:.4,ease:"power3.in"}},{t + .3:.2f});')
                lid = D._id()
                D.svg.append(f'<path id="{lid}" d="M{cos[keys[0]]["x"]},{yc + 150} L{cos[keys[-1]]["x"]},{yc + 150}" stroke="{DOWN}" stroke-width="6" '
                             f'fill="none" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
                D.js.append(f'tl.to("#{lid}",{{strokeDashoffset:0,duration:.6}},{t + .2:.2f});')
                extra.append(lid)
                D.sfx.append(("click-soft", t + .3))
            if "stamp" in act:
                i = _txt(D, 960, 560, H.escape(act["stamp"]), 120, DOWN, font="heavy", anchor="c",
                         extra=f"border:8px solid {DOWN};padding:6px 34px;border-radius:12px;")
                D.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:1.6,rotation:-8}},{{opacity:1,scale:1,rotation:-8,duration:.3,ease:"power3.in"}},{t:.2f});')
                D.js.append(f'tl.to("#{i}",{{opacity:.0,duration:.4}},{t + 2.4:.2f});')
                D.sfx.append(("stamp", t))
            if act.get("clear_stage"):
                for k in keys:
                    for e in (f"co{k}", f"lv{k}", f"th{k}"):
                        D.js.append(f'tl.to("#{e}",{{opacity:0,duration:.4}},{t:.2f});')
                    for m in range(4):
                        D.js.append(f'tl.to("#cu{k}{m}",{{opacity:0,duration:.3}},{t:.2f});')
                    D.js.append(f'tl.to("#{seg[k][0]}",{{opacity:0,duration:.3}},{t:.2f});')
                D.js.append(f'tl.to("#{cap}",{{opacity:0,duration:.3}},{t:.2f});')
                D.js.append(f'tl.to("#{clock}",{{opacity:0,duration:.3}},{t:.2f});')
                for e in extra:
                    D.js.append(f'tl.to("#{e}",{{opacity:0,duration:.3}},{t:.2f});')
            if "tag" in act:
                i = _txt(D, 300, 330, H.escape(act["tag"]), 34, LINE, font="heavy")
                _show(D, i, t, 0)
            if "fine" in act or "total" in act:
                scale = sc.get("fine_scale", 1100 / 8.0)    # 같은 축척: 억 달러당 픽셀
                v = act.get("value", act.get("total"))
                y = 450 + fines_y[0] * 130
                fines_y[0] += 1
                tot = "total" in act
                nm = _txt(D, 560, y + 14, H.escape(act.get("fine", "합계")), 34, CREAM, font="heavy", anchor="r")
                bar = D._id()
                D.items.append(f'<div id="{bar}" style="position:absolute;left:590px;top:{y}px;height:72px;width:{v * scale:.0f}px;border-radius:8px;'
                               f'background:{DOWN if tot else GOLD};transform-origin:0 50%;transform:scaleX(0)"></div>')
                vl = _txt(D, 590 + v * scale + 24, y + 14, H.escape(act.get("text", "")), 34, DOWN if tot else GOLD, font="heavy")
                _show(D, nm, t, 0)
                D.js.append(f'tl.to("#{bar}",{{scaleX:1,duration:.7,ease:"power2.out"}},{t:.2f});')
                _show(D, vl, t + .5, 0)
                D.sfx.append(("pop", t))


# ── giveback ─────────────────────────────────────────────────────────────────
def s_giveback(D, sc: dict, bt: list, dur: float):
    """오른 만큼 중 돌려준 몫 — 회사마다 같은 축척(월요일에 오른 폭 = 100%)의 기둥.
    초록 기둥 = 월요일에 오른 만큼, 위에서부터 내려오는 빨간 덮개 = 화요일에 돌려준 몫(100% 넘으면 금요일 선 아래로).
    다음 장면이 같은 그림을 이어받을 때는 {"preset": "final"} 로 끝 상태에서 시작한다(E2 주인공 사물 유지)."""
    from . import explain
    sc = dict(sc)
    sc.setdefault("theme", "dark")
    explain._setup(D, sc, title=False)
    _title(D, sc)
    cos = sc["companies"]          # [{"id","label","pct"(돌려준 %)}]
    n = len(cos)
    xl, xr = 540, 1820
    yb, yt = 720, 340              # 금요일 종가(0) · 월요일 종가(100%)
    U = (yb - yt) / 100.0
    cw = min(130, (xr - xl) / n * 0.55)
    X = {c["id"]: xl + (xr - xl) * (j + .5) / n for j, c in enumerate(cos)}
    ax = []
    for y, lab in ((yt, "월요일 종가 — 오른 만큼 100%"), (yb, "금요일 종가 — 0")):
        i = D._id()
        D.svg.append(f'<line id="{i}" x1="70" y1="{y}" x2="{xr}" y2="{y}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="10 9" opacity="0"/>')
        j = _txt(D, 70, y - 38, lab, 24, MUTED)
        ax += [i, j]
    el = {}
    for c in cos:
        x = X[c["id"]]
        g, r, pl, nm, kp = (D._id() for _ in range(5))
        D.items.append(f'<div id="{g}" style="position:absolute;left:{x - cw / 2:.0f}px;top:{yt}px;width:{cw:.0f}px;height:{yb - yt}px;border-radius:6px 6px 0 0;'
                       f'background:linear-gradient(180deg,#5FD394,#2F8F5C);transform-origin:50% 100%;transform:scaleY(0)"></div>')
        rh = c["pct"] * U
        D.items.append(f'<div id="{r}" style="position:absolute;left:{x - cw / 2 - 4:.0f}px;top:{yt}px;width:{cw + 8:.0f}px;height:{rh:.0f}px;border-radius:4px;'
                       f'background:repeating-linear-gradient(135deg,rgba(240,106,90,.95) 0 14px,rgba(200,70,60,.95) 14px 28px);transform-origin:50% 0;transform:scaleY(0)"></div>')
        D.items.append(f'<div id="{pl}" style="position:absolute;left:{x:.0f}px;top:{yt - 62}px;transform:translateX(-50%);font-family:heavy;font-size:40px;color:{DOWN};opacity:0">{c["pct"]:.0f}%</div>')
        D.items.append(f'<div id="{nm}" style="position:absolute;left:{x:.0f}px;top:{max(yb, yt + rh) + 22:.0f}px;transform:translateX(-50%);font-family:heavy;font-size:32px;color:{CREAM};white-space:nowrap;opacity:0">{H.escape(c["label"])}</div>')
        kh = max(0.0, 100 - c["pct"]) * U
        D.items.append(f'<div id="{kp}" style="position:absolute;left:{x:.0f}px;top:{yb - kh / 2 - 34:.0f}px;transform:translateX(-50%);width:{cw:.0f}px;text-align:center;line-height:1.1;word-break:keep-all;font-family:heavy;font-size:30px;color:#0D1A12;opacity:0"></div>')
        el[c["id"]] = dict(g=g, r=r, pl=pl, nm=nm, kp=kp)
    ids = [c["id"] for c in cos]
    kept: set[str] = set()

    def rise(which, t, d=.6):
        for j, k in enumerate(which):
            D.js.append(f'tl.to("#{el[k]["g"]}",{{scaleY:1,duration:{d},ease:"power2.out"}},{t + j * .07:.2f});')
            D.js.append(f'tl.to("#{el[k]["nm"]}",{{opacity:1,duration:.3}},{t + j * .07:.2f});')

    def back(k, t, d=.7):
        D.js.append(f'tl.to("#{el[k]["r"]}",{{scaleY:1,duration:{d},ease:"power2.in"}},{t:.2f});')
        D.js.append(f'tl.to("#{el[k]["pl"]}",{{opacity:1,duration:.3}},{t + d * .8:.2f});')

    for k_, (b, (t0, d)) in enumerate(zip(sc.get("beats", []), bt)):
        seq = t0 + 0.2
        for act in b.get("do") or []:
            t = _when(sc, k_, b, t0, d, act.get("t"), seq)
            seq = max(seq, t) + 0.6
            if act.get("preset") == "final":   # 앞 장면 끝 모습 그대로 시작
                for e in ax:
                    D.js.append(f'tl.set("#{e}",{{opacity:1}},0);')
                for k in ids:
                    D.js.append(f'tl.set("#{el[k]["g"]}",{{scaleY:1}},0);tl.set("#{el[k]["r"]}",{{scaleY:1}},0);'
                                f'tl.set("#{el[k]["pl"]}",{{opacity:1}},0);tl.set("#{el[k]["nm"]}",{{opacity:1}},0);')
            if act.get("axes"):
                for e in ax:
                    D.js.append(f'tl.fromTo("#{e}",{{opacity:0}},{{opacity:1,duration:.4}},{t:.2f});')
            if "rise" in act:
                rise(ids if act["rise"] == "all" else act["rise"], t)
                D.sfx.append(("whoosh-short", t))
            if "back" in act:
                for k in ([act["back"]] if isinstance(act["back"], str) else act["back"]):
                    back(k, t)
                    t += .25
                D.sfx.append(("click-soft", t))
            if "keep" in act:
                k = act["keep"]
                kept.add(k)
                D.js.append(f'tl.set("#{el[k]["kp"]}",{{textContent:{H.escape(act.get("text", ""))!r}}},{t:.2f});')
                D.js.append(f'tl.fromTo("#{el[k]["kp"]}",{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2)"}},{t:.2f});')
                D.sfx.append(("pop", t))
            if "focus" in act:
                on = set(act["focus"])
                for k in ids:
                    op = 1 if k in on else .22
                    for e in ("g", "r", "pl", "nm", "kp"):
                        D.js.append(f'tl.to("#{el[k][e]}",{{opacity:{op},duration:.4}},{t:.2f});' if e != "kp" else
                                    f'tl.to("#{el[k][e]}",{{autoAlpha:{op if op < 1 else 1},duration:.4}},{t:.2f});')
            if "unfocus" in act:
                for k in ids:
                    for e in ("g", "r", "pl", "nm"):
                        D.js.append(f'tl.to("#{el[k][e]}",{{opacity:1,duration:.4}},{t:.2f});')
                    if k in kept:
                        D.js.append(f'tl.to("#{el[k]["kp"]}",{{autoAlpha:1,duration:.4}},{t:.2f});')
            if "group" in act:
                ks = act["group"]
                a, z = min(X[k] for k in ks) - cw / 2 - 10, max(X[k] for k in ks) + cw / 2 + 10
                col = UP if act.get("tone") == "up" else DOWN if act.get("tone") == "down" else GOLD
                i = D._id()
                D.svg.append(f'<path id="{i}" d="M{a:.0f},{yt - 66} L{a:.0f},{yt - 84} L{z:.0f},{yt - 84} L{z:.0f},{yt - 66}" fill="none" stroke="{col}" stroke-width="4" '
                             f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
                D.js.append(f'tl.to("#{i}",{{strokeDashoffset:0,duration:.5}},{t:.2f});')
                j = _txt(D, (a + z) / 2, yt - 136, H.escape(act["text"]), 34, col, font="heavy", anchor="c")
                _show(D, j, t + .2)
                D.sfx.append(("pop", t))
            if "tag" in act:
                i = _txt(D, 1860, 96, H.escape(act["tag"]), 28, "#1A1D20", font="heavy", anchor="r",
                         extra=f"background:{GOLD};padding:6px 16px;border-radius:20px;")
                _show(D, i, t, 0)


# ── lifecost ─────────────────────────────────────────────────────────────────
def s_lifecost(D, sc: dict, bt: list, dur: float):
    """같은 매출 선 위에서 '몇 년으로 나누나'에 따라 해마다 비용 막대가 달라져 적자·흑자가 갈린다 (docs/68 E4·E5).
    items: [{"id","label","cost"}], revenue: 숫자, unit: "억 달러".
    do: {"revenue": true} 매출 선 · {"cost": id} 비용 막대 · {"gap": id} 매출 선과의 차이(적자 빨강·흑자 초록)
        {"rate": 1.0, "label": "금리 +1%p → 해마다 +1억"} 모든 막대 위에 같은 조각을 얹고 차이를 다시 씀 · {"preset": "final"}"""
    from . import explain
    sc = dict(sc)
    sc.setdefault("theme", "dark")
    explain._setup(D, sc, title=False)
    _title(D, sc)
    items, rev, unit = sc["items"], float(sc["revenue"]), sc.get("unit", "억 달러")
    top = max([rev] + [i["cost"] for i in items]) * 1.25
    yb, yt = 840, 260
    U = (yb - yt) / top
    n = len(items)
    X = {it["id"]: 560 + (1360 - 560) * j / max(1, n - 1) for j, it in enumerate(items)}
    bw = 190
    fmt = lambda v: f"{v:,.1f}".rstrip("0").rstrip(".")
    D.svg.append(f'<line x1="300" y1="{yb}" x2="1650" y2="{yb}" stroke="#4A535A" stroke-width="2"/>')
    ry = yb - rev * U
    rl = D._id()
    D.svg.append(f'<line id="{rl}" x1="300" y1="{ry:.0f}" x2="1650" y2="{ry:.0f}" stroke="{GOLD}" stroke-width="4" stroke-dasharray="14 10" opacity="0"/>')
    rlab = _txt(D, 1650, ry - 40, H.escape(sc.get("revenue_label", f"해마다 매출 {fmt(rev)}{unit}")), 30, GOLD, font="heavy", anchor="r")   # 오른쪽 끝: 왼쪽 첫 막대(적자 막대는 선 위로 솟음)와 겹치지 않게
    el = {}
    for it in items:
        x, c = X[it["id"]], it["cost"]
        b, cl, nm, gp, gl, rt = (D._id() for _ in range(6))
        D.items.append(f'<div id="{b}" style="position:absolute;left:{x - bw / 2:.0f}px;top:{yb - c * U:.0f}px;width:{bw}px;height:{c * U:.0f}px;'
                       f'background:linear-gradient(180deg,#8FA3B4,#5E7183);border-radius:6px 6px 0 0;transform-origin:50% 100%;transform:scaleY(0)"></div>')
        D.items.append(f'<div id="{cl}" style="position:absolute;left:{x:.0f}px;top:{yb - c * U + 14:.0f}px;transform:translateX(-50%);font-family:heavy;font-size:30px;color:#14181B;white-space:nowrap;opacity:0">비용 {fmt(c)}</div>')
        D.items.append(f'<div id="{nm}" style="position:absolute;left:{x:.0f}px;top:{yb + 18}px;transform:translateX(-50%);font-family:heavy;font-size:34px;color:{CREAM};white-space:nowrap;opacity:0">{H.escape(it["label"])}</div>')
        # 차이: 매출 선과 막대 꼭대기 사이를 칠함
        D.items.append(f'<div id="{gp}" style="position:absolute;left:{x - bw / 2:.0f}px;width:{bw}px;opacity:0"></div>')
        D.items.append(f'<div id="{gl}" style="position:absolute;left:{x + bw / 2 + 14:.0f}px;font-family:heavy;font-size:36px;white-space:nowrap;opacity:0"></div>')
        D.items.append(f'<div id="{rt}" style="position:absolute;left:{x - bw / 2:.0f}px;width:{bw}px;opacity:0;background:repeating-linear-gradient(135deg,#F0A04B 0 10px,#C77A2E 10px 20px);border-radius:6px 6px 0 0"></div>')
        el[it["id"]] = dict(b=b, cl=cl, nm=nm, gp=gp, gl=gl, rt=rt, cost=c)

    def gap_js(k, cost, t, d=.5):
        e = el[k]
        top_y, bar_y = ry, yb - cost * U
        y0, h = min(top_y, bar_y), abs(top_y - bar_y)
        loss = cost > rev
        col = DOWN if loss else UP
        txt = (f"적자 {fmt(cost - rev)}{unit}" if loss else f"흑자 {fmt(rev - cost)}{unit}")
        bg = "rgba(240,106,90,.55)" if loss else "rgba(79,203,134,.35)"
        D.js.append(f'tl.set("#{e["gp"]}",{{top:{y0:.0f},height:{h:.0f},background:"{bg}",border:"3px dashed {col}"}},{t:.2f});')
        D.js.append(f'tl.fromTo("#{e["gp"]}",{{opacity:0}},{{opacity:1,duration:{d}}},{t:.2f});')
        D.js.append(f'tl.set("#{e["gl"]}",{{top:{y0 + h / 2 - 22:.0f},color:"{col}",textContent:{txt!r}}},{t:.2f});')
        D.js.append(f'tl.fromTo("#{e["gl"]}",{{opacity:0,x:-8}},{{opacity:1,x:0,duration:.35}},{t + .1:.2f});')

    for k_, (b, (t0, d)) in enumerate(zip(sc.get("beats", []), bt)):
        seq = t0 + 0.2
        for act in b.get("do") or []:
            t = _when(sc, k_, b, t0, d, act.get("t"), seq)
            seq = max(seq, t) + 0.6
            if act.get("preset") == "final":
                D.js.append(f'tl.set("#{rl}",{{opacity:1}},0);tl.set("#{rlab}",{{opacity:1}},0);')
                for k, e in el.items():
                    D.js.append(f'tl.set("#{e["b"]}",{{scaleY:1}},0);tl.set("#{e["cl"]}",{{opacity:1}},0);tl.set("#{e["nm"]}",{{opacity:1}},0);')
                    gap_js(k, e["cost"], 0.0, 0.01)
            if act.get("revenue"):
                D.js.append(f'tl.to("#{rl}",{{opacity:1,duration:.5}},{t:.2f});')
                _show(D, rlab, t + .1, 0)
                D.sfx.append(("pencil", t))
            if "cost" in act:
                for k in ([act["cost"]] if isinstance(act["cost"], str) else act["cost"]):
                    e = el[k]
                    D.js.append(f'tl.to("#{e["b"]}",{{scaleY:1,duration:.6,ease:"power2.out"}},{t:.2f});')
                    D.js.append(f'tl.to("#{e["cl"]}",{{opacity:1,duration:.3}},{t + .45:.2f});')
                    D.js.append(f'tl.to("#{e["nm"]}",{{opacity:1,duration:.3}},{t:.2f});')
                D.sfx.append(("whoosh-short", t))
            if "gap" in act:
                for k in ([act["gap"]] if isinstance(act["gap"], str) else act["gap"]):
                    gap_js(k, el[k]["cost"], t)
                    t += .3
                D.sfx.append(("pop", t))
            if "rate" in act:
                r = float(act["rate"])
                for j, (k, e) in enumerate(el.items()):
                    nc = e["cost"] + r
                    D.js.append(f'tl.set("#{e["rt"]}",{{top:{yb - nc * U:.0f},height:{r * U:.0f}}},{t:.2f});')
                    D.js.append(f'tl.fromTo("#{e["rt"]}",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.45,ease:"bounce.out"}},{t + j * .15:.2f});')
                    gap_js(k, nc, t + .6 + j * .15)
                    e["cost"] = nc
                if act.get("label"):
                    i = _txt(D, 1650, act.get("y", 270), H.escape(act["label"]), 30, "#F0A04B", font="heavy", anchor="r")   # note(200)와 매출 글자(선 위) 사이 줄
                    _show(D, i, t, 0)
                D.sfx.append(("pop", t))
            if "note" in act:
                i = _txt(D, 1860, act.get("y", 200), H.escape(act["note"]), 28, MUTED, anchor="r")
                _show(D, i, t, 0)


# ── profitbar ────────────────────────────────────────────────────────────────
def s_profitbar(D, sc: dict, bt: list, dur: float):
    """매출 막대 = 비용(아래 회색) + 이익(위 초록). 값이 빠져 매출이 줄어도 비용은 그대로라 이익이 더 크게 준다 (E4·E5).
    cols: [{"id","label","revenue","cost"}]; do: {"col": id} · {"profit": id} · {"note": ...} · {"dim": true} · {"mini": [[이름, 값, 글자], ...], "title": ...}"""
    from . import explain
    sc = dict(sc)
    sc.setdefault("theme", "dark")
    explain._setup(D, sc, title=False)
    _title(D, sc)
    cols, unit = sc["cols"], sc.get("unit", "")
    top = max(c["revenue"] for c in cols) * 1.15
    yb, yt = 860, 250
    U = (yb - yt) / top
    X = {c["id"]: 460 + 520 * j for j, c in enumerate(cols)}
    bw = 240
    el = {}
    D.svg.append(f'<line x1="250" y1="{yb}" x2="1250" y2="{yb}" stroke="#4A535A" stroke-width="2"/>')
    for c in cols:
        x = X[c["id"]]
        ch, ph, nm, cl, pl, rl = (D._id() for _ in range(6))
        hc, hp = c["cost"] * U, (c["revenue"] - c["cost"]) * U
        D.items.append(f'<div id="{ch}" style="position:absolute;left:{x - bw / 2}px;top:{yb - hc:.0f}px;width:{bw}px;height:{hc:.0f}px;background:#5E6B76;transform-origin:50% 100%;transform:scaleY(0)"></div>')
        D.items.append(f'<div id="{ph}" style="position:absolute;left:{x - bw / 2}px;top:{yb - hc - hp:.0f}px;width:{bw}px;height:{hp:.0f}px;border-radius:6px 6px 0 0;background:linear-gradient(180deg,#5FD394,#2F8F5C);transform-origin:50% 100%;transform:scaleY(0)"></div>')
        D.items.append(f'<div id="{cl}" style="position:absolute;left:{x:.0f}px;top:{yb - hc / 2 - 20:.0f}px;transform:translateX(-50%);font-family:heavy;font-size:30px;color:#E6EAED;white-space:nowrap;opacity:0">비용 {c["cost"]:g}{unit}</div>')
        D.items.append(f'<div id="{pl}" style="position:absolute;left:{x:.0f}px;top:{yb - hc - hp / 2 - 24:.0f}px;transform:translateX(-50%);font-family:heavy;font-size:40px;color:#0D1A12;white-space:nowrap;opacity:0">이익 {c["revenue"] - c["cost"]:g}{unit}</div>')
        D.items.append(f'<div id="{rl}" style="position:absolute;left:{x:.0f}px;top:{yb - hc - hp - 54:.0f}px;transform:translateX(-50%);font-family:heavy;font-size:32px;color:{GOLD};white-space:nowrap;opacity:0">매출 {c["revenue"]:g}{unit}</div>')
        D.items.append(f'<div id="{nm}" style="position:absolute;left:{x:.0f}px;top:{yb + 18}px;transform:translateX(-50%);font-family:heavy;font-size:34px;color:{CREAM};white-space:nowrap;opacity:0">{H.escape(c["label"])}</div>')
        el[c["id"]] = dict(ch=ch, ph=ph, cl=cl, pl=pl, rl=rl, nm=nm)
    for k_, (b, (t0, d)) in enumerate(zip(sc.get("beats", []), bt)):
        seq = t0 + 0.2
        for act in b.get("do") or []:
            t = _when(sc, k_, b, t0, d, act.get("t"), seq)
            seq = max(seq, t) + 0.6
            if "col" in act:
                e = el[act["col"]]
                D.js.append(f'tl.to("#{e["ch"]}",{{scaleY:1,duration:.5}},{t:.2f});tl.to("#{e["cl"]}",{{opacity:1,duration:.3}},{t + .4:.2f});')
                D.js.append(f'tl.to("#{e["ph"]}",{{scaleY:1,duration:.5}},{t + .4:.2f});tl.to("#{e["rl"]}",{{opacity:1,duration:.3}},{t + .8:.2f});tl.to("#{e["nm"]}",{{opacity:1,duration:.3}},{t:.2f});')
                D.sfx.append(("whoosh-short", t))
            if "profit" in act:
                e = el[act["profit"]]
                D.js.append(f'tl.fromTo("#{e["pl"]}",{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2)"}},{t:.2f});')
                D.sfx.append(("pop", t))
            if act.get("dim"):
                for e in el.values():
                    for v in e.values():
                        D.js.append(f'tl.to("#{v}",{{opacity:.18,duration:.4}},{t:.2f});')
            if "note" in act:
                i = _txt(D, act.get("x", 1300), act.get("y", 330), H.escape(act["note"]), act.get("size", 40), act.get("color", DOWN), font="heavy")
                _show(D, i, t, 0)
                D.sfx.append(("pop", t))
            if "mini" in act:   # 오른쪽 작은 가로 막대 (같은 축척)
                rows = act["mini"]
                vmax = max(abs(r[1]) for r in rows) or 1
                if act.get("title"):
                    i = _txt(D, 1300, 470, H.escape(act["title"]), 28, MUTED)
                    _show(D, i, t, 0)
                for j, (nm_, v, txt) in enumerate(rows):
                    y = 520 + j * 80
                    a = _txt(D, 1300, y, H.escape(nm_), 30, CREAM, font="heavy")
                    bar = D._id()
                    w = 300 * abs(v) / vmax
                    D.items.append(f'<div id="{bar}" style="position:absolute;left:1500px;top:{y + 4}px;height:36px;width:{w:.0f}px;background:{DOWN};border-radius:4px;transform-origin:0 50%;transform:scaleX(0)"></div>')
                    vl = _txt(D, 1500 + w + 14, y, H.escape(txt), 30, DOWN, font="heavy")
                    tt = t + j * .35
                    _show(D, a, tt, 0)
                    D.js.append(f'tl.to("#{bar}",{{scaleX:1,duration:.5}},{tt:.2f});')
                    _show(D, vl, tt + .4, 0)
                D.sfx.append(("pop", t))


# ── pqbox ────────────────────────────────────────────────────────────────────
def s_pqbox(D, sc: dict, bt: list, dur: float):
    """매출 = 값 × 개수 를 넓이로: 가로 = 판 개수, 세로 = 값. 두 길의 넓이를 나란히 (E1·E5).
    boxes: [{"id","label","qty","price","text","x"}], cap: 만들 수 있는 양
    do: {"box": id} · {"spare": id, "text": ...} 만들 수 있지만 안 만든 몫(점선) · {"area": id} 넓이 칠하고 매출 글자 · {"headline": ...}"""
    from . import explain
    sc = dict(sc)
    sc.setdefault("theme", "dark")
    explain._setup(D, sc, title=False)
    _title(D, sc)
    boxes = sc["boxes"]
    yb = 860
    PX = sc.get("px_per_qty", 6.0)
    PY = sc.get("px_per_price", 4.6)
    cap = sc.get("cap", max(b["qty"] for b in boxes))
    el = {}
    for b in boxes:
        x0 = b["x"]
        w, h = b["qty"] * PX, b["price"] * PY
        r, a, lb, nm, sp, ql = (D._id() for _ in range(6))
        D.items.append(f'<div id="{r}" style="position:absolute;left:{x0}px;top:{yb - h:.0f}px;width:{w:.0f}px;height:{h:.0f}px;border:4px solid {CREAM};border-radius:4px;transform-origin:0 100%;transform:scale(0)"></div>')
        D.items.append(f'<div id="{a}" style="position:absolute;left:{x0 + 4}px;top:{yb - h + 4:.0f}px;width:{w - 8:.0f}px;height:{h - 8:.0f}px;background:{b.get("fill", "rgba(240,190,90,.45)")};opacity:0"></div>')
        ly = yb - h / 2 - 30 if h > 120 else yb - h - 70
        D.items.append(f'<div id="{lb}" style="position:absolute;left:{x0 + w / 2:.0f}px;top:{ly:.0f}px;transform:translateX(-50%);font-family:heavy;font-size:46px;color:{GOLD};white-space:nowrap;opacity:0">{H.escape(b["text"])}</div>')
        D.items.append(f'<div id="{nm}" style="position:absolute;left:{x0}px;top:{yb + 18}px;font-family:heavy;font-size:32px;color:{CREAM};white-space:nowrap;opacity:0">{H.escape(b["label"])}</div>')
        D.items.append(f'<div id="{ql}" style="position:absolute;left:{x0 - 14}px;top:{yb - h - 2:.0f}px;transform:translateX(-100%);font-family:sans-x;font-size:26px;color:{MUTED};white-space:nowrap;opacity:0">값 {b["price"]:g}원</div>'
                       f'<div id="{ql}q" style="position:absolute;left:{x0 + w - 4:.0f}px;top:{yb + 60}px;transform:translateX(-100%);font-family:sans-x;font-size:26px;color:{MUTED};white-space:nowrap;opacity:0">{b["qty"]:g}개</div>')
        sw = (cap - b["qty"]) * PX
        D.items.append(f'<div id="{sp}" style="position:absolute;left:{x0 + w:.0f}px;top:{yb - h:.0f}px;width:{max(sw, 0):.0f}px;height:{h:.0f}px;border:3px dashed {MUTED};border-left:none;opacity:0"></div>')
        el[b["id"]] = dict(r=r, a=a, lb=lb, nm=nm, sp=sp, ql=ql, h=h, x=x0, w=w)
    for k_, (bb, (t0, d)) in enumerate(zip(sc.get("beats", []), bt)):
        seq = t0 + 0.2
        for act in bb.get("do") or []:
            t = _when(sc, k_, bb, t0, d, act.get("t"), seq)
            seq = max(seq, t) + 0.6
            if "box" in act:
                e = el[act["box"]]
                D.js.append(f'tl.to("#{e["r"]}",{{scale:1,duration:.6,ease:"power2.out"}},{t:.2f});tl.to("#{e["nm"]}",{{opacity:1,duration:.3}},{t:.2f});')
                D.js.append(f'tl.to("#{e["ql"]}",{{opacity:1,duration:.3}},{t + .4:.2f});tl.to("#{e["ql"]}q",{{opacity:1,duration:.3}},{t + .4:.2f});')
                D.sfx.append(("pencil", t))
            if "spare" in act:
                e = el[act["spare"]]
                D.js.append(f'tl.to("#{e["sp"]}",{{opacity:1,duration:.4}},{t:.2f});')
                if act.get("text"):
                    i = _txt(D, e["x"] + e["w"] + 10, 860 - e["h"] - 44, H.escape(act["text"]), 26, MUTED)
                    _show(D, i, t + .2, 0)
            if "area" in act:
                e = el[act["area"]]
                D.js.append(f'tl.to("#{e["a"]}",{{opacity:1,duration:.5}},{t:.2f});')
                D.js.append(f'tl.fromTo("#{e["lb"]}",{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2)"}},{t + .3:.2f});')
                D.sfx.append(("pop", t))
            if "headline" in act:
                i = _txt(D, 960, act.get("y", 180), H.escape(act["headline"]), 46, act.get("color", GOLD), font="heavy", anchor="c")
                _show(D, i, t)
                D.sfx.append(("pop", t))


# ── samend ───────────────────────────────────────────────────────────────────
def _jar(D, jid, cx, n, top=380, w=240, h=300, cookie=True):
    """유리병 하나 + 쿠키 n개(아래부터 쌓임). id: {jid}, 쿠키 {jid}k0.."""
    pos = [(-62, 250), (0, 252), (62, 250), (-34, 202), (30, 204), (-66, 156), (0, 154), (64, 158), (-30, 108), (34, 110)]
    ck = "".join(
        f'<div id="{jid}k{i}" style="position:absolute;left:{w / 2 + x - 27:.0f}px;top:{y - 27}px;width:54px;height:54px;border-radius:50%;'
        f'background:radial-gradient(circle at 35% 30%,#E2A867,#B97636);box-shadow:inset -4px -5px 0 rgba(0,0,0,.18)">'
        f'<i style="position:absolute;left:16px;top:18px;width:9px;height:9px;border-radius:50%;background:#3A2414"></i>'
        f'<i style="position:absolute;left:34px;top:28px;width:8px;height:8px;border-radius:50%;background:#3A2414"></i>'
        f'<i style="position:absolute;left:22px;top:38px;width:7px;height:7px;border-radius:50%;background:#3A2414"></i></div>'
        for i, (x, y) in enumerate(pos[:n]))
    return (f'<div id="{jid}" style="position:absolute;left:{cx - w / 2:.0f}px;top:{top}px;width:{w}px;height:{h}px;opacity:0">'
            f'<div style="position:absolute;left:{w * .22:.0f}px;top:-26px;width:{w * .56:.0f}px;height:30px;border-radius:6px;background:#8E99A1"></div>'
            f'<div style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;border-radius:38px 38px 30px 30px;'
            f'border:4px solid rgba(214,226,232,.75);background:rgba(190,215,225,.08)"></div>{ck}</div>')


def s_samend(D, sc: dict, bt: list, dur: float):
    """같은 끝, 다른 과정 (docs/69 시각 먼저 시범). 끝 상태가 같은 대상 여럿을 나란히 놓고, 한 대상만 '줄어드는 과정'을 눈앞에서 겪게 한 뒤
    결과값(값표)을 같은 축척으로 붙여 과정이 결과를 바꿨음을 보인다 (E1 실물·E2 같은 병·E5 나란히).
    jars: {"a": {"label": "처음부터 10개", "n": 10, "x": 520, "price": 46.2}, "c": {"label": "10개 → 2개", "n": 10, "to": 2, "price": 71.5}}
    do: {"phone": [5, 3]} 가운데 휴대전화 숫자가 줄어듦 · {"phone_side": true} 왼쪽으로 물러남 · {"jar": "a"} 병 등장
        {"swap": "c"} 병째 바뀜(10개 병이 나가고 2개 병이 들어옴) · {"button": "c"} 숨은 버튼 깜빡임
        {"price": "a"} 값표 (c 는 숫자가 올라감) · {"equal": ["a","b"]} 두 값표 사이 ≈ · {"taste": true} 맛 막대 셋이 같은 높이
        {"focus": "c"} 나머지 흐리게 · {"link": "c"} 휴대전화 ↔ 병 c 를 잇는 선과 같은 모양 표시 · {"note": "..."} 아래 작은 주석"""
    from . import explain
    sc = dict(sc)
    sc.setdefault("theme", "dark")
    explain._setup(D, sc, title=False)
    _title(D, sc)
    jars = sc["jars"]
    top, jh = 360, 300
    for k, j in jars.items():
        D.items.append(_jar(D, f"j{k}", j["x"], j["n"], top=top, h=jh))
        D.items.append(f'<div id="j{k}lb" style="position:absolute;left:{j["x"]}px;top:{top + jh + 22}px;transform:translateX(-50%);font-family:heavy;'
                       f'font-size:34px;color:{CREAM};white-space:nowrap;opacity:0">{H.escape(j["label"])}</div>')
    unit = sc.get("unit", "¢")
    # 휴대전화 (지우의 화면): 가운데에서 시작
    D.items.append(f'<div id="ph" style="position:absolute;left:820px;top:250px;width:280px;height:500px;border-radius:40px;background:#14181B;'
                   f'border:6px solid #3C454C;opacity:0;transform-origin:50% 50%">'
                   f'<div style="position:absolute;left:30px;top:70px;width:220px;height:150px;border-radius:14px;background:#2A3238"></div>'
                   f'<div style="position:absolute;left:0;right:0;top:250px;text-align:center;font-family:heavy;font-size:46px;color:{DOWN}">'
                   f'<span id="phn">5</span>개 남음</div>'
                   f'<div style="position:absolute;left:40px;right:40px;top:360px;height:64px;border-radius:32px;background:{DOWN};'
                   f'color:#fff;font-family:heavy;font-size:30px;line-height:64px;text-align:center">결제하기</div></div>')
    extra = []
    for k_, (b, (t0, d)) in enumerate(zip(sc.get("beats", []), bt)):
        seq = t0 + 0.2
        for act in b.get("do") or []:
            t = _when(sc, k_, b, t0, d, act.get("t"), seq)
            seq = max(seq, t) + 0.6
            if "phone" in act:
                a0, a1 = act["phone"]
                D.js.append(f'tl.fromTo("#ph",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.45,ease:"power2.out"}},{t:.2f});')
                D.js.append(f'tl.set("#phn",{{textContent:"{a0}"}},{t:.2f});')
                for s in range(1, a0 - a1 + 1):
                    D.js.append(f'tl.set("#phn",{{textContent:"{a0 - s}"}},{t + .9 + s * .55:.2f});')
                    D.js.append(f'tl.fromTo("#phn",{{scale:1.5}},{{scale:1,duration:.3}},{t + .9 + s * .55:.2f});')
                    D.sfx.append(("click-soft", t + .9 + s * .55))
            if act.get("phone_side"):
                D.js.append(f'tl.to("#ph",{{left:70,top:300,scale:.62,duration:.8,ease:"power2.inOut"}},{t:.2f});')
            if "jar" in act:
                for j, k in enumerate(act["jar"] if isinstance(act["jar"], list) else [act["jar"]]):
                    D.js.append(f'tl.fromTo("#j{k}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.5,ease:"back.out(1.4)"}},{t + j * .35:.2f});')
                    D.js.append(f'tl.fromTo("#j{k}lb",{{opacity:0,y:12}},{{opacity:1,y:0,duration:.35}},{t + .25 + j * .35:.2f});')
                    D.sfx.append(("pop", t + j * .35))
            if "swap" in act:
                k = act["swap"]
                j = jars[k]
                D.items.append(_jar(D, f"j{k}n", j["x"], j["to"], top=top, h=jh))
                D.items.append(f'<div id="j{k}gh" style="position:absolute;left:{j["x"] - 130}px;top:{top - 10}px;width:260px;height:{jh + 20}px;'
                               f'border:3px dashed rgba(201,208,213,.45);border-radius:40px;opacity:0"></div>')
                D.js.append(f'tl.to("#j{k}",{{x:900,opacity:0,duration:.9,ease:"power2.in"}},{t:.2f});')
                D.js.append(f'tl.to("#j{k}gh",{{opacity:1,duration:.3}},{t + .5:.2f});')
                D.js.append(f'tl.fromTo("#j{k}n",{{opacity:0,x:900}},{{opacity:1,x:0,duration:.9,ease:"power2.out"}},{t + 1.0:.2f});')
                D.js.append(f'tl.to("#j{k}gh",{{opacity:0,duration:.4}},{t + 2.2:.2f});')
                D.sfx.append(("whoosh", t))
                D.sfx.append(("whoosh", t + 1.0))
            if "button" in act:
                j = jars[act["button"]]
                bid = D._id()
                D.items.append(f'<div id="{bid}" style="position:absolute;left:{j["x"] + 150}px;top:{top + jh - 40}px;opacity:0">'
                               f'<div style="width:40px;height:40px;border-radius:50%;background:{DOWN};box-shadow:0 0 0 8px rgba(240,106,90,.25)"></div>'
                               f'<div style="position:absolute;left:54px;top:4px;font-family:sans-x;font-size:26px;color:{MUTED};white-space:nowrap">숨은 버튼</div></div>')
                D.js.append(f'tl.to("#{bid}",{{opacity:1,duration:.3}},{t:.2f});')
                D.js.append(f'tl.fromTo("#{bid} div",{{scale:1}},{{scale:.8,duration:.18,yoyo:true,repeat:3}},{t + .3:.2f});')
                D.js.append(f'tl.to("#{bid}",{{opacity:0,duration:.4}},{t + 3.2:.2f});')
                D.sfx.append(("click-soft", t + .3))
            if "price" in act:
                for j_, k in enumerate(act["price"] if isinstance(act["price"], list) else [act["price"]]):
                    j = jars[k]
                    pid = f"pr{k}"
                    big = j.get("big")
                    D.items.append(f'<div id="{pid}" style="position:absolute;left:{j["x"]}px;top:{top - 120}px;transform:translateX(-50%);'
                                   f'padding:8px 26px;border-radius:12px;background:{GOLD if big else CREAM};color:#1A1D20;font-family:heavy;'
                                   f'font-size:{60 if big else 46}px;white-space:nowrap;opacity:0"><span id="{pid}v">{j["price"]}</span>{unit}</div>')
                    tt = t + j_ * .45
                    D.js.append(f'tl.fromTo("#{pid}",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.4,ease:"back.out(1.6)"}},{tt:.2f});')
                    if j.get("count_from") is not None:
                        D.js.append(f'tl.fromTo("#{pid}v",{{textContent:{j["count_from"]}}},{{textContent:{j["price"]},duration:1.4,ease:"power2.out",'
                                    f'snap:{{textContent:0.1}},onUpdate:function(){{var e=document.getElementById("{pid}v");e.textContent=(+e.textContent).toFixed(1)}}}},{tt + .1:.2f});')
                    D.sfx.append(("pop", tt))
            if "equal" in act:
                a, c = (jars[x] for x in act["equal"])
                i = _txt(D, (a["x"] + c["x"]) / 2, top - 112, "≈", 64, GOLD, font="heavy", anchor="c")
                _show(D, i, t, 0)
            if act.get("taste"):
                tl_ = _txt(D, 150, top + jh + 96, "맛", 30, MUTED, font="heavy")
                _show(D, tl_, t, 0)
                for j_, (k, j) in enumerate(jars.items()):
                    bid = D._id()
                    D.items.append(f'<div id="{bid}" style="position:absolute;left:{j["x"] - 90}px;top:{top + jh + 100}px;width:180px;height:26px;'
                                   f'border-radius:6px;background:{LINE};transform-origin:0 50%;transform:scaleX(0)"></div>')
                    D.js.append(f'tl.to("#{bid}",{{scaleX:1,duration:.5,ease:"power2.out"}},{t + .1 + j_ * .15:.2f});')
                lid = D._id()
                xs = [j["x"] for j in jars.values()]
                D.svg.append(f'<path id="{lid}" d="M{min(xs) - 120},{top + jh + 113} L{max(xs) + 120},{top + jh + 113}" stroke="{GOLD}" '
                             f'stroke-width="3" stroke-dasharray="10 10" fill="none" opacity="0"/>')
                D.js.append(f'tl.to("#{lid}",{{opacity:.9,duration:.4}},{t + .7:.2f});')
            if "focus" in act:
                for k in jars:
                    if k != act["focus"]:
                        for e in (f"j{k}", f"j{k}lb", f"pr{k}"):
                            D.js.append(f'tl.to("#{e}",{{opacity:.28,duration:.5}},{t:.2f});')
            if "link" in act:
                j = jars[act["link"]]
                lid = D._id()
                D.svg.append(f'<path id="{lid}" d="M180,{top + jh + 20} C420,{top + jh + 200} {j["x"] - 300},{top + jh + 200} {j["x"]},{top + jh + 64}" stroke="{GOLD}" stroke-width="5" '
                             f'fill="none" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
                D.js.append(f'tl.to("#ph",{{opacity:1,duration:.3}},{t:.2f});')
                D.js.append(f'tl.to("#{lid}",{{strokeDashoffset:0,duration:.8,ease:"power2.inOut"}},{t:.2f});')
                D.js.append(f'tl.fromTo("#ph",{{scale:.62}},{{scale:.7,duration:.3,yoyo:true,repeat:1}},{t + .8:.2f});')
                D.js.append(f'tl.fromTo("#j{act["link"]}lb",{{scale:1}},{{scale:1.15,color:"{GOLD}",duration:.3,yoyo:true,repeat:1}},{t + .8:.2f});')
                extra.append(lid)
            if "note" in act:
                i = _txt(D, 1840, 100, H.escape(act["note"]), 22, MUTED, anchor="r")
                _show(D, i, t, 0)


def register():
    from . import hybrid, explain
    hybrid.RENDER["pricewalk"] = explain._themed(s_pricewalk)
    hybrid.RENDER["standoff"] = explain._themed(s_standoff)
    hybrid.RENDER["giveback"] = explain._themed(s_giveback)
    hybrid.RENDER["lifecost"] = explain._themed(s_lifecost)
    hybrid.RENDER["profitbar"] = explain._themed(s_profitbar)
    hybrid.RENDER["pqbox"] = explain._themed(s_pqbox)
    hybrid.RENDER["samend"] = explain._themed(s_samend)
