"""원화 조각에서 휴대폰의 빈 빛나는 화면을 찾아 가림막(mask_<조각>.png)과 상자(screens.json)를 만든다.
렌더러(soldout_overlay.html uiLayer)는 지어낸 쇼핑 앱 화면을 이 가림막 안(빛나는 화면 픽셀)에만 그린다 — 손가락·테두리는 원화 그대로 남음.
python detect_screens.py <조각 폴더> <조각 이름...>"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
import cv2

src = Path(sys.argv[1]); out = {}
for n in sys.argv[2:]:
    a = np.asarray(Image.open(src / f"{n}.jpg").convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = (r + g + b) / 3; sat = a.max(-1) - a.min(-1)
    m = (lum > 200) & (sat < 60)
    ker = np.ones((5, 5), np.uint8)
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, ker)
    k, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    if k < 2:
        print(n, "화면 없음"); continue
    i = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    comp = lab == i
    ys, xs = np.where(comp); box = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    fill = comp.sum() / ((box[2] - box[0] + 1) * (box[3] - box[1] + 1))
    comp = cv2.morphologyEx(comp.astype(np.uint8), cv2.MORPH_CLOSE, ker) > 0
    mask = Image.fromarray((comp * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.2))
    rgba = Image.new("RGBA", mask.size, (255, 255, 255, 0)); rgba.putalpha(mask)
    rgba.save(src / f"mask_{n}.png")
    (cx, cy), (rw, rh), ang = cv2.minAreaRect(np.column_stack(np.where(comp))[:, ::-1].astype(np.float32))
    if rw > rh:
        rw, rh, ang = rh, rw, ang - 90
    ang = ((ang + 90) % 180) - 90
    out[n] = {"rot": [round(cx, 1), round(cy, 1), round(rw, 1), round(rh, 1), round(ang, 2)], "box": box, "area": round(float(comp.sum() / comp.size), 4), "fill": round(float(fill), 3)}
    print(n, out[n])
f = Path(__file__).resolve().parent / "screens.json"
old = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
old.update(out); f.write_text(json.dumps(old, ensure_ascii=False, indent=1), encoding="utf-8")
