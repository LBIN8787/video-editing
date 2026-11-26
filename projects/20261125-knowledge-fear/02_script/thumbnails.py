"""불안 편 썸네일 A/B/C (1280×720) + 휴대폰 크기 미리보기.
글씨 기본값(2026-11-26 사용자 확정): Noto Sans KR Black · 외곽선 없음(부드러운 그림자만) · 작은 이름 한 줄 + 주어 붙은 두 줄, 왼쪽 정렬.
문구는 비유 말고 주어 + 쉬운 질문, 영상 속 장면·문장과 같은 말.
python thumbnails.py <img 폴더(darwin.jpg)> <영상 프레임 폴더(f22.png·f240.png)> <출력 폴더>"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
GOLD, RED, INK, PAPER = (246, 196, 38), (228, 62, 52), (34, 36, 42), (239, 233, 222)


def font(size):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name("Black")
    except Exception:
        pass
    return f


def cover(im, box=(1280, 720), focus=(0.5, 0.5)):
    w, h = im.size; s = max(box[0] / w, box[1] / h)
    im = im.resize((int(w * s) + 1, int(h * s) + 1), Image.LANCZOS)
    x = int((im.width - box[0]) * focus[0]); y = int((im.height - box[1]) * focus[1])
    return im.crop((x, y, x + box[0], y + box[1]))


def text(im, small, lines, dark):
    """lines: [(글, 색 또는 None)] 두 줄. dark=True 면 밝은 글씨."""
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    fg = (250, 247, 240) if dark else INK
    y = 150
    d.text((64, y), small, font=font(40), fill=(*((205, 200, 190) if dark else (110, 104, 96)), 255)); y += 78
    for t, col in lines:
        d.text((60, y), t, font=font(112), fill=(*(col or fg), 255)); y += 138
    shadow = sh.copy().filter(ImageFilter.GaussianBlur(10))
    r, g, b, a = shadow.split(); a = a.point(lambda v: int(v * (0.55 if dark else 0.25)))
    shadow = Image.merge("RGBA", (*(Image.new("L", im.size, 0 if dark else 255),) * 3, a))
    base = im.convert("RGBA"); base.alpha_composite(shadow, (4, 6)); base.alpha_composite(sh)
    return base.convert("RGB")


def grad(im, color, left=True, width=760):
    g = Image.new("L", (1280, 1), 0)
    for x in range(1280):
        t = x if left else 1279 - x
        g.putpixel((x, 0), 245 if t < width * 0.55 else max(0, int(245 * (1 - (t - width * 0.55) / (width * 0.45)))))
    g = g.resize((1280, 720)); over = Image.new("RGB", (1280, 720), color)
    return Image.composite(over, im, g)


def main(img, frames, out):
    img, frames, out = Path(img), Path(frames), Path(out); out.mkdir(parents=True, exist_ok=True)
    V = {}
    # A — 첫 장면의 주인공(다윈, 퍼블릭 도메인 사진) + 제목의 질문
    a = Image.open(img / "darwin.jpg").convert("RGB")
    a = ImageEnhance.Contrast(a).enhance(1.12)
    canvas = Image.new("RGB", (1280, 720), PAPER)
    canvas.paste(cover(a, (760, 720), (0.5, 0.2)), (520, 0))
    canvas = grad(canvas, PAPER, left=True, width=900)
    V["A"] = (text(canvas, "다윈도 못 버틴 1초", [("불안은 왜", None), ("순식간에 켜질까?", RED)], dark=False),
              "첫 장면(유리 앞에서 뒤로 튄 다윈) + 영상 제목의 질문.")
    # B — 유리·뱀 장면(영상 0:22), 자막 칸 잘라 냄
    fr = Image.open(frames / "f22.png").convert("RGB")
    b = cover(fr.crop((0, 0, 700, 400)), focus=(0.5, 0.5))          # 빈 종이 결로 바탕
    part = fr.crop((850, 80, 1750, 880)).resize((810, 720))          # 유리·뱀만 (손글씨 이름표는 빼고)
    b.paste(part, (900, 0))
    b = grad(b, PAPER, left=True, width=1000)
    V["B"] = (text(b, "유리 앞의 다윈", [("머리는 알았는데", None), ("몸이 먼저 튀었다", RED)], dark=False),
              "1장 장면 그대로(머리는 안전한 걸 알았는데 몸이 먼저 움직임).")
    # C — 겹친 기억(영상 4:00), 어두운 바탕
    c = Image.open(frames / "f240.png").convert("RGB").crop((560, 60, 1920, 900))
    c = grad(cover(c, focus=(0.6, 0.5)), (30, 33, 40), left=True, width=700)
    V["C"] = (text(c, "2026 쥐 실험", [("공포를 배운 뇌,", None), ("기억이 흐려졌다", GOLD)], dark=True),
              "3장의 반전(예상: 또렷해짐 → 결과: 위험·안전 기억이 겹침).")
    for k, (im, _) in V.items():
        im.save(out / f"thumbnail_{k}.png")
    sheet = Image.new("RGB", (3 * 420, 360), "white")
    for i, k in enumerate(V):
        im = V[k][0]; sheet.paste(im.resize((400, 225)), (i * 420 + 10, 10)); sheet.paste(im.resize((168, 94)), (i * 420 + 10, 250))
    sheet.save(out / "thumbnail_preview.png")
    md = Path(__file__).resolve().parent.parent / "05_edit" / "thumbnails.md"
    md.write_text("# 썸네일 A/B/C (Drive `영상/20261125-knowledge-fear/05_edit/thumbnail_A~C.png`)\n\n" + "\n".join(
        f"- **{k}** · {why}" for k, (_, why) in V.items()) + "\n", encoding="utf-8")


main(*sys.argv[1:4])
