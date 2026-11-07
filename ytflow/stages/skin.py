"""그래픽 스킨 — 연출(무엇이·언제·어떻게 움직이나)과 분리된 '겉모습'(색·글꼴·배경·선 질감·사진 톤·자막 상자).

연출은 02_script/hybrid.json (장면 type·박자·강조 이벤트·카메라·전환·효과음) — 바꾸지 않는다.
그래픽은 skins/<id>/skin.yaml — 갈아 끼운다.  (docs/13-direction-vs-graphics.md)

고르는 곳 (앞이 우선): 환경변수 YTFLOW_SKIN → 프로젝트 edit.yaml 의 edit.skin → 채널 → 'paper-sketch'.

렌더러는 기본 스킨(paper-sketch)의 색으로 HTML 을 만들고, 마지막에 그 색을 '토큰'으로 보고 고른 스킨의 색으로 바꾼다.
(hex 와 rgba(r,g,b,a) 둘 다, 투명도는 그대로) → 장면 코드에 색을 새로 박아도 토큰 표에 있으면 스킨이 따라온다.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import numpy as np
import yaml
from PIL import Image, ImageDraw, ImageFilter

from .. import config

SKINS_DIR = config.ROOT / "skins"
FONTS = Path(__file__).resolve().parent.parent / "assets" / "fonts"

# 기본 스킨(paper-sketch)의 토큰 값 = 렌더러 코드에 들어 있는 색. 새 색을 코드에 쓰면 여기에도 이름을 붙인다.
TOKENS = {
    "base": "#EEE7DA",        # 바탕
    "ink": "#22304D",         # 기본 글씨·선
    "accent": "#C4452F",      # 강조(빨강)
    "card": "#FBF8F1",        # 카드·쪽지·이름 자막 바탕
    "card2": "#F7F2E6",       # 두 번째 카드(신문 등)
    "muted_text": "#5a5f6a",  # 보조 글씨(라벨·출처)
    "muted2": "#6b6f78",
    "line": "#9a9488",        # 보조 선
    "line2": "#B9B09E",       # 글줄 막대
    "line3": "#c9c0ae",
    "dim": "#a8a29a",         # 꺼진 칸
    "map_stroke": "#7d7568",  # 지도 선
    "ok": "#2E7D4F",          # 좋음(초록)
    "warn": "#C77B12",        # 주의(주황)
    "blue": "#2F5D8C",
    "marker": "#F3D36B",      # 형광펜
    "note_on_video": "#FFF3C4",  # 영상 위 손글씨
    "redact": "#1d1d1d",      # 검열 띠
    "deep": "#2b2f3a",
    "tape": "#ECDCAA",        # 테이프 (rgba(236,220,170,.85))
}


def current() -> str:
    e = config.load("pipeline").get("edit", {}) or {}
    return os.environ.get("YTFLOW_SKIN") or e.get("skin") or "paper-sketch"


def load(skin_id: str | None = None) -> dict:
    sid = skin_id or current()
    f = SKINS_DIR / sid / "skin.yaml"
    d = yaml.safe_load(f.read_text(encoding="utf-8")) if f.exists() else {}
    d.setdefault("id", sid)
    pal = dict(TOKENS)
    pal.update(d.get("palette") or {})
    d["palette"] = pal
    return d


def _rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def remap_html(html: str, sk: dict) -> str:
    """기본 토큰 색 → 스킨 색 (hex·rgba 모두)."""
    pal = sk["palette"]
    if all(pal[k].lower() == v.lower() for k, v in TOKENS.items()):
        return html
    hexmap = {v.lower(): pal[k] for k, v in TOKENS.items()}
    rgbmap = {_rgb(v): _rgb(pal[k]) for k, v in TOKENS.items()}
    html = re.sub(r"#[0-9a-fA-F]{6}\b", lambda m: hexmap.get(m.group(0).lower(), m.group(0)), html)

    def rg(m):
        r, g, b = (int(x) for x in m.group(1, 2, 3))
        if (r, g, b) in rgbmap:
            r, g, b = rgbmap[(r, g, b)]
        return f"rgba({r},{g},{b},{m.group(4)})"
    return re.sub(r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)", rg, html)


def apply_fonts(sk: dict) -> None:
    """글꼴 역할(title·value·box·note·label) → 파일. 글자 폭 계산(paper.FT)과 HTML 글꼴이 함께 바뀐다."""
    from . import paper
    for role, name in (sk.get("fonts") or {}).items():
        paper.PROFILE["fonts"][role] = FONTS / name


def paper_override(sk: dict) -> dict:
    p = sk["palette"]
    return {"base": p["base"], "ink": p["ink"], "red": p["accent"]}


def background(sk: dict, W: int, H: int) -> Image.Image:
    bg = sk.get("background", {"type": "paper"})
    t = bg.get("type", "paper")
    base = _rgb(sk["palette"]["base"])
    rng = np.random.default_rng(bg.get("seed", 7))
    if t == "paper":
        from . import paper
        return paper.paper_bg(W, H, seed=bg.get("seed", 7))
    arr = np.ones((H, W, 3), np.float32) * np.array(base, np.float32)
    if t in ("grain", "dark"):  # 필름 알갱이 + 가장자리 어둡게
        arr += rng.normal(0, bg.get("grain", 6), (H, W, 1))
        yy, xx = np.mgrid[0:H, 0:W]
        v = 1 - bg.get("vignette", 0.35) * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2
        arr *= v[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    if t == "grid":  # 모눈
        d = ImageDraw.Draw(im)
        c = _rgb(bg.get("grid_color", sk["palette"]["line3"]))
        step = bg.get("step", 48)
        for x in range(0, W, step):
            d.line([(x, 0), (x, H)], fill=c, width=1)
        for y in range(0, H, step):
            d.line([(0, y), (W, y)], fill=c, width=1)
    return im.filter(ImageFilter.GaussianBlur(0.3))


def rough_opts(sk: dict, opts: dict) -> dict:
    """선 질감: roughness 배율, bowing, 채우기 방식(hachure 빗금 / solid 면)."""
    r = sk.get("strokes", {})
    o = dict(opts)
    o["roughness"] = o.get("roughness", 1.3) * r.get("roughness_scale", 1.0)
    o["bowing"] = r.get("bowing", o.get("bowing", 1.2))
    if o.get("fill") and r.get("fill_style"):
        o["fillStyle"] = r["fill_style"]
    return o


def video_filter(sk: dict) -> str:
    """자료 화면 톤 (CSS filter): none | bw | sepia | 직접 쓴 CSS."""
    t = (sk.get("photo") or {}).get("tone", "none")
    return {"none": "", "bw": "grayscale(1) contrast(1.1)", "sepia": "sepia(.45) contrast(1.05)",
            "cool": "saturate(.7) hue-rotate(-8deg) contrast(1.05)"}.get(t, t)


def subtitle_style(sk: dict) -> dict:
    s = {"font": "NanumGothic", "size": 50, "text": "&H00FFFFFF", "outline": "&H00202020", "box": "&H8A1E1E1E",
         "border_style": 3, "outline_w": 14, "margin_v": 48}
    s.update(sk.get("subtitle") or {})
    return s


def preview(project, scenes: list[int], skins: list[str]) -> Path:
    """같은 연출(대본)을 스킨마다 렌더해 장면 끝 프레임을 나란히 붙인 비교표 → 05_edit/skin_preview.png.
    스킨마다 새 프로세스로 돌린다(글꼴 표가 프로세스 전역이라)."""
    import subprocess
    import sys
    out_dir = project.dir("edit") / "skin_preview"
    out_dir.mkdir(parents=True, exist_ok=True)
    code = r'''
import json, os, sys, subprocess
from pathlib import Path
from ytflow.project import Project
from ytflow.stages import hybrid
p = Project.open(sys.argv[1]); out = Path(sys.argv[2]); ids = [int(x) for x in sys.argv[3].split(",")]
spec = json.loads((p.dir("script") / "hybrid.json").read_text(encoding="utf-8"))
ch = {s["chapter"]: s for s in spec["scenes"] if s["type"] == "chapter"}
for s in spec["scenes"]:
    c = ch.get(s.get("chapter"))
    if c and s["type"] != "chapter": s["_chnum"], s["_chtitle"] = c["num"], c["title"]
durs = hybrid.voice(p, spec)
for sid in ids:
    sc = [s for s in spec["scenes"] if s["id"] == sid][0]
    bt, d = hybrid.timing(sc, durs)
    w = out / f"{os.environ['YTFLOW_SKIN']}_{sid}"
    hybrid.build_scene(p, spec, sc, bt, d, w)
    mp4 = out / f"{os.environ['YTFLOW_SKIN']}_{sid}.mp4"
    hybrid.render_scene(w, mp4)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{d - 0.7:.2f}", "-i", str(mp4), "-frames:v", "1", "-vf", "scale=640:-1",
                    str(out / f"{os.environ['YTFLOW_SKIN']}_{sid}.png")], check=True)
'''
    for sk in skins:
        env = dict(os.environ, YTFLOW_SKIN=sk)
        subprocess.run([sys.executable, "-c", code, project.path.name, str(out_dir), ",".join(map(str, scenes))],
                       env=env, check=True, cwd=str(config.ROOT))
    from PIL import ImageFont
    f = ImageFont.truetype(str(FONTS / "NanumGothic-Bold.ttf"), 30)
    sheet = Image.new("RGB", (200 + 640 * len(scenes), 360 * len(skins)), (30, 30, 30))
    d = ImageDraw.Draw(sheet)
    for r, sk in enumerate(skins):
        d.text((20, r * 360 + 160), sk, font=f, fill=(255, 255, 255))
        for c, sid in enumerate(scenes):
            im = Image.open(out_dir / f"{sk}_{sid}.png")
            sheet.paste(im, (200 + c * 640, r * 360))
    dst = project.dir("edit") / "skin_preview.png"
    sheet.save(dst)
    print(f"[skin] 비교표 → {dst}")
    return dst
