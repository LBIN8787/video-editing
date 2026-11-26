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
- punch : (시장, 2026-11-19 사용자 "썸네일 스타일을 좀 더 눈에 들어오게") 컬러 사진 꽉 채움 + 아주 큰 두 줄 글씨 +
          강조 단어는 노란 상자 위 검은 글씨 + 큰 숫자 칩(▲초록·▼빨강). 작은 손글씨 줄 대신 칩. "theme": "dark" 인 versus 도 같은 결.
          chips: [{"text": "엔비디아 ▼2.89%", "color": "down"|"up"|"yellow"}]
- trend : (2026-11-22 사용자: 40·50대 위주 → 젊은 유입층, "좀 트렌디하게"; 같은 날 "유아틱 아니야?" → 귀여운 3D 캐릭터 금지)
          시네마틱 실사풍 그림(GPT 이미지, 금융 다큐·경제지 표지 같은 조명) 꽉 채움 + 알약 태그 +
          블랙한산스 두 줄(딱딱한 그림자, 강조 한 단어만 네온) + 스티커. 말투는 구어체 질문.
- person: (시장, 2026-11-20 사용자: "유명인사가 썸네일에 나오거나 유명인사를 다룬 주제 내용들이 조회수가 높은 것 같은데")
          사건의 당사자 얼굴을 오른쪽에 크게(얼굴을 찾아 화면 높이의 40~50% 로 자름, 컬러) + 이름표(이름 · 직함) + 왼쪽 큰 두 줄.
          "person": {"name": "젠슨 황", "role": "엔비디아 CEO"}, "quote": "따옴표 한 마디"(선택). 근거 docs/55-celebrity-effect.md
