"""다모다란·앤트로픽 썸네일 다시 (2026-11-27 사용자: "기존 썸네일 메뉴얼을 확인해주세요 인지부하 없이 직관적으로 무얼 말하려는지 명확히").

확정 스타일(11-26 4차, 20261126-market-deep-dc-funding/02_script/make_thumbs_v4.py)을 그대로:
Noto Sans KR Black · 외곽선 없음(그림자만) · 작은 이름 한 줄 + 주어 붙은 주장 두 줄 · 왼쪽 정렬 ·
빨간 꼬리표·이름표 상자·VS 딱지 없음 · 깊은 금색/진홍 · 실제 인터뷰 화면 꽉, 얼굴 오른쪽.
이전 판의 문제: 주어(앤트로픽)가 없어 '무엇이 무너지나'를 영상을 봐야 알았음, 빨간 꼬리표·이름표 상자·VS.
실행: python projects/20261127-market-deep-anthropic-damodaran/02_script/make_thumbs.py
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


def person(src, crop, label, l1, l2, hl, hl_fill, cred, maxw=660):
    im = left_dark(frame(src, crop)).convert("RGBA")
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


PG = "화면: Prof G Markets 2026.11.20"
CW = "화면: CNBC 2026.11.20"


def thumb_a():   # 인물·경고: 누가 · 무엇이 · 어떻게 — 한 번에
    return person("pg_2093.jpg", (-330, 0, 950, 720), "가치평가 대가 다모다란", "앤트로픽, 매출 안 오면", "다 무너진다", "무너진다", CRIMSON, PG, maxw=720)


def thumb_b():   # 숫자: 무엇이 필요한가
    return person("pg_2200.jpg", (-330, 0, 950, 720), "가치평가 대가 다모다란", "앤트로픽 주가 버티려면", "매출 1조 달러", "1조 달러", GOLD, PG, maxw=720)


def thumb_c():   # 두 사람 맞대기 (사진 반반, 각자 주어+주장)
    half, ext, slant = W // 2, 90, 60
    left = bottom_dark(grade(Image.open(TH / "pg_2093.jpg").convert("RGB").crop((340, 0, 1060, 720)).resize((half + ext, H), Image.LANCZOS)))
    right = bottom_dark(grade(Image.open(TH / "cw_36.jpg").convert("RGB").crop((40, 25, 525, 510)).resize((half + ext, H), Image.LANCZOS)))
    bg = Image.new("RGB", (W, H))
    bg.paste(right, (half - ext, 0))
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([(0, 0), (half + slant, 0), (half - slant, H), (0, H)], fill=255)
    lay = Image.new("RGB", (W, H))
    lay.paste(left, (0, 0))
    im = Image.composite(lay, bg, m).convert("RGBA")
    ImageDraw.Draw(im).line([(half + slant, 0), (half - slant, H)], fill=(240, 240, 244), width=4)
    for x0, who, subj, claim, col in ((40, "다모다란", "앤트로픽은", "매출 안 오면 무너진다", CRIMSON),
                                      (half + 20, "캐시 우드", "앤트로픽", "확신 커졌다, 더 산다", GOLD)):
        size = 66
        while width_of(claim, size) > half - 80:
            size -= 2
        txt(im, (x0, 404), who, 32, fill=GREY, weight="Bold", main=False)
        txt(im, (x0, 452), subj, 58, fill=WHITE)
        txt(im, (x0, 528), claim, size, fill=col, track=-0.05)
    credit(im, f"{PG} · {CW}")
    return im.convert("RGB")


if __name__ == "__main__":
    old = OUT / "thumbs_v1"
    old.mkdir(exist_ok=True)
    for k in "ABC":
        p = OUT / f"thumbnail_{k}.png"
        if p.exists() and not (old / p.name).exists():
            p.replace(old / p.name)
    qa, out = {}, []
    for k, fn in (("A", thumb_a), ("B", thumb_b), ("C", thumb_c)):
        BOXES.clear()
        im = fn()
        im.save(OUT / f"thumbnail_{k}.png")
        out.append(im)
        small = min((b[3] - b[1]) for b in BOXES) * 168 / W
        clash = [b for b in BOXES if b[2] > W - 200 and b[3] > H - 90]
        qa[k] = {"timestamp_overlap": bool(clash), "smallest_text_px_at_168w": round(small, 1), "ok": not clash and small >= 6,
                 "note": "2판: 확정 스타일(Noto Black·외곽선 없음·주어+주장) — make_thumbs.py"}
    (OUT / "thumbnail_qa.json").write_text(json.dumps(qa, ensure_ascii=False, indent=1), encoding="utf-8")
    sheet = Image.new("RGB", (1290 + 340, 3 * 370 + 10), (30, 30, 32))
    for i, im in enumerate(out):
        sheet.paste(im.resize((640, 360)), (0, 10 + i * 370))
        sheet.paste(im.resize((168, 94)), (660, 10 + i * 370))
        sheet.paste(Image.open(old / f"thumbnail_{'ABC'[i]}.png").resize((640, 360)), (850, 10 + i * 370))
    sheet.save(OUT / "thumbnail_preview.png")
    print(qa)
