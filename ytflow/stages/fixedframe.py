"""고정 틀 비교 `fixedframe` — 같은 틀에서 한 가지만 바뀐다 (docs/67 R2-1: EBS 〈자본주의〉 '같은 ₩3000, 줄어드는 생선').

틀(탁자·표지판·물건)은 처음부터 끝까지 그대로이고, 표지판의 날짜·값이 넘어가며 물건의 높이만 바뀐다.
지나간 값(또는 기준 값)은 점선 윤곽으로 남겨 '지금'과 맞댄다. 카메라는 움직이지 않는다 — 숫자 장면(v31).

언제 고르나: 같은 대상의 시점 비교(주가·값·물량이 날짜마다). 대상이 여럿이면 bars, 계산 하나면 bignum.
높이는 값에 비례(0 기준) — 값의 차이를 과장하지 않으려고 축을 자르지 않는다.

hybrid.json:
  {"type": "fixedframe", "title": "...", "label": "출처 ...", "subject": "엔비디아 주가", "icon": "chip",
   "states": {"fri": {"date": "11월 20일 (금)", "value": 125.53, "text": "125.53달러"}, ...},
   "beats": [{"say": "...", "do": [{"set": "fri", "t": "금요일"}, {"set": "mon", "t": "165.05", "sub": "+31.48%"},
                                     {"ghost": "peak", "t": "239.24", "note": "아직 −31%"},
                                     {"calc": "(165.05 − 125.53) × 241.86억 주", "value": "약 9,560억 달러", "t": "9,560억"}]}]}
"""
from __future__ import annotations

import html as H

from .docu import _when

CREAM, INK_D, GOLD = "#EDE6D6", "#14171A", "#F0BE5A"
X0, BASE, HMAX = 960, 870, 430      # 물건 가운데·탁자 높이·가장 큰 값의 높이


