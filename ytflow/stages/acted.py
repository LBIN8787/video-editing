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
                D.items.append(f'<div id="{rid}" style="position:absolute;left:460px;top:880px;width:1000px;height:120px;opacity:0">'
                               f'<div style="position:absolute;left:0;right:0;top:58px;height:4px;background:repeating-linear-gradient(90deg,#9AA6AE 0 30px,transparent 30px 54px)"></div>'
                               f'<div style="position:absolute;left:0;top:30px"><div id="{rid}a" style="font-size:58px"><span style="display:inline-block;transform:scaleX(-1)">🚗</span></div></div>'
                               f'<div style="position:absolute;right:0;top:30px"><div id="{rid}b" style="font-size:58px">🚗</div></div>'
                               f'<div style="position:absolute;left:50%;top:-34px;transform:translateX(-50%);font-family:heavy;font-size:48px;color:{GOLD};white-space:nowrap">{H.escape(act["chicken"])}</div></div>')
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


def register():
    from . import hybrid, explain
    hybrid.RENDER["pricewalk"] = explain._themed(s_pricewalk)
    hybrid.RENDER["standoff"] = explain._themed(s_standoff)
