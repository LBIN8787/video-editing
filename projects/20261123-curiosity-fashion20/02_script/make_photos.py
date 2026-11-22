"""실제 자료 화면: 크로버 1919 논문(American Anthropologist 21(3), 퍼블릭 도메인 — 인터넷 아카이브 jstor-660477 의 660477.pdf)
→ <조각 폴더>/photo_ktitle.jpg(첫 쪽 제목·첫 문단), photo_kfig20.jpg(247쪽 그림 20 치마 폭). 1920×1080, 어두운 바탕 위 종이.
python make_photos.py <kroeber.pdf> <조각 폴더>"""
import sys
from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFilter

src, dst = Path(sys.argv[1]), Path(sys.argv[2]); dst.mkdir(parents=True, exist_ok=True)
doc = pdfium.PdfDocument(str(src))
JOBS = {"ktitle": (1, (0.02, 0.06, 0.98, 0.50)), "kfig20": (13, (0.04, 0.315, 0.96, 0.745))}
for name, (page, (x0, y0, x1, y1)) in JOBS.items():
    im = doc[page].render(scale=4).to_pil().convert("RGB")
    W, H = im.size
    crop = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    th = 820; tw = int(crop.width * th / crop.height)
    if tw > 1500:
        tw = 1500; th = int(crop.height * tw / crop.width)
    crop = crop.resize((tw, th), Image.LANCZOS)
    top = (1080 - th) // 2 - 40
    bg = Image.new("RGB", (1920, 1080), (28, 24, 21))
    g = Image.new("L", (1920, 1080), 0); ImageDraw.Draw(g).rectangle((960 - tw // 2 + 14, top + 18, 960 + tw // 2 + 14, top + th + 18), fill=170)
    bg.paste((8, 6, 5), (0, 0), g.filter(ImageFilter.GaussianBlur(22)))
    bg.paste(crop, (960 - tw // 2, top))
    bg.save(dst / f"photo_{name}.jpg", quality=93); print(name, crop.size)
