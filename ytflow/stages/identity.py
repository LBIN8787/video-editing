"""v15 카테고리 개성 (사용자 요청 2026-11-12: '채널을 묶어 운영해도 카테고리마다 특색이 있었으면',
'화면 전환 배경이 전부 NASA 사진 — 상황·카테고리·주제에 따라 바꿔 달라').

channels/brands.yaml 의 identity.<brand> 를 읽어 장면을 그 카테고리답게 바꾼다.
  - 장 표지: chapter_looks 를 장 번호 순서로 돌려 씀
        photo  듀오톤 자료 사진 (카테고리의 두 색으로 물들임, 출처 표기)
        board  코르크 증거판 위 핀 꽂은 카드        (시사)
        chalk  칠판 판서                              (호기심)
        dash   대시보드 바탕 + 큰 번호               (시장)
        window 은은한 빛 바탕 위 앱 창               (AI)
  - 인과 지도: structure 가 board 면 증거판(카드 + 붉은 실), chalk 면 칠판 팩
  - 상황별 팩: situation 이 있으면 manual 05 §0-6 의 기본 표 대신 카테고리 표

hybrid.json 에 "brand": "issues" (장면에 "brand" 를 쓰면 그 장면만). 없으면 아무것도 바꾸지 않음(예전 영상 그대로).
"""
from __future__ import annotations

import functools
import hashlib

import yaml

from .. import config

LOOK_BG = {"board": ("cork", "corkboard"), "chalk": ("chalk", "chalkboard"), "dash": ("dash", "midnight"), "window": ("glow", "midnight")}
_REGISTERED = False


@functools.lru_cache(maxsize=1)
def _all() -> dict:
    d = yaml.safe_load((config.ROOT / "channels" / "brands.yaml").read_text(encoding="utf-8")) or {}
    return d.get("identity") or {}


def get(spec: dict, sc: dict | None = None) -> dict | None:
    b = (sc or {}).get("brand") or spec.get("brand")
    idn = _all().get(b) if b else None
    return dict(idn, id=b) if idn else None


def prepare(spec: dict, sc: dict) -> None:
    """장면 dict 에 look·bg·skin·bg_src 를 채운다 (대본에 직접 쓴 값은 그대로 둠)."""
    idn = get(spec, sc)
    t = sc.get("type")
    look = sc.get("look")
    # 상황으로 직접 고른 모양 (카테고리와 상관없이): 인과 지도·비유에 "look": "board" | "chalk", 장 표지에 dash·window·board·chalk
    if t in ("map_causal", "analogy") and look in ("board", "chalk"):
        register()
        if look == "board" and t == "map_causal":
            sc["type"] = "board"
        sc.setdefault("bg", "cork" if look == "board" else "chalk")
        sc.setdefault("skin", "corkboard" if look == "board" else "chalkboard")
        return
    if t == "chapter" and look in LOOK_BG and not idn:
        register()
        bg, skin = LOOK_BG[look]
        sc.setdefault("bg", bg)
        sc.setdefault("skin", skin)
        return
    if not idn:
        return
    register()
    sc["_duo"] = idn.get("duotone")
    fo = spec.get("footage") or {}
    if t == "chapter":
        if not sc.get("look"):
            looks = idn.get("chapter_looks") or ["photo"]
            n = int(sc.get("chapter", 1) or 1)
            look = looks[(n - 1) % len(looks)]
            if look == "photo" and not fo:
                look = next((x for x in looks if x != "photo"), "window")
            sc["look"] = look
        look = sc["look"]
        if look == "photo":
            sc.setdefault("bg", "duotone")
            if fo:
                keys = list(fo)
                photos = [k for k in keys if fo[k].get("cover", True)]
                n = int(sc.get("chapter", 1) or 1)
                sc.setdefault("bg_src", (photos or keys)[(n - 1) % len(photos or keys)])
                sc["_credit"] = fo.get(sc["bg_src"], {}).get("credit", "")
            sc.setdefault("skin", "midnight" if idn["id"] == "ai" else "dark-doc")
        elif look in LOOK_BG:
            bg, skin = LOOK_BG[look]
            sc.setdefault("bg", bg)
            sc.setdefault("skin", skin)
        return
    if look == "plain":   # 이 장면은 카테고리 모양을 쓰지 않음
        return
    if t == "map_causal" and idn.get("structure") == "board":
        sc["type"] = "board"
        sc.setdefault("bg", "cork")
        sc.setdefault("skin", "corkboard")
        return
    if t in ("map_causal", "analogy") and idn.get("structure") == "chalk":
        sc.setdefault("bg", "chalk")
        sc.setdefault("skin", "chalkboard")
        return


