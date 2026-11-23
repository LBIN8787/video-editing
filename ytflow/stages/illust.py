"""손그림 삽화 장면 (스타일 illustrated, styles/illustrated/STYLE.md).

한 장의 삽화(그림체는 자유: 미드센추리 구아슈, 펜+수채, 평면 에디토리얼, 크레용, 판화 …) 위를
카메라가 박자마다 '지금 말하는 부분'으로 옮겨 가고, 손으로 그린 표시(동그라미·화살표·밑줄·말풍선·메모)가 그 순간 그려진다.
그림은 사람이 준비한다 → 없으면 '삽화 자리' 카드(무엇을 그릴지 적힌)로 렌더되고, `python -m ytflow art-brief <프로젝트>` 가 주문서를 만든다.

대본 (02_script/hybrid.json):
  {"type": "illust", "art": "fed_room.jpg",            # 04_assets/art/ 안 (가로 16:9 권장, 2400px 이상)
   "brief": "1950년대풍 회의실, 의원들이 금리 표를 보며 고민",   # 그림 주문 내용 (그림이 없을 때 자리 카드에도 표시)
   "credit": "그림: 채널 자체 제작",
   "reveal": "paint",                                  # 처음 나타나는 방식: paint(붓 쓸기)·fade·iris(동그랗게)
   "boil": true,                                       # 손그림 선이 살짝 살아 움직이는 느낌 (아주 약하게)
   "moves": [{"beat": 0, "focus": [0, 0, 1, 1]},       # 박자마다 카메라가 볼 곳 (그림 비율 0~1: x, y, 너비, 높이)
             {"beat": 1, "focus": [0.05, 0.0, 0.5, 0.5]}],
   "marks": [{"beat": 1, "kind": "circle", "at": [960, 420], "size": [520, 300]},     # 화면 좌표(1920×1080), 그 박자의 카메라 기준
             {"beat": 2, "kind": "arrow", "from": [600, 700], "to": [1100, 520]},
             {"beat": 2, "kind": "note", "at": [1180, 500], "text": "두 배로?"},
             {"beat": 3, "kind": "bubble", "at": [1400, 260], "text": "그냥 기다리면 되잖아"},
             {"beat": 3, "kind": "underline", "from": [700, 900], "to": [1200, 900]}],
   "beats": [...]}
"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

from .. import config

W, H = 1920, 1080


def art_dir(project) -> Path:
    return project.dir("assets") / "art"


def placeholder(out: Path, sc: dict) -> Path:
    """그림이 아직 없을 때: 무엇을 그릴지 적힌 자리 카드 (종이색, 점선 틀)."""
    from PIL import Image, ImageDraw
    from . import paper
    im = Image.new("RGB", (2400, 1350), (236, 228, 212))
    d = ImageDraw.Draw(im)
    for k in range(0, 2400, 40):   # 점선 틀
        d.line([(80 + k, 80), (100 + k, 80)], fill=(150, 140, 120), width=4) if k < 2240 else None
        d.line([(80 + k, 1270), (100 + k, 1270)], fill=(150, 140, 120), width=4) if k < 2240 else None
    for k in range(0, 1190, 40):
        d.line([(80, 80 + k), (80, 100 + k)], fill=(150, 140, 120), width=4)
        d.line([(2320, 80 + k), (2320, 100 + k)], fill=(150, 140, 120), width=4)
    f1, f2, f3 = paper.F(paper.SANS_X, 64), paper.F(paper.SERIF, 58), paper.F(paper.SANS, 40)
    d.text((1200, 300), f"삽화 자리 · 장면 #{sc.get('id')}", font=f1, fill=(120, 105, 85), anchor="mm")
    y = 520
    for ln in textwrap.wrap(sc.get("brief", "(그림 설명 없음)"), 30)[:5]:
        d.text((1200, y), ln, font=f2, fill=(60, 55, 50), anchor="mm")
        y += 90
    d.text((1200, 1150), f"04_assets/art/{sc.get('art', '')}", font=f3, fill=(120, 105, 85), anchor="mm")
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=90)
    return out


def brief(project) -> Path:
    """그림 주문서: 장면마다 파일 이름·내용·카메라가 볼 곳·표시가 들어갈 자리 → 02_script/art_brief.md"""
    spec = json.loads((project.dir("script") / "hybrid.json").read_text(encoding="utf-8"))
    rows = ["# 삽화 주문서", "", f"프로젝트 `{project.path.name}` · 그림은 `04_assets/art/` 에 아래 파일 이름으로 넣고 `python -m ytflow hybrid` 를 다시 실행합니다.", "",
            "- 크기: 가로 16:9, 2400×1350 이상 (카메라가 확대하므로 크게) · 형식 jpg/png",
            "- 그림체는 채널마다 하나로 통일 (styles/illustrated/STYLE.md §2 그림체 목록)",
            "- 글자는 그림에 넣지 않습니다 (화면 글자·자막은 편집에서 넣음). 실존 인물은 닮게 그리지 않습니다.", ""]
    for sc in spec["scenes"]:
        if sc.get("type") != "illust":
            continue
        have = (art_dir(project) / sc.get("art", "")).exists()
        rows += [f"## 장면 #{sc['id']} — `{sc.get('art')}` {'✅ 있음' if have else '⬜ 필요'}", "", f"- 내용: {sc.get('brief', '')}"]
        for m in sc.get("moves", []):
            x, y, w, h = m["focus"]
            rows.append(f"- 박자 {m['beat'] + 1}: 카메라가 그림의 가로 {x:.0%}~{x + w:.0%}, 세로 {y:.0%}~{y + h:.0%} 를 봄 → 이 자리에 '{sc['beats'][m['beat']]['say'][:30]}…' 에 맞는 것을")
        for m in sc.get("marks", []):
            rows.append(f"- 박자 {m['beat'] + 1}: 손그림 {m['kind']} {('“' + m['text'] + '”') if m.get('text') else ''} 이 들어갈 자리 비워 두기")
        rows.append("")
    out = project.dir("script") / "art_brief.md"
    out.write_text("\n".join(rows), encoding="utf-8")
    print(f"[art-brief] {out}")
    return out


def _cam(focus) -> tuple[float, float, float]:
    """그림 비율 사각형 → (확대, x이동px, y이동px). 그림은 화면에 꽉 차게(1920×1080) 놓고 transform-origin 0 0 기준."""
    x, y, w, h = focus
    s = max(1.0, min(1.0 / max(w, 1e-3), 1.0 / max(h, 1e-3)))
    cx, cy = (x + w / 2) * W, (y + h / 2) * H
    tx, ty = W / 2 - cx * s, H / 2 - cy * s
    tx = min(0.0, max(W - W * s, tx))   # 그림 밖(빈 곳)이 보이지 않게
    ty = min(0.0, max(H - H * s, ty))
    return s, tx, ty


def s_illust(D, sc: dict, bt: list, dur: float):
    import os
    import shutil
    from .hybrid import _e
    from . import paper
    from .paper import FT, fit
    a = D._work / "assets"
    proj = Path(sc["_project_dir"])
    src = proj / "04_assets" / "art" / sc.get("art", "")
    if not sc.get("art") or not src.exists():
        src = placeholder(proj / "04_assets" / "art" / f"_placeholder_{sc['id']:03d}.jpg", sc)
        D.qa.append("art/missing: 삽화가 아직 없어 자리 카드로 렌더 (python -m ytflow art-brief)")
    name = f"art_{sc['id']:03d}{src.suffix}"
    if (a / name).exists():
        (a / name).unlink()
    try:
        os.link(src, a / name)
    except OSError:
        shutil.copy(src, a / name)
    i = D._id()
    boil = sc.get("boil", True)
    filt = f"filter:url(#{i}boil);" if boil else ""
    D.media.append(
        (f'<svg width="0" height="0" style="position:absolute"><filter id="{i}boil"><feTurbulence id="{i}t" type="fractalNoise" baseFrequency="0.018" '
         f'numOctaves="2" seed="1"/><feDisplacementMap in="SourceGraphic" scale="2.2"/></filter></svg>' if boil else "") +
        f'<div id="{i}w" style="position:absolute;inset:0;overflow:hidden;background:#EDE5D4">'
        f'<div id="{i}c" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-origin:0 0">'
        f'<img src="assets/{name}" style="width:100%;height:100%;object-fit:cover;{filt}"></div></div>'
        f'<div style="position:absolute;inset:0;pointer-events:none;box-shadow:inset 0 0 160px rgba(40,30,20,.35)"></div>')
    if boil:   # 2fps 로 잡음 모양을 바꿔 선이 살짝 '살아 있게' (손그림 애니메이션의 boil 기법)
        k, t = 0, 0.0
        while t < dur:
            D.js.append(f'tl.set("#{i}t",{{attr:{{seed:{1 + k % 5}}}}},{t:.2f});')
            k, t = k + 1, t + 0.5
    rv = sc.get("reveal", "paint")
    if rv == "paint":
        D.css.append(f'#{i}w{{-webkit-mask-image:linear-gradient(105deg,#000 40%,rgba(0,0,0,0) 60%);-webkit-mask-size:300% 100%;'
                     f'-webkit-mask-repeat:no-repeat}}')
        D.js.append(f'tl.fromTo("#{i}w",{{webkitMaskPosition:"100% 0"}},{{webkitMaskPosition:"0% 0",duration:1.1,ease:"power2.inOut"}},0);')
        D.sfx.append(("whoosh-short", 0.1))
    elif rv == "iris":
        D.js.append(f'tl.fromTo("#{i}w",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(75% at 50% 50%)",duration:0.9,ease:"power2.out"}},0);')
    else:
        D.js.append(f'tl.fromTo("#{i}w",{{opacity:0}},{{opacity:1,duration:0.6}},0);')
    # 카메라: 박자마다 그 박자의 focus 로 (마지막 위치에서 천천히 계속 조금씩 당김)
    moves = {m["beat"]: m["focus"] for m in sc.get("moves", [])} or {0: [0, 0, 1, 1]}
    cur = _cam(moves.get(0, [0, 0, 1, 1]))
    D.js.append(f'tl.set("#{i}c",{{scale:{cur[0]:.3f},x:{cur[1]:.1f},y:{cur[2]:.1f}}},0);')
    starts = [t0 for t0, _ in bt] + [dur]
    for b in range(len(bt)):
        if b in moves and b > 0:
            nxt = _cam(moves[b])
            D.js.append(f'tl.to("#{i}c",{{scale:{nxt[0]:.3f},x:{nxt[1]:.1f},y:{nxt[2]:.1f},duration:1.4,ease:"power2.inOut"}},{max(starts[b] - 0.3, 0):.2f});')
            cur = nxt
    # 마지막 카메라에서 장면 끝까지 아주 천천히 밀기 (정지 화면 방지)
    s, tx, ty = cur
    last_b = max(moves)
    t_last = max(starts[last_b] - 0.3, 0) + (1.4 if last_b > 0 else 0)
    if dur - t_last > 0.5:
        s2 = s * 1.035
        cx, cy = (W / 2 - tx) / s, (H / 2 - ty) / s
        tx2, ty2 = min(0, max(W - W * s2, W / 2 - cx * s2)), min(0, max(H - H * s2, H / 2 - cy * s2))
        D.js.append(f'tl.to("#{i}c",{{scale:{s2:.3f},x:{tx2:.1f},y:{ty2:.1f},duration:{dur - t_last:.2f},ease:"none"}},{t_last:.2f});')
    # 손그림 표시: 그 박자에 카메라가 멈춘 뒤 그려지고, 다음 박자 시작에 사라짐
    ink = sc.get("mark_color", "#C4452F")
    for m in sc.get("marks", []):
        b = m["beat"]
        if b >= len(bt):
            continue
        t_on = bt[b][0] + (1.2 if b in moves and b > 0 else 0.3)
        t_off = starts[b + 1] - 0.15 if b + 1 < len(bt) else None
        kind = m["kind"]
        ids = []
        if kind == "circle":
            cx, cy = m["at"]
            w, h = m.get("size", [420, 240])
            k0 = len(D.rq)
            D.rough("ellipse", [cx, cy, w, h], ink, 6, at=t_on, dur=0.6, roughness=1.6)
            ids.append(f".r{k0}")
        elif kind in ("arrow", "underline"):
            (x0, y0), (x1, y1) = m["from"], m["to"]
            k0 = len(D.rq)
            D.rough("line", [x0, y0, x1, y1], ink, 6, at=t_on, dur=0.45, roughness=1.4)
            ids.append(f".r{k0}")
            if kind == "arrow":
                import math
                ang = math.atan2(y1 - y0, x1 - x0)
                for da in (2.6, -2.6):
                    k1 = len(D.rq)
                    D.rough("line", [x1, y1, x1 + 40 * math.cos(ang + da), y1 + 40 * math.sin(ang + da)], ink, 6, at=t_on + 0.4, dur=0.15, roughness=1.0)
                    ids.append(f".r{k1}")
        elif kind in ("note", "bubble"):
            x, y = m["at"]
            txt = m.get("text", "")
            f = fit(FT("note"), txt, 52, 640)
            tw = f.getlength(txt)
            j = D._id()
            if kind == "bubble":   # 생각 풍선: 종이색 구름 + 꼬리 동그라미 두 개, 펜 글씨
                D.items.append(f'<div id="{j}" style="position:absolute;left:{x - tw / 2 - 50:.0f}px;top:{y - 60:.0f}px;width:{tw + 100:.0f}px;height:120px;'
                               f'background:#FBF6EA;border-radius:60px;box-shadow:0 8px 22px rgba(0,0,0,.25);display:flex;align-items:center;justify-content:center;'
                               f'font-family:pen;font-size:{f.size}px;color:#2A2622">{_e(txt)}'
                               f'<div style="position:absolute;left:28%;bottom:-34px;width:34px;height:34px;border-radius:50%;background:#FBF6EA"></div>'
                               f'<div style="position:absolute;left:22%;bottom:-62px;width:20px;height:20px;border-radius:50%;background:#FBF6EA"></div></div>')
                D.js.append(f'tl.fromTo("#{j}",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(2)"}},{t_on:.2f});')
                D.sfx.append(("pop", t_on))
            else:
                D.items.append(f'<div id="{j}" style="position:absolute;left:{x:.0f}px;top:{y - 40:.0f}px;font-family:pen;font-size:{f.size}px;color:{ink};'
                               f'background:rgba(251,246,234,.88);padding:2px 16px;border-radius:8px;white-space:nowrap;transform:rotate(-2deg)">{_e(txt)}</div>')
                D.js.append(f'tl.fromTo("#{j}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.35}},{t_on + 0.2:.2f});')
                D.sfx.append(("pencil", t_on + 0.2))
            ids.append(f"#{j}")
        if t_off:
            for s_ in ids:
                D.js.append(f'tl.to("{s_}",{{opacity:0,duration:0.25}},{t_off:.2f});')
    D.label(sc.get("credit", ""), dark=True)
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""), dark=True)
    _ = paper


def register():
    from . import hybrid
    hybrid.RENDER["illust"] = s_illust


def main(argv: list[str]) -> None:
    from ..project import Project
    brief(Project.open(argv[0]))