공통: 굵은 고딕 + 두꺼운 테두리, 강조 단어 하나만 색, 오른쪽 아래(재생 시간 표시 자리) 비움.
"""
from __future__ import annotations

import json
import math
import random
import re
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
UP, DOWN, NAVY = (22, 168, 92), (226, 38, 38), (12, 18, 34)
TIMESTAMP_BOX = (1080, 630, W, H)   # 유튜브가 재생 시간을 덮는 자리


FIX = {"\u2212": "-", "\u2013": "-", "\u2014": "-", "\u2192": ">"}   # 나눔 글꼴에 없는 빼기·대시 기호 → 보이게


def _fix(t: str) -> str:
    return "".join(FIX.get(c, c) for c in t)


def _font(path, size):
    return ImageFont.truetype(str(path), int(size))


def series(project: Project | str) -> str | None:
    """시장 채널 썸네일 계열 (manual/09 §7-1 ⑬·⑭): 'brief' 브리핑(매일·주간) = 기업 사진·brief_tab 틀 / 'analysis' 분석(심층·기술 등) = 인물·analysis_frame 틀.
    목록에서 글씨를 읽지 않아도 둘이 갈리게 (2026-11-25 사용자: "브리핑이랑 분석이랑 구분 할 수 있도록 해주세요 글씨로 말구요")."""
    name = project if isinstance(project, str) else project.path.name
    m = re.match(r"\d{8}-market-(\w+)", name)
    if not m:
        return None
    return "brief" if m.group(1) in ("daily", "weekly") else "analysis"


def _bw(im: Image.Image) -> Image.Image:
    """브리핑 흑백: 대비를 조금 올린 회색 — 빨간 띠·초록/빨강 지수 숫자만 색으로 남음."""
    return ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(1.15).convert("RGB")


def _image(project: Project, spec: dict, img: dict) -> Image.Image:
    if img.get("file"):
        im = Image.open(project.path / img["file"]).convert("RGB")
        return _bw(im) if img.get("_bw") else im
    src = project.dir("assets") / "footage" / spec["footage"][img["src"]]["file"]
    out = project.dir("edit") / f"_thumb_src_{img['src']}.png"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(img.get("t", 1)), "-i", str(src),
                    "-frames:v", "1", str(out)], check=True)
    im = Image.open(out).convert("RGB")
    return _bw(im) if img.get("_bw") else im


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
    for ph in v.get("photos", []):   # 폴라로이드 사진 (영상의 photo 와 같은 처리: 흰 테두리·테이프·그림자·기울임)
        from PIL import ImageFont as _F
        src = Image.open(ph["file"]).convert("RGB")
        w, h = int(ph.get("w", 300)), int(ph.get("h", 240))
        src = ImageOps.fit(src, (w, h), centering=tuple(ph.get("focus", [0.5, 0.4])))
        src = ImageEnhance.Color(src).enhance(0.88)
        pad, bot = 14, (58 if ph.get("caption") else 14)
        card = Image.new("RGBA", (w + pad * 2, h + pad + bot), (251, 248, 241, 255))
        card.paste(src, (pad, pad))
        if ph.get("caption"):
            dd = ImageDraw.Draw(card)
            fc = _font(PEN, 44)
            dd.text((card.width / 2, h + pad + 6), ph["caption"], font=fc, fill=INK, anchor="mt")
        tape = Image.new("RGBA", (120, 32), (236, 220, 170, 210))
        card.alpha_composite(tape.rotate(4, expand=True), (card.width // 2 - 62, 0))
        card = card.rotate(ph.get("rot", -3), expand=True, resample=Image.BICUBIC)
        sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
        sh.paste((30, 24, 16, 90), mask=card.split()[3])
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        x0, y0 = int(ph["x"] - card.width / 2), int(ph["y"] - card.height / 2)
        base.alpha_composite(sh, (x0 + 6, y0 + 12))
        base.alpha_composite(card, (x0, y0))
    for ct in v.get("cutouts", []):   # 그림 조각 (영상의 stage 주인공과 같은 그림, 배경 투명) — 2026-11-14 v22
        im_ = Image.open(ct["file"]).convert("RGBA")
        hh = int(ct.get("h", 300))
        im_ = im_.resize((round(hh * im_.width / im_.height), hh), Image.LANCZOS)
        if ct.get("rot"):
            im_ = im_.rotate(ct["rot"], expand=True, resample=Image.BICUBIC)
        sh = Image.new("RGBA", im_.size, (0, 0, 0, 0))
        sh.paste((30, 24, 16, 80), mask=im_.split()[3])
        sh = sh.filter(ImageFilter.GaussianBlur(9))
        x0, y0 = int(ct["x"] - im_.width / 2), int(ct["y"] - im_.height / 2)
        base.alpha_composite(sh, (x0 + 4, y0 + 10))
        base.alpha_composite(im_, (x0, y0))
    for dr in v.get("drawings", []):
        if dr.get("sticker"):   # 둥근 스티커 (영상의 sticker 와 같음)
            d_ = int(dr.get("s", 180))
            st = Image.new("RGBA", (d_, d_), (0, 0, 0, 0))
            sd = ImageDraw.Draw(st)
            sd.ellipse([0, 0, d_ - 1, d_ - 1], fill=(251, 248, 241, 255))
            sd.ellipse([8, 8, d_ - 9, d_ - 9], fill=(196, 69, 47, 255) if dr.get("red") else (34, 48, 77, 255))
            kids_ = _children(dr["icon"])
            svg_ = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -1 26 26" fill="none" stroke="#F4EBDD" stroke-width="1.9" '
                    f'stroke-linecap="round" stroke-linejoin="round">{"".join(kids_)}</svg>')
            ic = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg_.encode(), output_width=int(d_ * .56), output_height=int(d_ * .56)))).convert("RGBA")
            st.alpha_composite(ic, (int(d_ * .22), int(d_ * .22)))
            shd = Image.new("RGBA", st.size, (0, 0, 0, 0)); shd.paste((30, 24, 16, 90), mask=st.split()[3]); shd = shd.filter(ImageFilter.GaussianBlur(8))
            base.alpha_composite(shd, (int(dr["x"] - d_ / 2 + 4), int(dr["y"] - d_ / 2 + 10)))
            base.alpha_composite(st, (int(dr["x"] - d_ / 2), int(dr["y"] - d_ / 2)))
            continue
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


def _punch(project: Project, spec: dict, v: dict) -> tuple[Image.Image, list]:
    """눈에 띄는 시장 썸네일: 컬러 사진 + 큰 글씨 + 노란 상자 강조 + 숫자 칩."""
    boxes = []
    im = _cover(_image(project, spec, v["image"]), W, H, *v["image"].get("focus", [0.5, 0.4]))
    im = ImageEnhance.Color(im).enhance(v.get("saturate", 1.35))
    im = ImageEnhance.Contrast(im).enhance(1.15)
    im = ImageEnhance.Brightness(im).enhance(0.62)
    base = im.convert("RGBA")
    # 왼쪽·아래를 더 어둡게 (글씨 자리)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for x in range(W):
        a = int(170 * max(0.0, 1 - x / (W * 0.85)) ** 1.2)
        sd.line([(x, 0), (x, H)], fill=(0, 0, 0, a))
    base.alpha_composite(sh)
    d = ImageDraw.Draw(base)
    tx, y = 56, v.get("text_y", 120)
    if v.get("top"):
        ft = _font(GOTHIC_X, 38)
        d.rounded_rectangle([tx - 4, y - 66, tx + ft.getlength(v["top"]) + 24, y - 14], 8, fill=RED)
        d.text((tx + 10, y - 62), v["top"], font=ft, fill=(255, 255, 255))
        boxes.append((tx, y - 66, tx + ft.getlength(v["top"]) + 24, y - 14))
    maxw = v.get("text_w", 1060)
    for ln in v["lines"]:
        s = v.get("size", 170)
        while _font(GOTHIC_X, s).getlength(ln) > maxw and s > 60:
            s -= 4
        f = _font(GOTHIC_X, s)
        cx = tx
        toks = ln.split(" ")
        for i, tok in enumerate(toks):
            word = tok + (" " if i < len(toks) - 1 else "")
            wl = f.getlength(tok)
            if any(h in tok for h in v.get("hl", [])):
                pad = s * 0.08
                d.rectangle([cx - pad, y + s * 0.02, cx + wl + pad, y + s * 1.08], fill=YELLOW)
                d.text((cx, y), tok, font=f, fill=(10, 10, 10))
            else:
                d.text((cx, y), tok, font=f, fill=(255, 255, 255), stroke_width=max(9, s // 10), stroke_fill=(0, 0, 0))
            cx += f.getlength(word)
        boxes.append((tx, y, cx, y + s))
        y += int(s * 1.16)
    chips = v.get("chips", [])
    if chips:
        y += 18
        cx = tx
        for c in chips:
            fs = c.get("size", v.get("chip_size", 64))
            f = _font(GOTHIC_X, fs)
            col = {"up": UP, "down": DOWN, "yellow": YELLOW}.get(c.get("color", "yellow"), YELLOW)
            fg = (10, 10, 10) if col == YELLOW else (255, 255, 255)
            w = f.getlength(c["text"]) + fs * 0.7
            d.rounded_rectangle([cx, y, cx + w, y + fs * 1.45], int(fs * 0.25), fill=col, outline=(0, 0, 0), width=4)
            d.text((cx + fs * 0.35, y + fs * 0.2), c["text"], font=f, fill=fg)
            boxes.append((cx, y, cx + w, y + fs * 1.45))
            cx += w + 24
    return base.convert("RGB"), boxes


def _versus_dark(v: dict) -> tuple[Image.Image, list]:
    """versus 의 눈에 띄는 판: 짙은 남색 + 노랑·빨강 큰 숫자 + 흰 제목."""
    base = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(base)
    boxes = []
    if v.get("headline"):
        if v.get("_week"):   # 오른쪽 위 주간 딱지 자리를 비움
            boxes += _text_block(d, [v["headline"]], v.get("hl", []), (W - 330) // 2, 46, W - 400, 96, align="center")
        else:
            boxes += _text_block(d, [v["headline"]], v.get("hl", []), 640, 46, 1180, 104, align="center")
    L, R = v["left"], v["right"]
    for (it, cx, col) in ((L, 330, YELLOW), (R, 950, DOWN)):
        sz = it.get("size", 230)
        while _font(GOTHIC_X, sz).getlength(it["value"]) > 520 and sz > 80:
            sz -= 8
        f = _font(GOTHIC_X, sz)
        d.text((cx, 360), it["value"], font=f, fill=col, anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
        fl = _font(GOTHIC_X, 52)
        d.text((cx, 540), it["label"], font=fl, fill=(255, 255, 255), anchor="mm")
        boxes.append((cx - f.getlength(it["value"]) / 2, 240, cx + f.getlength(it["value"]) / 2, 570))
    if v.get("mid"):   # 같은 종류의 두 판단을 맞붙일 때는 화살표(전→후) 대신 'vs' (2026-11-26, 화살표가 '바뀜'으로 읽힘)
        d.text((640, 360), v["mid"], font=_font(GOTHIC_X, 64), fill=(255, 255, 255), anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0))
    else:
        d.polygon([(600, 330), (680, 360), (600, 390)], fill=(255, 255, 255))
    return base, boxes


def _face_detector_ok() -> bool:
    try:
        import cv2
        return hasattr(cv2, "CascadeClassifier")
    except ImportError:
        return False


def _face_box(im: Image.Image):
    """가장 큰 얼굴 (x, y, w, h) — opencv 가 없거나 못 찾으면 None."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        return None
    if not hasattr(cv2, "CascadeClassifier"):   # OpenCV 5 에서 빠짐
        return None
    g = cv2.cvtColor(np.asarray(im.convert("RGB")), cv2.COLOR_RGB2GRAY)
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    fs = casc.detectMultiScale(g, 1.1, 5, minSize=(max(40, g.shape[1] // 20),) * 2)
    return max(fs, key=lambda f: f[2] * f[3]) if len(fs) else None


def _person_crop(im: Image.Image, w: int, h: int, face_h: float = 0.46, face_x: float = 0.5) -> Image.Image:
    """얼굴이 칸 높이의 face_h 가 되고, 얼굴 가운데가 칸의 (0.5, 0.40) 에 오도록 자름. 얼굴을 못 찾으면 위쪽 가운데."""
    f = _face_box(im)
    if f is None:
        return _cover(im, w, h, 0.5, 0.25)
    fx, fy, fw, fh = (int(x) for x in f)
    s = max(face_h * h / fh, w / im.width, h / im.height)
    im2 = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    cx, cy = (fx + fw / 2) * s, (fy + fh / 2) * s
    x = int(min(max(cx - w * face_x, 0), im2.width - w))
    y = int(min(max(cy - h * 0.40, 0), im2.height - h))
    return im2.crop((x, y, x + w, y + h))


def _person(project: Project, spec: dict, v: dict) -> tuple[Image.Image, list]:
    """인물 썸네일: 오른쪽 얼굴 크게(컬러) + 이름표, 왼쪽 검은 바탕 큰 두 줄 (+ 따옴표 한 마디)."""
    base = Image.new("RGBA", (W, H), (12, 14, 20, 255))
    blend = bool(v.get("blend"))   # 2026-11-26 사용자: "인물반 글씨반 말고 둘이 합쳐서" → 사진을 화면 전체에, 글씨는 사진 위에 (왼쪽만 어둡게)
    pw = W if blend else int(W * v.get("photo_width", 0.56))
    im = _person_crop(_image(project, spec, v["image"]), pw, H, v.get("face_h", 0.46))
    im = ImageEnhance.Contrast(im).enhance(1.08)
    # blend: 얼굴(칸 가운데)을 오른쪽 face_x 로 밀어 붙이고, 빈 왼쪽은 어두운 바탕 → 그 위 글씨
    base.paste(im, (int(W * (v.get("face_x", 0.66) - 0.5)), 0) if blend else (W - pw, 0))
    g = Image.new("L", (W, H), 0)   # 사진 왼쪽 가장자리를 검은 바탕으로 부드럽게
    gd = ImageDraw.Draw(g)
    if blend:   # 왼쪽 60% 를 반투명으로 어둡게 — 사진이 비치되 글씨는 읽힘
        span = int(W * v.get("shade_w", 0.62))
        sx = int(W * (v.get("face_x", 0.66) - 0.5))   # 밀어 붙인 사진의 왼쪽 끝 — 경계선이 안 보이게 그 근처는 완전히 어둡게 이어 줌
        for i in range(span):
            edge = 255 if i < sx else (255 * max(0.0, 1 - (i - sx) / 220) ** 1.4)
            gd.line([(i, 0), (i, H)], fill=int(max(v.get("shade", 205) * (1 - i / span) ** 1.2, edge)))
    else:
        for i in range(260):
            gd.line([(W - pw + i, 0), (W - pw + i, H)], fill=int(255 * (1 - i / 260) ** 1.5))
        gd.rectangle([0, 0, W - pw, H], fill=255)
    base = Image.composite(Image.new("RGBA", (W, H), (12, 14, 20, 255)), base, g)
    d = ImageDraw.Draw(base)
    boxes = []
    per = v.get("person") or {}
    if per.get("name"):   # 이름표: 얼굴 아래, 재생 시간 자리(오른쪽 아래) 피해서
        fn, fr = _font(GOTHIC_X, 46), _font(GOTHIC_X, 30)
        nx, ny = (int(W * 0.56) + 60 if blend else W - pw + 60), H - 170
        nw = max(fn.getlength(per["name"]), fr.getlength(per.get("role", ""))) + 40
        d.rounded_rectangle([nx, ny, nx + nw, ny + 104], 10, fill=(12, 14, 20, 235))
        d.rectangle([nx, ny, nx + 8, ny + 104], fill=RED)
        d.text((nx + 22, ny + 8), per["name"], font=fn, fill=(255, 255, 255))
        d.text((nx + 22, ny + 62), per.get("role", ""), font=fr, fill=(210, 214, 222))
        boxes.append((nx, ny, nx + nw, ny + 104))
    tx, y = 50, v.get("text_y", 120)
    if v.get("top"):
        ft = _font(GOTHIC_X, 38)
        d.rounded_rectangle([tx - 6, y - 66, tx + ft.getlength(v["top"]) + 26, y - 14], 10, fill=RED)
        d.text((tx + 10, y - 62), v["top"], font=ft, fill=(255, 255, 255))
        boxes.append((tx, y - 66, tx + ft.getlength(v["top"]) + 26, y - 14))
    fnt = {"bhs": BHS, "myeongjo": MYEONGJO_X}.get(v.get("font", ""), GOTHIC_X)   # 글씨체 고르기 (기본 나눔고딕 ExtraBold)
    boxes += _text_block(d, v["lines"], v.get("hl", []), tx, y, (int(W * 0.62) if blend else W - pw + 120), v.get("size", 132), font=fnt)
    if v.get("quote"):
        fq = _font(GOTHIC_X, 56)   # 휴대폰 목록(가로 168px)에서도 6px 넘게
        q = f"\u201c{v['quote']}\u201d"
        while fq.getlength(q) > W - pw + 90 and fq.size > 46:
            fq = _font(GOTHIC_X, fq.size - 2)
        yy = boxes[-1][3] + 34
        d.text((tx, yy), q, font=fq, fill=(255, 238, 190), stroke_width=4, stroke_fill=(10, 10, 10))
        boxes.append((tx, yy, tx + fq.getlength(q), yy + fq.size))
    if v.get("credit"):   # 사진 출처 (CC BY 표시 의무 — 작게)
        fc = _font(GOTHIC_X, 18)
        d.text((W - pw + 12, 10), v["credit"], font=fc, fill=(235, 235, 235), stroke_width=2, stroke_fill=(0, 0, 0))
    return base.convert("RGB"), boxes


def week_of(project: Project) -> dict | None:
    """주간 영상의 기간 표시 (2026-11-22 사용자: "주간영상 기간을 명시하고 뭐 11월 3주차 이런식으로 썸네일에 알리는게 어떤가요? 앞으로의 주간영상들도 같은 템플릿으로").
    프로젝트 날짜(YYYYMMDD) 이전의 가장 가까운 금요일까지 월~금 한 주. 'n월 n주차'는 그 주의 목요일이 속한 달·날짜로(목요일 기준 주차)."""
    import datetime as _dt
    name = project.path.name
    if "weekly" not in name or not name[:8].isdigit():
        return None
    d = _dt.date(int(name[:4]), int(name[4:6]), int(name[6:8]))
    fri = d - _dt.timedelta(days=(d.weekday() - 4) % 7)
    mon, thu = fri - _dt.timedelta(days=4), fri - _dt.timedelta(days=1)
    return {"label": f"{thu.month}월 {math.ceil(thu.day / 7)}주차", "range": f"{mon.month}.{mon.day} ~ {fri.month}.{fri.day}"}


def _week_badge(im: Image.Image, wk: dict, boxes: list) -> Image.Image:
    """오른쪽 위 기간 딱지 — 모든 주간 썸네일에 같은 자리·같은 모양 (시리즈 표시)."""
    im = im.convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    # 2026-11-22 사용자: "오른쪽 위의 노란색 너무 싼티나요" → 반투명 검정 판 + 흰 글씨 + 왼쪽 가는 빨간 선 (차분하게)
    f1, f2 = _font(GOTHIC_X, 44), _font(GOTHIC_X, 26)
    w = max(f1.getlength(wk["label"]), f2.getlength(wk["range"])) + 52
    x1, y0, h = W - 30, 30, 100
    x0 = x1 - w
    d.rounded_rectangle([x0, y0, x1, y0 + h], 8, fill=(8, 10, 16, 190))
    d.rectangle([x0, y0, x0 + 6, y0 + h], fill=RED + (255,))
    d.text((x0 + 26, y0 + 12), wk["label"], font=f1, fill=(255, 255, 255))
    d.text((x0 + 26, y0 + 64), wk["range"], font=f2, fill=(190, 196, 206))
    boxes.append((x0, y0, x1, y0 + h))
    return Image.alpha_composite(im, ov).convert("RGB")


def render(project: Project, spec: dict, v: dict) -> tuple[Image.Image, list]:
    sr = series(project)
    # 브리핑·분석은 고정 틀(⑭)로 갈리므로 사진은 둘 다 컬러 그대로 (2026-11-25 사용자: "굳이 흑백이 아니여도 브리핑과 분석이 구분가기만 하면 돼요").
    # 흑백을 원하는 변형만 "bw": true
    if sr and v.get("image") and v.get("bw"):
        v = dict(v, image=dict(v["image"], _bw=True), tone="none")
    elif sr and v.get("layout", "photo") == "photo" and "tone" not in v:
        v = dict(v, tone="none")                 # 시장 채널은 교양 채널의 옛 사진 톤을 쓰지 않음
    wk = v.get("week") or (spec.get("package") or {}).get("week") or week_of(project)
    im, boxes = _render_layout(project, spec, dict(v, _week=wk) if wk else v)
    if v.get("credit") and v.get("layout", "photo") not in ("person", "brief_tab", "analysis_frame"):   # 사진 출처 (CC BY 표시 의무) — 인물 판은 _person 이 씀
        d = ImageDraw.Draw(im)
        fc = _font(GOTHIC_X, 18)
        d.text((W - 14 - fc.getlength(v["credit"]), 10), v["credit"], font=fc, fill=(235, 235, 235), stroke_width=2, stroke_fill=(0, 0, 0))
    if wk:
        im = _week_badge(im, wk, boxes)
    tk = None if v.get("no_ticker") or v.get("layout") == "analysis_frame" else (v.get("ticker") or (spec.get("package") or {}).get("ticker"))   # 차트·칩이 있는 판은 지수 띠를 끔
    if tk:   # 아래 왼쪽 작은 지수 띠 [{"name": "S&P 500", "chg": "-3.70%"}] — 재생 시간 자리(TIMESTAMP_BOX)는 피함.
        # 일부러 작은 글씨라 휴대폰 글씨 점검(boxes)에는 넣지 않음 (manual/09 §7-1 ⑧, 2026-11-21 사용자)
        im = im.convert("RGBA")
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        fs = v.get("ticker_size", 30)
        fn, fc = _font(GOTHIC_X, fs), _font(GOTHIC_X, fs)
        x0, y0 = (28, 24) if v.get("layout") == "brief_tab" else (28, H - fs - 40)   # 브리핑 틀은 아래가 흰 상자 자리 → 위 왼쪽
        x = x0 + 16
        parts = []
        for t in tk:
            parts.append((t["name"] + " ", (235, 235, 235)))
            parts.append((t["chg"] + "   ", (255, 90, 80) if t["chg"].startswith("-") else (90, 220, 120)))
        wtot = sum(fn.getlength(a) for a, _ in parts) - fn.getlength("   ")
        d.rounded_rectangle([x0, y0 - 8, x0 + 32 + wtot, y0 + fs + 12], 10, fill=(0, 0, 0, 190))
        for a, col in parts:
            d.text((x, y0), a, font=fc, fill=col)
            x += fn.getlength(a)
        im = Image.alpha_composite(im, ov).convert("RGB")
    return im, boxes


def _chart(v: dict) -> tuple[Image.Image, list]:
    """차트 썸네일 (2026-11-22 사용자: "썸네일도 여러 각기다른 스타일을 제시하세요"): 짙은 바탕 + 실제 종가 선(하락은 빨강) +
    끝점의 큰 숫자 + 왼쪽 위 큰 두 줄. series: [값…], days: ["월", …], value: "-23%", value_label: "엔비디아 한 주"."""
    base = Image.new("RGB", (W, H), (10, 13, 22))
    d = ImageDraw.Draw(base, "RGBA")
    for i in range(H):   # 아래쪽을 살짝 밝게
        a = int(40 * (i / H) ** 2)
        d.line([(0, i), (W, i)], fill=(40, 20, 28, a))
    ys = v["series"]
    lo, hi = min(ys), max(ys)
    x0, x1, y0, y1 = 120, W - 330, 330, 590
    pts = [(x0 + (x1 - x0) * i / (len(ys) - 1), y0 + (y1 - y0) * (hi - y) / (hi - lo or 1)) for i, y in enumerate(ys)]
    for gy in (y0, (y0 + y1) / 2, y1):
        d.line([(x0, gy), (x1, gy)], fill=(255, 255, 255, 28), width=2)
    down = ys[-1] < ys[0]
    col = DOWN if down else UP
    d.polygon(pts + [(x1, y1 + 40), (x0, y1 + 40)], fill=col + (38,))
    d.line(pts, fill=col, width=10, joint="curve")
    for (x, y) in pts:
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(255, 255, 255))
    fd = _font(GOTHIC_X, 30)
    for (x, _), lab in zip(pts, v.get("days", [])):
        d.text((x, y1 + 50), lab, font=fd, fill=(170, 176, 190), anchor="mt")
    ex, ey = pts[-1]
    fv = _font(GOTHIC_X, 150)
    d.text((W - 40, min(ey, H - 260)), v["value"], font=fv, fill=col, anchor="rm", stroke_width=8, stroke_fill=(0, 0, 0))
    fl = _font(GOTHIC_X, 40)
    d.text((W - 44, min(ey, H - 260) + 96), v.get("value_label", ""), font=fl, fill=(235, 235, 235), anchor="rm")
    boxes = _text_block(d, v["lines"], v.get("hl", []), 60, v.get("text_y", 70), v.get("text_w", 900), v.get("size", 104))
    boxes.append((W - 40 - fv.getlength(v["value"]), min(ey, H - 260) - 80, W - 40, min(ey, H - 260) + 140))
    return base, boxes


BHS = FONTS / "BlackHanSans-Regular.ttf"
NEON = {"lime": (190, 255, 60), "pink": (255, 70, 160), "cyan": (60, 230, 255), "yellow": (255, 222, 40)}


def _trend(project: Project, spec: dict, v: dict) -> tuple[Image.Image, list]:
    """젊은 층용 (2026-11-22 사용자: "내 채널이 대부분 40대50대 이상이거든? 젊은 유입층을 늘리고싶은데 좀 트렌디하게").
    시네마틱 실사풍 그림(GPT 이미지) 꽉 채움 + 왼쪽 어둡게 + 알약 태그 + 블랙한산스 두 줄(검은 테두리·딱딱한 그림자, 강조 한 단어만 네온) + 작은 스티커 칩.
    v: image.file, top, lines, hl, accent(lime|pink|cyan|yellow), sticker(선택, 오른쪽 위 비스듬한 스티커), chips"""
    boxes = []
    acc = NEON.get(v.get("accent", "lime"), NEON["lime"])
    im = _cover(_image(project, spec, v["image"]), W, H, *v["image"].get("focus", [0.5, 0.5]))
    im = ImageEnhance.Color(im).enhance(v.get("saturate", 1.15))
    base = im.convert("RGBA")
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for x in range(W):
        a = int(205 * max(0.0, 1 - x / (W * 0.7)) ** 1.1)
        sd.line([(x, 0), (x, H)], fill=(6, 6, 14, a))
    base.alpha_composite(sh)
    d = ImageDraw.Draw(base)
    tx, y = 58, v.get("text_y", 200)
    if v.get("top"):
        ft = _font(BHS, 40)
        tw = ft.getlength(v["top"])
        d.rounded_rectangle([tx, y - 78, tx + tw + 44, y - 18], 30, fill=acc)
        d.text((tx + 22, y - 74), v["top"], font=ft, fill=(8, 8, 12))
        boxes.append((tx, y - 78, tx + tw + 44, y - 18))
    maxw = v.get("text_w", 760)
    for ln in v["lines"]:
        s = v.get("size", 132)
        while _font(BHS, s).getlength(ln) > maxw and s > 60:
            s -= 4
        f = _font(BHS, s)
        cx = tx
        toks = ln.split(" ")
        for i, tok in enumerate(toks):
            word = tok + (" " if i < len(toks) - 1 else "")
            col = acc if any(h in tok for h in v.get("hl", [])) else (255, 255, 255)
            off = max(6, s // 16)
            d.text((cx + off, y + off), tok, font=f, fill=(0, 0, 0), stroke_width=max(8, s // 12), stroke_fill=(0, 0, 0))   # 딱딱한 그림자
            d.text((cx, y), tok, font=f, fill=col, stroke_width=max(8, s // 12), stroke_fill=(0, 0, 0))
            cx += f.getlength(word)
        boxes.append((tx, y, cx, y + s))
        y += int(s * 1.1)
    chips = v.get("chips", [])
    if chips:
        y += 22
        cx = tx
        for c in chips:
            fs = c.get("size", 44)
            f = _font(BHS, fs)
            w = f.getlength(c["text"]) + fs * 0.9
            col = {"up": UP, "down": DOWN}.get(c.get("color"), (255, 255, 255))
            fg = (255, 255, 255) if c.get("color") in ("up", "down") else (10, 10, 10)
            d.rounded_rectangle([cx, y, cx + w, y + fs * 1.5], int(fs * 0.75), fill=col, outline=(0, 0, 0), width=4)
            d.text((cx + fs * 0.45, y + fs * 0.22), c["text"], font=f, fill=fg)
            boxes.append((cx, y, cx + w, y + fs * 1.5))
            cx += w + 18
    if v.get("sticker"):   # 비스듬한 스티커 한 장 (오른쪽 위)
        fs = 46
        f = _font(BHS, fs)
        tw = f.getlength(v["sticker"])
        lay = Image.new("RGBA", (int(tw + 70), int(fs * 1.9)), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle([4, 4, lay.width - 4, lay.height - 4], 18, fill=(255, 255, 255), outline=(0, 0, 0), width=5)
        ld.text((lay.width / 2, lay.height / 2), v["sticker"], font=f, fill=(10, 10, 10), anchor="mm")
        lay = lay.rotate(v.get("sticker_rot", 8), expand=True, resample=Image.BICUBIC)
        sx, sy = v.get("sticker_xy", [W - lay.width - 40, 40])
        base.alpha_composite(lay, (int(sx), int(sy)))
        boxes.append((sx, sy, sx + lay.width, sy + lay.height))
    return base.convert("RGB"), boxes


def _fit_font(d, text: str, size: int, maxw: int, minsize: int = 56):
    f = _font(GOTHIC_X, size)
    while d.textlength(text, font=f) > maxw and f.size > minsize:
        f = _font(GOTHIC_X, f.size - 4)
    return f


def _brief_tab(project: Project, spec: dict, v: dict) -> tuple[Image.Image, list]:
    """브리핑 고정 틀 (manual/09 §7-1 ⑭, 2026-11-25 사용자: "차라리 오선의 썸네일 제작방식을 참조하세요" ·
    "썸네일 제목은 그날의 장에 대한 짧은 핵심 내용이 들어가야합니다"): 사진 꽉 채움 + 왼쪽 아래 빨간 날짜 탭 +
    흰 상자 속 검은 글씨 한 줄(그날 장의 핵심) + 오른쪽 위 채널 표시. 매일 같은 틀이라 글씨를 읽지 않아도 브리핑으로 보임."""
    im = _cover(_image(project, spec, v["image"]), W, H, *v["image"].get("focus", [0.5, 0.4]))
    g = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(g)
    for y in range(H):   # 아래로 갈수록 어둡게 (흰 상자가 뜨게)
        gd.line([(0, y), (W, y)], fill=int(190 * max(0.0, (y - 260) / (H - 260)) ** 1.3))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, g)
    d = ImageDraw.Draw(im)
    boxes = []
    head = v.get("headline") or " ".join(v.get("lines", []))
    f = _fit_font(d, head, v.get("size", 96), W - 150)
    bx, by = 40, 600 - f.size - 44            # 상자 아래 끝이 재생 시간 자리(y 630) 위에서 끝나게
    tw = d.textlength(head, font=f)
    d.rectangle([bx, by, bx + tw + 56, by + f.size + 44], fill=(255, 255, 255))
    hl = [h for h in v.get("hl", []) if h in head]
    x = bx + 28
    if hl:   # 강조 낱말만 빨강 (한 곳)
        a, b = head.split(hl[0], 1)
        for part, col in ((a, (12, 12, 12)), (hl[0], RED), (b, (12, 12, 12))):
            d.text((x, by + 16), part, font=f, fill=col)
            x += d.textlength(part, font=f)
    else:
        d.text((x, by + 16), head, font=f, fill=(12, 12, 12))
    boxes.append((bx, by, bx + tw + 56, by + f.size + 44))
    if v.get("top"):
        fd = _font(GOTHIC_X, 40)
        dw = d.textlength(v["top"], font=fd)
        d.polygon([(bx, by - 64), (bx + dw + 40, by - 64), (bx + dw + 80, by), (bx, by)], fill=RED)
        d.text((bx + 20, by - 56), v["top"], font=fd, fill=(255, 255, 255))
        boxes.append((bx, by - 64, bx + dw + 80, by))
    title = (spec.get("package") or {}).get("channel_mark", "이어 읽는 시장")
    if title:
        fm = _font(GOTHIC_X, 22)
        mw = d.textlength(title, font=fm) + 28
        d.rounded_rectangle([W - 24 - mw, 20, W - 24, 62], 8, fill=(14, 14, 18))
        d.text((W - 24 - mw + 14, 28), title, font=fm, fill=(255, 255, 255))
    if v.get("credit"):
        fc = _font(GOTHIC_X, 18)
        d.text((W - 24 - fc.getlength(v["credit"]), 70), v["credit"], font=fc, fill=(235, 235, 235), stroke_width=2, stroke_fill=(0, 0, 0))
    return im, boxes


def _analysis_frame(project: Project, spec: dict, v: dict) -> tuple[Image.Image, list]:
    """분석 고정 틀 (manual/09 §7-1 ⑭): 검은 바탕 + 빨간 테두리 + 왼쪽 인물(컬러, 어둡게 이어 붙임) +
    오른쪽 작은 소제목 · 큰 두 줄 · 빨간 날짜 상자. 인물이 없으면 컬러 사물 사진을 같은 자리에."""
    base = Image.new("RGB", (W, H), (8, 8, 10))
    pw = int(W * v.get("photo_width", 0.48))
    src = _image(project, spec, v["image"])
    im = _person_crop(src, pw, H, v.get("face_h", 0.46)) if v.get("person") else _cover(src, pw, H, *v["image"].get("focus", [0.5, 0.35]))
    base.paste(im.convert("RGB"), (0, 0))
    g = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(g)
    for x in range(W):
        gd.line([(x, 0), (x, H)], fill=int(255 * min(1.0, max(0.0, (x - (pw - 220)) / 220))))
    base = Image.composite(Image.new("RGB", (W, H), (8, 8, 10)), base, g)
    d = ImageDraw.Draw(base)
    d.rectangle([0, 0, W - 1, H - 1], outline=RED, width=10)
    boxes = []
    xr = W - 60
    y = v.get("text_y", 170)
    if v.get("kicker"):
        fk = _font(GOTHIC_X, 46)
        d.text((xr, y), v["kicker"], font=fk, fill=(255, 255, 255), anchor="ra")
        boxes.append((xr - d.textlength(v["kicker"], font=fk), y, xr, y + 46))
        y += 70
    for i, ln in enumerate(v.get("lines", [])):
        f = _fit_font(d, ln, v.get("size", 120), W - pw - 60)
        col = (255, 206, 0) if any(h in ln for h in v.get("hl", [])) else (255, 255, 255)
        d.text((xr, y), ln, font=f, fill=col, anchor="ra")
        boxes.append((xr - d.textlength(ln, font=f), y, xr, y + f.size))
        y += f.size + 16
    if v.get("top"):
        fd = _font(GOTHIC_X, 38)
        dw = d.textlength(v["top"], font=fd)
        y = min(y + 18, 540)
        d.rectangle([xr - dw - 40, y, xr, y + 60], fill=RED)
        d.text((xr - 20, y + 30), v["top"], font=fd, fill=(255, 255, 255), anchor="rm")
        boxes.append((xr - dw - 40, y, xr, y + 60))
    per = v.get("person") or {}
    if per.get("name"):
        fn = _font(GOTHIC_X, 30)
        d.text((40, H - 70), per["name"] + (f" · {per['role']}" if per.get("role") else ""), font=fn, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    if v.get("credit"):
        fc = _font(GOTHIC_X, 18)
        d.text((24, 20), v["credit"], font=fc, fill=(235, 235, 235), stroke_width=2, stroke_fill=(0, 0, 0))
    return base, boxes


def _render_layout(project: Project, spec: dict, v: dict) -> tuple[Image.Image, list]:
    if v.get("layout") == "brief_tab":
        return _brief_tab(project, spec, v)
    if v.get("layout") == "analysis_frame":
        return _analysis_frame(project, spec, v)
    if v.get("layout") == "trend":
        return _trend(project, spec, v)
    if v.get("layout") == "person":
        return _person(project, spec, v)
    if v.get("layout") == "punch":
        return _punch(project, spec, v)
    if v.get("layout") == "chart":
        return _chart(v)
    if v.get("layout") == "versus" and v.get("theme") == "dark":
        return _versus_dark(v)
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


# ── 올릴 썸네일 고르기 (2026-11-20 사용자: "썸네일은 abc중에서 최대한 시장반응을 고려하여 조회수가 높게 나올 썸네일로 정해주세요 앞으로 말이죠")
# 근거: docs/49(같은 채널 안 터진/안 된 썸네일·제목 비교) · docs/55(유명 인물 효과). 점수는 그 조사에서 차이가 난 특징만 쓴다.
POLITICIANS = ("트럼프", "바이든", "시진핑", "푸틴", "이재명", "윤석열", "젤렌스키", "네타냐후")
# 클릭을 부르는 민감한 말 (manual/09 §7-1 ①-1, 2026-11-21 사용자: "블랙 ㅁㅁㅁ 등 공포감이 있는 핫한 키워드와 금리 연준").
# 근거 자료가 아니라 사용자 판단 — 반응(Studio 테스트 및 비교)을 보며 고친다. 팩트시트·매체 제목에 실제로 나온 말일 때만 점수.
FEAR = ("검은", "블랙", "폭락", "급락", "붕괴", "공포", "패닉", "쇼크", "충격", "경고", "위기", "버블", "거품", "조사", "대학살", "증발")
MACRO = ("금리", "연준", "인상", "인하", "파월", "FOMC", "국채", "환율")
COMMAND = ("사세요", "파세요", "사라", "팔아라", "지금 사", "무조건", "당장")


def _hot_words(project: Project) -> list[str]:
    """팩트시트 '## 핫 키워드'의 각 줄 첫 낱말 (manual/09 §7-1 ①)."""
    import re
    fs = project.dir("research") / "factsheet.md"
    if not fs.exists():
        return []
    m = re.search(r"## 핫 키워드[^\n]*\n(.*?)(?:\n## |\Z)", fs.read_text(encoding="utf-8"), re.S)
    if not m:
        return []
    # 줄 모양: "- 국내 제목 반복: '오픈AI 자금난'·'AI 거품'" / "- daily_brief ⑤ 주제어: 급락(9) · 전망(5)"
    # 콜론 앞은 이름표(국내·해외·제목·daily_brief…)라 키워드가 아님 — 예전엔 이름표 낱말이 키워드로 섞였음 (2026-11-23)
    # "→ 썸네일 큰 글씨…" 줄은 썸네일에 넣을 말이라 썸네일 글자와 맞대면 늘 맞으므로 뺌
    out: list[str] = []
    for ln in m.group(1).splitlines():
        ln = ln.strip().lstrip("-").strip()
        if not ln or ln.startswith(("썸네일", "→")):
            continue
        if re.search(r"[:：]", ln):
            ln = re.split(r"[:：]", ln, maxsplit=1)[1]
        ln = re.split(r"\s[—–]\s|\s\(", ln)[0]          # 뒤의 풀이·괄호 설명 버림
        quoted = re.findall(r"[‘'\"“]([^’'\"”]+)[’'\"”]", ln)
        items = quoted or re.split(r"[·,/]+", ln)
        for it in items:
            it = re.sub(r"\(\d+\)", "", it).strip(" *")
            if len(it) >= 2:   # 따옴표 구절은 통째로만 ('투자 우려'를 '투자'·'우려'로 쪼개면 흔한 낱말까지 점수)
                out.append(it)
    seen: set[str] = set()
    return [w for w in out if not (w in seen or seen.add(w))]


_src_text = ""


def score(v: dict, qa: dict, hot: list[str], title: str = "", sr: str | None = None) -> tuple[float, list[str]]:
    """한 변형의 점수와 이유. 높을수록 조회수 쪽 근거가 많음 (인과 증명이 아니라 같은 채널 안 비교의 경향)."""
    import re
    text = " ".join(v.get("lines", []) + [v.get("headline", ""), v.get("top", ""), v.get("kicker", "")] +
                    [x.get("value", "") for x in (v.get("left") or {}, v.get("right") or {})])
    sc, why = 0.0, []
    if not qa.get("ok"):
        sc -= 5; why.append("점검 실패(글자 크기·재생 시간 자리) −5")
    per = (v.get("person") or {}).get("name")
    if sr == "brief":   # 브리핑 = 기업 사진 (09 §7-1 ⑬) — 얼굴 가점 대신 기업 사진 가점, 인물은 분석 편으로
        if v.get("layout") == "person" or per:
            sc -= 3; why.append("브리핑에 인물 −3 — 인물은 분석 편 썸네일로 (09 §7-1 ⑬)")
        elif v.get("company") or Path(((v.get("image") or {}).get("file")) or "").name.startswith("co_"):
            sc += 2; why.append(f"그날 핵심 기업 사진({v.get('company') or '기업'}) +2 (09 §7-1 ⑬)")
        per = None
        if v.get("layout") == "brief_tab":
            sc += 2; why.append("브리핑 고정 틀(장 핵심 한 줄) +2 — 목록에서 시리즈로 보임 (09 §7-1 ⑭)")
    if sr == "analysis" and v.get("layout") == "analysis_frame":
        sc += 2; why.append("분석 고정 틀 +2 — 목록에서 시리즈로 보임 (09 §7-1 ⑭)")
    if v.get("layout") == "analysis_frame" and per and (qa.get("face_area") is None or qa.get("face_area", 0) >= 0.06):
        sc += 3; why.append(f"사건 당사자 얼굴({per}) +3 — docs/55")
        per = None
    if v.get("layout") == "person" and per and (qa.get("face_area") is None or qa.get("face_area", 0) >= 0.06):
        sc += 3; why.append(f"사건 당사자 얼굴 크게({per}) +3 — 인물 제목의 터진 영상 42% vs 안 된 10% (docs/55)")
        if per.split()[-1] in title or per in title:
            sc += 1; why.append("제목 앞에도 같은 이름 +1")
    hits = [w for w in hot if w in text] or [w for w in _hot_tokens(hot) if w in text]
    if hits:
        sc += 2; why.append(f"핫 키워드 큰 글씨({', '.join(hits[:2])}) +2 (manual/09 §7-1 ①)")
    src = _src_text  # 팩트시트 글 (낚시 막기: 거기 없는 말은 점수 없음)
    fear = [w for w in FEAR if w in text and w in src]
    if fear:
        sc += 1; why.append(f"공포·민감 키워드({fear[0]}) +1 (사용자 판단 2026-11-21, §7-1 ①-1)")
    mac = [w for w in MACRO if w in text and w in src]
    if mac:
        sc += 1; why.append(f"금리·연준 키워드({mac[0]}) +1 (사용자 판단 2026-11-21, §7-1 ①-1)")
    if re.search(r"\d", text):
        sc += 1.5; why.append("구체적 숫자 +1.5 (docs/49 §3)")
    if v.get("quote"):
        sc += 0.5; why.append("당사자 따옴표 발언 +0.5")
    if re.search(r"(가능성|할까|일까|될까|인가요|살릴까|오를까|내릴까)\s*[?？]", text):   # 추측형만 깎음 — 논쟁형·역설 질문은 후보 (manual/09 §7-1 2, 2026-11-21 사용자)
        sc -= 1.5; why.append("물음표 추측 −1.5 (docs/49)")
    if any(n in text for n in POLITICIANS) and not per:
        sc -= 1.5; why.append("정치인 이름만 −1.5 (docs/55: 0.82배)")
    if any(c in text for c in COMMAND):
        sc -= 2; why.append("사라·팔라 명령 −2")
    small = qa.get("smallest_text_px_at_168w", 0)
    if small >= 10:
        sc += 0.5; why.append("휴대폰 목록에서도 큰 글씨 +0.5")
    return round(sc, 2), why


_HOT_STOP = {"마감", "오늘", "어제", "하루", "월요일", "화요일", "수요일", "목요일", "금요일", "주말", "이후", "전망", "우려", "효과", "기록", "발표", "소식", "the", "and", "for", "with", "stocks", "stock"}


def _hot_tokens(hot: list[str]) -> list[str]:
    """핫 키워드가 기사 제목 통째일 때(예: '엔비디아 5.9%↓') 썸네일 글자와 맞대 볼 낱말 — 고유명사·지수 이름.
    통째 비교만 하면 짧은 썸네일 글자와 거의 안 맞아 +2 가 매일 0건이었음 (2026-11-25 사용자 지적 뒤 확인)."""
    out: list[str] = []
    for h in hot:
        for t in re.split(r"[\s·,…'\"‘’“”()\[\]:/|]+", h):
            t = re.sub(r"(은|는|이|가|을|를|의|에|에서|보다|도|만|과|와)$", "", t)
            if len(t) >= 2 and not re.search(r"\d", t) and t.lower() not in _HOT_STOP and t not in out:
                out.append(t)
    return out


def _vtext(v: dict) -> str:
    return " ".join(v.get("lines", []) + [v.get("headline", ""), v.get("top", ""), v.get("kicker", "")] +
                    [x.get("value", "") for x in (v.get("left") or {}, v.get("right") or {})])


def _rethumbs() -> dict:
    """data/analytics/actions.jsonl 의 rethumb 기록 → {영상 id: 지금 걸린 변형}."""
    f = Path(__file__).resolve().parents[2] / "data" / "analytics" / "actions.jsonl"
    out: dict = {}
    if f.exists():
        for ln in f.read_text(encoding="utf-8").splitlines():
            try:
                a = json.loads(ln)
            except Exception:
                continue
            if a.get("action") == "rethumb" and a.get("video"):
                out[a["video"]] = str(a.get("after", "")).upper()[:1] or out.get(a["video"])
    return out


def packaging_issues(project: Project) -> list[str]:
    """업로드 전 종합 검수(preflight)용 — 올릴 썸네일이 바로 앞 편과 같은 사진이거나, 제목·썸네일의 '혼자' 주장이 팩트시트와 어긋나면."""
    f = project.dir("edit") / "thumbnail_pick.json"
    hy = project.dir("script") / "hybrid.json"
    if not (f.exists() and hy.exists()):
        return []
    pk = json.loads(f.read_text(encoding="utf-8"))
    pkg = json.loads(hy.read_text(encoding="utf-8")).get("package") or {}
    v = next((t for t in pkg.get("thumbnails", []) if t.get("id") == pk.get("pick")), None)
    out: list[str] = []
    if v:
        rec = recent_uploads(project, 1)
        img = Path(((v.get("image") or {}).get("file")) or "").name
        if rec and img and img == rec[0]["image"]:
            out.append(f"썸네일 {v['id']} 가 바로 앞 편({rec[0]['project']})과 같은 사진({img}) — 새 사진(인물이면 다른 장면)으로 다시 (manual/09 §7-1)")
    fs = project.dir("research") / "factsheet.md"
    text = pkg.get("title", "") + " " + " ".join(_vtext(t) for t in pkg.get("thumbnails", []))
    out += only_claims(text, fs.read_text(encoding="utf-8") if fs.exists() else "")
    return out


def packaging_notes(project: Project) -> list[str]:
    """막지는 않고 알리기만 (스타일 기본값은 MUST 검사로 만들지 않음 — manual/README §3-1): 브리핑에 인물 썸네일."""
    f, hy = project.dir("edit") / "thumbnail_pick.json", project.dir("script") / "hybrid.json"
    if series(project) != "brief" or not (f.exists() and hy.exists()):
        return []
    pick_id = json.loads(f.read_text(encoding="utf-8")).get("pick")
    v = next((t for t in (json.loads(hy.read_text(encoding="utf-8")).get("package") or {}).get("thumbnails", []) if t.get("id") == pick_id), None)
    if v and (v.get("layout") == "person" or (v.get("person") or {}).get("name")):
        return [f"브리핑인데 썸네일 {v['id']} 가 인물 — 기본은 그날 핵심 기업 사진, 인물은 분석 편으로 (manual/09 §7-1 ⑬, company-photo pick)"]
    return []


def recent_uploads(project: Project, n: int = 3) -> list[dict]:
    """같은 줄기(날짜 뒤 이름이 같은 프로젝트, 예: …-market-daily)에서 이 편보다 앞서 실제로 올린 최근 n편의 썸네일 — 사진 파일·배치."""
    name = project.path.name
    m = re.match(r"(\d{8})-(.+)", name)
    if not m:
        return []
    day, stem = m.groups()
    out: list[dict] = []
    for d in sorted(project.path.parent.glob(f"*-{stem}"), reverse=True):
        dm = re.match(r"(\d{8})-", d.name)
        if not dm or dm.group(1) >= day or d.name.split("-", 1)[1] != stem:
            continue
        pub, hy = d / "05_edit" / "youtube_publish.json", d / "02_script" / "hybrid.json"
        if not (pub.exists() and hy.exists()):
            continue
        try:
            pj = json.loads(pub.read_text(encoding="utf-8"))
            used = re.search(r"thumbnail_([A-Z])", pj.get("thumbnail", "")).group(1)
            used = _rethumbs().get(pj.get("video_id", ""), used)   # 올린 뒤 ops-act rethumb 로 바꾼 것이 지금 걸린 것
            v = next(t for t in json.loads(hy.read_text(encoding="utf-8"))["package"]["thumbnails"] if t["id"] == used)
        except Exception:
            continue
        out.append({"project": d.name, "image": Path(((v.get("image") or {}).get("file")) or "").name,
                    "layout": v.get("layout", ""), "person": (v.get("person") or {}).get("name", "")})
        if len(out) >= n:
            break
    return out


def repeat_penalty(v: dict, recent: list[dict]) -> tuple[float, list[str]]:
    """구독자 목록에서 어제 영상과 같아 보이면 새 소식이라는 신호가 사라짐 (2026-11-25 사용자: "오늘올린 썸네일 이전과 계속 똑같은데").
    같은 사진 파일 = 거의 같은 썸네일 → 얼굴 가점(+3)을 넘게 깎음. 같은 인물(다른 사진)·같은 배치 연속은 조금만."""
    if not recent:
        return 0.0, []
    img = Path(((v.get("image") or {}).get("file")) or "").name
    per = (v.get("person") or {}).get("name", "")
    for i, r in enumerate(recent):
        if img and img == r["image"]:
            return (-5.0 if i == 0 else -3.0), [f"최근 올린 썸네일({r['project']})과 같은 사진 {'−5' if i == 0 else '−3'} — 목록에서 같은 영상처럼 보임"]
    d, why = 0.0, []
    if per and per == recent[0]["person"]:
        d -= 2; why.append(f"바로 앞 편도 같은 인물({per}) −2")
    if v.get("layout") and len(recent) >= 2 and all(r["layout"] == v.get("layout") for r in recent[:2]):
        d -= 1; why.append(f"같은 배치({v.get('layout')}) 세 편째 −1")
    return d, why


_PCT = re.compile(r"([가-힣]+|[A-Za-z&]{2,}(?:\([A-Z]+\))?)\s+[\d,]+(?:\.\d+)?\s*(?:달러|원|포인트|p)?\s*\(\s*([-−+]?\d+(?:\.\d+)?)%")


def only_claims(text: str, factsheet: str) -> list[str]:
    """'X만 -11%'·'왜 X만' 같은 '혼자' 주장을 팩트시트 숫자와 맞대 봄 — 같은 방향으로 X 만큼 이상 움직인 다른 종목이 있으면 틀린 말.
    (2026-11-25: '왜 마이크론만 -11%였나' — 같은 날 코어위브 −11.86%·델 −11.83% 로 마이크론보다 더 빠짐)"""
    vals: dict[str, float] = {}
    for nm, pc in _PCT.findall(factsheet or ""):
        vals.setdefault(nm.split("(")[0], float(pc.replace("−", "-")))
    out: list[str] = []
    for nm in dict.fromkeys(re.findall(r"([가-힣]+|[A-Za-z]{2,})만(?![가-힣])", text or "")):
        if nm not in vals:
            continue
        x = vals[nm]
        more = [f"{k} {v:+.2f}%" for k, v in vals.items() if k != nm and (v < 0) == (x < 0) and abs(v) >= abs(x)]
        if more:
            out.append(f"'{nm}만' — 팩트시트에 {nm}({x:+.2f}%)만큼 이상 같은 방향으로 움직인 종목이 있음: {', '.join(more[:4])}")
    return out


def pick(project: Project, pkg: dict, qa: dict) -> dict:
    """올릴 썸네일 하나 → 05_edit/thumbnail_pick.json (yt-publish 의 --thumb auto 가 읽음). package.thumb_pick 이 있으면 그대로."""
    hot = _hot_words(project)
    global _src_text
    fs = project.dir("research") / "factsheet.md"
    _src_text = fs.read_text(encoding="utf-8") if fs.exists() else ""
    title = pkg.get("title", "")
    sr = series(project)
    scores = {v["id"]: score(v, qa.get(v["id"], {}), hot, title, sr) for v in pkg["thumbnails"]}
    recent = recent_uploads(project)
    for v in pkg["thumbnails"]:
        s_, w_ = scores[v["id"]]
        d, why = repeat_penalty(v, recent)
        if d:
            scores[v["id"]] = (round(s_ + d, 2), w_ + why)
    forced = pkg.get("thumb_pick")
    best = forced if forced in scores else max(scores, key=lambda k: (scores[k][0], -ord(k[0])))
    res = {"pick": best, "forced": bool(forced in scores), "hot": hot, "series": sr,
           "recent": [{"project": r["project"], "image": r["image"], "layout": r["layout"]} for r in recent],
           "title_issues": only_claims(title + " " + " ".join(_vtext(v) for v in pkg["thumbnails"]), _src_text),
           "scores": {k: {"score": s_, "why": w} for k, (s_, w) in scores.items()}}
    (project.dir("edit") / "thumbnail_pick.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return res


def run(project: Project) -> dict:
    raw = (project.dir("script") / "hybrid.json").read_text(encoding="utf-8")
    spec = json.loads(raw)
    pkg = spec["package"]
    for v in pkg["thumbnails"]:  # 글자 기호 정리
        v["chips"] = [{**c, "text": _fix(c["text"])} for c in v.get("chips", [])]
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
    waiting = [v for v in pkg["thumbnails"] if (v.get("image") or {}).get("file") and not (project.path / v["image"]["file"]).exists()]
    for v in waiting:   # 그림·사진이 아직 없는 변형(PC 에서 그리는 초상 등)은 건너뛰고 나머지로 계속
        print(f"[thumbnail] {v['id']} 건너뜀 — 그림 없음: {v['image']['file']}")
    pkg["thumbnails"] = [v for v in pkg["thumbnails"] if v not in waiting]
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
        if v.get("layout") == "person":   # 얼굴이 휴대폰 목록에서도 알아볼 만큼 큰가 (docs/55: 인물 제목의 터진 영상 42% 가 큰 얼굴)
            if not _face_detector_ok():   # 얼굴 찾기가 없는 PC(OpenCV 5): 재지 못함 — 실패로 치지 않고 사람이 눈으로 (사진을 얼굴 중심으로 미리 자름)
                qa[v["id"]]["face_area"] = None
                continue
            fb = _face_box(im)
            fa = round(float(fb[2] * fb[3]) / (W * H), 3) if fb is not None else 0
            qa[v["id"]]["face_area"] = fa
            qa[v["id"]]["ok"] = qa[v["id"]]["ok"] and fa >= 0.06
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
    pk_ = pick(project, pkg, qa)
    md += ["## 올릴 썸네일 (자동 선택 — docs/49·55 근거 점수, `--thumb` 로 바꿀 수 있음)", f"**{pk_['pick']}**" + (" (대본에서 지정)" if pk_["forced"] else ""), ""]
    for k, v_ in pk_["scores"].items():
        md += [f"- {k}: {v_['score']}점 — " + " · ".join(v_["why"])]
    md += ["", "## 점검", "```json", json.dumps(qa, ensure_ascii=False, indent=1), "```"]
    (edir / "package.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[thumbnail] {len(made)}장 → {edir} (미리보기 thumbnail_preview.png, 점검 {qa}) · 올릴 것 {pk_['pick']} {pk_['scores'][pk_['pick']]['score']}점")
    return qa
