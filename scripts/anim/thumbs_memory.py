"""호기심 편(기억) 썸네일 A/B/C — 원화(판 + 조각) + 큰 두 줄 글씨, 강조 하나만 노랑, 오른쪽 아래 비움 (prompts/thumbnail.md).

    python scripts/anim/thumbs_memory.py <art 폴더(curiosity)> <출력 폴더>
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ART, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
FONT = Path(__file__).resolve().parents[2] / "ytflow/assets/fonts/NanumGothic-ExtraBold.ttf"
TW, TH = 1280, 720


def plate(name, cx=0.5, cy=0.5, zoom=1.0, dark=0.75):
    im = Image.open(ART / f"{name}.png").convert("RGB")
    s = max(TW / im.width, TH / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(0, round(im.width * cx - TW / 2)), im.width - TW)
    y = min(max(0, round(im.height * cy - TH / 2)), im.height - TH)
    im = im.crop((x, y, x + TW, y + TH))
    return ImageEnhance.Brightness(im).enhance(dark)


def put(bg, piece, x, y, h, flip=False):
    p = Image.open(ART / f"{piece}.png").convert("RGBA")
    p = p.resize((round(p.width * h / p.height), h), Image.LANCZOS)
    if flip:
        p = p.transpose(Image.FLIP_LEFT_RIGHT)
    bg.paste(p, (x - p.width // 2, y - p.height), p)


def text(bg, lines, x, y, size=118):
    d = ImageDraw.Draw(bg)
    f = ImageFont.truetype(str(FONT), size)
    for i, segs in enumerate(lines):
        cx = x
        for s, yellow in segs:
            d.text((cx, y + i * (size + 22)), s, font=f, fill="#ffd23f" if yellow else "white",
                   stroke_width=10, stroke_fill="#141414")
            cx += d.textlength(s, font=f)


# A: 영상엔 없던 유리 조각
a = plate("road74", .5, .62, 1.15, .7)
put(a, "glass", 640, 640, 200)
put(a, "s74_sure", 860, 700, 520, flip=True)
text(a, [[("영상엔 없던", False)], [("유리 조각", True)]], 60, 70)
# B: 내 글씨인데 기억이 다르다
b = plate("class86", .55, .5, 1.1, .72)
put(b, "stu_shock", 900, 790, 700)
text(b, [[("내 글씨인데", False)], [("기억이 다르다", True)]], 60, 70)
# C: 몇 번째로 다시 쓴 기억?
c = plate("desknight", .5, .55, 1.0, .75)
put(c, "manuscript", 860, 640, 520)
put(c, "pencil", 1010, 600, 330)
text(c, [[("몇 번째로", False)], [("다시 쓴", True), (" 기억?", False)]], 60, 70)

for k, im in zip("ABC", (a, b, c)):
    im.save(OUT / f"thumbnail_{k}.png")
prev = Image.new("RGB", (TW * 3 // 2 + 40, TH // 2 + 20), "white")
for i, im in enumerate((a, b, c)):
    prev.paste(im.resize((TW // 2, TH // 2)), (10 + i * (TW // 2 + 10), 10))
prev.save(OUT / "thumbnail_preview.png")
print("ok")
