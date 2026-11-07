"""그래픽 컴포넌트 — 같은 '연출 의도'를 다른 그림으로 그린다 (docs/13-direction-vs-graphics.md).

연출(대본)은 장면의 **의도**와 **데이터·박자**만 정한다:
    compare    두(여러) 값 비교          예) 719 vs 347, 50.9세 vs 39.1세
    proportion 전체 중 일부(비율)         예) 100명 중 33명
    flow       원인 → 결과 사슬           (인과 지도 칸 모양)
    chapter    장 표지
    lower      인물·장소 소개 자막(이름 띠)
그래픽 팩(skins/<id>/skin.yaml 의 components)이 의도마다 **컴포넌트**를 고른다:
    compare    : bars(막대) · duel(큰 숫자 맞대기) · pictogram(아이콘 줄)
    proportion : people(사람 100명) · waffle(네모 칸 100개) · donut(도넛)
    flow       : box(손그림 네모) · pill(둥근 알약) · sticky(포스트잇) · circle(동그라미)
    chapter    : paper(종이 한 장이 밀려옴) · type(화면 가득 큰 글씨)
    lower      : strip(종이 띠) · bar(얇은 선 + 글씨)
장면 하나만 바꾸려면 대본 장면에 "look": "<컴포넌트>".
예전 장면 type(bars·versus·people …)은 의도로 자동 변환된다 → 예전 대본도 그래픽 팩만 바꾸면 다른 그림으로 나온다.
변환할 수 없는 데이터(예: '스페인' vs '?' 처럼 숫자가 아님)는 원래 그림 그대로 둔다.
"""
from __future__ import annotations

import math
import re

INTENT = {"bars": "compare", "versus": "compare", "people": "proportion", "compare_values": "compare", "proportion": "proportion"}
DEFAULT = {"compare": None, "proportion": None, "flow": "box", "chapter": "paper", "lower": "strip"}


def component(D, intent: str, sc: dict | None = None):
    if sc and sc.get("look"):
        return sc["look"]
    return (D.skin.get("components") or {}).get(intent, DEFAULT.get(intent))


def _num(s) -> float | None:
    m = re.search(r"-?\d[\d,]*(?:\.\d+)?", str(s))
    return float(m.group().replace(",", "")) if m else None


# ---------------------------------------------------------------- 데이터 맞추기 (장면 type → 의도 데이터)
def compare_data(sc: dict) -> dict | None:
    t = sc["type"]
    if t in ("bars", "compare_values"):
        items = [{"label": i["label"], "value": float(i["value"]), "text": f'{i.get("text", i["value"])}'} for i in sc["items"]]
        return {"items": items, "unit": sc.get("unit", ""), "title": sc.get("title", ""), "question": "", "emph": 0}
    if t == "versus":
        L, R = sc["left"], sc["right"]
        a, b = _num(L["value"]), _num(R["value"])
        if a is None or b is None:
            return None
        q = sc["beats"][1].get("question", "") if len(sc["beats"]) > 1 else ""
        return {"items": [{"label": L["label"], "value": abs(a), "text": L["value"], "icon": L.get("icon")},
                          {"label": R["label"], "value": abs(b), "text": R["value"], "icon": R.get("icon")}],
                "unit": "", "title": sc.get("title", ""), "question": q, "emph": 1}
    return None


def proportion_data(sc: dict) -> dict | None:
    if sc["type"] in ("people", "proportion"):
        pct = float(sc.get("percent", sc.get("count", 0)))
        return {"pct": pct, "value": sc.get("value", f"{pct:g}%"), "caption": sc.get("caption", ""), "sub": sc.get("sub", ""),
                "title": sc.get("title", "")}
    return None


def dispatch(D, sc: dict, bt: list, dur: float, render: dict) -> bool:
    """그래픽 팩이 다른 컴포넌트를 고르면 그걸로 그리고 True. 아니면 False(원래 장면 함수로)."""
    intent = INTENT.get(sc["type"])
    if not intent:
        return False
    comp = component(D, intent, sc)
    if not comp:
        return False
    if intent == "compare":
        data = compare_data(sc)
        if not data:
            return False
        if comp == "bars" and sc["type"] != "bars":
            return _bars(D, sc, bt, data, render) or True
        if comp == "duel" and sc["type"] != "versus" and len(data["items"]) == 2:
            return _duel(D, sc, bt, data, render) or True
        if comp == "pictogram":
            return _pictogram(D, sc, bt, data) or True
        return False
    if intent == "proportion":
        data = proportion_data(sc)
        if not data:
            return False
        if comp == "waffle":
            return _waffle(D, sc, bt, data) or True
        if comp == "donut":
            return _donut(D, sc, bt, data) or True
        return False
    return False


# ---------------------------------------------------------------- compare
def _head(D, sc, title):
    from .hybrid import FT  # noqa: F401
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    if title:
        D.h1(title, y=140)


def _question(D, data, bt):
    from .hybrid import FT, W
    if data.get("question"):
        t = bt[-1][0]
        D.text(W / 2, 930 - 60, data["question"], FT("title"), 60, D.ink, at=t + 1.0)
        D.sfx.append(("pop", t + 1.0))


