"""꽉 채운 썸네일 D/E/F (2026-11-26 사용자: "썸네일에서 꼭 반반으로 하지말고 꽉 채운거도 보여주세요").

A~C 는 사진 반 · 글 반으로 나뉜 구도. D~F 는 사진 한 장이 화면 전체를 채우고 글씨를 그 위에 올림.
- D 원본 장면: 세마포 인터뷰(2026.11.18) 중 재시가 말하는 프레임 전체 + 오른쪽 어두운 벽 위에 주장
- E 보도 사진 꽉 채움: 아마존 보도 센터 사진을 화면 전체로 키우고 색을 어둡게 눌러 큰 글씨 두 줄
- F 얼굴 확대 + 숫자: 인터뷰 프레임의 얼굴을 크게 당기고 '116%' 한 숫자로
재료: 04_assets/thumb/sem_frame_290.jpg · sem_frame_279.jpg (raw/semafor_full.mp4 에서 ffmpeg 로 뽑은 프레임), raw/jassy_press.jpg
실행: python projects/20261126-market-deep-dc-funding/02_script/make_thumbs_full.py
"""
import json

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

import make_thumbs as T
from make_thumbs import BOLD, HEAD, INK, RED, WHITE, YEL, H, W, cover, font, tag, text_line

PROJ = T.PROJ
RAW = PROJ / "04_assets" / "footage" / "raw"


def grade(im, dark=0.8, sat=0.85, cool=1.04):
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Brightness(im).enhance(dark)
    r, g, b = im.split()
    return Image.merge("RGB", (r, g, b.point(lambda v: min(255, int(v * cool)))))


def shade(im, side="right", strength=0.75, start=0.35):
    """화면을 나누지 않고 한쪽만 서서히 어둡게 — 글씨 읽히는 자리."""
    m = Image.new("L", im.size, 0); dm = ImageDraw.Draw(m)
    if side in ("right", "left"):
        for i in range(W):
            t = i / W if side == "right" else 1 - i / W
            dm.line([(i, 0), (i, H)], fill=int(255 * strength * max(0, (t - start) / (1 - start)) ** 0.9))
    else:  # bottom
        for j in range(H):
            t = j / H
            dm.line([(0, j), (W, j)], fill=int(255 * strength * max(0, (t - start) / (1 - start)) ** 0.9))
    return Image.composite(Image.new("RGB", im.size, (6, 8, 14)), im, m)


def thumb_d():
    bg = Image.open(PROJ / "04_assets" / "thumb" / "sem_frame_290.jpg").convert("RGB")
    bg = cover(bg.crop((0, 40, 1280, 720)), focus=(0.4, 0.5))   # 위쪽 행사 자막 줄 잘라 냄
    bg = shade(grade(bg, 0.85), "right", 0.8, 0.42).convert("RGBA")
    d = ImageDraw.Draw(bg)
    x = 640
    # 따옴표는 실제 말에만 — 재시 원문 "headwinds on your short-term free cash flow … once you get a few years out … you really like the free cash flow"
    tag(d, (x, 40), "아마존 CEO 재시의 답 (11월 18일, 요약)", font(BOLD, 30), bg=(20, 22, 30), fg=WHITE)
    text_line(d, (x, 104), "지금은 역풍", font(HEAD, 104))
    text_line(d, (x, 222), "몇 년 뒤 회수", font(HEAD, 104), hl="몇 년 뒤")
    tag(d, (x, 372), "그 돈, 번 돈 넘어 빚으로", font(BOLD, 40), bg=RED, fg=WHITE)
    tag(d, (x, 446), "칩 수요의 열쇠 = 채권시장", font(BOLD, 36), bg=YEL, fg=INK)
    d.text((24, H - 34), "영상: 세마포(Semafor) 인터뷰 · 인용", font=font(BOLD, 16), fill=(200, 200, 205))
    return bg.convert("RGB")


