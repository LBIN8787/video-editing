"""흰 바탕 시트 → 연결 성분으로 사물 잘라 투명 PNG. python cut.py 시트.png 이름1 이름2 이름3"""
import sys
from collections import deque
import numpy as np
from PIL import Image, ImageFilter


def label(mask):
    h, w = mask.shape; lab = np.zeros((h, w), int); n = 0
    for y in range(h):
        for x in range(w):
            if mask[y, x] and not lab[y, x]:
                n += 1; q = deque([(y, x)]); lab[y, x] = n
                while q:
                    cy, cx = q.popleft()
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]:
                                lab[ny, nx] = n; q.append((ny, nx))
    return lab, n


def cut(sheet, names, outdir):
    im = Image.open(sheet).convert("RGB"); a = np.asarray(im)
    white = a.min(axis=2) > 238
    s = 4; lab, n = label(~white[::s, ::s])
    sizes = np.bincount(lab.ravel())[1:]
    top = sorted(range(1, n + 1), key=lambda i: -sizes[i - 1])[:len(names)]
    comps = []
    for i in top:
        ys, xs = np.where(lab == i); comps.append((xs.min() * s, ys.min() * s, (xs.max() + 1) * s, (ys.max() + 1) * s, i))
    comps.sort()
    full = np.kron(lab, np.ones((s, s), int))[:a.shape[0], :a.shape[1]]
    for (x0, y0, x1, y1, i), nm in zip(comps, names):
        m = np.asarray(Image.fromarray(((full == i) * 255).astype("uint8")).filter(ImageFilter.MaxFilter(9))) > 0
        sub = (m & ~white)[y0:y1, x0:x1]; h, w = sub.shape
        out = np.zeros_like(sub); q = deque()
        for y in range(h):
            for x in (0, w - 1):
                if not sub[y, x] and not out[y, x]: out[y, x] = 1; q.append((y, x))
        for x in range(w):
            for y in (0, h - 1):
                if not sub[y, x] and not out[y, x]: out[y, x] = 1; q.append((y, x))
        while q:
            cy, cx = q.popleft()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < h and 0 <= nx < w and not sub[ny, nx] and not out[ny, nx]: out[ny, nx] = 1; q.append((ny, nx))
        al = Image.fromarray(((~out.astype(bool)) * 255).astype("uint8")).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
        piece = im.crop((x0, y0, x1, y1)).convert("RGBA"); piece.putalpha(al)
        pad = 12; c = Image.new("RGBA", (piece.width + 2 * pad, piece.height + 2 * pad), (0, 0, 0, 0)); c.paste(piece, (pad, pad))
        c.save(f"{outdir}/{nm}.png"); print(nm, c.size)


if __name__ == "__main__":
    import os
    cut(sys.argv[1], sys.argv[2:], os.path.dirname(sys.argv[1]))
