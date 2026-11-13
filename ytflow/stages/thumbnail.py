"""썸네일 만들기 (1280x720 PNG, 변형 A/B/C — 유튜브 '테스트 및 비교'에 3장까지 올릴 수 있음).

    python -m ytflow thumbnail <프로젝트>

입력: 02_script/hybrid.json 의 "package" (제목 후보·썸네일 변형). 규칙은 prompts/thumbnail.md.
출력: 05_edit/thumbnail_<id>.png, 작은 크기 미리보기 thumbnail_preview.png (휴대폰 목록 크기에서도 읽히는지),
      05_edit/package.md (제목·썸네일·이유), 점검 결과 thumbnail_qa.json.

배치(layout):
- photo : 자료 사진을 한쪽에 꽉 채우고(흑백·어둡게), 반대쪽에 큰 두 줄 글씨. 손그림 빨간 동그라미·화살표·도장.
- versus: 종이 바탕에 두 숫자 맞대기 (채널의 종이·손그림 정체성).
- board : 이야기 그림판(story 장면)과 같은 얼굴 — 종이 바탕 + 선으로 그린 사람·사물(drawings) + 큰 두 줄 글씨 + 빨간 펜 표시.
          호기심 채널(이야기형)용. drawings: [{"icon": "chess"|"shirt"|"bot"|… , "pose": "think"(사람), "x", "y", "s", "color"}]
공통: 굵은 고딕 + 두꺼운 테두리, 강조 단어 하나만 색, 오른쪽 아래(재생 시간 표시 자리) 비움.
"""
from __future__ import annotations

import json
import math
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

from ..project import Project

W, H = 1280, 720
FONTS = Path(__file__).resolve().parent.parent / "assets" / "fonts"
GOTHIC_X = FONTS / "NanumGothic-ExtraBold.ttf"
MYEONGJO_X = FONTS / "NanumMyeongjo-ExtraBold.ttf"
PEN = FONTS / "NanumPenScript-Regular.ttf"
PAPER, INK, RED, YELLOW = (238, 231, 218), (34, 48, 77), (214, 58, 42), (255, 214, 64)
TIMESTAMP_BOX = (1080, 630, W, H)   # 유튜브가 재생 시간을 덮는 자리


FIX = {"\u2212": "-", "\u2013": "-", "\u2014": "-", "\u2192": ">"}   # 나눔 글꼴에 없는 빼기·대시 기호 → 보이게


def _fix(t: str) -> str:
    return "".join(FIX.get(c, c) for c in t)


def _font(path, size):
    return ImageFont.truetype(str(path), int(size))


def _image(project: Project, spec: dict, img: dict) -> Image.Image:
    if img.get("file"):
        return Image.open(project.path / img["file"]).convert("RGB")
    src = project.dir("assets") / "footage" / spec["footage"][img["src"]]["file"]
    out = project.dir("edit") / f"_thumb_src_{img['src']}.png"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(img.get("t", 1)), "-i", str(src),
                    "-frames:v", "1", str(out)], check=True)
    return Image.open(out).convert("RGB")


