"""썸네일 3차 — 아이스먼 편(20261126-market-deep-eisman-capex) 기준으로 다시 (2026-11-26 사용자: "아이스먼 썸네일을 보고 썸네일 다시 제작해주세요 그 기준에 따라서요").

아이스먼 편 기준:
- A·B: 실제 인터뷰 화면을 꽉 채움, 얼굴은 오른쪽 크게, 왼쪽 어두운 자리에 빨간 꼬리표(누가) + 큰 흰 글씨 두 줄(그 사람의 실제 말, 따옴표), 핵심 낱말만 노랑
  + 아래 이름표(빨간 막대 + 이름 + 한 줄 소개), 위 가운데 작은 '화면: … (날짜)'
- C: 글자만 — 위 한 줄 질문, 가운데 노랑 vs 빨강 두 낱말 맞대기, 아래 두 사람 이름
따옴표 안은 실제 말의 번역만: 재시(세마포 11.18) "headwinds on your short-term free cash flow … gets very good",
위글스워스(블룸버그 11.17) "AI boom became debt-financed".
실행: python projects/20261126-market-deep-dc-funding/02_script/make_thumbs_v3.py
"""
import json

from PIL import Image, ImageDraw, ImageFilter

import make_thumbs as T
from make_thumbs import BOLD, INK, RED, WHITE, YEL, H, W, font

PROJ = T.PROJ
TH = PROJ / "04_assets" / "thumb"
NAVY = (14, 20, 40)


def left_dark(im, start=0.62, strength=0.92):
    """왼쪽을 어둡게 — 글씨 자리 (얼굴이 있는 오른쪽은 그대로)."""
    m = Image.new("L", im.size, 0); dm = ImageDraw.Draw(m)
    for i in range(W):
        t = 1 - i / (W * start)
        dm.line([(i, 0), (i, H)], fill=int(255 * strength * max(0, min(1, t * 1.25))))
    return Image.composite(Image.new("RGB", im.size, (12, 12, 16)), im, m)


def line2(d, x, y, s, f, hl=None):
    T.text_line(d, (x, y), s, f, hl=hl, stroke=5)


def nameplate(d, x, y, name, role):
    fn, fr = font(BOLD, 42), font(BOLD, 30)
    w = max(d.textlength(name, font=fn), d.textlength(role, font=fr)) + 44
    d.rounded_rectangle([x, y, x + w, y + 112], radius=10, fill=(14, 14, 18))
    d.rectangle([x, y, x + 8, y + 112], fill=RED)
    d.text((x + 26, y + 10), name, font=fn, fill=WHITE)
    d.text((x + 26, y + 64), role, font=fr, fill=(225, 225, 230))
    T.BOXES.append((x, y, x + w, y + 112))


def credit(d, s):
    f = font(BOLD, 18)
    d.text((W // 2 - d.textlength(s, font=f) // 2 + 120, 10), s, font=f, fill=(235, 235, 240), stroke_width=2, stroke_fill=INK)


def person(src, crop, who_tag, l1, l2, hl, name, role, cred):
    src_im = Image.open(TH / src).convert("RGB")
    cw, ch = crop[2] - crop[0], crop[3] - crop[1]
    ext = src_im.resize((cw, ch)).filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.45))   # 화면 밖은 흐린 같은 장면으로 (검은 띠 대신)
    ext.paste(src_im, (-crop[0], -crop[1]))
    fr = ext.resize((W, H), Image.LANCZOS)
    bg = left_dark(fr)
    d = ImageDraw.Draw(bg)
    size = 96
    while max(ImageDraw.Draw(bg).textlength(s, font=font(BOLD, size)) for s in (l1, l2)) > 600:
        size -= 4
    f = font(BOLD, size)
    T.tag(d, (44, 150), who_tag, font(BOLD, 36))
    line2(d, 44, 228, l1, f, hl)
    line2(d, 44, 228 + int(size * 1.25), l2, f, hl)
    nameplate(d, 620, 540, name, role)
    credit(d, cred)
    return bg