def situation_skin(spec: dict, sc: dict, base_skin: str) -> str | None:
    """카테고리 표가 있으면 그것으로, 없으면 None (→ edit10 기본 표)."""
    idn = get(spec, sc)
    if not idn or not idn.get("situation"):
        return None
    from . import edit10
    for name, (types, _l, _d) in edit10.SITUATION.items():
        if sc.get("type") in types:
            for cand in idn["situation"].get(name) or []:
                if cand != base_skin:
                    return cand
    return None


# ---------------------------------------------------------------- 장 표지
def _h(key: str, lo: float, hi: float) -> float:
    v = int(hashlib.md5(key.encode()).hexdigest()[:6], 16) / 0xFFFFFF
    return lo + (hi - lo) * v


def chapter_board(D, sc, bt, dur):
    """코르크 판에 핀으로 꽂힌 사건 파일 카드: 작은 머리글 + 제목 + 붉은 밑줄."""
    from .hybrid import FT, W, HH, fit
    x0, y0, w, h = W / 2 - 540, HH / 2 - 225, 1080, 450
    c = D._id()
    D.items.append(f'<div id="{c}" style="position:absolute;left:{x0:.0f}px;top:{y0:.0f}px;width:{w}px;height:{h}px;background:#F1E9D5;'
                   f'box-shadow:0 18px 40px rgba(0,0,0,.45),0 2px 0 rgba(0,0,0,.08) inset;transform:rotate(-1.2deg)"></div>')
    D.js.append(f'tl.fromTo("#{c}",{{opacity:0,y:-50,rotation:-4}},{{opacity:1,y:0,rotation:-1.2,duration:0.6,ease:"power2.out"}},0.15);')
    D.text(W / 2, y0 + 95, f"사건 파일 · {sc.get('num', '')}", FT("label"), 34, "#9A3226", at=0.55)
    f = fit(FT("title"), sc["title"], 86, w - 160)
    D.text(W / 2, y0 + 225, sc["title"], FT("title"), f.size, "#2A221B", at=0.75)
    tw = f.getlength(sc["title"])
    D.rough("line", [W / 2 - tw / 2, y0 + 290, W / 2 + tw / 2, y0 + 293], "#B8322A", 5, at=1.1, dur=0.45)
    if sc.get("sub"):
        D.text(W / 2, y0 + 360, sc["sub"], FT("label"), 34, "#5C5248", at=1.3)
    _pin(D, W / 2, y0 + 18, 0.75)


def _pin(D, x, y, at):
    p = D._id()
    D.items.append(f'<div id="{p}" data-layout-ignore style="position:absolute;left:{x - 17:.0f}px;top:{y - 17:.0f}px;width:34px;height:34px;border-radius:50%;'
                   f'background:radial-gradient(circle at 35% 35%,#F07A6C,#A8261C 70%);box-shadow:3px 6px 8px rgba(0,0,0,.45)"></div>')
    D.js.append(f'tl.fromTo("#{p}",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.5)"}},{at:.2f});')


def chapter_chalk(D, sc, bt, dur):
    """칠판 판서: 큰 번호 + 제목(분필 손글씨) + 노란 분필 밑줄 + 작은 동그라미."""
    from .hybrid import FT, W, fit
    D.css.append(".t{text-shadow:0 0 3px rgba(238,240,234,.35)}")
    D.text(W / 2 - 360, 330, f"{sc.get('num', '')}.", FT("value"), 210, D.red, at=0.35)
    f = fit(FT("title"), sc["title"], 120, W - 420)
    D.text(W / 2, 600, sc["title"], FT("title"), f.size, D.ink, at=0.7)
    tw = f.getlength(sc["title"])
    D.rough("line", [W / 2 - tw / 2, 690, W / 2 + tw / 2, 698], D.red, 6, at=1.2, dur=0.5)
    D.rough("ellipse", [W / 2 - 360, 330, 230, 230], D.ink, 3, at=0.6, dur=0.6)


