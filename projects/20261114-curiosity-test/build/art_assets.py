"""ChatGPT 웹에서 받은 그림 → 그림판용 투명 조각(art).

받은 그림은 흰 배경(#FFFFFF 근처)에 그려져 있다. 테두리와 이어진 흰색만 지우므로
그림 안쪽의 흰 구름·유리 반사는 그대로 남는다(바깥과 닿지 않으니까).

    python3 build/art_assets.py            # 02_script/art_plan.json 의 이름표대로 자름
    python3 build/art_assets.py --list     # 무엇을 자를지 확인

원본: 04_assets/story/raw/<file>   →   조각: 04_assets/story/gen/<name>.png
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[3]
PROJ = ROOT / "projects" / "20261114-curiosity-test"
RAW = PROJ / "04_assets" / "story" / "raw"
GEN = PROJ / "04_assets" / "story" / "gen"


def enclosed_white(near: np.ndarray, min_frac: float) -> np.ndarray:
    """테두리와 닿지 않은 흰 덩어리(벤치 다리 사이 같은 곳)를 찾는다 — 4배 줄여서 라벨링."""
    h, w = near.shape
    small = near[::4, ::4] > 0
    sh, sw = small.shape
    seen = np.zeros_like(small, dtype=bool)
    out = np.zeros_like(small, dtype=bool)
    min_cells = max(4, int(min_frac * sh * sw))
    for y0 in range(sh):
        for x0 in range(sw):
            if not small[y0, x0] or seen[y0, x0]:
                continue
            stack, cells, border = [(y0, x0)], [], False
            seen[y0, x0] = True
            while stack:
                y, x = stack.pop()
                cells.append((y, x))
                if y in (0, sh - 1) or x in (0, sw - 1):
                    border = True
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < sh and 0 <= nx < sw and small[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
            if not border and len(cells) >= min_cells:
                for y, x in cells:
                    out[y, x] = True
    return np.kron(out, np.ones((4, 4), dtype=bool))[:h, :w]


def cut_one(src: Path, dst: Path, white: int = 243, trim: int = 2,
            crop: list[int] | None = None, fill_enclosed: float = 0.0) -> tuple[int, int]:
    im = Image.open(src).convert("RGBA")
    if crop:
        im = im.crop(tuple(int(v) for v in crop))
    rgb = np.asarray(im)[..., :3].astype(np.uint8)
    near = (rgb.min(axis=2) >= white).astype(np.uint8) * 255     # 흰색 후보
    lab = Image.fromarray(near, "L")
    d = ImageDraw.Draw(lab)
    w, h = lab.size
    seeds = [(x, y) for x in range(0, w, 24) for y in (0, h - 1)] + \
            [(x, y) for y in range(0, h, 24) for x in (0, w - 1)]
    for s in seeds:                       # 테두리와 이어진 흰색만 128 로 채운다
        if lab.getpixel(s) == 255:
            ImageDraw.floodfill(lab, s, 128, thresh=0)
    bg = np.asarray(lab) == 128
    if fill_enclosed:                     # 그림 안쪽에 갇힌 흰 바탕도 지운다(벤치 다리 사이 등)
        bg = bg | enclosed_white(near, fill_enclosed)
    fg = ~bg
    ys, xs = np.where(fg)
    if len(xs) == 0:
        raise RuntimeError(f"{src.name}: 남는 그림이 없습니다")
    y0, y1 = max(0, ys.min() - trim), min(h, ys.max() + 1 + trim)
    x0, x1 = max(0, xs.min() - trim), min(w, xs.max() + 1 + trim)
    alpha = (fg.astype(np.uint8) * 255)[y0:y1, x0:x1]
    alpha = np.asarray(Image.fromarray(alpha, "L").filter(ImageFilter.GaussianBlur(0.8)))
    out = np.dstack([rgb[y0:y1, x0:x1], alpha])
    GEN.mkdir(parents=True, exist_ok=True)
    Image.fromarray(out).save(dst)
    return x1 - x0, y1 - y0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    plan = json.loads((PROJ / "02_script" / "art_plan.json").read_text(encoding="utf-8"))
    for item in plan["art"]:
        src = RAW / item["file"]
        dst = GEN / f"{item['name']}.png"
        if a.list:
            print(f"{item['file']} → {dst.name}")
            continue
        if not src.exists():
            print(f"[art] 건너뜀 (원본 없음): {src}")
            continue
        w, h = cut_one(src, dst, crop=item.get("crop"), fill_enclosed=item.get("fill_enclosed", 0.0))
        print(f"[art] {src.name} → gen/{dst.name} ({w}×{h})")


if __name__ == "__main__":
    main()
