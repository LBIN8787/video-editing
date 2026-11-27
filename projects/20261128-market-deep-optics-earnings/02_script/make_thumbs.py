"""광학·연결 실적 앞 썸네일 — 확정 스타일(다모다란 편 make_thumbs.py 그대로: Noto Sans KR Black·외곽선 없음·작은 이름 + 주어 붙은 주장 두 줄·왼쪽 정렬).
원본 화면: Marvell 공식(CNBC Squawk 11.02) 머피, CNBC(11.06) 헐스턴 — 방송 자막 띠·로고는 잘라 냄.
실행: python projects/20261128-market-deep-optics-earnings/02_script/make_thumbs.py
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H = 1280, 720
PROJ = Path(__file__).resolve().parent.parent
TH = PROJ / "04_assets" / "thumb"
OUT = PROJ / "05_edit"
NOTO = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
GOLD, CRIMSON, WHITE, GREY = (246, 196, 38), (228, 62, 52), (250, 250, 250), (200, 202, 210)
BOXES = []


def font(size, weight="Black"):
    f = ImageFont.truetype(NOTO, size)
    f.set_variation_by_name(weight)
    return f


def txt(im, xy, s, size, fill=WHITE, weight="Black", track=-0.04, hl=None, hl_fill=GOLD, shadow=True, main=True, anchor="l"):
    f = font(size, weight)
    d = ImageDraw.Draw(im)
    adv = [d.textlength(c, font=f) + size * track for c in s]
    width = sum(adv) - size * track
    x, y = xy
    if anchor == "c":
        x -= width / 2
    hs = s.index(hl) if hl and hl in s else -1
    cols = [hl_fill if hs >= 0 and hs <= i < hs + len(hl) else fill for i in range(len(s))]
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ds = ImageDraw.Draw(sh)
        cx = x
        for c, a in zip(s, adv):
            ds.text((cx + 2, y + size * 0.06), c, font=f, fill=(0, 0, 0, 190))
            cx += a
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(size * 0.08)))
        d = ImageDraw.Draw(im)
    cx = x
    for c, a, col in zip(s, adv, cols):
        d.text((cx, y), c, font=f, fill=col)
        cx += a
    bb = (x, y + size * 0.15, x + width, y + size * 1.15)
    if main:
        BOXES.append(bb)
    return bb


def width_of(s, size, track=-0.05):
    f = font(size)
    d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    return sum(d.textlength(c, font=f) + size * track for c in s) - size * track


def grade(im):
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(1.06)
    return im.filter(ImageFilter.UnsharpMask(2, 90, 2))


def left_dark(im, start=0.62, strength=0.9):
    m = Image.new("L", im.size, 0)
    dm = ImageDraw.Draw(m)
    for i in range(W):
        t = 1 - i / (W * start)
        dm.line([(i, 0), (i, H)], fill=int(255 * strength * max(0, min(1, t * 1.25))))
    return Image.composite(Image.new("RGB", im.size, (10, 10, 13)), im, m)


def bottom_dark(im, start=0.42, strength=0.92):
    m = Image.new("L", im.size, 0)
    dm = ImageDraw.Draw(m)
    for j in range(im.size[1]):
        dm.line([(0, j), (im.size[0], j)], fill=int(255 * strength * max(0, (j / im.size[1] - start) / (1 - start)) ** 0.8))
    return Image.composite(Image.new("RGB", im.size, (10, 10, 13)), im, m)


def frame(src, crop):
    s = Image.open(TH / src).convert("RGB")
    if src.startswith("pg_"):   # 원본 화면 오른쪽 위 방송 로고는 흐리게 (남의 로고를 썸네일에 크게 싣지 않음)
        box = (1080, 0, 1280, 70)
        s.paste(s.crop(box).filter(ImageFilter.GaussianBlur(14)), box[:2])
    cw, ch = crop[2] - crop[0], crop[3] - crop[1]
    ext = s.resize((cw, ch)).filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.45))
    ext.paste(s, (-crop[0], -crop[1]))
    return grade(ext.resize((W, H), Image.LANCZOS))


def credit(im, s):
    txt(im, (24, H - 34), s, 17, fill=(175, 177, 185), weight="Medium", track=0, shadow=False, main=False)


def region(src, box):
    """원본 화면의 한 부분(방송 띠 위)을 높이 720 으로 키워 오른쪽에 둔다"""
    s = Image.open(TH / src).convert("RGB").crop(box)
    w = int(s.width * H / s.height)
    s = grade(s.resize((w, H), Image.LANCZOS))
    bg = s.resize((W, H)).filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.4))
    bg.paste(s, (W - w, 0))
    return bg


def person(src, box, label, l1, l2, hl, hl_fill, cred, maxw=700):
    im = left_dark(region(src, box), start=0.66).convert("RGBA")
    d = ImageDraw.Draw(im)
    d.rectangle([48, 214, 56, 252], fill=hl_fill)
    txt(im, (70, 206), label, 34, fill=GREY, weight="Bold", track=-0.02, main=False)
    size = 108
    while max(width_of(s, size) for s in (l1, l2)) > maxw:
        size -= 4
    txt(im, (44, 270), l1, size, track=-0.05)
    txt(im, (44, 270 + size * 1.18), l2, size, track=-0.05, hl=hl, hl_fill=hl_fill)
    credit(im, cred)
    return im.convert("RGB")


SQ = "화면: Marvell 공식(CNBC) 2026.11.02"
PL = "화면: CNBC 2026.11.06"
M_BOX = ("loT1_50.jpg", (40, 40, 640, 500))
H_BOX = ("zbp8_85.jpg", (40, 40, 512, 500))


def thumb_a():
    return person(*M_BOX, "마벨 CEO 맷 머피", "광학이 데이터센터", "안으로 들어온다", "안으로", GOLD, SQ)


def thumb_b():
    return person(*H_BOX, "루멘텀 CEO 마이클 헐스턴", "수요는 넘친다는데", "주가는 왜 급락?", "급락", CRIMSON, PL)


def thumb_c():
    half, slant = W // 2, 60
    def side(src, box):
        s = Image.open(TH / src).convert("RGB").crop(box)
        s = s.resize((int(s.width * H / s.height), H), Image.LANCZOS)
        x0 = max(0, (s.width - (half + 90)) // 2)
        return bottom_dark(grade(s.crop((x0, 0, x0 + half + 90, H))))
    left, right = side(*M_BOX), side(*H_BOX)
    bg = Image.new("RGB", (W, H))
    bg.paste(right, (half - 90, 0))
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([(0, 0), (half + slant, 0), (half - slant, H), (0, H)], fill=255)
    lay = Image.new("RGB", (W, H))
    lay.paste(left, (0, 0))
    im = Image.composite(lay, bg, m).convert("RGBA")
    ImageDraw.Draw(im).line([(half + slant, 0), (half - slant, H)], fill=(240, 240, 244), width=4)
    for x0, who, subj, claim, col in ((40, "마벨 머피", "광학은", "데이터센터 안으로", GOLD),
                                      (half + 20, "루멘텀 헐스턴", "수요는", "이보다 강할 수 없다", CRIMSON)):
        size = 66
        while width_of(claim, size) > half - 80:
            size -= 2
        txt(im, (x0, 404), who, 32, fill=GREY, weight="Bold", main=False)
        txt(im, (x0, 452), subj, 58, fill=WHITE)
        txt(im, (x0, 528), claim, size, fill=col, track=-0.05)
    credit(im, f"{SQ} · {PL}")
    return im.convert("RGB")


if __name__ == "__main__":
    qa, out = {}, []
    for k, fn in (("A", thumb_a), ("B", thumb_b), ("C", thumb_c)):
        BOXES.clear()
        im = fn()
        im.save(OUT / f"thumbnail_{k}.png")
        out.append(im)
        small = min((b[3] - b[1]) for b in BOXES) * 168 / W
        clash = [b for b in BOXES if b[2] > W - 200 and b[3] > H - 90]
        qa[k] = {"timestamp_overlap": bool(clash), "smallest_text_px_at_168w": round(small, 1), "ok": not clash and small >= 6,
                 "note": "확정 스타일(Noto Black·외곽선 없음·주어+주장) — make_thumbs.py"}
    (OUT / "thumbnail_qa.json").write_text(json.dumps(qa, ensure_ascii=False, indent=1), encoding="utf-8")
    sheet = Image.new("RGB", (660 + 180, 3 * 370 + 10), (30, 30, 32))
    for i, im in enumerate(out):
        sheet.paste(im.resize((640, 360)), (0, 10 + i * 370))
        sheet.paste(im.resize((168, 94)), (660, 10 + i * 370))
    sheet.save(OUT / "thumbnail_preview.png")
    print(qa)
