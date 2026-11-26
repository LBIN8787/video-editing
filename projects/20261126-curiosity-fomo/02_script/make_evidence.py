"""증거 자리(실제 논문 첫 장) 화면 → <조각 폴더>/ev_<이름>.jpg (1920×1080). 출처(설명란에 적음):
  przy    : Przybylski 외 (2013) Computers in Human Behavior 29 — selfdeterminationtheory.org 공개 PDF 1쪽
  whillans: Whillans 외 (2017) Personality and Social Psychology Bulletin 43(12) — 하버드 경영대학원 공개 PDF 1쪽
python make_evidence.py <PDF 폴더> <조각 폴더>"""
import sys
from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFilter

src, dst = Path(sys.argv[1]), Path(sys.argv[2]); dst.mkdir(parents=True, exist_ok=True)
JOBS = {"przy": ("przy.pdf", 0, (0.0, 0.02, 1.0, 0.40)), "whillans": ("whillans.pdf", 0, (0.0, 0.02, 1.0, 0.40))}
for name, (f, page, (x0, y0, x1, y1)) in JOBS.items():
    im = pdfium.PdfDocument(str(src / f))[page].render(scale=3).to_pil().convert("RGB")
    W, H = im.size
    crop = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    tw = 1240; th = int(crop.height * tw / crop.width)
    if th > 820:
        th = 820; tw = int(crop.width * th / crop.height)
    crop = crop.resize((tw, th), Image.LANCZOS)
    bg = Image.new("RGB", (1920, 1080), (28, 24, 21))
    g = Image.new("L", (1920, 1080), 0); ImageDraw.Draw(g).rectangle((960 - tw // 2 + 14, 200 + 18, 960 + tw // 2 + 14, 200 + th + 18), fill=170)
    bg.paste((8, 6, 5), (0, 0), g.filter(ImageFilter.GaussianBlur(22)))
    bg.paste(crop, (960 - tw // 2, 200))
    bg.save(dst / f"ev_{name}.jpg", quality=93); print(name, crop.size)
