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
from .paper import fit

W, HH = 1920, 1080
CARD = "#FDFCF8"
MUTED = "#55595f"
INK = "#1F242E"
RED = "#B8322E"
NAVY = "#23418C"
HEAVY = paper.FONT_DIR / "BlackHanSans-Regular.ttf"   # 굵은 제목·숫자 (OFL)
BOLD = paper.SANS_X                                     # 라벨 (나눔고딕 ExtraBold)
FAM = {str(HEAVY): "heavy", str(BOLD): "sans-x", str(paper.PEN): "pen", str(paper.SANS): "sans"}
SHADOW = "0 1px 1px rgba(30,24,16,.18),0 4px 6px rgba(30,24,16,.14),0 14px 24px rgba(30,24,16,.18)"

# 붓 자국: 가장자리를 흔들고(변위) 마른 붓 결(가로 줄무늬 투명도)을 입힌다
DEFS = """<defs>
<filter id="xbrush" filterUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080">
 <feTurbulence type="fractalNoise" baseFrequency="0.03 0.08" numOctaves="3" seed="3" result="n"/>
 <feDisplacementMap in="SourceGraphic" in2="n" scale="9" xChannelSelector="R" yChannelSelector="G" result="d"/>
 <feTurbulence type="fractalNoise" baseFrequency="0.012 0.55" numOctaves="2" seed="11" result="s"/>
 <feColorMatrix in="s" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.3 1.55" result="sa"/>
 <feComposite in="d" in2="sa" operator="in"/>
</filter>
<filter id="xink" filterUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080">
 <feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="5" result="n"/>
 <feDisplacementMap in="SourceGraphic" in2="n" scale="3" xChannelSelector="R" yChannelSelector="G"/>
</filter>
</defs>"""


def _setup(D, sc: dict, title: bool = True):
    """설명 무대 공통 바탕: 실사 구겨진 종이, 굵은 글꼴, 붓 필터, 왼쪽 위 제목 (2026-11-20 사용자: 배경부터 디테일 부족)."""
    import shutil
    from .. import config
    from . import crumple
    work = getattr(D, "_work", None)
    if work is not None:
        a = work / "assets"
        (a / "fonts").mkdir(parents=True, exist_ok=True)
        if not (a / "fonts" / HEAVY.name).exists():
            shutil.copy(HEAVY, a / "fonts" / HEAVY.name)
        bg = crumple.background(config.CACHE_DIR, seed=int(sc.get("paper_seed", 7)))
        if not (a / bg.name).exists():
            shutil.copy(bg, a / bg.name)
        D.media.insert(0, f'<img src="assets/{bg.name}" style="position:absolute;left:0;top:0;width:{W}px;height:{HH}px">')
    D.css.append(f"@font-face{{font-family:heavy;src:url('assets/fonts/{HEAVY.name}')}}")
    D.svg.insert(0, DEFS)
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    if title and sc.get("title"):   # 레퍼런스처럼 왼쪽 위에 작고 굵게 (가운데 큰 제목·밑줄 대신)
        _txt(D, 150, 112, sc["title"], HEAVY, 44, "#3A3F48", at=0.15, anchor="lm")


def _txt(D, x, y, s, font, size, color, at=None, gap=0.12, dur=0.45, anchor="mm", ls=0.0, shadow=False):
    """글자 하나 (굵은 글꼴 포함). hyper.Doc.text 와 같은 등장 방식, id 도 같은 규칙."""
    i = D._id()
    fam = FAM.get(str(font), "sans")
    ax = {"m": "-50%", "l": "0", "r": "-100%"}[anchor[0]]
    sh = ";text-shadow:0 2px 3px rgba(30,24,16,.18)" if shadow else ""
    D.items.append(f'<div id="{i}w" class="t" style="left:{x:.0f}px;top:{y:.0f}px;font-family:{fam};font-size:{size:.0f}px;'
                   f'color:{color};letter-spacing:{ls}px;transform:translate({ax},-50%){sh}"><span id="{i}">{H.escape(s)}</span></div>')
    t = D.at(at, gap)
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:18}},{{opacity:1,y:0,duration:{dur},ease:"power2.out"}},{t:.2f});')
    return t


