"""원화 2×2 시트 → 칸 <시트>_tl|tr|bl|br.jpg (1920×1080, Lanczos + 약한 선명화). python cut_sheets.py <시트 폴더> <조각 폴더>"""
import sys
from pathlib import Path
from PIL import Image, ImageFilter
src, dst = Path(sys.argv[1]), Path(sys.argv[2]); dst.mkdir(parents=True, exist_ok=True)
for p in sorted(src.glob("*.png")):
    im = Image.open(p).convert("RGB"); W, H = im.size; w, h = W // 2, H // 2
    for k, (x, y) in {"tl": (0, 0), "tr": (w, 0), "bl": (0, h), "br": (w, h)}.items():
        c = im.crop((x + 2, y + 2, x + w - 2, y + h - 2)).resize((1920, 1080), Image.LANCZOS)
        c.filter(ImageFilter.UnsharpMask(1.2, 60, 2)).save(dst / f"{p.stem}_{k}.jpg", quality=93)
    print(p.stem, im.size)