def _cover(im: Image.Image, w: int, h: int, fx: float = 0.5, fy: float = 0.4) -> Image.Image:
    s = max(w / im.width, h / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * fx)
    y = int((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def _rough_ellipse(d: ImageDraw.ImageDraw, box, color=RED, width=11, seed=1):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    for k in range(2):
        pts = []
        a0 = rnd.uniform(-0.6, 0.0)
        for i in range(64):
            a = a0 + 2.15 * math.pi * i / 63
            j = 1 + rnd.uniform(-0.035, 0.035)
            pts.append((cx + rx * j * math.cos(a), cy + ry * j * math.sin(a)))
        d.line(pts, fill=color, width=width - 3 * k, joint="curve")


def _rough_arrow(d, x0, y0, x1, y1, color=RED, width=14):
    d.line([(x0, y0), ((x0 + x1) / 2 + 6, (y0 + y1) / 2 - 4), (x1, y1)], fill=color, width=width, joint="curve")
    ang = math.atan2(y1 - y0, x1 - x0)
    for s in (-0.5, 0.5):
        d.line([(x1, y1), (x1 - 52 * math.cos(ang + s), y1 - 52 * math.sin(ang + s))], fill=color, width=width)


def _stamp(base: Image.Image, text: str, cx: int, cy: int, size: int = 64, rot: float = -12):
    f = _font(GOTHIC_X, size)
    tw = f.getlength(text)
    pad = 26
    layer = Image.new("RGBA", (int(tw + pad * 2 + 20), int(size * 1.5 + pad)), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([6, 6, layer.width - 6, layer.height - 6], outline=RED + (255,), width=8)
    d.text((layer.width / 2, layer.height / 2), text, font=f, fill=RED + (255,), anchor="mm")
    layer = layer.rotate(rot, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))


def _text_block(d: ImageDraw.ImageDraw, lines: list[str], hl: list[str], x: int, y: int, maxw: int, size: int,
                align: str = "left", fill=(255, 255, 255), stroke=(15, 15, 15), font=GOTHIC_X, gap: float = 1.14) -> list:
    """줄마다 크기를 maxw 에 맞춘 굵은 글씨. hl 에 든 단어만 노란색. 그린 글자 상자 목록을 돌려준다(점검용)."""
    boxes = []
    for ln in lines:
        s = size
        while _font(font, s).getlength(ln) > maxw and s > 40:
            s -= 4
        f = _font(font, s)
        lw = f.getlength(ln)
        cx = x if align == "left" else x - lw / 2
        tokens = ln.split(" ")
        for i, tok in enumerate(tokens):
            word = tok + (" " if i < len(tokens) - 1 else "")
            col = (RED if sum(stroke[:3]) > 500 else YELLOW) if any(h in tok for h in hl) else fill   # 종이 바탕에서는 노랑 대신 빨강 (읽히게)
            d.text((cx, y), word, font=f, fill=col, stroke_width=max(8, s // 11), stroke_fill=stroke)
            cx += f.getlength(word)
        boxes.append((x if align == "left" else x - lw / 2, y, (x if align == "left" else x - lw / 2) + lw, y + s))
        y += int(s * gap)
    return boxes


def _board(base: Image.Image, v: dict) -> Image.Image:
    """종이 결 + 선 그림 (story.py 의 그림과 같은 모양)."""
    import io
    import cairosvg
    import numpy as np
    from .story import POSES, _children
    rng = np.random.default_rng(7)
    noise = (rng.normal(0, 6, (H // 4, W // 4))).astype(np.int16)
    n = Image.fromarray(np.clip(128 + noise, 0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2))
    paper = Image.merge("RGB", [ImageOps.autocontrast(n, cutoff=0).point(lambda q, c=c: int(c - 10 + q * 20 / 255)) for c in PAPER])
    base = paper.convert("RGBA")
    for dr in v.get("drawings", []):
        kids = POSES[dr["pose"]] if dr.get("pose") else _children(dr["icon"])
        col = dr.get("color", "#22304D")
        sw = dr.get("sw", 1.6)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -1 26 26" fill="none" stroke="{col}" stroke-width="{sw}" '
               f'stroke-linecap="round" stroke-linejoin="round">{"".join(kids)}</svg>')
        s_ = int(dr.get("s", 300))
        im = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=s_, output_height=s_))).convert("RGBA")
        base.alpha_composite(im, (int(dr["x"] - s_ / 2), int(dr["y"] - s_ / 2)))
        if dr.get("label"):
            dd = ImageDraw.Draw(base)
            fl = _font(PEN, dr.get("lfs", 52))
            dd.text((dr["x"], dr["y"] + s_ / 2 + 4), dr["label"], font=fl, fill=INK, anchor="mt")
    return base


def render(project: Project, spec: dict, v: dict) -> tuple[Image.Image, list]:
    base = Image.new("RGBA", (W, H), PAPER + (255,))
    boxes = []
    if v.get("layout", "photo") == "photo":
        side = v.get("photo_side", "right")
        pw = int(W * v.get("photo_width", 0.62))
        im = _image(project, spec, v["image"])
        im = _cover(im, pw if side != "full" else W, H, *v["image"].get("focus", [0.5, 0.35]))
        if v.get("tone", "old") == "old":   # 오래된 사진 느낌(교양 채널 정체성). 화면 캡처 등 색이 중요한 사진은 "tone": "none"
            im = ImageOps.grayscale(im).convert("RGB")
            im = ImageEnhance.Contrast(im).enhance(1.25)
            im = ImageOps.colorize(ImageOps.grayscale(im), (18, 20, 28), (236, 226, 205))
        px = W - im.width if side == "right" else 0
        base.paste(im, (px, 0))
        # 사진과 글씨 쪽 사이를 부드럽게 (어두운 그라데이션)
        g = Image.new("L", (W, H), 0)
        gd = ImageDraw.Draw(g)
        for i in range(380):
            a = int(255 * (1 - i / 380) ** 1.6)
            xx = px + i if side == "right" else px + im.width - i
            gd.line([(xx, 0), (xx, H)], fill=a)
        dark = Image.new("RGBA", (W, H), (14, 16, 24, 255))
        mask = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(mask)
        if side == "right":
            md.rectangle([0, 0, px, H], fill=255)
        elif side == "left":
            md.rectangle([px + im.width, 0, W, H], fill=255)
        mask = Image.composite(Image.new("L", (W, H), 255), mask, g) if side != "full" else Image.new("L", (W, H), 150)
        base = Image.composite(dark, base, mask)
        d = ImageDraw.Draw(base)
        tx = 60 if side in ("right", "full") else px + im.width + 40
        maxw = (px - 40 if side == "right" else W - tx - 50) if side != "full" else 760
        maxw = max(maxw, 560)
        y = v.get("text_y", 150)
        if v.get("top"):
            ft = _font(GOTHIC_X, 40)
            d.rounded_rectangle([tx - 6, y - 70, tx + ft.getlength(v["top"]) + 26, y - 14], 10, fill=RED)
            d.text((tx + 10, y - 66), v["top"], font=ft, fill=(255, 255, 255))
            boxes.append((tx, y - 70, tx + ft.getlength(v["top"]) + 26, y - 14))
        boxes += _text_block(d, v["lines"], v.get("hl", []), tx, y, maxw, v.get("size", 150))
        if v.get("sub"):
            fs = _font(PEN, 58)
            yy = boxes[-1][3] + 30
            d.text((tx + 4, yy), v["sub"], font=fs, fill=(255, 238, 190), stroke_width=4, stroke_fill=(10, 10, 10))
            boxes.append((tx, yy, tx + fs.getlength(v["sub"]), yy + 60))
    elif v.get("layout") == "board":   # 이야기 그림판: 영상 속 그림과 같은 선 그림 + 큰 글씨 (2026-11-13)
        base = _board(base, v)
        d = ImageDraw.Draw(base)
        tx, y = v.get("text_x", 60), v.get("text_y", 90)
        if v.get("top"):
            ft = _font(GOTHIC_X, 40)
            d.rounded_rectangle([tx - 6, y - 70, tx + ft.getlength(v["top"]) + 26, y - 14], 10, fill=RED)
            d.text((tx + 10, y - 66), v["top"], font=ft, fill=(255, 255, 255))
            boxes.append((tx, y - 70, tx + ft.getlength(v["top"]) + 26, y - 14))
        boxes += _text_block(d, v["lines"], v.get("hl", []), tx, y, v.get("text_w", 760), v.get("size", 130), fill=INK, stroke=PAPER)
        if v.get("sub"):
            fs = _font(PEN, 64)
            yy = boxes[-1][3] + 24
            d.text((tx + 4, yy), v["sub"], font=fs, fill=RED)
            boxes.append((tx, yy, tx + fs.getlength(v["sub"]), yy + 64))
    else:  # versus: 종이 바탕 두 숫자
        d = ImageDraw.Draw(base)
        L, R = v["left"], v["right"]
        for (it, cx, col) in ((L, 330, INK), (R, 950, RED)):
            sz = it.get("size", 250)
            while _font(MYEONGJO_X, sz).getlength(it["value"]) > 440 and sz > 80:   # 반쪽 안 + 가운데 vs 와 안 겹치게
                sz -= 10
            f = _font(MYEONGJO_X, sz)
            d.text((cx, 330), it["value"], font=f, fill=col, anchor="mm")
            fl = _font(GOTHIC_X, 46)
            d.text((cx, 520), it["label"], font=fl, fill=INK, anchor="mm")
            boxes.append((cx - f.getlength(it["value"]) / 2, 200, cx + f.getlength(it["value"]) / 2, 560))
        d.text((640, 330), "vs", font=_font(PEN, 110), fill=(120, 120, 120), anchor="mm")
        if v.get("headline"):
            boxes += _text_block(d, [v["headline"]], v.get("hl", []), 640, 40, 1180, 110, align="center", fill=INK,
                                 stroke=PAPER)
    d = ImageDraw.Draw(base)
    for m in v.get("marks", []):  # 손그림 표시 (채널 정체성: 빨간 펜)
        if m["type"] == "circle":
            _rough_ellipse(d, m["box"], seed=len(m["box"]))
        elif m["type"] == "arrow":
            _rough_arrow(d, *m["from"], *m["to"])
        elif m["type"] == "stamp":
            _stamp(base, m["text"], *m["at"], size=m.get("size", 64), rot=m.get("rot", -12))
        elif m["type"] == "x":
            x0, y0, x1, y1 = m["box"]
            d.line([(x0, y0), (x1, y1)], fill=RED, width=16)
            d.line([(x0, y1), (x1, y0)], fill=RED, width=16)
    return base.convert("RGB"), boxes


def run(project: Project) -> dict:
    raw = (project.dir("script") / "hybrid.json").read_text(encoding="utf-8")
    spec = json.loads(raw)
    pkg = spec["package"]
    for v in pkg["thumbnails"]:  # 글자 기호 정리
        for k in ("top", "sub", "headline"):
            if v.get(k):
                v[k] = _fix(v[k])
        v["lines"] = [_fix(x) for x in v.get("lines", [])]
        for side in ("left", "right"):
            if v.get(side):
                v[side] = {**v[side], "value": _fix(v[side]["value"]), "label": _fix(v[side]["label"])}
    edir = project.dir("edit")
    edir.mkdir(parents=True, exist_ok=True)
    qa, made = {}, []
    for v in pkg["thumbnails"]:
        im, boxes = render(project, spec, v)
        out = edir / f"thumbnail_{v['id']}.png"
        im.save(out, optimize=True)
        made.append((v, out, im))
        tx0, ty0, tx1, ty1 = TIMESTAMP_BOX
        clash = [b for b in boxes if b[2] > tx0 and b[3] > ty0]
        small = min((b[3] - b[1]) for b in boxes) * 168 / W if boxes else 0     # 휴대폰 목록(가로 168px)에서 가장 작은 글자 높이
        qa[v["id"]] = {"timestamp_overlap": bool(clash), "smallest_text_px_at_168w": round(small, 1),
                       "ok": not clash and small >= 6}
    # 미리보기: 실제 크기(1280) 옆에 유튜브 목록 크기 360 / 휴대폰 168
    sheet = Image.new("RGB", (1280 + 380, 720 * len(made) + 20 * (len(made) - 1)), (24, 24, 24))
    for i, (v, out, im) in enumerate(made):
        y = i * 740
        sheet.paste(im, (0, y))
        sheet.paste(im.resize((360, 202), Image.LANCZOS), (1300, y))
        sheet.paste(im.resize((168, 94), Image.LANCZOS), (1300, y + 230))
        ImageDraw.Draw(sheet).text((1300, y + 340), f"{v['id']}", font=_font(GOTHIC_X, 60), fill=(255, 255, 255))
    sheet.save(edir / "thumbnail_preview.png")
    (edir / "thumbnail_qa.json").write_text(json.dumps(qa, ensure_ascii=False, indent=1), encoding="utf-8")
    md = [f"# 제목·썸네일 — {project.path.name}", "", f"**제목(기본):** {pkg['title']}", "", "**제목 후보 (A/B 시험용)**"]
    md += [f"{k + 1}. {t}" for k, t in enumerate(pkg.get("title_options", []))]
    md += ["", "**제목을 이렇게 정한 이유**"] + [f"- {r}" for r in pkg.get("title_why", [])] + ["", "## 썸네일"]
    for v, out, _ in made:
        md += [f"### {v['id']} — {v.get('name', '')}", f"![{v['id']}]({out.name})", ""] + [f"- {r}" for r in v.get("why", [])] + [""]
    md += ["## 점검", "```json", json.dumps(qa, ensure_ascii=False, indent=1), "```"]
    (edir / "package.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[thumbnail] {len(made)}장 → {edir} (미리보기 thumbnail_preview.png, 점검 {qa})")
    return qa
