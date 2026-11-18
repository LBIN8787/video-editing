"""원화 미리보기: python board.py <art/video 폴더> <출력.jpg> 이름1 이름2 ...  (판은 16:9 칸, 조각은 초록 바탕)"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
d, out, names = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
W, H = 640, 360
cols = 3
s = Image.new("RGBA", (W * cols, H * ((len(names) + cols - 1) // cols)), (40, 90, 60, 255))
dr = ImageDraw.Draw(s)
for k, n in enumerate(names):
    p = d / f"{n}.png"
    if not p.exists():
        continue
    im = Image.open(p).convert("RGBA")
    im.thumbnail((W - 6, H - 6))
    x, y = (k % cols) * W, (k // cols) * H
    s.alpha_composite(im, (x + 3, y + 3))
    dr.rectangle([x, y, x + 150, y + 18], fill="black"); dr.text((x + 3, y + 3), n, fill="yellow")
s.convert("RGB").save(out, quality=85)
