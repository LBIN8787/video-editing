"""편집 기준 v10→v12 (manual 05 §0-4) — 기본으로 켜짐. 끄려면 대본 맨 위 "edit_v10": false.
v12(2026-11-11 사용자 판정 '너무 정신없다·배경음 억지'): 전환은 부드러운 겹침, 장 표지만 밀기, 카메라는 한 방향으로 아주 천천히, 배경음은 기본 없음.

A2 장면 전환   : 딱 자르기 대신 앞 장면 끝 0.3초 + 다음 장면 처음 0.35초에 걸친 전환 (wipe·push·zoom·iris 를 돌려 씀)
A3 장면 안 움직임: 박자마다, 긴 박자는 4.5초마다 카메라가 살짝 다가가거나 옮겨 감 (멈춘 화면 줄이기)
A1 소리        : 전환마다 휙 소리, 장 표지 앞 상승음(riser)·표지에 낮은 타격음, 정리판 차임, 잔잔한 배경 패드(직접 합성, 목소리 나올 때 낮춤)
B11 정리판(recap) · B3 사물 그림 통계(isotype) · A5 사진 장 표지(chapter look=photo)
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from .hybrid import FT, HH, W, _e, fit

KINDS = ["wipe", "push", "zoom", "iris"]
NO_PULSE = {"kb", "journey", "kinetic", "chapter", "footage", "zoomshot", "outro"}
WHOOSH = {"wipe": "whoosh", "push": "whoosh-short", "zoom": "whoosh", "iris": "whoosh-short"}


def kind_of(spec: dict, sc_id: int) -> str:
    """v12 (사용자 판정 '너무 정신없다'): 보통 장면 사이는 부드러운 겹침(fade), 장 표지로 들어갈 때만 밀기(push)."""
    sc = next((s for s in spec["scenes"] if s["id"] == sc_id), None)
    if sc and sc.get("tr"):
        return sc["tr"]
    return "push" if sc and sc.get("type") == "chapter" else "fade"


def apply(D, spec: dict, sc: dict, bt: list, dur: float):
    ids = [s["id"] for s in spec["scenes"]]
    first, last = sc["id"] == ids[0], sc["id"] == ids[-1]
    acc = D.red
    # ---- 들어오기 (첫 장면 제외)
    if not first:
        k = kind_of(spec, sc["id"])
        if k == "fade":
            D.js.append('tl.fromTo("#root",{opacity:0},{opacity:1,duration:0.35,ease:"power1.out"},0);')
        elif k == "wipe":
            i = D._id()
            D.top = getattr(D, "top", []) + [f'<div id="{i}" style="position:absolute;inset:0;background:{acc};z-index:50" data-layout-ignore></div>']
            D.js.append(f'tl.fromTo("#{i}",{{x:0}},{{x:{W},duration:0.4,ease:"power3.in"}},0);')
        elif k == "push":
            D.js.append(f'tl.fromTo("#root",{{x:{W * 0.12:.0f},opacity:0}},{{x:0,opacity:1,duration:0.5,ease:"power2.out"}},0);')
        elif k == "zoom":
            D.js.append('tl.fromTo("#root",{scale:0.82,filter:"blur(14px)",opacity:0.4},{scale:1,filter:"blur(0px)",opacity:1,duration:0.45,ease:"power3.out"},0);')
        elif k == "iris":
            D.js.append('tl.fromTo("#root",{clipPath:"circle(0% at 50% 50%)"},{clipPath:"circle(80% at 50% 50%)",duration:0.5,ease:"power2.out"},0);')
    # ---- 나가기 (마지막 장면 제외) — 다음 장면의 전환과 이어지게
    if not last:
        nxt = ids[ids.index(sc["id"]) + 1]
        k = kind_of(spec, nxt)
        t = max(0.0, dur - 0.3)
        if k == "fade":
            D.js.append(f'tl.to("#root",{{opacity:0,duration:0.25,ease:"power1.in"}},{t:.2f});')
        elif k == "wipe":
            i = D._id()
            D.top = getattr(D, "top", []) + [f'<div id="{i}" style="position:absolute;inset:0;background:{acc};z-index:50;transform:translateX(-{W}px)" data-layout-ignore></div>']
            D.js.append(f'tl.fromTo("#{i}",{{x:{-W}}},{{x:0,duration:0.3,ease:"power3.out"}},{t:.2f});')
        elif k == "push":
            D.js.append(f'tl.to("#root",{{x:{-W * 0.12:.0f},opacity:0,duration:0.3,ease:"power2.in"}},{t:.2f});')
        elif k == "zoom":
            D.js.append(f'tl.to("#root",{{scale:1.2,filter:"blur(14px)",opacity:0.4,duration:0.3,ease:"power3.in"}},{t:.2f});')
        elif k == "iris":
            D.js.append(f'tl.to("#root",{{clipPath:"circle(0% at 50% 50%)",duration:0.3,ease:"power2.in"}},{t:.2f});')
        if k == "push":   # 소리는 장이 바뀔 때만, 작게 (v12)
            D.sfx.append(("whoosh-short", max(0.0, dur - 0.25)))
    # ---- 장면 안 움직임 (카메라가 박자마다 다가감)
    fx = sc.get("fx") or []
    if sc.get("type") not in NO_PULSE and not ({"tilt", "dolly"} & set(fx if isinstance(fx, list) else [fx])):
        D.css.append("#layer{transform-origin:50% 50%}")
        marks = []
        for k, (b0, bd) in enumerate(bt):
            if k > 0:
                marks.append(b0)
            n = int(bd // 4.5)
            marks += [b0 + bd * (j + 1) / (n + 1) for j in range(n)] if bd > 5 else []
        # v12: 장면 내내 한 방향으로 아주 천천히 다가가기만 (박자마다 흔들지 않음)
        D.js.append(f'tl.fromTo("#layer",{{scale:1}},{{scale:1.025,duration:{max(1.0, dur - 0.3):.2f},ease:"none"}},0);')


# ---------------------------------------------------------------- B11 정리판
def s_recap(D, sc, bt, dur):
    """장 끝 정리판: 지금까지의 한 줄 결론을 쌓는다. 이전 줄은 흐리게, 이번 줄은 밝게 타자."""
    D.label(sc.get("label", "정리"))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    items = sc["items"]
    new = sc.get("new_from", len(items) - 1)
    D.h1(sc.get("title", "여기까지 정리"), y=170)
    from .hybrid import accent_text
    acc_t = accent_text(D)
    r, g, b = (int(D.red.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    on_acc = "#15171D" if 0.299 * r + 0.587 * g + 0.114 * b > 150 else "#FFFFFF"
    y0 = 330
    step = 150 if len(items) <= 4 else 118   # 5줄 이상이면 촘촘히 (마지막 줄이 아래 자막에 가리지 않게: 330+4*118=802)
    for k, it in enumerate(items):
        y = y0 + k * step
        fresh = k >= new
        b = min(k - new, len(bt) - 1) if fresh else 0
        at = (bt[b][0] + 0.3) if fresh else 0.25 + 0.15 * k
        i = D._id()
        col = D.ink if fresh else "rgba(236,229,213,.45)"
        D.items.append(f'<div id="{i}" style="position:absolute;left:260px;top:{y}px;width:1400px;display:flex;align-items:center;gap:30px;'
                       f'font-family:sans-x;font-size:46px;color:{col};opacity:0">'
                       f'<span style="flex:none;width:74px;height:74px;border-radius:12px;background:{D.red if fresh else "transparent"};'
                       f'border:3px solid {acc_t};color:{on_acc if fresh else acc_t};display:flex;align-items:center;justify-content:center;'
                       f'font-size:38px;font-weight:700">{k + 1}</span><span>{_e(it)}</span></div>')
        D.js.append(f'tl.fromTo("#{i}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},{at:.2f});')
        if fresh:
            D.sfx.append(("chime", at))


# ---------------------------------------------------------------- B3 사물 그림 통계
def s_isotype(D, sc, bt, dur):
    """사물 아이콘 줄: total 개 중 lost 개가 흐려지며 빠진다 (예: 기름통 10통 중 3통). 숫자 라벨 2개."""
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D.h1(sc.get("title", ""), y=150)
    n, lost, icon = sc.get("total", 10), sc.get("lost", 3), sc.get("icon", "fuel")
    size, gap = 120, 34
    x0 = W / 2 - (n * size + (n - 1) * gap) / 2 + size / 2
    y = 480
    t0 = bt[0][0] + 0.4
    from .icons import svg_markup
    for k in range(n):
        i = D._id()
        mk = svg_markup(icon, size, D.red if k < n - lost else D.ink) or ""
        x = x0 + k * (size + gap)
        D.items.append(f'<div id="{i}" class="i" style="left:{x - size / 2:.0f}px;top:{y - size / 2:.0f}px">{mk}</div>')
        D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(2)"}},{t0 + 0.08 * k:.2f});')
        if k >= n - lost and len(bt) > 1:
            tb = bt[1][0] + 0.3 + 0.25 * (k - (n - lost))
            D.js.append(f'tl.to("#{i}",{{opacity:0.15,y:40,rotation:-12,duration:0.5,ease:"power2.in"}},{tb:.2f});')
            D.sfx.append(("pop", tb))
    D.text(W / 2, 680, sc.get("before", ""), FT("value"), 64, D.ink, at=t0 + 0.9)
    if len(bt) > 1 and sc.get("after"):
        D.text(W / 2, 790, sc["after"], FT("value"), 78, D.red, at=bt[1][0] + 0.5 + 0.25 * lost)


# ---------------------------------------------------------------- A5 사진 장 표지
def chapter_photo(D, sc, bt, dur):
    """장 표지 'photo': 흐린 자료 사진 바탕(backdrop photo) 위에 큰 번호 + 제목 + 가는 선이 그려짐."""
    from .hybrid import accent_text
    D.text(W / 2, 360, f"{sc.get('num', '')}", FT("value"), 220, accent_text(D), at=0.35)
    f = fit(FT("title"), sc["title"], 92, W - 300)
    D.text(W / 2, 560, sc["title"], FT("title"), f.size, D.ink, at=0.6)
    w = f.getlength(sc["title"])
    D.rough("line", [W / 2 - w / 2, 630, W / 2 + w / 2, 634], D.red, 5, at=0.95, dur=0.45)
    i = D._id()
    D.items.append(f'<div id="{i}" style="position:absolute;left:0;right:0;top:0;bottom:0;box-shadow:inset 0 0 220px rgba(0,0,0,.6)"></div>')
    D.js.append('tl.fromTo("#layer",{scale:1.08},{scale:1,duration:%.2f,ease:"none"},0);' % dur)


def register():
    from . import hybrid
    orig = hybrid.RENDER["chapter"]

    def chapter(D, sc, bt, dur):
        return chapter_photo(D, sc, bt, dur) if sc.get("look") == "photo" else orig(D, sc, bt, dur)
    hybrid.RENDER.update({"recap": s_recap, "isotype": s_isotype, "chapter": chapter})


# ---------------------------------------------------------------- A1 배경 패드 (직접 합성 — 저작권 걱정 없음)
def pad(out: Path, dur: float, mood: str = "calm") -> Path:
    """낮은 화음 4개(사인파) + 느린 떨림 + 저역 통과 + 울림. 목소리 밑에 깔리는 잔잔한 바탕."""
    notes = {"calm": [110.0, 164.81, 220.0, 277.18], "tense": [98.0, 146.83, 196.0, 233.08]}[mood]
    expr = "+".join(f"0.18*sin(2*PI*{f}*t)*(0.6+0.4*sin(2*PI*{0.05 + 0.03 * k:.2f}*t))" for k, f in enumerate(notes))
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    f"aevalsrc='{expr}':s=48000:d={dur + 1:.2f}", "-af",
                    f"lowpass=f=900,aecho=0.8:0.7:120|260:0.25|0.18,afade=t=in:d=2,afade=t=out:st={max(0, dur - 2.5):.2f}:d=2.5,volume=0.5",
                    "-ac", "2", str(out)], check=True)
    return out


def prepare(spec: dict, sc: dict):
    """장 표지에 look 이 없으면 사진 표지로: 자료 화면을 장 번호 순서로 돌려 씀 (사용자 판정 2026-11-10: 전환 때 배경도 바뀌는 게 낫다)."""
    if sc.get("type") != "chapter" or sc.get("look") or not spec.get("footage"):
        return
    keys = list(spec["footage"])
    n = int(sc.get("chapter", 1) or 1)
    sc.setdefault("bg", "photo")
    sc.setdefault("bg_src", keys[(n - 1) % len(keys)])
    sc["look"] = "photo"


# ---------------------------------------------------------------- A1 배경음 (등록부 assets/bgm/bgm.yaml 의 곡)
def bgm_track(tid: str) -> dict | None:
    import yaml
    from .. import config
    reg = yaml.safe_load((config.ROOT / "assets" / "bgm" / "bgm.yaml").read_text(encoding="utf-8")) or {}
    t = (reg.get("tracks") or {}).get(tid)
    if not t:
        return None
    f = config.ROOT / "assets" / "bgm" / t["file"]
    if not f.exists():   # 음원은 커밋하지 않으므로 없으면 등록부 주소에서 다시 받음
        subprocess.run(["curl", "-sSL", "-o", str(f), t["url"]], check=False)
    return dict(t, path=f) if f.exists() else None


def music(out: Path, dur: float, tid: str) -> Path | None:
    """곡을 영상 길이에 맞춰 반복·자르고, 음량을 -28 LUFS 안팎으로 맞춘 뒤 앞뒤 페이드."""
    t = bgm_track(tid)
    if not t:
        return None
    # 곡이 영상보다 짧으면 이음매를 3초 겹쳐(acrossfade) 이어 붙임 — 딱 끊기는 반복 없이
    src = str(t["path"])
    ln = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                              capture_output=True, text=True).stdout or 0)
    n = max(1, int((dur + 1) // max(1.0, ln - 3)) + 1) if ln else 1
    ins = sum((["-i", src] for _ in range(n)), [])
    chain, last = [], "[0:a]"
    for k in range(1, n):
        chain.append(f"{last}[{k}:a]acrossfade=d=3:c1=tri:c2=tri[x{k}]")
        last = f"[x{k}]"
    chain.append(f"{last}atrim=0:{dur + 0.5:.2f},loudnorm=I=-30:TP=-8:LRA=7,afade=t=in:d=1.5,afade=t=out:st={max(0, dur - 3):.2f}:d=3[o]")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *ins, "-filter_complex", ";".join(chain),
                    "-map", "[o]", "-ar", "48000", "-ac", "2", str(out)], check=True)
    return out


# hybrid 보다 먼저 이 모듈을 불러온 경우(순환 import)에도 새 장면이 등록되게
import sys as _sys  # noqa: E402
if "ytflow.stages.hybrid" in _sys.modules and hasattr(_sys.modules["ytflow.stages.hybrid"], "RENDER") \
        and "recap" not in _sys.modules["ytflow.stages.hybrid"].RENDER:
    register()


# ---------------------------------------------------------------- 상황별 바탕 (v14, 2026-11-11 사용자 판정)
# "배경은 특정 배경으로 고정이 아니라 그 상황에 어울리게 — 스타일에 포함되는 내용"
# 영상의 기본 팩(edit.yaml skin)은 오프닝·장 표지·자료 화면·끝처럼 '얼굴' 장면에 쓰고,
# 나머지 장면은 하는 일(숫자·발언·구조)에 맞는 팩을 고른다. 밝기 계열(밝음/어두움)은 기본 팩과 맞춰 너무 튀지 않게.
SITUATION = {
    "data":      ({"bars", "chart", "versus", "bignum", "isotype", "people", "compare_values", "newsdesk"}, ["slate", "clean-white"], ["midnight", "blueprint"]),
    "voice":     ({"quote"}, ["clean-white", "slate"], ["dark-doc", "forest"]),
    "structure": ({"map_causal", "analogy", "checklist", "recap", "timeline"}, ["paper-sketch", "clean-white"], ["forest", "midnight"]),
}


def situation_skin(sc: dict, base_skin: str) -> str | None:
    """장면 type → 상황 → 그 상황의 팩 (기본 팩과 같은 것은 건너뜀). 해당 없으면 None(기본 팩)."""
    from . import skin as _skin
    b = (_skin.load(base_skin).get("palette", {}) or {}).get("base") or "#F3EFE6"
    dark = sum(int(b.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)) < 300
    for _, (types, light, darkl) in SITUATION.items():
        if sc.get("type") in types:
            for cand in (darkl if dark else light):
                if cand != base_skin:
                    return cand
    return None
