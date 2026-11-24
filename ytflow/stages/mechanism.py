"""설명 애니메이션 (mechanism) — 원리를 움직임으로 보여 준다 (3b1b 식, 2026-11-24 사용자:
"트랜스포머 등을 서술 할 때 글로만 하면 이해하기 힘들고 지루하지만 모션그래픽을 잘 사용하면 한눈에 들어오듯이요 … 3b1b 등" ·
"설명을 할 때 모션그래픽으로 시각화로 잘 설명하거나 지루하지 않도록 잘 보여주고싶은거에요").

원칙 (docs/64 §설명 애니메이션):
  1. 한 장면 = 한 장치. 등장한 사물은 끝까지 화면에 남고, 바뀔 때는 사라지지 않고 **변한다**(채워지고·흐르고·끊기고·식는다).
  2. 대본의 동사가 곧 움직임 — 각 단계(cue)는 그 낱말을 말하는 순간 시작.
  3. 색은 뜻이 하나: 돈·현금 = 초록, 주문·칩 = 주황, 위험·손실 = 빨강, 꺼진 것 = 회색.
  4. 숫자는 그것이 가리키는 사물에 붙는다 (막대 끝·노드 옆).
  5. 카메라는 고정 (v31). 움직이는 것은 사물.

kind "loop" — 파는 쪽이 사는 쪽에 돈을 대고, 그 돈이 주문이 되어 돌아오는 고리 (벤더 파이낸싱·순환금융).
  "mechanism": {
    "kind": "loop",
    "seller": "엔비디아", "buyer": "AI 회사·네오클라우드", "rival": "다른 칩 회사",
    "money_label": "지분·보증·임대", "order_label": "칩 주문 = 매출",
    "guarantee": "보증 최대 1,050억 달러", "loss": ["받을 칩값", "넣은 투자금"],
    "cues": {"need": "…", "burn": "…", "debt": "…", "cash": "…", "fund": "…", "order": "…",
             "guarantee": "…", "lockin": "…", "real": "…", "fail": "…", "loss": "…", "orders_gone": "…"}
  }
cue 에 없는 단계는 그리지 않는다. 낱말은 그 장면 박자의 대사에서 찾는다.
"""
from __future__ import annotations

import html as H
import math

GREEN, ORANGE, RED, GREY, INK, MUTED = "#3DDC97", "#F2A93B", "#FF6B5E", "#5C6370", "#E8EEF6", "#9AA4B2"


def _e(s) -> str:
    return H.escape(str(s))


def _cue_times(sc: dict, bt: list) -> dict:
    from . import motion2
    out = {}
    cues = (sc.get("mechanism") or {}).get("cues") or {}
    for name, word in cues.items():
        for k, (b, (t0, d)) in enumerate(zip(sc["beats"], bt)):
            if word and word in (b.get("say") or ""):
                t = motion2.row_time(sc, k, b, t0, d, word) if sc.get("_project_dir") else None
                out[name] = max(t0, (t if t is not None else t0 + 0.3) - 0.1)
                break
    return out


def _qbez(p0, p1, p2, n=14):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


def _travel(D, el_id: str, pts: list, start: float, dur: float, ox: float, oy: float):
    """사물 하나가 점들을 따라 한 번 지나감 (GSAP keyframes, x·y 는 처음 자리 기준)."""
    seg = dur / (len(pts) - 1)
    kf = ",".join(f'{{x:{x - ox:.0f},y:{y - oy:.0f},duration:{seg:.3f},ease:"none"}}' for x, y in pts[1:])
    D.js.append(f'tl.set("#{el_id}",{{x:{pts[0][0] - ox:.0f},y:{pts[0][1] - oy:.0f},opacity:1}},{start:.2f});'
                f'tl.to("#{el_id}",{{keyframes:[{kf}]}},{start:.2f});'
                f'tl.set("#{el_id}",{{opacity:0}},{start + dur:.2f});')


def _node(D, x, y, r, label, sub, color, at, nid=None):
    i = nid or D._id()
    D.items.append(
        f'<div id="{i}" style="position:absolute;left:{x - r:.0f}px;top:{y - r:.0f}px;width:{2 * r}px;height:{2 * r}px;border-radius:50%;'
        f'border:6px solid {color};background:rgba(20,26,36,.92);box-shadow:0 0 40px {color}33;opacity:0;display:flex;align-items:center;'
        f'justify-content:center;flex-direction:column;text-align:center">'
        f'<div style="font-family:heavy,sans-x;font-size:{40 if len(label) <= 5 else (30 if len(label) <= 8 else 24)}px;color:{INK};line-height:1.2;padding:0 16px;word-break:keep-all">{_e(label)}</div>'
        + (f'<div style="font-family:sans,sans-x;font-size:24px;color:{MUTED};margin-top:6px">{_e(sub)}</div>' if sub else "")
        + '</div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.5,ease:"back.out(1.8)"}},{at:.2f});')
    D.sfx.append(("pop", at))
    return i


def _bar(D, x, y_bottom, w, h_full, color, label, at, frac_from=0.0, frac_to=1.0, dur=0.9):
    """아래에서 위로 차는 막대 (통). 반환: (막대 id, 채움 id)."""
    i, f = D._id(), D._id()
    D.items.append(
        f'<div id="{i}" style="position:absolute;left:{x:.0f}px;top:{y_bottom - h_full:.0f}px;width:{w}px;height:{h_full}px;'
        f'border:3px solid {color}88;border-radius:8px;opacity:0;overflow:hidden">'
        f'<div id="{f}" style="position:absolute;left:0;right:0;bottom:0;height:100%;background:{color};transform-origin:bottom;transform:scaleY({frac_from})"></div></div>'
        f'<div id="{i}l" style="position:absolute;left:{x + w / 2 - 50:.0f}px;top:{y_bottom + 10:.0f}px;width:100px;text-align:center;white-space:nowrap;'
        f'font-family:sans-x,sans;font-size:26px;color:{MUTED};opacity:0">{_e(label)}</div>')
    D.js.append(f'tl.to("#{i},#{i}l",{{opacity:1,duration:0.3}},{at:.2f});'
                f'tl.fromTo("#{f}",{{scaleY:{frac_from}}},{{scaleY:{frac_to},duration:{dur},ease:"power2.out"}},{at + 0.1:.2f});')
    return i, f


def _tag(D, x, y, text, color, at, size=34, anchor="mm"):
    i = D._id()
    tx = {"m": "-50%", "l": "0", "r": "-100%"}[anchor[0]]
    D.items.append(f'<div id="{i}" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;transform:translate({tx},-50%);white-space:nowrap;'
                   f'font-family:sans-x,sans;font-size:{size}px;color:{color};opacity:0">{_e(text)}</div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.35}},{at:.2f});')
    return i


