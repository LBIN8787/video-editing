"""썸네일 A/B/C 합성 (2026-11-26 사용자: "인물사진을 단순히 이어붙이는게 아니라 합성하거나 좀 바꿔서 매번 똑같은 구도는 아니되 영상 내용을 잘 설명 할 수 있도록").

재료 (04_assets/thumb/, 미디어라 커밋 안 함 — 다시 만드는 법은 아래):
- bg_tower.png · bg_vault.png · bg_campus.png — Codex CLI $imagegen(ChatGPT 구독)으로 생성, 프롬프트는 gen.sh 호출 기록(REPORT.md). 실제 로고·얼굴 없음
- jassy_2010.jpg — 위키미디어 공용 'Andy Jassy in 2010.jpg' (CC BY 2.0) → jassy_cut.png (OpenCV GrabCut 누끼, scratchpad cutout.py)
세 장은 클릭 동기와 구도를 다르게 (14 §4): A 인물·발언(인물 왼쪽, 장면에 녹임) · B 구조(사람 없음, 돈의 흐름 그림) · C 숫자 맞대기(오른쪽 막대).
실행: python projects/20261126-market-deep-dc-funding/02_script/make_thumbs.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
SRC = PROJ / "04_assets" / "thumb"
OUT = PROJ / "05_edit"
FONTS = PROJ.parents[1] / "ytflow" / "assets" / "fonts"
HEAD = str(FONTS / "BlackHanSans-Regular.ttf")
BOLD = str(FONTS / "NanumGothic-ExtraBold.ttf")
W, H = 1280, 720
YEL, RED, WHITE, INK = (255, 214, 0), (235, 52, 52), (255, 255, 255), (12, 14, 20)


def font(p, s):
    return ImageFont.truetype(p, s)


def cover(im, w=W, h=H, focus=(0.5, 0.5)):
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1])
    return im.crop((x, y, x + w, y + h))


def text_line(d, xy, s, f, fill=WHITE, hl=None, stroke=8, anchor="la"):
    """한 줄을 쓰되 hl 낱말만 노랑. 굵은 검은 테두리(휴대폰 목록에서 읽히게)."""
    x, y = xy
    if anchor == "ra":
        x -= d.textlength(s, font=f)
    parts = [(s, fill)] if not hl or hl not in s else [(s[:s.index(hl)], fill), (hl, YEL), (s[s.index(hl) + len(hl):], fill)]
    for t, c in parts:
        if t:
            d.text((x, y), t, font=f, fill=c, stroke_width=stroke, stroke_fill=INK)
            x += d.textlength(t, font=f)


def tag(d, xy, s, f, bg=RED, fg=WHITE, pad=(16, 8)):
    x, y = xy
    tw = d.textlength(s, font=f); bb = f.getbbox(s)
    d.rounded_rectangle([x, y, x + tw + pad[0] * 2, y + (bb[3] - bb[1]) + pad[1] * 2 + 6], radius=8, fill=bg)
    d.text((x + pad[0], y + pad[1] - bb[1] + 3), s, font=f, fill=fg)


def vignette(im, strength=0.55, side=None):
    """가장자리·한쪽을 어둡게 — 글씨 자리."""
    m = Image.new("L", im.size, 0); dm = ImageDraw.Draw(m)
    if side == "right":
        for i in range(W):
            dm.line([(i, 0), (i, H)], fill=int(255 * strength * max(0, (i - W * 0.45) / (W * 0.55))))
    elif side == "top":
        for j in range(H):
            dm.line([(0, j), (W, j)], fill=int(255 * strength * max(0, 1 - j / (H * 0.55))))
    else:
        dm.ellipse([-W * 0.25, -H * 0.3, W * 1.25, H * 1.3], fill=0); m = Image.eval(m, lambda v: 255 - v)
        m = m.filter(ImageFilter.GaussianBlur(120)); m = Image.eval(m, lambda v: int(v * strength))
    dark = Image.new("RGB", im.size, (5, 7, 12))
    return Image.composite(dark, im, m)


def person_into(bg, cut, box_h, x, y_bottom, grade=(1.0, 1.0, 1.0), rim=(255, 170, 80)):
    """누끼 인물을 장면에 녹이기: 장면 색으로 살짝 보정 + 뒤쪽 테두리 빛(조명 방향) + 바닥 그림자."""
    r = box_h / cut.height
    p = cut.resize((round(cut.width * r), box_h), Image.LANCZOS)
    rgb = p.convert("RGB"); a = p.getchannel("A")
    rgb = ImageEnhance.Contrast(rgb).enhance(1.08)
    rr, gg, bb = rgb.split()
    rgb = Image.merge("RGB", (rr.point(lambda v: min(255, int(v * grade[0]))), gg.point(lambda v: min(255, int(v * grade[1]))), bb.point(lambda v: min(255, int(v * grade[2])))))
    glow = Image.new("RGBA", p.size, rim + (0,)); ga = a.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(10))
    glow.putalpha(ga.point(lambda v: int(v * 0.55)))
    y = y_bottom - p.height
    bg.alpha_composite(glow, (x + 6, y - 4))
    pp = rgb.convert("RGBA"); pp.putalpha(a)
    bg.alpha_composite(pp, (x, y))
    return bg


def thumb_a():
    """A 인물·발언 — 재시를 빚 서류 더미 옆 공사장 장면에 녹여 넣고, 그의 말을 따옴표로."""
    bg = cover(Image.open(SRC / "bg_tower.png").convert("RGB"), focus=(0.65, 0.5))
    bg = vignette(bg, 0.5).convert("RGBA")
    cut = Image.open(SRC / "jassy_cut.png").convert("RGBA")
    cut = cut.crop((180, 0, 1720, 1100))   # 머리~가슴 (다리는 프레임 밖으로)
    person_into(bg, cut, 640, -40, H + 40, grade=(1.02, 0.98, 1.06), rim=(255, 160, 70))
    d = ImageDraw.Draw(bg)
    # 2차 (2026-11-26 사용자: "그래서 영상이 무슨 내용이지? 뭐가 핵심이고 뭘 주장하는 거지") — 소재(그의 말) 대신 주장을 큰 글씨로, 말은 근거로 작게
    tag(d, (600, 46), "빅테크 AI 투자의 돈줄", font(BOLD, 36))
    text_line(d, (600, 112), "번 돈 넘어", font(HEAD, 112))
    text_line(d, (600, 236), "빚으로 짓는다", font(HEAD, 112), hl="빚으로")
    tag(d, (600, 384), "아마존 CEO 재시: “25년에 나눠 쓰는 세상 아니다”", font(BOLD, 26), bg=(20, 22, 30), fg=WHITE)
    tag(d, (600, 446), "칩 수요의 열쇠 = 채권시장", font(BOLD, 34), bg=YEL, fg=INK)
    d.text((24, H - 34), "사진: Andy Jassy in 2010 (CC BY 2.0) · 배경은 생성 그림", font=font(BOLD, 16), fill=(200, 200, 205))
    return bg.convert("RGB")


def thumb_b():
    """B 구조 — 빌린 돈(서류) → 칩 → 금고. 사람 없이 돈의 흐름을 한 장으로."""
    bg = cover(Image.open(SRC / "bg_vault.png").convert("RGB"), focus=(0.5, 0.6))
    bg = vignette(bg, 0.65, side="top").convert("RGBA")
    d = ImageDraw.Draw(bg)
    # 2차: 결론(칩 수요를 정하는 곳)을 큰 글씨로, 그림 위 딱지는 그 결론에 이르는 돈의 길
    ft = font(BOLD, 34)
    tw = d.textlength("빅테크가 AI 칩 사는 돈, 언제까지?", font=ft)
    tag(d, (W // 2 - tw // 2 - 16, 26), "빅테크가 AI 칩 사는 돈, 언제까지?", ft, bg=(20, 22, 30), fg=WHITE)
    text_line(d, (W // 2 - d.textlength("열쇠는 금고 아닌", font=font(HEAD, 104)) // 2, 96), "열쇠는 금고 아닌", font(HEAD, 104))
    text_line(d, (W // 2 - d.textlength("채권시장", font=font(HEAD, 120)) // 2, 210), "채권시장", font(HEAD, 120), hl="채권시장")
    f = font(BOLD, 30)
    tag(d, (40, 590), "번 돈 넘는 몫은 빚으로", f, bg=RED, fg=WHITE)
    tag(d, (W // 2 - 70, 640), "칩값으로", f, bg=(20, 22, 30), fg=YEL)
    tag(d, (900, 360), "파는 쪽 금고로", f, bg=(20, 22, 30), fg=WHITE)
    return bg.convert("RGB")


def thumb_c():
    """C 숫자 맞대기 — 아마존 석 달: 번 돈 424억 vs 쓴 돈 773억 (오른쪽 어두운 자리에 막대)."""
    bg = cover(Image.open(SRC / "bg_campus.png").convert("RGB"), focus=(0.35, 0.5))
    bg = vignette(bg, 0.6, side="right").convert("RGBA")
    d = ImageDraw.Draw(bg)
    x0 = 640
    # 2차: 아마존 하나 대신 빅테크 다섯 곳 합계 — 주제(빅테크 AI 투자)와 주장(모자란 건 빚)을 숫자로
    tag(d, (x0, 30), "빅테크 5곳 AI 투자 (7~9월)", font(BOLD, 32), bg=(20, 22, 30), fg=WHITE)
    text_line(d, (x0, 92), "번 돈의 116%", font(HEAD, 96), hl="116%")
    text_line(d, (x0, 196), "모자란 건 빚", font(HEAD, 96), hl="빚")
    fl, fn = font(BOLD, 32), font(HEAD, 56)
    maxw = 560
    for i, (lab, v, txt, col) in enumerate((("번 돈", 1986, "1,986억", (90, 170, 255)), ("쓴 돈", 2304, "2,304억", RED))):
        y = 330 + i * 110
        d.text((x0, y + 18), lab, font=fl, fill=WHITE, stroke_width=4, stroke_fill=INK)
        bw = int(maxw * v / 2304 * 0.55)
        d.rounded_rectangle([x0 + 110, y + 10, x0 + 110 + bw, y + 70], radius=10, fill=col)
        d.text((x0 + 125 + bw, y + 4), txt, font=fn, fill=WHITE, stroke_width=5, stroke_fill=INK)
    tag(d, (x0, 570), "칩 수요가 언제까지 가나 = 채권시장이 정한다", font(BOLD, 26), bg=YEL, fg=INK)
    return bg.convert("RGB")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    out = []
    for k, fn in (("A", thumb_a), ("B", thumb_b), ("C", thumb_c)):
        im = fn(); p = OUT / f"thumbnail_{k}.png"; im.save(p); out.append(im)
    # 휴대폰 목록 크기 미리보기 (가로 168px 기준 ×2) + 큰 판
    sheet = Image.new("RGB", (W, H * 3 // 2 + 40), (245, 245, 247))
    for i, im in enumerate(out):
        sheet.paste(im.resize((W // 2 - 20, H // 2 - 11)), ((i % 2) * (W // 2) + 10, (i // 2) * (H // 2) + 10))
    for i, im in enumerate(out):
        sheet.paste(im.resize((336, 189)), (10 + i * 346, H + 10 + 20))
    sheet.save(OUT / "thumbnail_preview.png")
    print("ok", [str(OUT / f"thumbnail_{k}.png") for k in "ABC"])