def _bars(D, sc, bt, data, render):
    fake = dict(sc, items=[{"label": i["label"], "value": i["value"]} for i in data["items"]], unit=data["unit"],
                title=data["title"] or "")
    if data["emph"] == 1 and len(fake["items"]) == 2:   # 강조 항목을 첫 칸(빨강)으로
        fake["items"] = fake["items"][::-1]
    render["bars"](D, fake, bt, 0)
    _question(D, data, bt)


def _duel(D, sc, bt, data, render):
    a, b = data["items"]
    fake = dict(sc, left={"value": a["text"], "label": a["label"], "icon": a.get("icon") or "scale"},
                right={"value": b["text"], "label": b["label"], "icon": b.get("icon") or "scale"},
                beats=sc["beats"] + ([{"question": data["question"]}] if len(sc["beats"]) < 2 else []))
    render["versus"](D, fake, bt if len(bt) > 1 else bt + [(bt[-1][0] + 0.8, 1.0)], 0)


def _pictogram(D, sc, bt, data):
    """아이콘 줄: 값마다 같은 크기 아이콘을 늘어놓는다(최대값 = 20개). 강조 줄은 강조색."""
    from .hybrid import FT, fit
    _head(D, sc, data["title"])
    items = data["items"]
    top = max(i["value"] for i in items) or 1
    n_rows = len(items)
    y0 = 330 if n_rows <= 2 else 280
    step = min(230, 520 // max(n_rows, 1))
    t1 = bt[-1][0]
    g = D._id()
    out = []
    for r, it in enumerate(items):
        y = y0 + r * step
        n = max(1, round(20 * it["value"] / top))
        col = D.red if r == data["emph"] else D.ink
        D.text(330, y, it["label"], FT("box"), fit(FT("box"), it["label"], 42, 300).size, D.ink, at=t1 + 0.1 + r * 0.9, anchor="rm")
        for k in range(n):
            cx = 390 + k * 56
            out.append(f'<g class="{g}r{r}" style="opacity:0"><circle cx="{cx}" cy="{y - 18}" r="11" fill="{col}"/>'
                       f'<path d="M{cx - 16},{y + 22} v-8 a16,14 0 0 1 32,0 v8 z" fill="{col}"/></g>')
        D.js.append(f'tl.to(".{g}r{r}",{{opacity:1,duration:0.12,stagger:0.03}},{t1 + 0.2 + r * 0.9:.2f});')
        D.text(390 + n * 56 + 30, y, it["text"] if it.get("text") else f'{it["value"]:g}', FT("value"), 64, col,
               at=t1 + 0.6 + r * 0.9, anchor="lm", counter=True)
        D.sfx.append(("pop", t1 + 0.3 + r * 0.9))
    D.svg.append("".join(out))
    if data["unit"]:
        D.text(1700, 220, data["unit"], FT("note"), 40, "#5a5f6a", at=t1)
    _question(D, data, bt)


# ---------------------------------------------------------------- proportion
def _fill_time(sc, bt):
    return next((t for b, (t, _) in zip(sc["beats"], bt) if b.get("fill")), bt[-1][0])


def _right_text(D, data, tf, x=1180):
    from .hybrid import FT, fit
    D.text(x, 470, data["value"], FT("value"), 150, D.red, at=tf + 0.6, anchor="lm", counter=True)
    D.text(x, 600, data["caption"], FT("note"), fit(FT("note"), data["caption"], 50, 700).size, D.ink, at=tf + 0.9, anchor="lm")
    if data["sub"]:
        D.text(x, 690, data["sub"], FT("label"), fit(FT("label"), data["sub"], 34, 700).size, "#5a5f6a", at=tf + 1.1, anchor="lm")


def _waffle(D, sc, bt, data):
    """네모 칸 100개, 비율만큼 강조색으로 차오름 (왼쪽 위부터)."""
    _head(D, sc, data["title"])
    g = D._id()
    n = round(data["pct"])
    out = []
    x0, y0, s = 330, 250, 62
    for k in range(100):
        r_, c_ = divmod(k, 10)
        x, y = x0 + c_ * s, y0 + r_ * s
        out.append(f'<rect class="{g}" x="{x}" y="{y}" width="{s - 10}" height="{s - 10}" rx="6" fill="#c9c0ae" style="opacity:0"/>')
        if k < n:
            out.append(f'<rect class="{g}h" x="{x}" y="{y}" width="{s - 10}" height="{s - 10}" rx="6" fill="{D.red}" style="opacity:0"/>')
    D.svg.append("".join(out))
    D.js.append(f'tl.to(".{g}",{{opacity:1,duration:0.15,stagger:0.006}},{bt[0][0] + 0.3:.2f});')
    tf = _fill_time(sc, bt)
    D.js.append(f'tl.to(".{g}h",{{opacity:1,duration:0.12,stagger:0.015}},{tf + 0.3:.2f});')
    D.sfx.append(("pop", tf + 0.3))
    _right_text(D, data, tf)


def _donut(D, sc, bt, data):
    """도넛 그래프: 비율만큼 호가 그려지고 가운데 숫자."""
    from .hybrid import FT
    _head(D, sc, data["title"])
    cx, cy, r, w = 640, 560, 250, 70
    circ = 2 * math.pi * r
    g = D._id()
    D.svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#c9c0ae" stroke-width="{w}"/>'
                 f'<circle id="{g}" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{D.red}" stroke-width="{w}" '
                 f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}" transform="rotate(-90 {cx} {cy})"/>')
    tf = _fill_time(sc, bt)
    D.js.append(f'tl.to("#{g}",{{strokeDashoffset:{circ * (1 - data["pct"] / 100):.1f},duration:1.2,ease:"power2.out"}},{tf + 0.3:.2f});')
    D.text(cx, cy, data["value"], FT("value"), 120, D.red, at=tf + 0.5, counter=True)
    D.sfx.append(("pop", tf + 0.4))
    _right_text(D, dict(data, value=""), tf)


