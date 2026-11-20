"""설명 무대 — 원리를 글·숫자 대신 '한 무대 위에서 바뀌는 물체'로 (docs/51, 벤치마크 docs/31).

월텍남 모션그래픽 벤치마크에서 반복해 쓰인 세 가지 문법을 하이브리드 장면으로 옮긴다.
한 장면 = 한 무대. 앞 박자에 나온 물체·기준선은 남기고, 대사의 동사에 맞춰 다음 요소만 바뀐다.

- afterline  사건 이후 누적  : 시간선 위 사건 표식(금지·날짜) → '이후' 구간이 붉게 열림 → 카드가 하나씩 쌓임 → 수량 문구
- spread     두 값 사이 간격(diff) : 재료 → 공정 → 제품 소품을 화살표로 → 두 가격 높이 + 점선 연장 → 괄호로 차이(이름·식)
                               → 한쪽 값이 바뀌면 옛 높이는 점선 윤곽으로 남고 간격이 줄어듦
- share      전체 중 몫      : 전체 막대(100%) → 부분이 차례로 채워짐 → 비교 눈금(예: 3분의 1) → 관련 구간을 괄호로 묶어 합계

박자 형식 (모든 장면 공통):
  "beats": [{"say": "...", "show": ["event", "after"], "at": {"after": "제재 뒤에도"}}, ...]
  show 에 적은 부품이 그 박자에 나온다. at 에 대사 속 단어를 적으면 그 단어를 말하는 순간에 맞춘다
  (없으면 박자 시작부터 0.5초 간격). show 가 없는 박자는 앞 화면을 그대로 둔다.
"""
from __future__ import annotations

import html as H

from . import paper
from .paper import FT, fit

W, HH = 1920, 1080
CARD = "#FBF8F1"
MUTED = "#5a5f6a"


# ---------------------------------------------------------------- 공통
def _schedule(sc: dict, bt: list) -> dict:
    """부품 이름 → 등장 시각(장면 안 초). 같은 부품을 두 번 적으면 처음 것."""
    from . import motion2
    when: dict = {}
    for k, (b, (t0, d)) in enumerate(zip(sc["beats"], bt)):
        words = b.get("at") or {}
        for i, part in enumerate(b.get("show") or []):
            if part in when:
                continue
            t = t0 + 0.2 + i * 0.5
            if words.get(part) and sc.get("_project_dir"):
                t = max(t0, motion2.row_time(sc, k, b, t0, d, words[part]) - 0.1)
            when[part] = (round(t, 2), d, t0)
    return when


def _div(D, style: str, inner: str = "") -> str:
    i = D._id()
    D.items.append(f'<div id="{i}" style="position:absolute;{style}">{inner}</div>')
    return i


def _pop(D, i: str, at: float, frm: str = "opacity:0,scale:0.6", to: str = "opacity:1,scale:1", dur: float = 0.4,
         ease: str = "back.out(2)"):
    D.js.append(f'tl.fromTo("#{i}",{{{frm}}},{{{to},duration:{dur},ease:"{ease}"}},{at:.2f});')


def _dashed(D, x0, y0, x1, y1, color, at, width=3, dur=0.5):
    """점선 기준선 (그려지듯 왼쪽→오른쪽으로 나타남)."""
    i = D._id()
    D.svg.append(f'<line id="{i}" x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y1:.0f}" stroke="{color}" '
                 f'stroke-width="{width}" stroke-dasharray="14 10" stroke-linecap="round" style="opacity:0"/>')
    j = D._id()
    D.svg.append(f'<clipPath id="{j}"><rect x="{min(x0, x1) - 10:.0f}" y="{min(y0, y1) - 10:.0f}" width="0" '
                 f'height="{abs(y1 - y0) + 20:.0f}"/></clipPath>')
    D.svg[-2] = D.svg[-2].replace('style="opacity:0"', f'style="opacity:0" clip-path="url(#{j})"')
    D.js.append(f'tl.set("#{i}",{{opacity:1}},{at:.2f});'
                f'tl.to("#{j} rect",{{attr:{{width:{abs(x1 - x0) + 20:.0f}}},duration:{dur},ease:"power1.inOut"}},{at:.2f});')
    return i


