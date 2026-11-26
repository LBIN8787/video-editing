"""썸네일 A/B/C v3 — 문구는 v2(같은 주제 인기 영상 비교: 이름 + 의혹을 바로), 모양은 채널 공통 확정 스타일(2026-11-26):
Noto Sans KR Black · 굵은 외곽선 없음(부드러운 그림자) · 작은 이름 한 줄 + 주장 두 줄 왼쪽 정렬 · 이름표 상자 없음 · 깊은 금색/진홍.
그림은 본편과 같은 재현 그림(A안, Codex). 결과는 Drive 영상 폴더 thumbs/."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

EP = Path(r"G:\내 드라이브\ytflow\영상\20261126-history-sohyeon")
OUT = EP / "thumbs"; OUT.mkdir(exist_ok=True)
W, H = 1280, 720
NOTO = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
GOLD, CRIMSON, WHITE, GREY = (246, 196, 38), (228, 62, 52), (250, 250, 250), (205, 205, 210)


def font(size, weight="Black"):
    f = ImageFont.truetype(NOTO, size); f.set_variation_by_name(weight); return f


def txt(im, xy, s, size, fill=WHITE, hl=None, hl_fill=GOLD, weight="Black", track=-0.045):
    f = font(size, weight); d = ImageDraw.Draw(im)
    adv = [d.textlength(c, font=f) + size * track for c in s]; x, y = xy
    hs = s.index(hl) if hl and hl in s else -1
    cols = [hl_fill if 0 <= hs <= i < hs + len(hl) else fill for i in range(len(s))]
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh); cx = x
    for c, a in zip(s, adv): ds.text((cx + 2, y + size * .06), c, font=f, fill=(0, 0, 0, 200)); cx += a
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(size * .08))); d = ImageDraw.Draw(im); cx = x
    for c, a, col in zip(s, adv, cols): d.text((cx, y), c, font=f, fill=col); cx += a
    return sum(adv)


def crop(img, cx, cy, cw, bright=1.0, size=(W, H)):
    im = Image.open(EP / img).convert("RGB"); w, h = im.size; asp = size[1] / size[0]
    box = (int(cx * w), int(cy * h), int((cx + cw) * w), int(cy * h + cw * w * asp))
    im = ImageEnhance.Brightness(im.crop(box).resize(size, Image.LANCZOS)).enhance(bright)
    im = ImageEnhance.Contrast(im).enhance(1.1)
    return im.filter(ImageFilter.UnsharpMask(2, 80, 2))


def left_dark(im, start=.62, k=.9):
    m = Image.new("L", (W, 1))
    for i in range(W): m.putpixel((i, 0), int(255 * k * max(0, min(1, (1 - i / (W * start)) * 1.25))))
    return Image.composite(Image.new("RGB", (W, H), (10, 10, 13)), im, m.resize((W, H)))


def bottom_dark(im, start=.45, k=.9):
    m = Image.new("L", (1, H))
    for j in range(H): m.putpixel((0, j), int(255 * k * max(0, (j / H - start) / (1 - start)) ** .8))
    return Image.composite(Image.new("RGB", (W, H), (10, 10, 13)), im, m.resize((W, H)))


def layout(im, name, l1, l2, hl1=None, hl2=None, c1=GOLD, c2=GOLD, size=104):
    im = im.convert("RGBA"); y = H - 70 - 2 * int(size * 1.08) - 52
    txt(im, (64, y), name, 40, fill=GREY, weight="Bold", track=-.02)
    txt(im, (60, y + 56), l1, size, hl=hl1, hl_fill=c1)
    txt(im, (60, y + 56 + int(size * 1.08)), l2, size, hl=hl2, hl_fill=c2)
    return im.convert("RGB")


# A — 아버지 인조(왼쪽) · 아들 소현세자(오른쪽) 합친 판
a = Image.new("RGB", (W, H))
king = crop("art/N11_injo.png", .64, .25, .11, 2.1, size=(560, H)); prince = crop("samples/A3_observatory.png", .1, .0, .42, 1.0, size=(760, H))
a.paste(king, (0, 0)); a.paste(prince, (520, 0))
m = Image.linear_gradient("L").rotate(90).resize((120, H)); a.paste(king.crop((440, 0, 560, H)), (440, 0), m)
a = bottom_dark(a, .38, .95)
layout(a, "소현세자 · 1645", "아버지 인조가", "아들을 독살했나?", hl2="독살", c2=CRIMSON).save(OUT / "thumbnail_A.png")

# B — 병상의 세자
b = bottom_dark(left_dark(crop("art/N6_physician.png", .2, .05, .62, 1.3), .55, .75), .4, .9)
layout(b, "소현세자 · 1645", "귀국 두 달 만에", "갑자기 죽은 세자", hl1="두 달").save(OUT / "thumbnail_B.png")

# C — 실제 실록 사진 + 세자
c = Image.new("RGB", (W, H), (12, 12, 15))
r = Image.open(EP / "real" / "R_sillok.jpg").convert("RGB"); r.thumbnail((700, 720)); c.paste(ImageEnhance.Brightness(r).enhance(.6), (0, (H - r.height) // 2))
c.paste(crop("samples/A3_observatory.png", .12, .02, .34, .95, size=(600, H)), (680, 0))
c = bottom_dark(c, .4, .95)
layout(c, "인조실록이 남긴 죽음", "누가 소현세자를", "죽였나?", hl1="소현세자", hl2="죽였나?", c2=CRIMSON).save(OUT / "thumbnail_C.png")

pv = Image.new("RGB", (3 * 660 + 40, 520), (24, 24, 24)); dp = ImageDraw.Draw(pv)
for i, n in enumerate("ABC"):
    im = Image.open(OUT / f"thumbnail_{n}.png"); pv.paste(im.resize((640, 360)), (20 + i * 660, 20)); pv.paste(im.resize((168, 94)), (20 + i * 660, 400))
    dp.text((210 + i * 660, 420), n, font=font(40), fill=(255, 255, 255))
pv.save(OUT / "thumbnail_preview.png"); print("ok")