def _path_draw(D, d: str, color: str, width: float, at: float, dur: float = 0.5, flt: str = "", opacity: float = 1.0):
    """SVG 경로를 그려지듯 (붓 필터 선택)."""
    i = D._id()
    f = f' filter="url(#{flt})"' if flt else ""
    D.svg.append(f'<path id="{i}" d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
                 f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" opacity="{opacity}"{f}/>')
    D.js.append(f'tl.to("#{i}",{{strokeDashoffset:0,duration:{dur},ease:"power2.inOut"}},{at:.2f});')
    return i


def _chip(size: int, uid: str) -> str:
    """금색 다리가 달린 칩 그림 (선 아이콘 대신 물체처럼)."""
    pins = []
    for k in range(7):
        o = 22 + k * 9.3
        pins += [f'<rect x="{o:.1f}" y="6" width="4.6" height="14" rx="1"/>', f'<rect x="{o:.1f}" y="80" width="4.6" height="14" rx="1"/>',
                 f'<rect x="6" y="{o:.1f}" width="14" height="4.6" rx="1"/>', f'<rect x="80" y="{o:.1f}" width="14" height="4.6" rx="1"/>']
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100"><defs>'
            f'<linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F3D27A"/>'
            f'<stop offset=".5" stop-color="#C9962E"/><stop offset="1" stop-color="#8A6418"/></linearGradient>'
            f'<linearGradient id="b{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2E4A8E"/>'
            f'<stop offset="1" stop-color="#121E44"/></linearGradient>'
            f'<radialGradient id="d{uid}" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#3F64B8"/>'
            f'<stop offset="1" stop-color="#16244F"/></radialGradient></defs>'
            f'<g fill="url(#g{uid})" stroke="#7A5512" stroke-width=".6">{"".join(pins)}</g>'
            f'<rect x="17" y="17" width="66" height="66" rx="5" fill="url(#b{uid})" stroke="url(#g{uid})" stroke-width="3"/>'
            f'<rect x="28" y="28" width="44" height="44" rx="2.5" fill="url(#d{uid})" stroke="#0B1330" stroke-width="1.2"/>'
            f'<path d="M30 31 L56 31 L30 57 Z" fill="#fff" opacity=".13"/>'
            f'<circle cx="24" cy="24" r="2.2" fill="#C9962E"/></svg>')


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
    _setup(D, sc)


