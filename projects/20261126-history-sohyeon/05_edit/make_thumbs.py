"""썸네일 A/B/C v2 — 사용자: "제목과 썸네일을 봤을 때 이게 뭔 내용이지? 뭘 말하고 싶은 건지 모르겠어요".
같은 주제 인기 영상 12개 썸네일을 비교(05_edit/package.md): 잘 되는 썸네일은 ① 이름(소현세자)과 의혹(독살·아버지 인조)을
아래쪽 큰 두 줄로 바로 말하고 ② 대립하는 두 사람 얼굴을 크게 ③ 강조 한 낱말만 색. 구조만 따르고 그림·문구는 우리 것.
그림은 본편과 같은 재현 그림(A안, Codex). 결과는 Drive 영상 폴더 thumbs/."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

EP = Path(r"G:\내 드라이브\ytflow\영상\20261126-history-sohyeon")
OUT = EP / "thumbs"; OUT.mkdir(exist_ok=True)
W, H = 1280, 720
BOLD = r"C:\Windows\Fonts\malgunbd.ttf"
YEL, RED, IVORY = (255, 214, 64), (225, 38, 38), (250, 246, 238)


def crop(img, cx, cy, cw, bright=1.0, aspect=9 / 16, size=(W, H)):
    im = Image.open(EP / img).convert("RGB"); w, h = im.size
    box = (int(cx * w), int(cy * h), int((cx + cw) * w), int(cy * h + cw * w * aspect))
    return ImageEnhance.Brightness(im.crop(box).resize(size, Image.LANCZOS)).enhance(bright)


def bottom_band(im, top=0.42):
    g = Image.new("L", (1, H))
    for y in range(H):
        t = (y / H - top) / (1 - top); g.putpixel((0, y), int(255 * max(0, min(1, t)) ** 0.8 * 0.92))
    return Image.composite(Image.new("RGB", (W, H)), im, g.resize((W, H)))


def two_lines(d, rows, size=112, y=None):
    """rows=[[(글, 색), ...], ...] 가운데 정렬, 아래쪽 큰 두 줄."""
    f = ImageFont.truetype(BOLD, size)
    y = y if y is not None else H - 40 - len(rows) * int(size * 1.12)
    for parts in rows:
        tot = sum(d.textlength(s, font=f) for s, _ in parts); x = (W - tot) / 2
        for s, c in parts:
            d.text((x, y), s, font=f, fill=c, stroke_width=9, stroke_fill=(0, 0, 0)); x += d.textlength(s, font=f)
        y += int(size * 1.12)


def tag(d, s, xy, bg=RED, size=40):
    f = ImageFont.truetype(BOLD, size); x, y = xy; tw = d.textlength(s, font=f)
    d.rounded_rectangle((x, y, x + tw + 36, y + size + 22), 8, fill=bg); d.text((x + 18, y + 8), s, font=f, fill=(255, 255, 255))


def fit_check(rows, size):
    f = ImageFont.truetype(BOLD, size); d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    return max(sum(d.textlength(s, font=f) for s, _ in r) for r in rows) < W - 60


# A — 아버지(인조) 와 아들(소현세자) 두 얼굴 + "아버지가 독살했나? / 소현세자의 죽음"
a = Image.new("RGB", (W, H))
king = crop("art/N11_injo.png", 0.615, 0.25, 0.15, 2.2, aspect=720 / 640, size=(640, 720))
prince = crop("samples/A3_observatory.png", 0.12, 0.02, 0.34, 1.0, aspect=720 / 640, size=(640, 720))
a.paste(king, (0, 0)); a.paste(prince, (640, 0))
mask = Image.linear_gradient("L").rotate(90).resize((120, H)); a.paste(king.crop((520, 0, 640, H)), (520, 0), mask)
a = bottom_band(a, .40); d = ImageDraw.Draw(a)
tag(d, "아버지 · 인조", (30, 30), bg=(40, 40, 40)); tag(d, "아들 · 소현세자", (W - 330, 30), bg=(40, 40, 40))
rowsA = [[("아버지가 ", IVORY), ("독살", RED), ("했나?", IVORY)], [("소현세자의 죽음", YEL)]]
assert fit_check(rowsA, 118); two_lines(d, rowsA, 118); a.save(OUT / "thumbnail_A.png")

# B — 병상의 세자 + "귀국 두 달 만에 / 죽은 소현세자" + '실록: 독에 중독된 듯' 쪽지
b = bottom_band(crop("art/N6_physician.png", 0.2, 0.05, 0.62, 1.25), .38); d = ImageDraw.Draw(b)
tag(d, "실록: \"약물에 중독된 사람 같았다\"", (30, 30), size=38)
rowsB = [[("귀국 ", IVORY), ("두 달", YEL), (" 만에", IVORY)], [("죽은 소현세자", IVORY)]]
assert fit_check(rowsB, 120); two_lines(d, rowsB, 120); b.save(OUT / "thumbnail_B.png")

# C — 실록 종이 + 세자 얼굴, "누가 소현세자를 / 죽였나" (380년 미해결)
c = Image.new("RGB", (W, H), (20, 16, 12))
paper = Image.new("RGB", (700, H), (214, 196, 156)); dp = ImageDraw.Draw(paper); fs = ImageFont.truetype(r"C:\Windows\Fonts\batang.ttc", 52)
for i, s in enumerate(["온몸이 전부 검은빛이었고", "일곱 구멍에서 선혈이", "마치 약물에 중독되어", "죽은 사람과 같았다"]):
    dp.text((50, 60 + i * 80), s, font=fs, fill=(42, 30, 20))
dp.ellipse((30, 270, 560, 360), outline=(190, 20, 25), width=8)
c.paste(paper.rotate(3, expand=False, fillcolor=(20, 16, 12)), (-40, 0))
c.paste(crop("samples/A3_observatory.png", 0.12, 0.02, 0.34, .95, aspect=720 / 640, size=(640, 720)), (640, 0))
c = bottom_band(c, .45); d = ImageDraw.Draw(c)
tag(d, "인조실록 · 1645", (30, 30), size=36)
rowsC = [[("누가 ", IVORY), ("소현세자", YEL), ("를", IVORY)], [("죽였나", RED)]]
assert fit_check(rowsC, 120); two_lines(d, rowsC, 120); c.save(OUT / "thumbnail_C.png")

# 미리보기: 실제 크기 + 휴대폰 목록 크기
pv = Image.new("RGB", (3 * 660 + 40, 520), (24, 24, 24)); dp = ImageDraw.Draw(pv)
for i, (n, im) in enumerate([("A", a), ("B", b), ("C", c)]):
    pv.paste(im.resize((640, 360)), (20 + i * 660, 20)); pv.paste(im.resize((168, 94)), (20 + i * 660, 400))
    dp.text((210 + i * 660, 420), n, font=ImageFont.truetype(BOLD, 40), fill=(255, 255, 255))
pv.save(OUT / "thumbnail_preview.png"); print("ok", OUT)