# ---------------------------------------------------------------- flow 칸 모양
def node(D, x, y, bw, bh, col, state, at, d):
    """인과 지도 칸 그리기 — 모양은 그래픽 팩의 flow 컴포넌트."""
    style = component(D, "flow")
    fill = "rgba(196,69,47,0.22)" if state == "active" else None
    width = 3.5 if state == "active" else 2.8
    if style == "circle":
        D.rough("ellipse", [x, y, bw, bh + 20], col, width, fill=fill, at=at, dur=d, gap=0.0)
    elif style == "pill":
        i = D._id()
        bgc = "rgba(196,69,47,0.22)" if state == "active" else "#FBF8F1"
        D.items.insert(0, f'<div id="{i}" style="position:absolute;left:{x - bw / 2:.0f}px;top:{y - bh / 2:.0f}px;width:{bw}px;height:{bh}px;'
                          f'border-radius:{bh / 2:.0f}px;border:4px solid {col};background:{bgc}"></div>')
        D.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:{max(d, 0.01):.2f}}},{at:.2f});')
    elif style == "sticky":
        i = D._id()
        bgc = "#F3D36B" if state == "active" else "#FBF8F1"
        rot = ((x * 7 + y * 3) % 5 - 2) * 0.8
        D.items.insert(0, f'<div id="{i}" style="position:absolute;left:{x - bw / 2:.0f}px;top:{y - bh / 2:.0f}px;width:{bw}px;height:{bh}px;'
                          f'background:{bgc};box-shadow:0 8px 18px rgba(0,0,0,.22);transform:rotate({rot:.1f}deg);'
                          f'border-top:14px solid rgba(0,0,0,.06)"></div>')
        D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:{max(d, 0.01):.2f}}},{at:.2f});')
    else:  # box
        D.rough("rectangle", [x - bw / 2, y - bh / 2, bw, bh], col, width, fill=fill, at=at, dur=d, gap=0.0)


# ---------------------------------------------------------------- chapter
def chapter_type(D, sc: dict):
    """장 표지 'type': 강조색 판이 화면을 덮고 거대한 장 번호 + 제목."""
    from .hybrid import FT, W, HH, fit
    i = D._id()
    D.media.append(f'<div id="{i}" style="position:absolute;inset:0;background:{D.red}"></div>')
    D.js.append(f'tl.fromTo("#{i}",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.55,ease:"power3.out"}},0);')
    D.sfx.append(("whoosh", 0.0))
    D.text(170, 430, f"{sc.get('num', '')}", FT("value"), 360, "#FBF8F1", at=0.45, anchor="lm")
    f = fit(FT("title"), sc["title"], 96, W - 700)
    D.text(560, 470, sc["title"], FT("title"), f.size, "#FBF8F1", at=0.7, anchor="lm")
    D.rough("line", [560, 560, 560 + f.getlength(sc["title"]), 564], "#FBF8F1", 5, at=1.1, dur=0.4)


# ---------------------------------------------------------------- lower third
def lower_bar(D, name: str, role: str, at: float):
    """이름 자막 'bar': 카드 없이 얇은 강조선 + 굵은 이름 + 작은 설명."""
    from .hybrid import FT, fit, _e
    i = D._id()
    f = fit(FT("title"), name, 50, 900)
    D.items.append(
        f'<div id="{i}" style="position:absolute;left:96px;top:770px">'
        f'<div style="width:90px;height:6px;background:{D.red};margin-bottom:12px"></div>'
        f'<div style="font-family:sans-x;font-size:{f.size}px;color:#FFFFFF;text-shadow:0 2px 10px rgba(0,0,0,.8);white-space:nowrap">{_e(name)}</div>'
        f'<div style="font-family:sans;font-size:26px;color:#EEEEEE;text-shadow:0 2px 8px rgba(0,0,0,.8);white-space:nowrap;margin-top:4px">{_e(role)}</div></div>')
    D.js.append(f'tl.fromTo("#{i}",{{x:-40,opacity:0}},{{x:0,opacity:1,duration:0.45,ease:"power3.out"}},{at:.2f});')
    D.sfx.append(("click-soft", at))