# ---------------------------------------------------------------- afterline: 사건 이후 누적
def s_afterline(D, sc: dict, bt: list, dur: float):
    """시간선 위 사건 표식 → 이후 구간 → 카드 누적 → 수량 문구 (벤치마크 4:52~4:57)."""
    _head(D, sc)
    when = _schedule(sc, bt)
    first = bt[0][0]
    ev = sc.get("event", {})
    y, x0, x1, ex = 560, 170, 1760, 330
    t_ev = when.get("event", (first + 0.2,))[0]
    _path_draw(D, f"M{x0} {y} L{ex + 40} {y + 1}", "#20242C", 5, t_ev - 0.15, 0.35, "xink")
    # 사건 표식: 붓으로 칠한 금지 표시(기본) 또는 아이콘
    if ev.get("mark", "ban") == "ban":
        r = 62
        circ = f"M{ex} {y - r} A{r} {r} 0 1 1 {ex - 0.1} {y - r}"
        _path_draw(D, circ, "#7E1C18", 24, t_ev + 0.02, 0.5, "xbrush", 0.55)   # 아래 짙은 붓
        _path_draw(D, circ, "#C33A31", 17, t_ev, 0.5, "xbrush")
        k = r * 0.7
        _path_draw(D, f"M{ex - k} {y - k} L{ex + k} {y + k}", "#C33A31", 17, t_ev + 0.45, 0.22, "xbrush")
    else:
        D.icon(ev["mark"], ex, y, 130, RED, at=t_ev)
    D.sfx.append(("pop", t_ev))
    if ev.get("name"):
        _txt(D, ex, y - 140, ev["name"], HEAVY, fit(HEAVY, ev["name"], 56, 360).size, INK, at=t_ev + 0.3, ls=-0.5)
    if ev.get("date"):
        _txt(D, ex + 40, y + 130, ev["date"], HEAVY, fit(HEAVY, ev["date"], 36, 440).size, "#4A4E55", at=t_ev + 0.45)
    # 이후 구간: 붉은 붓 띠가 오른쪽으로 칠해짐
    t_af = when.get("after", (t_ev + 1.0,))[0]
    _path_draw(D, f"M{ex + 75} {y + 1} L{x1} {y - 2}", "#8E2420", 28, t_af + 0.03, 0.9, "xbrush", 0.6)
    _path_draw(D, f"M{ex + 75} {y} L{x1} {y - 2}", "#C2463C", 22, t_af, 0.9, "xbrush", 1.0)
    if ev.get("tag"):
        _txt(D, ex + 200, y + 46, ev["tag"], paper.PEN, 50, RED, at=t_af + 0.3)
    D.sfx.append(("whoosh-short", t_af))
    # 카드 누적: 같은 간격으로 하나씩, 선 위에 살짝 기울어 놓임
    it = sc.get("items", {})
    labels = it.get("labels") or [str(k + 1) for k in range(int(it.get("count", 6)))]
    n = len(labels)
    t_it, d_it, _ = when.get("items", (t_af + 0.8, 3.0, 0))
    span = min(max(d_it * 0.75, 0.9), 0.45 * n + 0.4)
    lx0, lx1 = 590, 1650
    step = (lx1 - lx0) / max(n - 1, 1) if n > 1 else 0
    cw = min(168, step * 0.8 if n > 1 else 168)
    chh = cw * 1.2
    import numpy as _np
    rr = _np.random.default_rng(sc.get("id", 1) * 13)
    for k, lab in enumerate(labels):
        cx = lx0 + k * step if n > 1 else (lx0 + lx1) / 2
        at = t_it + span * k / max(n - 1, 1)
        ic = it.get("icon", "chip")
        if ic == "chip":
            mk = _chip(int(cw * 0.66), f"{sc.get('id', 0)}_{k}")
        else:
            from .icons import svg_markup
            mk = svg_markup(ic, int(cw * 0.55), INK) or ""
        lsz = fit(HEAVY, lab, 56, cw - 20).size
        rot = rr.uniform(-1.6, 1.6)
        card = (f'<div style="width:{cw:.0f}px;height:{chh:.0f}px;background:linear-gradient(180deg,#FFFEFB,#F1EEE6);'
                f'border-radius:7px;box-shadow:{SHADOW};display:flex;flex-direction:column;align-items:center;'
                f'justify-content:center;gap:2px;transform:rotate({rot:.2f}deg)">{mk}<div style="font-family:heavy;'
                f'font-size:{lsz}px;color:{NAVY};line-height:1">{H.escape(lab)}</div></div>')
        cid = _div(D, f"left:{cx - cw / 2:.0f}px;top:{y - 22 - chh:.0f}px", card)
        _pop(D, cid, at, "opacity:0,y:-36,scale:0.86", "opacity:1,y:0,scale:1", 0.38, "back.out(1.8)")
        D.sfx.append(("click-soft", at))
    # 수량 문구: 앞은 먹색, 강조는 붉게 크게
    hl = sc.get("headline")
    if hl:
        t_hl = when.get("headline", (t_it + span + 0.4,))[0]
        pre, emph = hl.get("pre", ""), hl.get("emph", "")
        fp, fe = paper.F(HEAVY, 50), paper.F(HEAVY, 92)
        wp, we = fp.getlength(pre + " "), fe.getlength(emph)
        cx = (lx0 + lx1) / 2 + 40
        xs = cx - (wp + we) / 2
        _txt(D, xs, y + 122, pre, HEAVY, 50, INK, at=t_hl, anchor="lm")
        _txt(D, xs + wp, y + 114, emph, HEAVY, 92, "#B5302B", at=t_hl + 0.2, anchor="lm", shadow=True)
        D.sfx.append(("pop", t_hl + 0.2))