def _arc_svg(D, pts, color, width, at, dashed=False):
    i = D._id()
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    D.svg.append(f'<path id="{i}" d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
                 f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" opacity="0.55"/>')
    D.js.append(f'tl.to("#{i}",{{strokeDashoffset:0,duration:0.7,ease:"power2.inOut"}},{at:.2f});')
    return i


def s_mechanism(D, sc: dict, bt: list, dur: float):
    from .explain import _setup
    _setup(D, sc, title=False)
    m = sc.get("mechanism") or {}
    kind = m.get("kind", "loop")
    if kind == "loop":
        _loop(D, sc, bt, dur, m)
    elif kind == "tank":
        _tank(D, sc, bt, dur, m)


def _card(D, sc, key, x, y, el, at):
    """설명 무대의 흰 카드 그대로 (아이콘 + 굵은 이름) — 2026-11-24 사용자: 애니메이션은 좋은데 '퀄리티나 직관성이 기존보다 떨어진다'."""
    from .explain import _el_html
    inner, w, h = _el_html(D, sc, key, dict(el, kind="card"))
    i = D._id()
    D.items.append(f'<div id="{i}" style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;opacity:0;z-index:5">{inner}</div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:-30,scale:0.86}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(1.7)"}},{at:.2f});')
    D.sfx.append(("click-soft", at))
    return i, w, h


def _caption(D, steps: list):
    """화면 위 가운데 '지금 무슨 단계인가' 한 줄 — 단계가 바뀌면 글이 바뀐다 (설명 글을 화면 여기저기 흩지 않음)."""
    for k, (t, text) in enumerate(steps):
        i = D._id()
        D.items.append(f'<div id="{i}" style="position:absolute;left:0;right:0;top:92px;text-align:center;opacity:0;z-index:8">'
                       f'<span style="display:inline-block;padding:10px 26px;border-radius:40px;background:rgba(10,12,16,.72);border:2px solid rgba(255,255,255,.16);'
                       f'font-family:heavy,sans-x;font-size:46px;color:#F4F1EA;white-space:nowrap">{_e(text)}</span></div>')
        D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{t:.2f});')
        if k + 1 < len(steps):
            D.js.append(f'tl.to("#{i}",{{opacity:0,y:-12,duration:0.25}},{steps[k + 1][0] - 0.25:.2f});')


def _coin(D, x, y, size=60):
    i = D._id()
    D.items.append(f'<div id="{i}" style="position:absolute;left:{x - size / 2:.0f}px;top:{y - size / 2:.0f}px;width:{size}px;height:{size}px;border-radius:50%;'
                   f'background:radial-gradient(circle at 35% 30%,#FFE79A,#F2C14E 55%,#C9921E);border:3px solid #9C6E12;box-shadow:0 4px 10px rgba(0,0,0,.4);'
                   f'display:flex;align-items:center;justify-content:center;font-family:heavy,sans-x;font-size:{size * 0.55:.0f}px;color:#6B4A08;opacity:0;z-index:7">$</div>')
    return i


def _chiptok(D, x, y, size=66):
    from .icons import svg_markup
    i = D._id()
    D.items.append(f'<div id="{i}" style="position:absolute;left:{x - size / 2:.0f}px;top:{y - size / 2:.0f}px;width:{size}px;height:{size}px;border-radius:8px;'
                   f'background:linear-gradient(180deg,#FFFEFB,#F1EEE6);box-shadow:0 4px 10px rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center;opacity:0;z-index:7">'
                   f'{svg_markup("microchip", int(size * 0.7), "#1E2330") or ""}</div>')
    return i


def _arc_label(D, x, y, text, color, at, size=36):
    i = D._id()
    D.items.append(f'<div id="{i}" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;transform:translate(-50%,-50%);white-space:nowrap;padding:4px 14px;'
                   f'border-radius:8px;background:rgba(10,12,16,.6);font-family:sans-x,sans;font-size:{size}px;color:{color};opacity:0;z-index:6">{_e(text)}</div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:0.35}},{at:.2f});')
    return i


def _hbar(D, x, y, w, h, color, label, at, hatch=False):
    i = D._id()
    bg = f"repeating-linear-gradient(45deg,{color},{color} 12px,#8E2420 12px,#8E2420 24px)" if hatch else color
    D.items.append(f'<div id="{i}" style="position:absolute;left:{x:.0f}px;top:{y - h / 2:.0f}px;width:{w:.0f}px;height:{h}px;border-radius:6px;background:{bg};'
                   f'transform-origin:left;transform:scaleX(0);display:flex;align-items:center;padding-left:14px;box-sizing:border-box;'
                   f'font-family:sans-x,sans;font-size:30px;color:#10141B;white-space:nowrap">{_e(label)}</div>')
    D.js.append(f'tl.to("#{i}",{{scaleX:1,duration:0.7,ease:"power3.out"}},{at:.2f});')
    return i


def _x_mark(D, x, y, at):
    i = D._id()
    D.items.append(f'<div id="{i}" style="position:absolute;left:{x - 45:.0f}px;top:{y - 50:.0f}px;width:90px;height:100px;font-family:heavy,sans-x;'
                   f'font-size:96px;line-height:100px;text-align:center;color:{RED};opacity:0;z-index:9">✕</div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:2.4}},{{opacity:1,scale:1,duration:0.3,ease:"power4.in"}},{at:.2f});')
    return i