def chapter_dash(D, sc, bt, dur):
    """대시보드: 왼쪽 위 'CHAPTER 0N' 머리글 + 큰 번호 + 제목 + 얇은 강조선 (가짜 수치는 그리지 않음)."""
    from .hybrid import FT, W, fit
    n = str(sc.get("num", ""))
    D.text(300, 330, f"CHAPTER {n.zfill(2)}", FT("label"), 34, D.red, at=0.3, anchor="lm")
    D.text(300, 470, n.zfill(2), FT("value"), 200, D.ink, at=0.45, anchor="lm", counter=True)
    f = fit(FT("title"), sc["title"], 96, W - 820)
    D.text(620, 470, sc["title"], FT("title"), f.size, D.ink, at=0.8, anchor="lm")
    i = D._id()
    D.items.append(f'<div id="{i}" style="position:absolute;left:300px;top:620px;width:{W - 600}px;height:3px;background:{D.red};transform-origin:left center"></div>')
    D.js.append(f'tl.fromTo("#{i}",{{scaleX:0}},{{scaleX:1,duration:0.8,ease:"power2.inOut"}},1.0);')


def chapter_window(D, sc, bt, dur):
    """은은한 빛 위에 떠 있는 앱 창: 창 막대(점 세 개 + 탭 이름) + 번호 + 제목."""
    from .hybrid import FT, W, HH, fit
    x0, y0, w, h = W / 2 - 600, HH / 2 - 270, 1200, 540
    c = D._id()
    D.items.append(f'<div id="{c}" style="position:absolute;left:{x0:.0f}px;top:{y0:.0f}px;width:{w}px;height:{h}px;border-radius:18px;'
                   f'background:rgba(16,30,48,.88);border:1px solid rgba(160,190,220,.22);box-shadow:0 30px 80px rgba(0,0,0,.55);overflow:hidden">'
                   f'<div style="height:58px;background:rgba(255,255,255,.05);border-bottom:1px solid rgba(160,190,220,.16);position:relative">'
                   + "".join(f'<span style="position:absolute;top:21px;left:{24 + k * 26}px;width:15px;height:15px;border-radius:50%;background:{col}"></span>'
                             for k, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")))
                   + f'<span style="position:absolute;top:14px;left:130px;padding:4px 18px;border-radius:8px 8px 0 0;background:rgba(255,255,255,.07);'
                     f'font-family:sans;font-size:22px;color:#9FB0C6">chapter-{sc.get("num", "")}</span></div></div>')
    D.js.append(f'tl.fromTo("#{c}",{{opacity:0,scale:0.96,y:20}},{{opacity:1,scale:1,y:0,duration:0.6,ease:"power2.out"}},0.15);')
    D.text(W / 2, y0 + 210, f"{sc.get('num', '')}", FT("value"), 140, D.red, at=0.6)
    f = fit(FT("title"), sc["title"], 84, w - 160)
    D.text(W / 2, y0 + 380, sc["title"], FT("title"), f.size, D.ink, at=0.85)


# ---------------------------------------------------------------- 증거판 (인과 지도의 시사판)
def s_board(D, sc, bt, dur):
    """map_causal 과 같은 대본(reveal·draw·active)을 코르크 판 위 카드 + 붉은 실로."""
    from .hybrid import FT, fit
    mp = sc["_map"]
    D.label(sc.get("label", ""), dark=True)   # 코르크 위: 어두운 반투명 띠 + 흰 글자
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    if sc.get("title"):
        D.h1(sc["title"], y=130, size=56)
    CW, CH = 350, 150
    when, strings, active = {}, [], []
    for bi, (b, (t0, d)) in enumerate(zip(sc["beats"], bt)):
        for k_i, k in enumerate(b.get("reveal", [])):
            when.setdefault(k, t0 + 0.25 + 0.3 * k_i)
        for e_i, e in enumerate(b.get("draw", [])):
            strings.append((e, t0 + 0.7 + 0.45 * e_i))
            D.sfx.append(("pencil", t0 + 0.7 + 0.45 * e_i))
        if b.get("active"):
            active.append((b["active"], t0 + 1.0))
    under = len(D.items)          # 실은 카드 아래에 깔고 핀만 위에 (실이 카드 글자를 가로지르지 않게)
    for k, at in when.items():   # 카드 + 글자 (카드가 먼저, 글자는 그 위)
        nd = mp["nodes"][k]
        x, y = nd["x"], nd["y"]
        rot = _h(k, -3.0, 3.0)
        c = D._id()
        D.items.append(f'<div id="{c}" style="position:absolute;left:{x - CW / 2:.0f}px;top:{y - CH / 2:.0f}px;width:{CW}px;height:{CH}px;background:#F1E9D5;'
                       f'box-shadow:0 10px 22px rgba(0,0,0,.42);transform:rotate({rot:.1f}deg)"></div>')
        D.js.append(f'tl.fromTo("#{c}",{{opacity:0,y:-24}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{at:.2f});')
        D.icon(nd.get("icon", ""), x, y - 22, 44, "#2A221B", at=at + 0.1, gap=0.0)
        D.text(x, y + 36, nd["label"], FT("box"), fit(FT("box"), nd["label"], 34, CW - 30).size, "#2A221B", at=at + 0.15, gap=0.0)
    paths, js = [], []
    for (a, b2), at in strings:   # 붉은 실: 핀에서 핀으로, 살짝 처짐
        p, q = mp["nodes"][a], mp["nodes"][b2]
        x1, y1, x2, y2 = p["x"], p["y"] - CH / 2 + 10, q["x"], q["y"] - CH / 2 + 10
        mx, my = (x1 + x2) / 2, max(y1, y2) + 26
        i = D._id()
        paths.append(f'<path id="{i}" d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" fill="none" stroke="#C7322A" stroke-width="4" '
                     f'stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" style="filter:drop-shadow(2px 4px 3px rgba(0,0,0,.4))"/>')
        js.append(f'tl.to("#{i}",{{strokeDashoffset:0,duration:0.5,ease:"power1.inOut"}},{at:.2f});')
    D.items.insert(under, f'<svg data-layout-ignore style="position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible">{"".join(paths)}</svg>')
    D.js.extend(js)
    for k, at in when.items():   # 핀은 실 위
        nd = mp["nodes"][k]
        _pin(D, nd["x"], nd["y"] - CH / 2 + 10, at + 0.25)
    for k, at in active:          # 지금 말하는 카드: 노란 분필 동그라미
        nd = mp["nodes"][k]
        D.rough("ellipse", [nd["x"], nd["y"], CW + 70, CH + 70], D.red, 4.5, at=at, dur=0.55, roughness=1.4)


def register() -> None:
    """hybrid.RENDER 에 증거판 장면과 장 표지 모양을 더한다 (한 번만)."""
    global _REGISTERED
    if _REGISTERED:
        return
    from . import hybrid   # hybrid 를 불러오면 edit10 이 장 표지(photo)를 먼저 등록함 → 그 위에 감싼다
    orig = hybrid.RENDER["chapter"]
    looks = {"board": chapter_board, "chalk": chapter_chalk, "dash": chapter_dash, "window": chapter_window}

    def chapter(D, sc, bt, dur):
        if sc.get("look") in looks:
            return looks[sc["look"]](D, sc, bt, dur)
        r = orig(D, sc, bt, dur)
        if sc.get("look") == "photo" and sc.get("_credit"):
            D.label("자료 사진 · " + sc["_credit"][:90], dark=True)   # 라이선스·작자를 앞에 (잘려도 남게)
        return r
    hybrid.RENDER.update({"chapter": chapter, "board": s_board})
    _REGISTERED = True