# ---------------------------------------------------------------- spread: 두 값 사이 간격
def s_spread(D, sc: dict, bt: list, dur: float):
    """재료 → 공정 → 제품 소품, 두 가격 높이, 점선 연장, 괄호 차이, 값이 바뀌면 옛 높이는 점선 윤곽 (벤치마크 9:09~10:15)."""
    _head(D, sc)
    when = _schedule(sc, bt)
    first = bt[0][0]
    steps = sc.get("steps", [])
    xs = [330, 860, 1390][: len(steps)] if len(steps) <= 3 else [330 + k * 1060 / (len(steps) - 1) for k in range(len(steps))]
    yi = 290
    t_st = when.get("steps", (first + 0.2, 3.0, first))
    for k, (st, x) in enumerate(zip(steps, xs)):
        at = t_st[0] + k * 0.7
        if st.get("word") and sc.get("_project_dir"):   # 소품마다 그 이름을 말하는 순간
            from . import motion2
            for kb, (b, (tb, db)) in enumerate(zip(sc["beats"], bt)):
                if st["word"] in b.get("say", ""):
                    at = max(tb, motion2.row_time(sc, kb, b, tb, db, st["word"]) - 0.1)
                    break
        from .icons import svg_markup
        mk = svg_markup(st.get("icon", "package"), 112, INK) or ""
        rot = (-1.4, 1.1, -0.8, 1.5)[k % 4]
        sid = _div(D, f"left:{x - 92}px;top:{yi - 92}px;width:184px;height:184px;border-radius:14px;"
                      f"background:linear-gradient(180deg,#FFFEFB,#EFEBE2);box-shadow:{SHADOW};display:flex;align-items:center;"
                      f"justify-content:center;transform:rotate({rot}deg)", mk)
        _pop(D, sid, at, "opacity:0,y:-30,scale:0.85", "opacity:1,y:0,scale:1", 0.4, "back.out(1.8)")
        _txt(D, x, yi + 130, st.get("label", ""), HEAVY, fit(HEAVY, st.get("label", ""), 40, 300).size, INK, at=at + 0.1)
        if k:
            _path_draw(D, f"M{xs[k - 1] + 120} {yi} L{x - 125} {yi}", "#3A3F48", 6, at - 0.4, 0.35, "xink")
            _path_draw(D, f"M{x - 145} {yi - 16} L{x - 122} {yi} L{x - 145} {yi + 16}", "#3A3F48", 6, at - 0.1, 0.15, "xink")
        D.sfx.append(("pop", at))
    # 가격 블록: 첫 소품 아래 '재료값', 마지막 소품 아래 '제품값'
    lo, hi = sc["low"], sc["high"]
    base, top = 970, 545
    vmax = max(hi["value"], lo["value"], (sc.get("change") or {}).get("value", 0)) * 1.08
    hgt = lambda v: (base - top) * v / vmax   # noqa: E731
    bw = 210
    xl, xh = xs[0], xs[-1]
    D.rough("line", [xl - 200, base, xh + 230, base + 1], INK, 3, at=when.get("low", (first + 1,))[0] - 0.2, dur=0.4)

    def block(x, v, col, at, label, txt):
        h = hgt(v)
        bid = _div(D, f"left:{x - bw / 2:.0f}px;top:{base - h:.0f}px;width:{bw}px;height:{h:.0f}px;"
                      f"background:linear-gradient(90deg,{col}F2,{col}CC 55%,{col}E6);box-shadow:{SHADOW};"
                      f"border-radius:6px 6px 0 0;transform-origin:center bottom")
        _pop(D, bid, at, "scaleY:0", "scaleY:1", 0.6, "power2.out")
        vid = f"e{D.n + 1}"   # 값 글자 id (D.text 가 다음에 만드는 것)
        _txt(D, x, base - h - 40, txt, HEAVY, 52, col, at=at + 0.4)
        _txt(D, x, base + 40, label, BOLD, fit(BOLD, label, 34, 280).size, col, at=at + 0.2)
        return bid, vid

    t_lo = when.get("low", (first + 1.0,))[0]
    block(xl, lo["value"], INK, t_lo, lo["label"], lo.get("text", str(lo["value"])))
    yl = base - hgt(lo["value"])
    _dashed(D, xl + bw / 2, yl, xh + 170, yl, INK, t_lo + 0.6, dur=0.8)   # 재료값 높이를 제품 쪽까지 연장
    t_hi = when.get("high", (t_lo + 1.0,))[0]
    hid, hv = block(xh, hi["value"], RED, t_hi, hi["label"], hi.get("text", str(hi["value"])))
    D.sfx.append(("pencil", t_lo + 0.6))
    # 괄호: 두 높이 사이 = 차이
    g = sc.get("diff", {})
    yh = base - hgt(hi["value"])
    bx = xh + bw / 2 + 30
    t_g = when.get("diff", (t_hi + 1.0,))[0]
    ch = sc.get("change")
    t_c = when.get("change", (None,))[0] if ch else None
    kb = len(D.rq)   # 앞 괄호 (값이 바뀌면 흐리게)
    _bracket_v(D, bx, yh, yl, RED, t_g)
    gl = g.get("label", "")
    gsz = fit(HEAVY, gl, 54, W - bx - 70).size
    _txt(D, bx + 50, (yh + yl) / 2 - (24 if g.get("formula") else 0), gl, HEAVY, gsz, RED, at=t_g + 0.3, anchor="lm")
    if g.get("formula"):
        _txt(D, bx + 50, (yh + yl) / 2 + 32, g["formula"], paper.PEN, fit(paper.PEN, g["formula"], 34, W - bx - 80).size, MUTED,
               at=t_g + 0.6, anchor="lm")
    D.sfx.append(("pencil", t_g))
    if ch and t_c is not None:
        # 옛 높이는 점선 윤곽으로 남기고, 제품 블록이 새 높이로 내려간다. 옛 값·옛 괄호는 흐리게.
        h_old, h_new = hgt(hi["value"]), hgt(ch["value"])
        ghost = _div(D, f"left:{xh - bw / 2:.0f}px;top:{base - h_old:.0f}px;width:{bw}px;height:{h_old:.0f}px;"
                        f"border:3px dashed {RED};border-bottom:none;border-radius:6px 6px 0 0;opacity:0")
        D.js.append(f'tl.to("#{ghost}",{{opacity:.6,duration:.2}},{t_c:.2f});')
        D.js.append(f'tl.to("#{hid}",{{scaleY:{h_new / h_old:.4f},duration:.9,ease:"power2.inOut"}},{t_c + 0.1:.2f});')
        D.js.append(f'tl.to(".r{kb},#{hv}",{{opacity:.22,duration:.3}},{t_c:.2f});')
        D.arrow(xh - bw / 2 - 40, base - h_old + 10, xh - bw / 2 - 40, base - h_new - 10, RED, at=t_c + 0.2)
        _txt(D, xh, base - h_new - 40, ch.get("text", str(ch["value"])), HEAVY, 52, RED, at=t_c + 1.0)
        if base - h_new < yl - 30:
            _bracket_v(D, bx, base - h_new, yl, RED, t_c + 1.1)
        if ch.get("label"):
            lx = xh - bw / 2 - 90   # 블록 왼쪽 빈 곳 (두 블록 사이)
            _txt(D, lx, yl - 70, ch["label"], paper.PEN, fit(paper.PEN, ch["label"], 50, lx - xl - bw / 2 - 40).size, INK,
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
    bar = _div(D, f"left:{x0}px;top:{y}px;width:{x1 - x0}px;height:{h}px;border-radius:8px;"
                  f"background:linear-gradient(180deg,#FFFEFB,#EEEAE1);box-shadow:{SHADOW};transform-origin:left center")
    _pop(D, bar, t_tot, "opacity:0,scaleX:0.2", "opacity:1,scaleX:1", 0.6, "power2.out")
    if sc.get("total"):
        _txt(D, x1, y + h + 55, sc["total"], BOLD, 34, MUTED, at=t_tot + 0.4, anchor="rm")
    _txt(D, x0, y + h + 55, "0", BOLD, 30, MUTED, at=t_tot + 0.4)
    _txt(D, x1, y - 30, "100%", BOLD, 30, MUTED, at=t_tot + 0.4)
    total = float(sc.get("of", 100))
    cols = ["#B8322E", "#E08A3C", NAVY, "#2E7D4F"]
    xa = x0
    seg = []
    for k, p in enumerate(sc.get("parts", [])):
        w = (x1 - x0) * p["value"] / total
        col = p.get("color") or cols[k % len(cols)]
        t = when.get(f"p{k}", (t_tot + 0.8 + k * 1.2,))[0]
        i = _div(D, f"left:{xa + 6:.0f}px;top:{y + 8}px;width:{w - 6:.0f}px;height:{h - 16}px;border-radius:4px;"
                    f"background:linear-gradient(180deg,{col},{col}D9);box-shadow:inset 0 -6px 10px rgba(0,0,0,.12);"
                    f"transform-origin:left center")
        _pop(D, i, t, "scaleX:0", "scaleX:1", 0.7, "power2.out")
        lab = p["label"] + (f' {p["text"]}' if p.get("text") else "")
        _txt(D, xa + w / 2, y + h + 55 + (48 if k % 2 else 0), lab, BOLD, fit(BOLD, lab, 36, max(w + 120, 260)).size,
               col, at=t + 0.4)
        D.sfx.append(("pop", t))
        seg.append((xa, xa + w))
        xa += w
    mk = sc.get("mark")
    if mk:
        t = when.get("mark", (xa,))[0] if "mark" in when else (first + 2)
        xm = x0 + (x1 - x0) * mk["value"] / total
        _dashed(D, xm, y - 70, xm, y + h + 20, INK, t, width=4, dur=0.4)
        _txt(D, xm, y - 100, mk.get("label", ""), paper.PEN, 58, INK, at=t + 0.2)
    sm = sc.get("sum")
    if sm and seg:
        t = when.get("sum", (first + 3,))[0]
        idx = sm.get("parts", list(range(len(seg))))
        xa_, xb_ = seg[idx[0]][0], seg[idx[-1]][1]
        _bracket_h(D, xa_ + 4, xb_ - 4, y - 14, RED, t)
        ty = y - 175 if mk else y - 85   # 눈금 글자(y-100)보다 위
        _txt(D, (xa_ + xb_) / 2, ty, sm.get("label", ""), HEAVY, fit(HEAVY, sm.get("label", ""), 58, 900).size, RED,
               at=t + 0.3)
        D.sfx.append(("pencil", t))


# ---------------------------------------------------------------- 등록
def register():
    from . import hybrid
    hybrid.RENDER["afterline"] = s_afterline
    hybrid.RENDER["spread"] = s_spread
    hybrid.RENDER["share"] = s_share