def _loop(D, sc, bt, dur, m):
    """돈이 고리를 돈다: 파는 쪽 → (돈) → 사는 쪽 → (칩 주문) → 파는 쪽. 카드는 설명 무대의 흰 카드."""
    from .icons import svg_markup
    T = _cue_times(sc, bt)
    first = bt[0][0] + 0.2
    S, B = (1400, 440), (520, 440)
    steps = sorted((T[k], v) for k, v in (m.get("steps") or {}).items() if k in T)
    if steps:
        _caption(D, steps)
    s_id, sw, sh = _card(D, sc, "seller", *S, {"icon": m.get("seller_icon", "cpu"), "label": m.get("seller", "파는 쪽"), "w": 300}, first)
    b_id, bw, bh = _card(D, sc, "buyer", *B, {"icon": m.get("buyer_icon", "building-2"), "label": m.get("buyer", "사는 쪽"), "w": 340, "size": 40},
                         T.get("need", first + 0.5))
    # 사는 쪽 아래: 버는 돈 < 쓰는 돈, 모자란 만큼 빚
    bx0 = B[0] - 210
    t_burn = T.get("burn", T.get("need", first) + 1.5)
    _hbar(D, bx0, 720, 170, 54, GREEN, "버는 돈", t_burn)
    _hbar(D, bx0, 792, 420, 54, "#FF8A7E", "쓰는 돈", t_burn + 0.5)
    if "debt" in T:
        _hbar(D, bx0 + 174, 720, 246, 54, RED, "", T["debt"], hatch=True)
        _arc_label(D, bx0 + 297, 862, "모자란 만큼 = 빚", RED, T["debt"] + 0.4, 32)
    # 파는 쪽 아래: 쌓인 현금(동전 더미)
    pile = []
    if "cash" in T:
        for k in range(15):
            cx, cy = S[0] - 120 + (k % 5) * 58, 870 - (k // 5) * 50
            c = _coin(D, cx, cy, 54)
            pile.append(c)
            D.js.append(f'tl.fromTo("#{c}",{{opacity:0,y:-120}},{{opacity:1,y:0,duration:0.35,ease:"bounce.out",immediateRender:false}},{T["cash"] + k * 0.06:.2f});')
        _arc_label(D, S[0] - 4, 690, "엔비디아의 현금", GREEN, T["cash"] + 0.4, 30)
    # 고리
    p_money = _qbez((S[0] - sw / 2 - 10, S[1] - 40), (960, 60), (B[0] + bw / 2 + 10, B[1] - 40), 16)
    p_order = _qbez((B[0] + bw / 2 + 10, B[1] + 50), (960, 830), (S[0] - sw / 2 - 10, S[1] + 50), 16)
    t_fund, t_fail = T.get("fund"), T.get("fail", 1e9)
    t_order = T.get("order", (t_fund + 2.5) if t_fund else None)
    rev_f = None
    if t_fund:
        _arc_svg(D, p_money, GREEN, 10, t_fund)
        _arc_label(D, 960, 210, m.get("money_label", "돈을 댄다"), GREEN, t_fund + 0.3)
    if t_order:
        _arc_svg(D, p_order, ORANGE, 10, t_order)
        _arc_label(D, 960, 722, m.get("order_label", "주문 = 매출"), ORANGE, t_order + 0.3)
        rb = D._id()
        D.items.append(f'<div id="{rb}" style="position:absolute;left:{S[0] + 200}px;top:330px;width:76px;height:220px;border:3px solid {ORANGE}99;border-radius:8px;overflow:hidden;opacity:0">'
                       f'<div id="{rb}f" style="position:absolute;left:0;right:0;bottom:0;height:100%;background:{ORANGE};transform-origin:bottom;transform:scaleY(0.08)"></div></div>')
        _arc_label(D, S[0] + 238, 580, "매출", ORANGE, t_order + 0.5, 30)
        D.js.append(f'tl.to("#{rb}",{{opacity:1,duration:0.3}},{t_order + 0.4:.2f});')
        rev_f = f"{rb}f"
    if t_fund:
        end = min(t_fail, bt[-1][0] + bt[-1][1]) - 0.2
        period, travel = 1.6, 1.4
        coins = [_coin(D, p_money[0][0], p_money[0][1]) for _ in range(3)]
        chips = [_chiptok(D, p_order[0][0], p_order[0][1]) for _ in range(3)]
        t, n, rv = t_fund + 0.6, 0, 0.08
        while t + travel < end and n < 40:
            _travel(D, coins[n % 3], p_money, t, travel, p_money[0][0], p_money[0][1])
            if pile and n < len(pile) - 8:   # 동전 하나가 더미에서 빠져나감
                D.js.append(f'tl.to("#{pile[-1 - n]}",{{opacity:0,y:-30,duration:0.3}},{t:.2f});')
            if t_order and t + travel >= t_order:
                _travel(D, chips[n % 3], p_order, t + travel, travel, p_order[0][0], p_order[0][1])
                rv = min(0.95, rv + 0.09)
                D.js.append(f'tl.to("#{rev_f}",{{scaleY:{rv:.2f},duration:0.3}},{t + 2 * travel:.2f});'
                            f'tl.fromTo("#{s_id}",{{scale:1}},{{scale:1.05,duration:0.12,yoyo:true,repeat:1,immediateRender:false}},{t + 2 * travel:.2f});')
            t += period
            n += 1
    # 보증: 사는 쪽 카드에 방패 + 점선 테두리
    if "guarantee" in T:
        tg = T["guarantee"]
        g = D._id()
        D.items.append(f'<div id="{g}" style="position:absolute;left:{B[0] - bw / 2 - 22:.0f}px;top:{B[1] - bh / 2 - 22:.0f}px;width:{bw + 44:.0f}px;height:{bh + 44:.0f}px;'
                       f'border:6px dashed {GREEN};border-radius:16px;opacity:0;z-index:4"></div>')
        sh_ = D._id()
        D.items.append(f'<div id="{sh_}" style="position:absolute;left:{B[0] - bw / 2 - 60:.0f}px;top:{B[1] - bh / 2 - 60:.0f}px;width:96px;height:96px;border-radius:50%;'
                       f'background:#15392A;border:4px solid {GREEN};display:flex;align-items:center;justify-content:center;opacity:0;z-index:9">'
                       f'{svg_markup("shield-check", 60, GREEN) or ""}</div>')
        D.js.append(f'tl.fromTo("#{g}",{{opacity:0,scale:1.15}},{{opacity:1,scale:1,duration:0.5,ease:"power3.out"}},{tg:.2f});'
                    f'tl.fromTo("#{sh_}",{{opacity:0,scale:2,rotation:-30}},{{opacity:1,scale:1,rotation:0,duration:0.4,ease:"back.out(2)"}},{tg + 0.2:.2f});')
        D.sfx.append(("pop", tg + 0.2))
    # 묶어 두기: 다른 칩 회사의 길이 막힘
    if "lockin" in T:
        tl_ = T["lockin"]
        r_id, rw, rh = _card(D, sc, "rival", 150, B[1], {"icon": "factory", "label": m.get("rival", "다른 회사"), "w": 190, "size": 28}, tl_)
        D.js.append(f'tl.to("#{r_id}",{{opacity:0.5,filter:"grayscale(1)",duration:0.4}},{tl_ + 1.0:.2f});')
        _arc_svg(D, [(150 + rw / 2 + 6, B[1]), (B[0] - bw / 2 - 30, B[1])], GREY, 8, tl_ + 0.3)
        _x_mark(D, (150 + rw / 2 + B[0] - bw / 2) / 2, B[1], tl_ + 0.8)
    # 무너지면: 사는 쪽 카드가 기울고 꺼짐, 주문 길이 끊김, 파는 쪽은 두 번 잃음
    if "fail" in T:
        tf = T["fail"]
        D.js.append(f'tl.to("#{b_id}",{{rotation:-9,y:40,filter:"grayscale(1) brightness(.7)",duration:0.6,ease:"power2.in"}},{tf:.2f});')
        D.js.append(f'tl.to("svg path",{{stroke:"{GREY}",duration:0.4}},{tf + 0.4:.2f});')
        mx, my = p_order[4]
        _x_mark(D, mx, my, tf + 0.5)
        D.sfx.append(("whoosh", tf))
        t_loss = T.get("loss", tf + 1.2)
        for k, lab in enumerate(m.get("loss") or []):   # 손실은 더미 위에 빨간 카드로 — 동전이 그만큼 사라짐
            li = D._id()
            D.items.append(f'<div id="{li}" style="position:absolute;left:{S[0] - 190:.0f}px;top:{720 + k * 74:.0f}px;width:380px;height:62px;border-radius:8px;'
                           f'background:#B5302A;color:#fff;font-family:heavy,sans-x;font-size:36px;display:flex;align-items:center;justify-content:center;opacity:0;z-index:9">− {_e(lab)}</div>')
            D.js.append(f'tl.fromTo("#{li}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.35,ease:"power3.out"}},{t_loss + k * 0.7:.2f});')
            for c in pile[k * 4:(k + 1) * 4]:
                D.js.append(f'tl.to("#{c}",{{opacity:0,y:30,duration:0.3}},{t_loss + k * 0.7 + 0.2:.2f});')
        if "orders_gone" in T and rev_f:
            D.js.append(f'tl.to("#{rev_f}",{{scaleY:0.1,background:"{GREY}",duration:0.8}},{T["orders_gone"]:.2f});')


def _tank(D, sc, bt, dur, m):
    """통장(물통): 돈은 크게 먼저 퍼 가고(약속), 매출은 위에서 조금씩·점점 굵게 들어온다. 모자라면 밖에서 구한 돈이 채운다.
    아하: 매출 물줄기는 굵어지는데 다음 약속이 더 크게 퍼 가서 통장이 다시 바닥난다 (오픈AI '매출이 느는데 왜 모자라나')."""
    T = _cue_times(sc, bt)
    first = bt[0][0] + 0.2
    end = bt[-1][0] + bt[-1][1]
    steps = sorted((T[k], v) for k, v in (m.get("steps") or {}).items() if k in T)
    if steps:
        _caption(D, steps)
    X0, X1, TOP, BOT = 760, 1160, 260, 820      # 통장 안쪽
    ZERO = 740                                   # 이 아래는 '모자람'
    # 통장 그릇 · 바닥 아래 빨간 구역 · '0' 선
    tank, water, red = D._id(), D._id(), D._id()
    D.items.append(
        f'<div id="{tank}" style="position:absolute;left:{X0 - 10}px;top:{TOP}px;width:{X1 - X0 + 20}px;height:{BOT - TOP + 10}px;border:8px solid #E8EEF6;'
        f'border-top:none;border-radius:0 0 26px 26px;opacity:0;z-index:5"></div>'
        f'<div id="{red}" style="position:absolute;left:{X0 - 2}px;top:{ZERO}px;width:{X1 - X0 + 4}px;height:{BOT - ZERO + 2}px;'
        f'background:repeating-linear-gradient(45deg,{RED}55,{RED}55 12px,transparent 12px,transparent 24px);border-radius:0 0 20px 20px;opacity:0;z-index:3"></div>'
        f'<div id="{water}" style="position:absolute;left:{X0 - 2}px;top:{TOP}px;width:{X1 - X0 + 4}px;height:{BOT - TOP + 2}px;background:linear-gradient(180deg,#5FE3A8,#2BAF78);'
        f'border-radius:0 0 20px 20px;transform-origin:bottom;transform:scaleY(0);opacity:.92;z-index:4"></div>')
    lvl = lambda y: (BOT - y) / (BOT - TOP)     # 화면 높이 → 물 비율
    D.js.append(f'tl.to("#{tank}",{{opacity:1,duration:0.4}},{first:.2f});'
                f'tl.to("#{water}",{{scaleY:{lvl(520):.3f},duration:0.8,ease:"power2.out"}},{first + 0.2:.2f});')
    _arc_label(D, (X0 + X1) / 2, BOT + 40, m.get("tank_label", "통장 (현금)"), INK, first + 0.3, 34)
    zl = D._id()
    D.items.append(f'<div id="{zl}" style="position:absolute;left:{X0 - 70}px;top:{ZERO - 2}px;width:{X1 - X0 + 140}px;height:0;border-top:4px dashed {RED};opacity:0;z-index:6"></div>')
    D.js.append(f'tl.to("#{zl}",{{opacity:1,duration:0.3}},{first + 0.4:.2f});')
    _arc_label(D, X0 - 130, ZERO + 30, m.get("zero_label", "바닥"), RED, first + 0.5, 30)
    level = [520.0]

    def set_level(y, at, d=0.7):
        level[0] = y
        D.js.append(f'tl.to("#{water}",{{scaleY:{max(0.0, lvl(y)):.3f},duration:{d},ease:"power2.inOut"}},{at:.2f});')
        if y >= ZERO - 4:
            D.js.append(f'tl.to("#{red}",{{opacity:1,duration:0.3}},{at + d * 0.6:.2f});'
                        f'tl.set("#{water}",{{background:"linear-gradient(180deg,#FF8A7E,#C9463B)"}},{at + d * 0.6:.2f});')
        else:
            D.js.append(f'tl.to("#{red}",{{opacity:0,duration:0.3}},{at:.2f});'
                        f'tl.set("#{water}",{{background:"linear-gradient(180deg,#5FE3A8,#2BAF78)"}},{at:.2f});')

    # 위: 매출 수도꼭지 (구독료·사용료) — 물줄기가 시간이 갈수록 굵어짐
    t_in = T.get("in")
    stream = None
    if t_in:
        _card(D, sc, "faucet", 450, 330, {"icon": m.get("in_icon", "credit-card"), "label": m.get("in_label", "매출"), "w": 300, "size": 34}, t_in)
        stream = D._id()
        D.svg.append(f'<path id="{stream}" d="M600 330 Q 900 300 900 {TOP + 150}" fill="none" stroke="#5FE3A8" stroke-width="6" '
                     f'stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
        D.js.append(f'tl.to("#{stream}",{{strokeDashoffset:0,duration:0.6,ease:"power2.out"}},{t_in + 0.2:.2f});')
        _arc_label(D, 450, 450, m.get("in_note", "매달 조금씩"), GREEN, t_in + 0.4, 30)

    # 오른쪽: 퍼 가는 약속 — 카드 크기가 1배·2배·4배, 통장 바닥에서 화살표로 빠져나감
    outs = m.get("outs") or []
    ev = []
    for k, o in enumerate(outs):
        t = T.get(o.get("cue", ""))
        if t is None:
            continue
        y = 330 + k * 190
        w = 250 + k * 50
        cid, cw, ch = _card(D, sc, f"out{k}", 1560, y, {"icon": o.get("icon", "server"), "label": o["label"], "w": w, "size": 30 + k * 4}, t)
        _arc_svg(D, _qbez((X1 + 12, BOT - 60), (1300, y + 60), (1560 - cw / 2 - 12, y), 10), RED, 8 + k * 4, t + 0.2)
        ev.append((t + 0.5, "set", o["to"]) if o.get("to") else (t + 0.5, "drop", o.get("drop", 120)))
        D.sfx.append(("whoosh-short", t + 0.5))
        if stream and o.get("thicker"):
            D.js.append(f'tl.to("#{stream}",{{attr:{{"stroke-width":{6 + 7 * k}}},duration:0.6}},{t + 1.2:.2f});')

    # 매출이 들어오며 조금씩 차오름 (in 뒤로, 약속이 퍼 가는 순간은 건너뜀) — 약속이 하나 지날 때마다 물줄기가 굵어짐
    if t_in:
        cues_out = sorted(T[o["cue"]] for o in outs if o.get("cue") in T)
        t, k_out = t_in + 1.0, 0
        while t < end - 1.0:
            busy = [c for c in cues_out if c - 0.4 < t < c + 1.6]
            if busy:
                t = busy[0] + 1.6
                continue
            k_out = sum(1 for c in cues_out if c < t)
            ev.append((t, "rise_last" if cues_out and k_out == len(cues_out) else "rise", m.get("in_rate", 10) + m.get("in_growth", 8) * k_out))
            t += 1.2

    # 아래 왼쪽: 밖에서 구한 돈 — 동전이 쏟아져 통장을 채움
    t_ext = T.get("ext")
    if t_ext:
        _card(D, sc, "ext", 450, 640, {"icon": m.get("ext_icon", "landmark"), "label": m.get("ext_label", "밖에서 구한 돈"), "w": 300, "size": 32}, t_ext)
        for k in range(8):
            c = _coin(D, 640, 610, 50)
            D.js.append(f'tl.set("#{c}",{{opacity:1}},{t_ext + 0.4 + k * 0.12:.2f});'
                        f'tl.fromTo("#{c}",{{x:0,y:0}},{{keyframes:[{{x:{(X0 + X1) / 2 - 640 - 40 + k * 10:.0f},y:{-260 - (k % 3) * 20},duration:0.35,ease:"power1.out"}},'
                        f'{{y:{TOP + 60 - 610:.0f},duration:0.3,ease:"power2.in"}}],immediateRender:false}},{t_ext + 0.4 + k * 0.12:.2f});'
                        f'tl.to("#{c}",{{opacity:0,duration:0.15}},{t_ext + 1.1 + k * 0.12:.2f});')
        ev.append((t_ext + 1.2, "set", m.get("ext_level", 470)))
    for t, kind, v in sorted(ev):   # 시간 순서로 물 높이를 따라감
        if kind == "drop":
            set_level(min(BOT - 6, level[0] + v), t, 0.8)
        elif kind == "rise":
            set_level(max(TOP + 40, level[0] - v), t, 1.0)
        elif kind == "rise_last":   # 마지막 약속 뒤: 매출이 들어와도 바닥 위로는 못 올라옴 (결론: 그래도 모자라다)
            set_level(max(ZERO + 14, level[0] - v), t, 1.0)
        else:
            set_level(v, t, 0.9)

    # 끝: 한 줄 결론
    if "verdict" in T and m.get("verdict_text"):
        _arc_label(D, (X0 + X1) / 2, TOP - 60 + 0, m.get("verdict_text", ""), RED, T["verdict"], 36)


def gapline(D, sc: dict, bt: list):
    """기존 설명 무대 아래 빈자리에 '시간 줄' 하나만 더한다 (2026-11-24 사용자: "이전에 만든거에 살짝만 추가하는게 더 … 깔끔할거같아요").
    나가는 돈(빨강, 축 아래)은 크게 먼저, 들어오는 돈(초록, 축 위)은 작게 매달. 틈은 괄호 하나로, 글은 괄호에 붙는다.
      "gapline": {"cues": {"out1": "먼저", "in": "매출은", "gap": "틈이", "out2": "다음 모델이", "regap": "다시 벌립니다"},
                  "labels": {"out": "나가는 돈", "in": "들어오는 돈", "gap": "틈 = 밖에서 구할 돈", "regap": "더 큰 약속 → 틈이 다시 벌어진다"}}"""
    g = sc.get("gapline") or {}
    T = _cue_times(dict(sc, mechanism={"cues": g.get("cues") or {}}), bt)
    L = {"out": "나가는 돈", "in": "들어오는 돈", "gap": "틈 = 밖에서 구할 돈", "regap": "더 큰 약속 → 틈이 다시 벌어진다", **(g.get("labels") or {})}
    AX, XA, XB = 700, 220, 1700
    t0 = min([v for v in T.values()] or [bt[0][0] + 0.5])
    ax = D._id()
    D.items.append(f'<div id="{ax}" style="position:absolute;left:{XA}px;top:{AX - 2}px;width:{XB - XA}px;height:4px;background:#C9CED6;transform-origin:left;transform:scaleX(0);z-index:4"></div>')
    D.js.append(f'tl.to("#{ax}",{{scaleX:1,duration:0.6,ease:"power2.out"}},{t0:.2f});')
    _arc_label(D, XB + 70, AX, "시간 →", MUTED, t0 + 0.3, 28)

    def bar(x, h, up, color, at, w=46):
        i = D._id()
        top = AX - h if up else AX + 2
        D.items.append(f'<div id="{i}" style="position:absolute;left:{x - w / 2:.0f}px;top:{top:.0f}px;width:{w}px;height:{h:.0f}px;background:{color};'
                       f'border-radius:{"6px 6px 0 0" if up else "0 0 6px 6px"};transform-origin:{"bottom" if up else "top"};transform:scaleY(0);z-index:5"></div>')
        D.js.append(f'tl.to("#{i}",{{scaleY:1,duration:0.45,ease:"power3.out"}},{at:.2f});')
        return i

    def bracket(xa, xb, y, color, at, label, open_end=False):
        i = D._id()
        style = "dashed" if open_end else "solid"
        D.items.append(f'<div id="{i}" style="position:absolute;left:{xa:.0f}px;top:{y:.0f}px;width:{xb - xa:.0f}px;height:22px;border:5px {style} {color};border-bottom:none;'
                       f'border-radius:8px 8px 0 0;{"border-right:none;" if open_end else ""}transform-origin:left;transform:scaleX(0);z-index:6"></div>')
        D.js.append(f'tl.to("#{i}",{{scaleX:1,duration:0.6,ease:"power2.inOut"}},{at:.2f});')
        _arc_label(D, (xa + xb) / 2, y - 34, label, color, at + 0.4, 36)

    x_out1, h_out1 = 300, 120
    if "out1" in T:
        bar(x_out1, h_out1, False, RED, T["out1"], 90)
        _arc_label(D, x_out1, AX + h_out1 + 34, L["out"], RED, T["out1"] + 0.3, 30)
    # 들어오는 돈: 작게, 매달 하나씩 (점점 조금 커짐). 처음 약속을 따라잡는 곳에서 다음 약속.
    xs, catch = [], None
    if "in" in T:
        t_end_in = T.get("out2", bt[-1][0] + bt[-1][1]) - 0.3
        x, h, acc, k = x_out1 + 110, 16.0, 0.0, 0
        t = T["in"] + 0.3
        step = max(0.35, (t_end_in - t) / 8)
        while x < 1040 and t < t_end_in:
            bar(x, h, True, GREEN, t)
            acc += h
            if catch is None and acc >= h_out1:
                catch = x
            xs.append(x)
            x += 64
            h += 4
            t += step
        _arc_label(D, x_out1 + 200, AX + 36, L["in"], GREEN, T["in"] + 0.4, 28)
    if "gap" in T:
        bracket(x_out1 - 45, (catch or 1000) + 24, 560, RED, T["gap"], L["gap"])
    if "out2" in T:
        x2 = (xs[-1] + 100) if xs else (catch or 1000) + 90
        bar(x2, 190, False, RED, T["out2"], 120)
        tr = T.get("regap", T["out2"] + 1.5)
        x, h = x2 + 110, 40.0
        k = 0
        while x < XB - 30:
            bar(x, h, True, GREEN, tr + 0.4 + k * 0.25)
            x += 64
            h += 5
            k += 1
        bracket(x2 - 60, XB, 560, RED, tr, L["regap"], open_end=True)


def flowtoken(D, sc: dict, bt: list):
    """기존 설명 무대에 '움직이는 것 하나'만 더한다: 동전이 이미 그려진 화살표 길을 따라 카드 사이를 돈다 (2026-11-24 '기존 장면 + 살짝').
      "flow": {"path": ["nv", "cu", "or", "nv"], "cue": "돌아옵니다", "tokens": ["coin", "coin", "chip"], "pulse": "nv", "pulse_label": "매출 +"}"""
    f = sc.get("flow") or {}
    els = sc.get("els") or {}
    names = [n for n in f.get("path") or [] if n in els]
    if len(names) < 2:
        return
    T = _cue_times(dict(sc, mechanism={"cues": {"go": f.get("cue", "")}}), bt)
    start = T.get("go", bt[-1][0] + 0.5) + 0.8
    end = bt[-1][0] + bt[-1][1] - 0.4
    P = [(els[n]["x"], els[n]["y"]) for n in names]
    segs = []
    for a, b in zip(P, P[1:]):   # 화살표처럼 살짝 휜 길 — 카드 위는 지나지 않고 카드 가장자리에서 나타나고 사라짐
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = b[0] - a[0], b[1] - a[1]
        c = (mx - dy * 0.12, my + dx * 0.12)
        q = lambda u: ((1 - u) ** 2 * a[0] + 2 * (1 - u) * u * c[0] + u * u * b[0], (1 - u) ** 2 * a[1] + 2 * (1 - u) * u * c[1] + u * u * b[1])
        segs.append([q(0.28 + 0.44 * i / 10) for i in range(11)])
    toks = f.get("tokens") or ["coin"]
    lap = f.get("lap", 3.6)
    seg_d = lap / len(segs)
    pool = [_coin(D, P[0][0], P[0][1], 64) if (toks[k % len(toks)] == "coin") else _chiptok(D, P[0][0], P[0][1], 64) for k in range(len(segs) * 3)]
    t, n = start, 0
    pn = f.get("pulse")
    while t + lap < end and n < 30:
        for j, sg in enumerate(segs):
            _travel(D, pool[(n % 3) * len(segs) + j], sg, t + j * seg_d, seg_d * 0.9, P[0][0], P[0][1])
        if pn in els:
            pid = D._id()
            x, y = els[pn]["x"], els[pn]["y"]
            D.items.append(f'<div id="{pid}" style="position:absolute;left:{x + 130}px;top:{y - 120}px;white-space:nowrap;padding:4px 14px;border-radius:8px;'
                           f'background:rgba(10,12,16,.6);font-family:heavy,sans-x;font-size:44px;color:{GREEN};opacity:0;z-index:9">{_e(f.get("pulse_label", "+"))}</div>')
            D.js.append(f'tl.fromTo("#{pid}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3}},{t + lap:.2f});'
                        f'tl.to("#{pid}",{{opacity:0,y:-20,duration:0.4}},{t + lap + 0.8:.2f});')
        t += f.get("every", 1.4)
        n += 1


def checklist_pics(D, sc: dict, bt: list):
    """체크리스트 오른쪽 빈자리: 지금 말하는 줄을 '그림 하나'로 (글 목록 + 움직이는 그림, 2026-11-24 '원래 정적인 장면에 살짝').
    v2 (2026-11-24 사용자: "모션그래픽 퀄리티만 좀 높이면"): 크게·두껍게, 숫자는 올라가며, 결론은 알약 배지, 그림끼리는 옆으로 넘기기,
    움직임이 설명을 한다(진행선이 점을 따라 차오름 · 받는 돈과 나가는 현금을 나란히 · 쓰러진 회사 몫이 남은 회사로 날아감).
    sc["pics"] = [{"beat": 0, "t": "늦게", "kind": "timeline" | "bars" | "decay" | "switch" | "survive", ...}]"""
    import re as _re
    from . import motion2
    from .icons import svg_markup
    INKC, REDC, GRN, GRY, MUT = getattr(D, "ink", "#2B2B2B"), getattr(D, "red", "#B5302A"), "#2E7D4F", "#A3A8B0", "#5B606A"
    SH = "0 2px 3px rgba(30,24,16,.18),0 10px 22px rgba(30,24,16,.16)"
    ents = []
    for e in sc["pics"]:
        kb = e.get("beat", 0)
        b, (t0, d) = sc["beats"][kb], bt[kb]
        at = t0 + 0.3
        if e.get("t") and sc.get("_project_dir"):
            at = max(t0, (motion2.row_time(sc, kb, b, t0, d, e["t"]) or at) - 0.1)
        ents.append((at, t0 + d, e))
    ents.sort(key=lambda x: x[0])
    X0, X1, CX = 1150, 1830, 1490

    def div(html, at, frm="opacity:0,y:18", to="opacity:1,y:0", dur=0.45, ease="power3.out"):
        i = D._id()
        D.items.append(html.replace('id="ID"', f'id="{i}"'))
        D.js.append(f'tl.fromTo("#{i}",{{{frm}}},{{{to},duration:{dur},ease:"{ease}"}},{at:.2f});')
        return i

    def label(x, y, text, color, size, at, fam="sans-x", weight=""):
        return div(f'<div id="ID" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;white-space:nowrap;'
                   f'font-family:{fam},sans;font-size:{size}px;{weight}color:{color};opacity:0;z-index:6">'
                   f'<div style="transform:translate(-50%,-50%)">{_e(text)}</div></div>', at)

    def badge(x, y, text, color, at, count=None, size=46, sign=False):
        """결론 알약: 옅은 바탕 + 왼쪽 색 띠, 튀어나와 한 번 숨 쉬듯. count=(앞, 숫자, 뒤) 면 0 부터 올라감."""
        i = D._id()
        inner = _e(text)
        if count:
            pre, num, post = count
            dec = len(str(num).split(".")[1]) if "." in str(num) else 0
            sg = '(o.v>0?"+":"")+' if sign else ""
            inner = f'{_e(pre)}<span id="{i}_n">0</span>{_e(post)}'
            D.js.append(f'(function(){{var o={{v:0}};tl.to(o,{{v:{num},duration:0.9,ease:"power2.out",onUpdate:function(){{'
                        f'var s=o.v.toFixed({dec});document.getElementById("{i}_n").textContent={sg}s;}}}},{at + 0.15:.2f});}})();')
        D.items.append(f'<div id="{i}" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;opacity:0;z-index:7">'
                       f'<div style="transform:translate(-50%,-50%);white-space:nowrap;padding:12px 30px 12px 26px;border-radius:14px;'
                       f'background:{color}1F;border-left:9px solid {color};font-family:heavy,sans-x;font-size:{size}px;color:{color};'
                       f'box-shadow:0 6px 16px rgba(30,24,16,.10)">{inner}</div></div>')
        D.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(2)"}},{at:.2f});'
                    f'tl.to("#{i}",{{scale:1.06,duration:0.18,yoyo:true,repeat:1,ease:"sine.inOut"}},{at + 1.1:.2f});')
        D.sfx.append(("pop", at))
        return i

    def card(x, y, icon, text, at, w=220, color=None, h=170):
        col = color or INKC
        return div(f'<div id="ID" style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;width:{w}px;height:{h}px;border-radius:12px;'
                   f'background:linear-gradient(180deg,#FFFEFB,#F1EEE6);box-shadow:{SH};'
                   f'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;opacity:0;z-index:5">'
                   f'{svg_markup(icon, 78, col) or ""}<div style="font-family:heavy,sans-x;font-size:32px;color:{col}">{_e(text)}</div></div>',
                   at, "opacity:0,y:-24,scale:.85", "opacity:1,y:0,scale:1", 0.5, "back.out(1.7)")

    def line(x1, y1, x2, y2, color, w, at, dur=0.6):
        i = D._id()
        D.svg.append(f'<path id="{i}" d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="{color}" stroke-width="{w}" fill="none" stroke-linecap="round" '
                     f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
        D.js.append(f'tl.to("#{i}",{{strokeDashoffset:0,duration:{dur},ease:"power2.inOut"}},{at:.2f});')
        return i

    def runner(x1, y1, x2, y2, color, start, n=3, gap=0.55, dur=0.9, size=18):
        """선을 따라 흐르는 작은 점들 — '주문이 이쪽으로 간다'."""
        for k in range(n):
            r = div(f'<div id="ID" style="position:absolute;left:{x1 - size / 2:.0f}px;top:{y1 - size / 2:.0f}px;width:{size}px;height:{size}px;'
                    f'border-radius:50%;background:{color};box-shadow:0 0 0 5px {color}33;opacity:0;z-index:6"></div>',
                    start + k * gap, "opacity:0,x:0,y:0", f"opacity:0,x:{x2 - x1:.0f},y:{y2 - y1:.0f}", dur, "power1.inOut")
            D.js.append(f'tl.set("#{r}",{{opacity:1}},{start + k * gap + 0.01:.2f});tl.to("#{r}",{{opacity:0,duration:0.15}},{start + k * gap + dur - 0.1:.2f});')

    def bar(x, y, w, h, color, at, txt="", origin="left", dur=0.6, extra="", ease="power3.out"):
        sx = "scaleX" if origin in ("left", "right") else "scaleY"
        return div(f'<div id="ID" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{h:.0f}px;background:{color};'
                   f'transform-origin:{origin};border-radius:6px;display:flex;align-items:center;justify-content:center;font-family:heavy,sans-x;'
                   f'font-size:30px;color:#fff;white-space:nowrap;box-shadow:0 4px 10px rgba(30,24,16,.12);{extra}">{_e(txt)}</div>',
                   at, f"{sx}:0,opacity:1", f"{sx}:1,opacity:1", dur, ease)

    for k, (at, bend, e) in enumerate(ents):
        nxt = ents[k + 1][0] if k + 1 < len(ents) else None
        n0, s0 = len(D.items), len(D.svg)
        kind = e.get("kind")
        span = (nxt or bend) - at
        if kind == "timeline":   # 결정 → 보임 → 닿음: 점이 지나가면 진행선이 빨갛게 차오르고, 칸마다 '몇 달'이 붙는다
            st = e.get("steps", ["생산을 정함", "남는 게 보임", "줄인 게 닿음"])
            gaps = e.get("gaps", ["몇 달", "또 몇 달"])
            Y = 560
            xs = [X0 + 70, CX, X1 - 70]
            run = max(4.0, min(12.0, span * 0.6))
            bar(xs[0], Y - 6, xs[-1] - xs[0], 12, "#D9D4C8", at + 0.05, dur=0.5)
            bar(xs[0], Y - 6, xs[-1] - xs[0], 12, REDC, at + 0.3, dur=run, ease="none")
            for j, (x, s_) in enumerate(zip(xs, st)):
                ta = at + 0.3 + run * j / (len(xs) - 1)
                last = j == len(xs) - 1
                col = REDC if last else INKC
                nid = div(f'<div id="ID" style="position:absolute;left:{x - 22:.0f}px;top:{Y - 22}px;width:44px;height:44px;border-radius:50%;'
                          f'background:#FFFEFB;border:7px solid {col};box-sizing:border-box;opacity:0;z-index:7"></div>', at + 0.15 + 0.12 * j,
                          "opacity:0,scale:0", "opacity:1,scale:1", 0.35, "back.out(2)")
                D.js.append(f'tl.to("#{nid}",{{backgroundColor:"{col}",scale:1.35,duration:0.18,ease:"power2.out"}},{ta:.2f});'
                            f'tl.to("#{nid}",{{scale:1,duration:0.3,ease:"back.out(2)"}},{ta + 0.18:.2f});')
                label(x, Y - 70, s_, col, 38 if last else 34, ta, "heavy" if last else "sans-x")
                if j:
                    gx = (xs[j - 1] + x) / 2
                    div(f'<div id="ID" style="position:absolute;left:{gx:.0f}px;top:{Y + 70}px;opacity:0;z-index:6"><div style="transform:translate(-50%,-50%);'
                        f'display:flex;align-items:center;gap:8px;padding:6px 16px;border-radius:10px;background:{REDC}14;font-family:heavy,sans-x;font-size:32px;color:{REDC};white-space:nowrap">'
                        f'{svg_markup("calendar", 34, REDC) or ""}{_e(gaps[j - 1])}</div></div>', ta - 0.5)
            dot = div(f'<div id="ID" style="position:absolute;left:{xs[0] - 15:.0f}px;top:{Y - 15}px;width:30px;height:30px;border-radius:50%;background:{REDC};'
                      f'box-shadow:0 0 0 10px {REDC}2E;opacity:0;z-index:8"></div>', at + 0.3, "opacity:0", "opacity:1", 0.2)
            D.js.append(f'tl.to("#{dot}",{{x:{xs[-1] - xs[0]:.0f},duration:{run:.2f},ease:"none"}},{at + 0.3:.2f});')
            # 그동안 공장은 계속 만든다: 아래에 상자가 하나씩 쌓임
            for j in range(5):
                div(f'<div id="ID" style="position:absolute;left:{X0 + 150 + j * 80:.0f}px;top:{Y + 150}px;opacity:0">{svg_markup("package", 54, MUT) or ""}</div>',
                    at + 0.6 + run * (j + 0.5) / 5, "opacity:0,y:-30", "opacity:1,y:0", 0.35, "bounce.out")
            label(CX, Y + 250, e.get("note", "그동안 공장은 계속 만든다"), MUT, 32, at + 0.6)
        elif kind == "bars":     # 위: 장부 원가 40 vs 판매가 30 → 넘친 10 이 장부 적자 / 아래: 받는 돈 30 vs 나가는 현금 15 → +15
            u = 14.0
            dep, cash, price = e.get("dep", 25), e.get("cash", 15), e.get("price", 30)
            xa = CX - (dep + cash) * u / 2
            y1, y2 = 440, 690
            label(xa, y1 - 78, e.get("head", "칩 하나 장부 원가"), INKC, 32, at, "heavy")
            bar(xa, y1 - 40, dep * u, 80, GRY, at + 0.2, f"지은 공장 몫 {dep}")
            bar(xa + dep * u, y1 - 40, cash * u, 80, REDC, at + 0.7, f"현금 {cash}", dur=0.45)
            tp = at + max(2.0, span * 0.32)
            px = xa + price * u
            line(px, y1 - 70, px, y1 + 60, GRN, 8, tp, dur=0.35)
            label(px, y1 + 88, f"판매가 {price}", GRN, 32, tp, "heavy")
            over = div(f'<div id="ID" style="position:absolute;left:{px:.0f}px;top:{y1 - 40}px;width:{(dep + cash - price) * u:.0f}px;height:80px;'
                       f'background:repeating-linear-gradient(45deg,#FFFFFF55,#FFFFFF55 8px,transparent 8px,transparent 18px);outline:4px dashed #FFFFFF;outline-offset:-6px;border-radius:0 6px 6px 0;opacity:0;z-index:6"></div>',
                       tp + 0.5, "opacity:0", "opacity:1", 0.3)
            D.js.append(f'tl.to("#{over}",{{opacity:.45,duration:0.25,yoyo:true,repeat:3}},{tp + 0.9:.2f});')
            badge(X1 - 150, y1 - 120, "", REDC, tp + 0.8, ("장부 ", price - dep - cash, "원"), 40, True)
            # 아래: 현금만 보면
            tc = tp + max(1.6, span * 0.22)
            label(xa, y2 - 92, "현금만 보면", INKC, 32, tc, "heavy")
            bar(xa, y2 - 56, price * u, 48, GRN, tc + 0.2, f"받는 돈 {price}")
            bar(xa, y2 + 2, cash * u, 48, REDC, tc + 0.6, f"나가는 현금 {cash}", dur=0.45)
            bx0, bx1 = xa + cash * u, xa + price * u
            div(f'<div id="ID" style="position:absolute;left:{bx0:.0f}px;top:{y2 + 2}px;width:{bx1 - bx0:.0f}px;height:48px;border:4px dashed {GRN};'
                f'border-radius:6px;box-sizing:border-box;opacity:0;z-index:5"></div>', tc + 1.1, "opacity:0,scaleX:0", "opacity:1,scaleX:1", 0.4)
            badge(CX, y2 + 135, "", GRN, tc + 1.4, ("현금은 ", price - cash, "원 남음"), 44, True)
        elif kind == "decay":    # 쌓아 둔 상자가 하나씩 바래고, 아래 '재고 가치' 막대가 같이 줄어든다
            boxes = []
            label(CX, 345, e.get("head", "창고에 쌓인 재고"), INKC, 34, at, "heavy")
            for j in range(6):
                bx, by = CX - 180 + (j % 3) * 180, 450 + (j // 3) * 150
                boxes.append(div(f'<div id="ID" style="position:absolute;left:{bx - 75:.0f}px;top:{by - 62:.0f}px;width:150px;height:124px;border-radius:10px;'
                                 f'background:#E9C46A;border:4px solid #9C6E12;box-sizing:border-box;display:flex;align-items:center;justify-content:center;'
                                 f'box-shadow:{SH};opacity:0">{svg_markup("package", 74, "#6B4A08") or ""}</div>',
                                 at + j * 0.12, "opacity:0,y:-70", "opacity:1,y:0", 0.5, "bounce.out"))
            td = at + max(1.5, span * 0.28)
            vw = 520
            label(CX - vw / 2 - 20, 762, "재고 가치", MUT, 28, at + 0.9)
            vb = bar(CX - vw / 2 + 60, 744, vw - 60, 36, "#C9A13B", at + 0.9)
            for j, bi in enumerate(boxes):
                D.js.append(f'tl.to("#{bi}",{{backgroundColor:"#D6D6D6",borderColor:"#8A8A8A",scale:.93,duration:0.5,ease:"power2.out"}},{td + j * 0.45:.2f});')
            D.js.append(f'tl.to("#{vb}",{{scaleX:.55,backgroundColor:"{REDC}",duration:{0.45 * 6:.2f},ease:"power1.inOut"}},{td:.2f});')
            if e.get("value"):
                m = _re.match(r"(.*?)([\d.]+)(.*)", e["value"])
                badge(CX, 850, e["value"], REDC, td + 3.0, (m.group(1), float(m.group(2)), m.group(3)) if m else None, 40)
            label(CX, 912, e.get("sub", ""), MUT, 28, td + 3.3)
        elif kind == "switch":   # 주문이 우리 칩으로 흐르다 끊기고(✕ 도장), 경쟁사 칩 쪽으로 흐름이 옮겨 간다
            cy_, by_ = 400, 720
            card(CX, cy_, "users", e.get("customer", "고객"), at, 230)
            card(X0 + 140, by_, "cpu", e.get("us", "우리 칩"), at + 0.25, 230)
            card(X1 - 140, by_, "cpu", e.get("rival", "경쟁사 칩"), at + 0.45, 230)
            ax, ay, bx2, by2 = X0 + 190, by_ - 88, CX - 80, cy_ + 88
            l1 = line(ax, ay, bx2, by2, INKC, 8, at + 0.8)
            runner(bx2, by2, ax, ay, INKC, at + 1.3, n=3, gap=0.5)
            tc = at + max(2.4, span * 0.4)
            D.js.append(f'tl.to("#{l1}",{{stroke:"{GRY}",duration:0.4}},{tc:.2f});')
            i = div(f'<div id="ID" style="position:absolute;left:{(ax + bx2) / 2:.0f}px;top:{(ay + by2) / 2:.0f}px;opacity:0;z-index:8">'
                    f'<div style="transform:translate(-50%,-50%) rotate(-8deg);width:92px;height:92px;border-radius:50%;background:{REDC};color:#fff;'
                    f'display:flex;align-items:center;justify-content:center;font-family:heavy,sans-x;font-size:60px;box-shadow:{SH}">✕</div></div>',
                    tc + 0.15, "opacity:0,scale:1.8", "opacity:1,scale:1", 0.28, "power4.in")
            D.sfx.append(("impact-bass-1", tc + 0.4))
            cx2, cy2 = X1 - 190, by_ - 88
            line(cx2, cy2, CX + 80, cy_ + 88, REDC, 8, tc + 0.7)
            runner(CX + 80, cy_ + 88, cx2, cy2, REDC, tc + 1.3, n=4, gap=0.45)
            badge(CX, by_ + 150, e.get("note", "검증 몇 달 → 다음 제품까지 경쟁사 몫"), REDC, tc + 1.6, None, 34)
        elif kind == "survive":  # 셋이 버티다 C 가 쓰러지면, C 의 몫이 조각나 A·B 막대로 날아가 쌓인다
            xs = [X0 + 120, CX, X1 - 120]
            names = e.get("names", ["A 회사", "B 회사", "C 회사"])
            ids = [card(x, 370, "factory", nm, at + j * 0.18, 200) for j, (x, nm) in enumerate(zip(xs, names))]
            BOT, H0, H1 = 790, 110, 190
            bars_ = [div(f'<div id="ID" style="position:absolute;left:{x - 55:.0f}px;top:{BOT - H0}px;width:110px;height:{H0}px;background:#8C929C;'
                         f'border-radius:8px 8px 0 0;transform-origin:bottom;box-shadow:0 4px 10px rgba(30,24,16,.12)"></div>',
                         at + 0.5 + j * 0.15, "scaleY:0,opacity:1", "scaleY:1,opacity:1", 0.6, "power3.out") for j, x in enumerate(xs)]
            tf = at + max(2.2, span * 0.33)
            D.js.append(f'tl.to("#{ids[2]}",{{rotation:-14,y:36,opacity:0.35,filter:"grayscale(1)",duration:0.6,ease:"power2.in"}},{tf:.2f});'
                        f'tl.to("#{bars_[2]}",{{backgroundColor:"#C9C9C9",duration:0.3}},{tf + 0.3:.2f});')
            D.sfx.append(("impact-bass-1", tf + 0.55))
            label(xs[2], 600, "쓰러짐", REDC, 34, tf + 0.5, "heavy")
            # C 의 몫이 두 조각으로 → A·B 위에 얹힘
            tg = tf + 1.1
            for j in (0, 1):
                piece = div(f'<div id="ID" style="position:absolute;left:{xs[2] - 55:.0f}px;top:{BOT - H0 + j * H0 / 2:.0f}px;width:110px;height:{H0 / 2:.0f}px;'
                            f'background:{GRN};border-radius:6px;z-index:6;opacity:0"></div>', tg + j * 0.25, "opacity:0", "opacity:1", 0.15)
                dx = xs[j] - xs[2]
                land = BOT - H0 - (H1 - H0) - (BOT - H0 + j * H0 / 2)
                D.js.append(f'tl.to("#{piece}",{{keyframes:[{{y:{-170 - j * 20},x:{dx / 2:.0f},duration:0.4,ease:"power1.out"}},'
                            f'{{x:{dx:.0f},y:{land:.0f},height:{H1 - H0},duration:0.45,ease:"power2.in"}}]}},{tg + j * 0.25 + 0.1:.2f});')
                D.js.append(f'tl.to("#{bars_[j]}",{{height:{H1},top:{BOT - H1},backgroundColor:"{GRN}",duration:0.4,ease:"back.out(1.6)"}},{tg + j * 0.25 + 0.95:.2f});'
                            f'tl.to("#{piece}",{{opacity:0,duration:0.2}},{tg + j * 0.25 + 1.1:.2f});')
            D.js.append(f'tl.to("#{bars_[2]}",{{scaleY:0,duration:0.4,ease:"power2.in"}},{tg:.2f});')
            badge(CX, BOT + 82, e.get("note", "남은 쪽이 다음 호황을 나눔"), GRN, tg + 1.6, None, 36)
        new_ids = [m.group(1) for it in D.items[n0:] for m in [_re.search(r'id="([^"]+)"', it)] if m]
        new_ids += [m.group(1) for it in D.svg[s0:] for m in [_re.search(r'id="([^"]+)"', it)] if m]
        if nxt and new_ids:   # 다음 그림으로: 옆으로 넘기기 (지금 것은 왼쪽으로 빠지고, 다음 것은 아래에서 올라옴)
            D.js.append(f'tl.to("{",".join("#" + x for x in new_ids)}",{{opacity:0,x:"-=70",duration:0.32,ease:"power2.in",stagger:0.01}},{nxt - 0.4:.2f});')
        D.sfx.append(("whoosh-short" if k else "click-soft", at))


def register():
    from . import hybrid
    from .explain import _themed
    hybrid.RENDER["mechanism"] = _themed(s_mechanism)
