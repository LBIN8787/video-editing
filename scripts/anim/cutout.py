"""흰 배경 시트 → 투명 조각 (scipy 없이 OpenCV). 가장자리와 이어진 배경색만 지워서 옷의 흰 부분은 남긴다.

    python scripts/anim/cutout.py <시트.png> <출력폴더> 이름1,이름2,...
조각은 왼쪽부터 순서대로. 조각 수가 다르면 큰 덩어리 기준으로 다시 묶는다.
"""
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np


def cut(sheet: Path, outdir: Path, names: list[str], tol: int = 26) -> list[Path]:
    a = cv2.imread(str(sheet), cv2.IMREAD_UNCHANGED)
    if a.shape[2] == 3:
        a = cv2.cvtColor(a, cv2.COLOR_BGR2BGRA)
    rgb = a[..., :3].astype(int)
    c = np.concatenate([rgb[:12, :12].reshape(-1, 3), rgb[:12, -12:].reshape(-1, 3), rgb[-12:, :12].reshape(-1, 3), rgb[-12:, -12:].reshape(-1, 3)])
    bg = np.median(c, axis=0)
    near = (np.abs(rgb - bg).max(axis=2) < tol).astype(np.uint8)
    n, lab = cv2.connectedComponents(near, connectivity=4)
    border = np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])
    border = border[border != 0] if near[0, 0] == 0 else border
    bgmask = np.isin(lab, border) & (near == 1)
    fg = (~bgmask).astype(np.uint8)
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    # 작은 부스러기 지우기
    k, cl, st, _ = cv2.connectedComponentsWithStats(fg, connectivity=8)
    keep = np.zeros_like(fg)
    for i in range(1, k):
        if st[i, cv2.CC_STAT_AREA] > 1500:
            keep[cl == i] = 1
    fg = keep
    cols = fg.sum(axis=0) > 2
    segs, run = [], None
    for x, v in enumerate(cols):
        if v and run is None:
            run = x
        if not v and run is not None:
            segs.append([run, x]); run = None
    if run is not None:
        segs.append([run, len(cols)])
    for gap in (60, 40, 24, 12, 4, 1):
        m = []
        for s in segs:
            if m and s[0] - m[-1][1] < gap:
                m[-1][1] = s[1]
            else:
                m.append(list(s))
        m = [s for s in m if s[1] - s[0] > 40]
        if len(m) == len(names):
            break
    if len(m) != len(names):
        raise RuntimeError(f"조각 {len(m)}개 ≠ 이름 {len(names)}개: {sheet}")
    soft = cv2.GaussianBlur(fg.astype(np.float32), (0, 0), 0.8)
    # 배경색이 섞인 가장자리 색 빼기(흰 테두리 줄이기)
    out = a.copy()
    out[..., 3] = (soft * 255).clip(0, 255).astype(np.uint8)
    outdir.mkdir(parents=True, exist_ok=True)
    res = []
    for (x0, x1), nm in zip(m, names):
        ys = np.where(fg[:, x0:x1].any(axis=1))[0]
        y0, y1 = max(0, ys[0] - 6), min(a.shape[0], ys[-1] + 6)
        p = outdir / f"{nm}.png"
        cv2.imwrite(str(p), out[y0:y1, max(0, x0 - 6):x1 + 6])
        res.append(p)
    return res


if __name__ == "__main__":
    print([p.name for p in cut(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3].split(","))])