def thumb_a():   # 세마포 11.18 — 정면을 보며 말하는 프레임, 재시가 오른쪽에 오게 왼쪽 0~1250 만
    return person("semb_10.jpg", (0, 0, 1250, 703), "아마존 CEO 재시",
                  "\"AI 투자, 당장 현금 줄어도", "몇 년 뒤 돈 된다\"", "돈 된다",   # 원문: headwinds on short-term free cash flow … free cash flow and ROIC get very good
                  "앤디 재시", "아마존 CEO", "화면: 세마포(Semafor) 인터뷰 (2026.11.18)")


def thumb_b():   # 블룸버그 팟캐스트 11.17 — 자막 띠는 잘라 낸 클립에서
    return person("wg_2.jpg", (-420, 0, 1500, 1080), "FT 위글스워스",
                  "\"빅테크, 번 돈은 바닥", "이제 빚으로 짓는다\"", "빚으로",   # 원문: the AI boom became debt-financed … this year they kind of tapped out … bond markets
                  "로빈 위글스워스", "파이낸셜타임스 칼럼니스트", "화면: 블룸버그 팟캐스트 (2026.11.17)")


def thumb_c():
    bg = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(bg)
    f1 = font(BOLD, 92)
    s = "빅테크 AI 투자, 누가 맞나"
    T.text_line(d, (W // 2 - d.textlength(s, font=f1) // 2, 60), s, f1, hl="누가", stroke=5)
    a, b = "돈 된다", "빚 낸다"
    fv = font(BOLD, 44); size = 210
    while True:   # 두 낱말 + vs 가 화면 폭(양쪽 50) 안에 들어올 때까지 줄임
        fb = font(BOLD, size)
        wa, wb, wv = d.textlength(a, font=fb), d.textlength(b, font=fb), d.textlength("vs", font=fv)
        if wa + wb + wv + 40 + 20 <= W - 100:
            break
        size -= 6
    x = (W - (wa + wv + wb + 40)) // 2; y = 350 - size // 2
    d.text((x, y), a, font=fb, fill=YEL, stroke_width=10, stroke_fill=INK); T.BOXES.append(d.textbbox((x, y), a, font=fb))
    lx = x + wa + 20 + wv / 2
    d.line([(lx, y + 30), (lx, y + size + 10)], fill=(120, 126, 150), width=4)   # vs 글자 대신 가는 선 (2026-11-26 사용자: vs 가 저퀄리티)
    xb = x + wa + wv + 40
    d.text((xb, y), b, font=fb, fill=RED, stroke_width=10, stroke_fill=INK); T.BOXES.append(d.textbbox((xb, y), b, font=fb))
    fs = font(BOLD, 56)
    for s2, cx in (("AI 투자는", x + wa / 2), ("빅테크는", xb + wb / 2)):   # 주어 (2026-11-26 사용자: 주어를 붙이세요)
        d.text((cx - d.textlength(s2, font=fs) / 2, y - 60), s2, font=fs, fill=WHITE)
        T.BOXES.append(d.textbbox((cx - d.textlength(s2, font=fs) / 2, y - 60), s2, font=fs))
    fn = font(BOLD, 50)
    for s2, cx in (("아마존 재시", x + wa / 2), ("FT 위글스워스", xb + wb / 2)):
        d.text((cx - d.textlength(s2, font=fn) / 2, 560), s2, font=fn, fill=WHITE)
        T.BOXES.append(d.textbbox((cx - d.textlength(s2, font=fn) / 2, 560), s2, font=fn))
    return bg


def thumb_d():
    """두 의견 맞대기 — 비스듬히 나눈 두 얼굴, 가운데 가는 사선 하나 (VS 딱지 없음: 2026-11-26 사용자 '저 vs 이런게 너무 저퀄리티')."""
    half, ext, slant = W // 2, 90, 70
    bg = Image.new("RGB", (W, H), (10, 10, 14))
    shade = lambda im: Image.composite(Image.new("RGB", im.size, (8, 8, 12)), im, _bottom_mask(im.size))
    left = shade(Image.open(TH / "semb_10.jpg").convert("RGB").crop((470, 40, 1470, 1040)).resize((half + ext, H), Image.LANCZOS))
    right = shade(Image.open(TH / "wgb_3.jpg").convert("RGB").crop((380, 0, 1460, 1080)).resize((half + ext, H), Image.LANCZOS))
    bg.paste(right, (half - ext, 0))
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([(0, 0), (half + slant, 0), (half - slant, H), (0, H)], fill=255)
    lay = Image.new("RGB", (W, H)); lay.paste(left, (0, 0))
    bg = Image.composite(lay, bg, m)
    d = ImageDraw.Draw(bg)
    d.line([(half + slant, 0), (half - slant, H)], fill=(245, 245, 248), width=5)
    ft = font(BOLD, 46); s = "빅테크 AI 투자, 누가 맞나"
    T.text_line(d, (half - d.textlength(s, font=ft) // 2, 22), s, ft, hl="누가", stroke=6)
    fs = font(BOLD, 48)
    csz = 76
    while max(d.textlength(c, font=font(BOLD, csz)) for c in ("몇 년 뒤 돈 된다", "이제 빚으로 짓는다")) > half - 90:
        csz -= 2
    fc = font(BOLD, csz)
    for cx, who, subj, claim, col, src in ((half // 2 - 30, "아마존 CEO 재시", "AI 투자는", "몇 년 뒤 돈 된다", YEL, "\"당장 현금은 줄어도\""),
                                          (half + half // 2 + 10, "FT 위글스워스", "빅테크는", "이제 빚으로 짓는다", RED, "\"번 돈은 바닥\"")):
        fw = font(BOLD, 46)
        d.text((cx - d.textlength(who, font=fw) / 2, 388), who, font=fw, fill=(230, 230, 235), stroke_width=3, stroke_fill=INK)
        T.BOXES.append(d.textbbox((cx - d.textlength(who, font=fw) / 2, 388), who, font=fw))
        for s2, f2, c2, yy in ((subj, fs, WHITE, 454), (claim, fc, col, 514)):
            w2 = d.textlength(s2, font=f2)
            d.text((cx - w2 / 2, yy), s2, font=f2, fill=c2, stroke_width=6, stroke_fill=INK)
            T.BOXES.append(d.textbbox((cx - w2 / 2, yy), s2, font=f2, stroke_width=6))
        fn = font(BOLD, 26)
        d.text((cx - d.textlength(src, font=fn) / 2, 616), src, font=fn, fill=(215, 215, 220))
    d.text((14, H - 26), "화면: 세마포(Semafor) 2026.11.18 · 블룸버그 팟캐스트 2026.11.17", font=font(BOLD, 16), fill=(190, 190, 195))
    return bg


def _bottom_mask(size):
    m = Image.new("L", size, 0); dm = ImageDraw.Draw(m)
    for j in range(size[1]):
        dm.line([(0, j), (size[0], j)], fill=int(255 * 0.93 * max(0, (j / size[1] - 0.4) / 0.6) ** 0.8))
    return m


if __name__ == "__main__":
    old = T.OUT / "thumbs_v2"; old.mkdir(exist_ok=True)
    for k in "ABCDEF":
        p = T.OUT / f"thumbnail_{k}.png"
        if p.exists() and not (old / p.name).exists():
            p.replace(old / p.name)
    qa, out = {}, []
    for k, fn in (("A", thumb_a), ("B", thumb_b), ("C", thumb_c), ("D", thumb_d)):
        T.BOXES.clear()
        im = fn(); im.save(T.OUT / f"thumbnail_{k}.png"); out.append(im)
        small = min((b[3] - b[1]) for b in T.BOXES) * 168 / W
        clash = [b for b in T.BOXES if b[2] > W - 200 and b[3] > H - 90]
        qa[k] = {"timestamp_overlap": bool(clash), "smallest_text_px_at_168w": round(small, 1), "ok": not clash and small >= 6,
                 "note": "3차: 아이스먼 편 기준(make_thumbs_v3.py)"}
    (T.OUT / "thumbnail_qa.json").write_text(json.dumps(qa, ensure_ascii=False, indent=1), encoding="utf-8")
    print(qa)
    sheet = Image.new("RGB", (W + 380, H * 4 + 60), (28, 28, 30))
    for i, im in enumerate(out):
        sheet.paste(im, (0, i * (H + 20)))
        sheet.paste(im.resize((360, 202)), (W + 10, i * (H + 20)))
        sheet.paste(im.resize((168, 94)), (W + 10, i * (H + 20) + 220))
    sheet.save(T.OUT / "thumbnail_preview.png")