def _bracket_v(D, x, ya, yb, color, at, side="right"):
    """세로 괄호 (두 높이 사이). side=right 면 '}' 모양."""
    s = 1 if side == "right" else -1
    m = (ya + yb) / 2
    pts = [[x, ya], [x + 18 * s, ya + 14], [x + 18 * s, m - 12], [x + 34 * s, m], [x + 18 * s, m + 12], [x + 18 * s, yb - 14], [x, yb]]
    return D.rough("curve", [pts], color, 4, at=at, dur=0.45, roughness=0.6)


def _bracket_h(D, xa, xb, y, color, at):
    """가로 괄호 (구간 위, 가운데가 위로 뾰족)."""
    m = (xa + xb) / 2
    pts = [[xa, y], [xa + 14, y - 18], [m - 12, y - 18], [m, y - 34], [m + 12, y - 18], [xb - 14, y - 18], [xb, y]]
    return D.rough("curve", [pts], color, 4, at=at, dur=0.45, roughness=0.6)


def _head(D, sc):
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    if sc.get("title"):
        D.h1(sc["title"], y=140)


# ---------------------------------------------------------------- afterline: 사건 이후 누적
def s_afterline(D, sc: dict, bt: list, dur: float):
    """시간선 위 사건 표식 → 이후 구간 → 카드 누적 → 수량 문구 (벤치마크 4:52~4:57)."""
    _head(D, sc)
    when = _schedule(sc, bt)
    first = bt[0][0]
    ev = sc.get("event", {})
    y, x0, x1, ex = 620, 170, 1760, 360
    t_ev = when.get("event", (first + 0.2,))[0]
    D.rough("line", [x0, y, ex + 70, y + 1], D.ink, 4, at=t_ev - 0.1, dur=0.35)
    # 사건 표식: 손그림 금지 표시(기본) 또는 아이콘
    if ev.get("mark", "ban") == "ban":
        D.rough("ellipse", [ex, y, 150, 150], D.red, 9, at=t_ev, dur=0.45, roughness=1.0)
        D.rough("line", [ex - 52, y - 52, ex + 52, y + 52], D.red, 9, at=t_ev + 0.35, dur=0.2, roughness=0.8)
    else:
        D.icon(ev["mark"], ex, y, 130, D.red, at=t_ev)
    D.sfx.append(("pop", t_ev))
    if ev.get("name"):
        D.text(ex, y - 190, ev["name"], FT("label"), fit(FT("label"), ev["name"], 46, 360).size, D.ink, at=t_ev + 0.3)
    if ev.get("date"):
        D.text(ex, y + 130, ev["date"], FT("label"), fit(FT("label"), ev["date"], 34, 420).size, MUTED, at=t_ev + 0.45)
    # 이후 구간: 붉은 굵은 띠가 오른쪽으로 열림
    t_af = when.get("after", (t_ev + 1.0,))[0]
    i = _div(D, f"left:{ex + 78}px;top:{y - 7}px;width:{x1 - ex - 78}px;height:14px;border-radius:7px;"
                f"background:{D.red};opacity:.75;transform-origin:left center")
    _pop(D, i, t_af, "scaleX:0", "scaleX:1", 0.8, "power2.out")
    D.rough("line", [ex + 75, y, x1, y + 1], D.ink, 2, at=t_af, dur=0.8)
    if ev.get("tag"):
        D.text(ex + 210, y + 50, ev["tag"], paper.PEN, 50, D.red, at=t_af + 0.3)
    D.sfx.append(("whoosh-short", t_af))
    # 카드 누적: 같은 간격으로 하나씩 (2 → 3 → … 처럼 늘어남)
    it = sc.get("items", {})
    labels = it.get("labels") or [str(k + 1) for k in range(int(it.get("count", 6)))]
    n = len(labels)
    t_it, d_it, _ = when.get("items", (t_af + 0.8, 3.0, 0))
    span = min(max(d_it * 0.75, 0.9), 0.45 * n + 0.4)
    lx0, lx1 = 640, 1680
    step = (lx1 - lx0) / max(n - 1, 1) if n > 1 else 0
    cw = min(150, step * 0.82 if n > 1 else 150)
    for k, lab in enumerate(labels):
        cx = lx0 + k * step if n > 1 else (lx0 + lx1) / 2
        at = t_it + span * k / max(n - 1, 1)
        ic = it.get("icon", "microchip")
        from .icons import svg_markup
        mk = svg_markup(ic, int(cw * 0.55), D.ink) or ""
        lsz = fit(FT("value"), lab, 54, cw - 16).size
        card = (f'<div style="width:{cw:.0f}px;height:{cw * 1.12:.0f}px;background:{CARD};border-radius:10px;'
                f'box-shadow:0 6px 14px rgba(40,30,20,.22);display:flex;flex-direction:column;align-items:center;'
                f'justify-content:center;gap:6px">{mk}<div style="font-family:serif-x;font-size:{lsz}px;'
                f'color:{D.blue};line-height:1">{H.escape(lab)}</div></div>')
        cid = _div(D, f"left:{cx - cw / 2:.0f}px;top:{y - 30 - cw * 1.12:.0f}px", card)
        _pop(D, cid, at, "opacity:0,y:-40,scale:0.8", "opacity:1,y:0,scale:1", 0.35, "back.out(2.2)")
        D.sfx.append(("click-soft", at))
    # 수량 문구: 앞은 먹색, 강조는 붉게 크게
    hl = sc.get("headline")
    if hl:
        t_hl = when.get("headline", (t_it + span + 0.4,))[0]
        pre, emph = hl.get("pre", ""), hl.get("emph", "")
        fp, fe = paper.F(FT("label"), 46), paper.F(FT("title"), 78)
        wp, we = fp.getlength(pre + " "), fe.getlength(emph)
        cx = (lx0 + lx1) / 2
        xs = cx - (wp + we) / 2
        D.text(xs, y + 105, pre, FT("label"), 46, D.ink, at=t_hl, anchor="lm")
        D.text(xs + wp, y + 98, emph, FT("title"), 78, D.red, at=t_hl + 0.2, anchor="lm")
        D.sfx.append(("pop", t_hl + 0.2))