def s_fixed(D, sc: dict, bt: list, dur: float):
    from . import explain
    sc = dict(sc)
    sc.setdefault("theme", "dark")
    explain._setup(D, sc, title=False)
    js = D.js
    if sc.get("title"):
        tid = D._id()
        D.items.append(f'<div id="{tid}" style="position:absolute;left:150px;top:86px;font-family:heavy;font-size:44px;color:#E9EEF0;opacity:0">'
                       f'{H.escape(sc["title"])}</div>')
        js.append(f'tl.fromTo("#{tid}",{{opacity:0,x:-18}},{{opacity:1,x:0,duration:.45}},0.15);')
    states = sc.get("states", {})
    vmax = max(abs(s["value"]) for s in states.values()) or 1
    keys = list(states)

    # 표지판: 날짜 칸 | 값 칸 — 상태마다 글자를 겹쳐 두고 넘김
    sign = D._id()
    cells = {"date": (520, [states[k]["date"] for k in keys]), "val": (440, [states[k]["text"] for k in keys])}
    cap = {"date": "날짜", "val": sc.get("subject", "값")}
    sx = X0 - (520 + 440 + 24) / 2
    html_cells = []
    for name, (w, texts) in cells.items():
        spans = "".join(f'<div id="{sign}{name}{j}" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;'
                        f'font-family:heavy;font-size:58px;color:{CREAM};opacity:0;backface-visibility:hidden">{H.escape(t)}</div>'
                        for j, t in enumerate(texts))
        html_cells.append(f'<div style="position:absolute;left:{sx:.0f}px;top:220px;width:{w}px;height:110px;perspective:600px">'
                          f'<div style="position:absolute;left:0;top:-40px;font-family:sans-x;font-size:26px;color:#9AA6AE">{H.escape(cap[name])}</div>'
                          f'<div style="position:absolute;inset:0;border-radius:10px;background:linear-gradient(180deg,#232A30,#161B1F);'
                          f'box-shadow:inset 0 -2px 0 #0A0C0D,0 8px 24px rgba(0,0,0,.45)"></div>'
                          f'<div style="position:absolute;left:0;right:0;top:54px;height:2px;background:#0A0C0D;opacity:.7"></div>{spans}</div>')
        sx += w + 24
    D.items.append("".join(html_cells))
    sub = D._id()
    D.items.append(f'<div id="{sub}" style="position:absolute;left:{X0 + 256:.0f}px;top:340px;transform:translateX(-50%);font-family:heavy;'
                   f'font-size:34px;color:#4FCB86;opacity:0"></div>')

    # 탁자와 물건 (높이 = 값 비례, 아래 기준)
    D.items.append(f'<div style="position:absolute;left:{X0 - 470}px;top:{BASE}px;width:940px;height:3px;background:linear-gradient(90deg,transparent,#6B7480 15%,#6B7480 85%,transparent)"></div>')
    obj = D._id()
    icon = explain._chip(HMAX, f"ff{sc.get('id', 0)}") if sc.get("icon", "chip") == "chip" else ""
    D.items.append(f'<div id="{obj}" style="position:absolute;left:{X0 - HMAX / 2:.0f}px;top:{BASE - HMAX:.0f}px;width:{HMAX}px;height:{HMAX}px;'
                   f'transform-origin:50% 100%;transform:scale(0);filter:drop-shadow(0 14px 22px rgba(0,0,0,.55))">{icon}</div>')
    ghosts = {}
    for k in keys:
        gid = D._id()
        s_ = abs(states[k]["value"]) / vmax
        hh = HMAX * s_
        # 지나간 값: 같은 물건을 같은 비율로 흐리게 (네모 윤곽이면 그림과 모양이 달라 크기 비교가 어긋남)
        D.items.append(f'<div id="{gid}" style="position:absolute;left:{X0 - HMAX / 2:.0f}px;top:{BASE - HMAX:.0f}px;width:{HMAX}px;height:{HMAX}px;'
                       f'transform-origin:50% 100%;transform:scale({s_:.4f});opacity:0;filter:grayscale(1) brightness(1.5)">{icon}</div>')
        lid = D._id()
        D.items.append(f'<div id="{lid}" style="position:absolute;left:{X0 + hh * 0.46 + 24:.0f}px;top:{BASE - hh * 0.94:.0f}px;font-family:sans-x;font-size:28px;'
                       f'color:#C9D0D5;white-space:nowrap;opacity:0">{H.escape(states[k]["date"])} · {H.escape(states[k]["text"])}'
                       f'<div id="{lid}n" style="font-family:heavy;font-size:36px;color:{GOLD};margin-top:4px"></div></div>')
        ghosts[k] = (gid, lid)

    cur = None
    note_y = 470
    for k, (b, (t0, d)) in enumerate(zip(sc.get("beats", []), bt)):
        seq = t0 + 0.2
        for act in b.get("do") or []:
            t = _when(sc, k, b, t0, d, act.get("t"), seq)
            seq = max(seq, t) + 0.5
            if "set" in act and act["set"] in states:
                j = keys.index(act["set"])
                for name in cells:
                    if cur is not None:
                        js.append(f'tl.to("#{sign}{name}{cur}",{{rotationX:90,opacity:0,duration:.18,ease:"power1.in"}},{t:.2f});')
                    js.append(f'tl.fromTo("#{sign}{name}{j}",{{rotationX:-90,opacity:0}},{{rotationX:0,opacity:1,duration:.3,ease:"power2.out"}},{t + 0.16:.2f});')
                scale = abs(states[act["set"]]["value"]) / vmax
                js.append(f'tl.to("#{obj}",{{scale:{scale:.4f},duration:.7,ease:"power3.out"}},{t + 0.1:.2f});')
                js.append(f'tl.set("#{sub}",{{textContent:{H.escape(act.get("sub", ""))!r},opacity:{1 if act.get("sub") else 0}}},{t + 0.4:.2f});')
                D.sfx.append(("click-soft", t))
                cur = j
            if "ghost" in act and act["ghost"] in ghosts:
                gid, lid = ghosts[act["ghost"]]
                js.append(f'tl.fromTo("#{gid}",{{opacity:0}},{{opacity:.22,duration:.5}},{t:.2f});')
                js.append(f'tl.fromTo("#{lid}",{{opacity:0,x:-10}},{{opacity:1,x:0,duration:.4}},{t + 0.2:.2f});')
                if act.get("note"):
                    js.append(f'tl.set("#{lid}n",{{textContent:{H.escape(act["note"])!r}}},{t + 0.2:.2f});')
                D.sfx.append(("pop", t))
            if "calc" in act:
                cid = D._id()
                D.items.append(f'<div id="{cid}" style="position:absolute;left:150px;top:{note_y}px;width:520px;opacity:0">'
                               f'<div style="font-family:sans-x;font-size:28px;color:#9AA6AE">{H.escape(act["calc"])}</div>'
                               f'<div style="font-family:heavy;font-size:54px;color:{GOLD};margin-top:6px">{H.escape(act.get("value", ""))}</div>'
                               + (f'<div style="font-family:sans-x;font-size:24px;color:#7C8590;margin-top:2px">{H.escape(act["tag"])}</div>' if act.get("tag") else "")
                               + "</div>")
                js.append(f'tl.fromTo("#{cid}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.45}},{t:.2f});')
                note_y += 190
                D.sfx.append(("pop", t))


def register():
    from . import hybrid, explain
    hybrid.RENDER["fixedframe"] = explain._themed(s_fixed)
