"""썸네일 4차 — '왜 싼티가 나나' 고친 판 (2026-11-26 사용자: "폰트 등에서 왜이리 싼티가 날까요").

3차(make_thumbs_v3.py)와 같은 구도·문구, 바꾼 것만:
1) 글꼴: 나눔고딕 ExtraBold(본문용) → Noto Sans KR Black(가장 굵은 단계), 자간 좁힘
2) 굵은 검은 외곽선 → 없앰, 부드러운 그림자만
3) 글씨 층 5개 → 2~3개 (작은 이름 · 주어+주장), 가운데 정렬 → 왼쪽 정렬로 묶음
4) 쨍한 원색 노랑·빨강 → 조금 깊은 톤
5) 영상 정지 화면 → 대비·선명도·색 살짝 보정
실행: python projects/20261126-market-deep-dc-funding/02_script/make_thumbs_v4.py
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

import make_thumbs as T

W, H = T.W, T.H
PROJ = T.PROJ
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
    """자간을 좁혀 한 글자씩 + 부드러운 그림자. hl 낱말만 다른 색. anchor: l(왼쪽 기준) / c(가운데 기준)."""
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
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
        cx = x
        for c, a in zip(s, adv):
            ds.text((cx + 2, y + size * 0.06), c, font=f, fill=(0, 0, 0, 190)); cx += a
        sh = sh.filter(ImageFilter.GaussianBlur(size * 0.08))
        im.alpha_composite(sh)
        d = ImageDraw.Draw(im)
    cx = x
    for c, a, col in zip(s, adv, cols):
        d.text((cx, y), c, font=f, fill=col); cx += a
    bb = (x, y + size * 0.15, x + width, y + size * 1.15)
    if main:
        BOXES.append(bb)
    return bb


def grade(im):
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(1.06)
    return im.filter(ImageFilter.UnsharpMask(2, 90, 2))


def left_dark(im, start=0.62, strength=0.9):
    m = Image.new("L", im.size, 0); dm = ImageDraw.Draw(m)
    for i in range(W):
        t = 1 - i / (W * start)
        dm.line([(i, 0), (i, H)], fill=int(255 * strength * max(0, min(1, t * 1.25))))
    return Image.composite(Image.new("RGB", im.size, (10, 10, 13)), im, m)


def bottom_dark(im, start=0.42, strength=0.92):
    m = Image.new("L", im.size, 0); dm = ImageDraw.Draw(m)
    for j in range(im.size[1]):
        dm.line([(0, j), (im.size[0], j)], fill=int(255 * strength * max(0, (j / im.size[1] - start) / (1 - start)) ** 0.8))
    return Image.composite(Image.new("RGB", im.size, (10, 10, 13)), im, m)


def frame(src, crop):
    s = Image.open(TH / src).convert("RGB")
    cw, ch = crop[2] - crop[0], crop[3] - crop[1]
    ext = s.resize((cw, ch)).filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.45))
    ext.paste(s, (-crop[0], -crop[1]))
    return grade(ext.resize((W, H), Image.LANCZOS))


def credit(im, s):
    txt(im, (24, H - 34), s, 17, fill=(175, 177, 185), weight="Medium", track=0, shadow=False, main=False)


def person(src, crop, label, l1, l2, hl, hl_fill, cred):
    im = left_dark(frame(src, crop)).convert("RGBA")
    d = ImageDraw.Draw(im)
    d.rectangle([48, 214, 56, 252], fill=hl_fill)   # 이름 앞 작은 색 막대 (꼬리표 상자 대신)
    txt(im, (70, 206), label, 34, fill=GREY, weight="Bold", track=-0.02, main=False)
    size = 104
    while max(ImageDraw.Draw(im).textlength(s, font=font(size)) for s in (l1, l2)) * 0.95 > 640:   # 얼굴에 닿지 않게
        size -= 4
    txt(im, (44, 270), l1, size, track=-0.05)
    txt(im, (44, 270 + size * 1.18), l2, size, track=-0.05, hl=hl, hl_fill=hl_fill)
    credit(im, cred)
    return im.convert("RGB")


def thumb_a():
    return person("semb_10.jpg", (0, 0, 1250, 703), "아마존 CEO 앤디 재시", "AI 투자,", "몇 년 뒤 돈 된다", "돈 된다", GOLD,
                  "화면: 세마포(Semafor) 인터뷰 2026.11.18")


def thumb_b():
    return person("wg_2.jpg", (-420, 0, 1500, 1080), "파이낸셜타임스 로빈 위글스워스", "빅테크,", "이제 빚으로 짓는다", "빚으로", CRIMSON,
                  "화면: 블룸버그 팟캐스트 2026.11.17")


def thumb_c():
    im = Image.new("RGBA", (W, H), (13, 16, 26, 255))
    txt(im, (W / 2, 70), "빅테크 AI 투자, 누가 맞나", 54, fill=GREY, weight="Bold", track=-0.03, anchor="c")
    for cx, subj, claim, col, who in ((W * 0.27, "AI 투자는", "돈 된다", GOLD, "아마존 CEO 재시"),
                                      (W * 0.73, "빅테크는", "빚 낸다", CRIMSON, "FT 위글스워스")):
        txt(im, (cx, 220), subj, 58, fill=WHITE, weight="Bold", anchor="c")
        txt(im, (cx, 285), claim, 176, fill=col, track=-0.06, anchor="c")
        txt(im, (cx, 540), who, 40, fill=GREY, weight="Bold", anchor="c", main=False)
    ImageDraw.Draw(im).line([(W / 2, 250), (W / 2, 520)], fill=(70, 76, 96), width=3)
    return im.convert("RGB")


def thumb_d():
    half, ext, slant = W // 2, 90, 60
    left = bottom_dark(grade(Image.open(TH / "semb_10.jpg").convert("RGB").crop((470, 40, 1470, 1040)).resize((half + ext, H), Image.LANCZOS)))
    right = bottom_dark(grade(Image.open(TH / "wgb_3.jpg").convert("RGB").crop((380, 0, 1460, 1080)).resize((half + ext, H), Image.LANCZOS)))
    bg = Image.new("RGB", (W, H)); bg.paste(right, (half - ext, 0))
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon([(0, 0), (half + slant, 0), (half - slant, H), (0, H)], fill=255)
    lay = Image.new("RGB", (W, H)); lay.paste(left, (0, 0))
    im = Image.composite(lay, bg, m).convert("RGBA")
    ImageDraw.Draw(im).line([(half + slant, 0), (half - slant, H)], fill=(240, 240, 244), width=4)
    for x0, who, subj, claim, col in ((40, "아마존 CEO 재시", "AI 투자는", "몇 년 뒤 돈 된다", GOLD),
                                      (half + 20, "FT 위글스워스", "빅테크는", "이제 빚으로 짓는다", CRIMSON)):
        size = 70
        while ImageDraw.Draw(im).textlength(claim, font=font(size)) * 0.96 > half - 70:
            size -= 2
        txt(im, (x0, 404), who, 32, fill=GREY, weight="Bold", main=False)
        txt(im, (x0, 452), subj, 58, fill=WHITE)
        txt(im, (x0, 528), claim, size, fill=col, track=-0.05)
    credit(im, "화면: 세마포(Semafor) 2026.11.18 · 블룸버그 팟캐스트 2026.11.17")
    return im.convert("RGB")


if __name__ == "__main__":
    v3 = OUT / "thumbs_v3"; v3.mkdir(exist_ok=True)
    for k in "ABCD":
        p = OUT / f"thumbnail_{k}.png"
        if p.exists() and not (v3 / p.name).exists():
            p.replace(v3 / p.name)
    qa, out = {}, []
    for k, fn in (("A", thumb_a), ("B", thumb_b), ("C", thumb_c), ("D", thumb_d)):
        BOXES.clear()
        im = fn(); im.save(OUT / f"thumbnail_{k}.png"); out.append(im)
        small = min((b[3] - b[1]) for b in BOXES) * 168 / W
        clash = [b for b in BOXES if b[2] > W - 200 and b[3] > H - 90]
        qa[k] = {"timestamp_overlap": bool(clash), "smallest_text_px_at_168w": round(small, 1), "ok": not clash and small >= 6,
                 "note": "4차: Noto Sans KR Black·외곽선 없음·층 줄임(make_thumbs_v4.py) — 작은 이름 줄은 측정에서 뺌"}
    (OUT / "thumbnail_qa.json").write_text(json.dumps(qa, ensure_ascii=False, indent=1), encoding="utf-8")
    print(qa)
    # 전·후 비교: 왼쪽 3차, 오른쪽 4차
    cmp = Image.new("RGB", (1290, 4 * 370 + 10), (30, 30, 32))
    for i, (k, im) in enumerate(zip("ABCD", out)):
        cmp.paste(Image.open(v3 / f"thumbnail_{k}.png").resize((640, 360)), (0, 10 + i * 370))
        cmp.paste(im.resize((640, 360)), (650, 10 + i * 370))
    cmp.save(OUT / "thumbnail_v3_vs_v4.png")