# ---------------------------------------------------------------- spread: 두 값 사이 간격
def s_spread(D, sc: dict, bt: list, dur: float):
    """재료 → 공정 → 제품 소품, 두 가격 높이, 점선 연장, 괄호 차이, 값이 바뀌면 옛 높이는 점선 윤곽 (벤치마크 9:09~10:15)."""
    _head(D, sc)
    when = _schedule(sc, bt)
    first = bt[0][0]
    steps = sc.get("steps", [])
    xs = [330, 860, 1390][: len(steps)] if len(steps) <= 3 else [330 + k * 1060 / (len(steps) - 1) for k in range(len(steps))]
    yi = 300
    t_st = when.get("steps", (first + 0.2, 3.0, first))
    for k, (st, x) in enumerate(zip(steps, xs)):
        at = t_st[0] + k * 0.7
        if st.get("word") and sc.get("_project_dir"):   # 소품마다 그 이름을 말하는 순간
            from . import motion2
            for kb, (b, (tb, db)) in enumerate(zip(sc["beats"], bt)):
                if st["word"] in b.get("say", ""):
                    at = max(tb, motion2.row_time(sc, kb, b, tb, db, st["word"]) - 0.1)
                    break
        D.icon(st.get("icon", "package"), x, yi, 120, D.ink, at=at)
        D.text(x, yi + 95, st.get("label", ""), FT("label"), fit(FT("label"), st.get("label", ""), 38, 300).size, D.ink, at=at + 0.1)
        if k:
            D.arrow(xs[k - 1] + 95, yi, x - 95, yi, MUTED, at=at - 0.35)
        D.sfx.append(("pop", at))
    # 가격 블록: 첫 소품 아래 '재료값', 마지막 소품 아래 '제품값'
    lo, hi = sc["low"], sc["high"]
    base, top = 960, 470
    vmax = max(hi["value"], lo["value"], (sc.get("change") or {}).get("value", 0)) * 1.08
    hgt = lambda v: (base - top) * v / vmax   # noqa: E731
    bw = 210
    xl, xh = xs[0], xs[-1]
    D.rough("line", [xl - 200, base, xh + 230, base + 1], D.ink, 3, at=when.get("low", (first + 1,))[0] - 0.2, dur=0.4)

    def block(x, v, col, at, label, txt):
        h = hgt(v)
        bid = _div(D, f"left:{x - bw / 2:.0f}px;top:{base - h:.0f}px;width:{bw}px;height:{h:.0f}px;"
                      f"background:repeating-linear-gradient(-41deg,{col}33 0 6px,{col}10 6px 15px);"
                      f"border:4px solid {col};border-bottom:none;border-radius:6px 6px 0 0;transform-origin:center bottom")
        _pop(D, bid, at, "scaleY:0", "scaleY:1", 0.6, "power2.out")
        vid = f"e{D.n + 1}"   # 값 글자 id (D.text 가 다음에 만드는 것)
        D.text(x, base - h - 40, txt, FT("value"), 52, col, at=at + 0.4)
        D.text(x, base + 40, label, FT("label"), fit(FT("label"), label, 34, 280).size, col, at=at + 0.2)
        return bid, vid

    t_lo = when.get("low", (first + 1.0,))[0]
    block(xl, lo["value"], D.ink, t_lo, lo["label"], lo.get("text", str(lo["value"])))
    yl = base - hgt(lo["value"])
    _dashed(D, xl + bw / 2, yl, xh + 170, yl, D.ink, t_lo + 0.6, dur=0.8)   # 재료값 높이를 제품 쪽까지 연장
    t_hi = when.get("high", (t_lo + 1.0,))[0]
    hid, hv = block(xh, hi["value"], D.red, t_hi, hi["label"], hi.get("text", str(hi["value"])))
    D.sfx.append(("pencil", t_lo + 0.6))
    # 괄호: 두 높이 사이 = 차이
    g = sc.get("diff", {})
    yh = base - hgt(hi["value"])
    bx = xh + bw / 2 + 30
    t_g = when.get("diff", (t_hi + 1.0,))[0]
    ch = sc.get("change")
    t_c = when.get("change", (None,))[0] if ch else None
    kb = len(D.rq)   # 앞 괄호 (값이 바뀌면 흐리게)
    _bracket_v(D, bx, yh, yl, D.red, t_g)
    gl = g.get("label", "")
    gsz = fit(FT("title"), gl, 54, W - bx - 70).size
    D.text(bx + 50, (yh + yl) / 2 - (24 if g.get("formula") else 0), gl, FT("title"), gsz, D.red, at=t_g + 0.3, anchor="lm")
    if g.get("formula"):
        D.text(bx + 50, (yh + yl) / 2 + 32, g["formula"], paper.PEN, fit(paper.PEN, g["formula"], 34, W - bx - 80).size, MUTED,
               at=t_g + 0.6, anchor="lm")
    D.sfx.append(("pencil", t_g))
    if ch and t_c is not None:
        # 옛 높이는 점선 윤곽으로 남기고, 제품 블록이 새 높이로 내려간다. 옛 값·옛 괄호는 흐리게.
        h_old, h_new = hgt(hi["value"]), hgt(ch["value"])
        ghost = _div(D, f"left:{xh - bw / 2:.0f}px;top:{base - h_old:.0f}px;width:{bw}px;height:{h_old:.0f}px;"
                        f"border:3px dashed {D.red};border-bottom:none;border-radius:6px 6px 0 0;opacity:0")
        D.js.append(f'tl.to("#{ghost}",{{opacity:.6,duration:.2}},{t_c:.2f});')
        D.js.append(f'tl.to("#{hid}",{{scaleY:{h_new / h_old:.4f},duration:.9,ease:"power2.inOut"}},{t_c + 0.1:.2f});')
        D.js.append(f'tl.to(".r{kb},#{hv}",{{opacity:.22,duration:.3}},{t_c:.2f});')
        D.arrow(xh - bw / 2 - 40, base - h_old + 10, xh - bw / 2 - 40, base - h_new - 10, D.red, at=t_c + 0.2)
        D.text(xh, base - h_new - 40, ch.get("text", str(ch["value"])), FT("value"), 52, D.red, at=t_c + 1.0)
        if base - h_new < yl - 30:
            _bracket_v(D, bx, base - h_new, yl, D.red, t_c + 1.1)
        if ch.get("label"):
            lx = xh - bw / 2 - 90   # 블록 왼쪽 빈 곳 (두 블록 사이)
            D.text(lx, yl - 70, ch["label"], paper.PEN, fit(paper.PEN, ch["label"], 50, lx - xl - bw / 2 - 40).size, D.ink,
                   at=t_c + 1.3, anchor="rm")
        D.sfx.append(("whoosh-short", t_c))


