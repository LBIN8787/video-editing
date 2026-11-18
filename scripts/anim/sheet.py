"""확인용 정지 화면 묶음: python sheet.py <폴더>  → 폴더/sheet.jpg (s_<초>.jpg 를 시간 순으로)"""
import glob, os, re, sys
from PIL import Image, ImageDraw
d = sys.argv[1]
fs = sorted(glob.glob(os.path.join(d, "s_*.jpg")), key=lambda f: float(re.search(r"s_([\d.]+)\.jpg$", f).group(1)))
W, H = 480, 270
s = Image.new("RGB", (W * 4, H * ((len(fs) + 3) // 4)), "white"); dr = ImageDraw.Draw(s)
for k, f in enumerate(fs):
    s.paste(Image.open(f).resize((W, H)), ((k % 4) * W, (k // 4) * H))
    dr.rectangle([(k % 4) * W, (k // 4) * H, (k % 4) * W + 60, (k // 4) * H + 16], fill="black")
    dr.text(((k % 4) * W + 4, (k // 4) * H + 2), re.search(r"s_([\d.]+)\.jpg$", f).group(1), fill="yellow")
s.save(os.path.join(d, "sheet.jpg"), quality=85)