def thumb_e():
    ph = Image.open(RAW / "jassy_press.jpg").convert("RGB")
    bg = cover(ph, focus=(0.5, 0.22))                         # 얼굴이 화면 위·가운데
    bg = grade(bg, 0.7, 0.75, 1.06)
    bg = shade(bg, "bottom", 0.92, 0.35).convert("RGBA")
    d = ImageDraw.Draw(bg)
    tag(d, (40, 36), "빅테크 AI 투자의 돈줄", font(BOLD, 36))
    f1 = font(HEAD, 128)
    s = "번 돈 넘어, 빚으로"
    text_line(d, (W // 2 - d.textlength(s, font=f1) // 2, 420), s, f1, hl="빚으로", stroke=10)
    s2 = "AI 칩 수요는 언제까지? 열쇠는 채권시장"
    f2 = font(BOLD, 38)
    tag(d, (W // 2 - d.textlength(s2, font=f2) // 2 - 16, 572), s2, f2, bg=YEL, fg=INK)
    d.text((24, H - 30), "사진: 아마존 보도 센터", font=font(BOLD, 16), fill=(200, 200, 205))
    return bg.convert("RGB")


def thumb_f():
    fr = Image.open(PROJ / "04_assets" / "thumb" / "sem_frame_279.jpg").convert("RGB")
    face = fr.crop((300, 0, 1020, 405))                       # 머리·어깨가 다 들어오게 1.8배만 당김
    bg = face.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))
    bg = shade(grade(bg, 0.8, 0.8), "left", 0.85, 0.35)
    bg = shade(bg, "bottom", 0.6, 0.6).convert("RGBA")
    d = ImageDraw.Draw(bg)
    tag(d, (40, 40), "빅테크 5곳 · 7~9월 AI 투자", font(BOLD, 34), bg=(20, 22, 30), fg=WHITE)
    text_line(d, (40, 110), "번 돈의", font(HEAD, 96))
    text_line(d, (40, 214), "116%", font(HEAD, 200), hl="116%", stroke=12)
    tag(d, (40, 470), "모자란 건 빚 — 칩 수요가 걸렸다", font(BOLD, 38), bg=RED, fg=WHITE)
    d.text((W - 360, H - 34), "영상: 세마포(Semafor) 인터뷰 · 인용", font=font(BOLD, 16), fill=(200, 200, 205))
    return bg.convert("RGB")


if __name__ == "__main__":
    qa = json.loads((T.OUT / "thumbnail_qa.json").read_text(encoding="utf-8")) if (T.OUT / "thumbnail_qa.json").exists() else {}
    out = []
    for k, fn in (("D", thumb_d), ("E", thumb_e), ("F", thumb_f)):
        T.BOXES.clear()
        im = fn(); im.save(T.OUT / f"thumbnail_{k}.png"); out.append(im)
        clash = [b for b in T.BOXES if b[2] > W - 200 and b[3] > H - 90]
        small = min((b[3] - b[1]) for b in T.BOXES) * 168 / W
        qa[k] = {"timestamp_overlap": bool(clash), "smallest_text_px_at_168w": round(small, 1), "ok": not clash and small >= 6,
                 "note": "꽉 채운 구도(make_thumbs_full.py) — 출처 표기 줄은 측정에서 뺌"}
    (T.OUT / "thumbnail_qa.json").write_text(json.dumps(qa, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: qa[k] for k in "DEF"})
    sheet = Image.new("RGB", (W, H * 3 // 2 + 40), (245, 245, 247))
    for i, im in enumerate(out):
        sheet.paste(im.resize((W // 2 - 20, H // 2 - 11)), ((i % 2) * (W // 2) + 10, (i // 2) * (H // 2) + 10))
    for i, im in enumerate(out):
        sheet.paste(im.resize((336, 189)), (10 + i * 346, H + 30))
    sheet.save(T.OUT / "thumbnail_preview_full.png")