# ---------------------------------------------------------------- share: 전체 중 몫
def s_share(D, sc: dict, bt: list, dur: float):
    """전체 막대 → 부분이 차례로 채워짐 → 비교 눈금 → 괄호로 합계 (벤치마크 4:35~4:43)."""
    _head(D, sc)
    when = _schedule(sc, bt)
    first = bt[0][0]
    x0, x1, y, h = 260, 1660, 580, 140
    t_tot = when.get("total", (first + 0.2,))[0]
    D.rough("rectangle", [x0, y, x1 - x0, h], D.ink, 3.5, at=t_tot, dur=0.6)
    if sc.get("total"):
        D.text(x1, y + h + 55, sc["total"], FT("label"), 34, MUTED, at=t_tot + 0.4, anchor="rm")
    D.text(x0, y + h + 55, "0", FT("label"), 30, MUTED, at=t_tot + 0.4)
    D.text(x1, y - 30, "100%", FT("label"), 30, MUTED, at=t_tot + 0.4)
    total = float(sc.get("of", 100))
    cols = [D.red, "#D9824B", D.blue, "#2E7D4F"]
    xa = x0
    seg = []
    for k, p in enumerate(sc.get("parts", [])):
        w = (x1 - x0) * p["value"] / total
        col = p.get("color") or cols[k % len(cols)]
        t = when.get(f"p{k}", (t_tot + 0.8 + k * 1.2,))[0]
        i = _div(D, f"left:{xa + 3:.0f}px;top:{y + 3}px;width:{w - 3:.0f}px;height:{h - 6}px;background:{col};opacity:.85;"
                    f"transform-origin:left center")
        _pop(D, i, t, "scaleX:0", "scaleX:1", 0.7, "power2.out")
        lab = p["label"] + (f' {p["text"]}' if p.get("text") else "")
        D.text(xa + w / 2, y + h + 55 + (48 if k % 2 else 0), lab, FT("label"), fit(FT("label"), lab, 36, max(w + 120, 260)).size,
               col, at=t + 0.4)
        D.sfx.append(("pop", t))
        seg.append((xa, xa + w))
        xa += w
    mk = sc.get("mark")
    if mk:
        t = when.get("mark", (xa,))[0] if "mark" in when else (first + 2)
        xm = x0 + (x1 - x0) * mk["value"] / total
        _dashed(D, xm, y - 70, xm, y + h + 20, D.ink, t, width=4, dur=0.4)
        D.text(xm, y - 100, mk.get("label", ""), paper.PEN, 58, D.ink, at=t + 0.2)
    sm = sc.get("sum")
    if sm and seg:
        t = when.get("sum", (first + 3,))[0]
        idx = sm.get("parts", list(range(len(seg))))
        xa_, xb_ = seg[idx[0]][0], seg[idx[-1]][1]
        _bracket_h(D, xa_ + 4, xb_ - 4, y - 14, D.red, t)
        ty = y - 175 if mk else y - 85   # 눈금 글자(y-100)보다 위
        D.text((xa_ + xb_) / 2, ty, sm.get("label", ""), FT("title"), fit(FT("title"), sm.get("label", ""), 58, 900).size, D.red,
               at=t + 0.3)
        D.sfx.append(("pencil", t))


# ---------------------------------------------------------------- 등록
def register():
    from . import hybrid
    hybrid.RENDER["afterline"] = s_afterline
    hybrid.RENDER["spread"] = s_spread
    hybrid.RENDER["share"] = s_share
