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
    a = cv2.imdecode(np.fromfile(str(sheet), np.uint8), cv2.IMREAD_UNCHANGED)   # 한글 경로도 읽히게
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
    # 머리카락 사이처럼 바깥과 막힌 흰 틈: 윤곽 가까이(눈 흰자처럼 안쪽 깊은 곳은 그대로)에 있는 순백 덩어리는 배경으로
    dist_out = cv2.distanceTransform(fg, cv2.DIST_L2, 3)
    holes = ((near == 1) & ~bgmask).astype(np.uint8)
    hn, hl, hs, _ = cv2.connectedComponentsWithStats(holes, connectivity=4)
    diff0 = np.abs(rgb - bg).max(axis=2)
    total = max(1, int(fg.sum()))
    for i in range(1, hn):
        ar = hs[i, cv2.CC_STAT_AREA]
        if ar < 6:
            continue
        sel = hl == i
        if diff0[sel].mean() >= 12:
            continue
        # 윤곽 가까운 틈(머리카락 사이) 또는 팔·다리 사이처럼 눈 흰자보다 큰 틈 → 배경. 말풍선 속처럼 아주 큰 흰 면은 그대로
        if dist_out[sel].min() < 22 and ar <= 15000 or 250 <= ar <= min(15000, total * 0.03):
            fg[sel] = 0
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
    colsum = fg.sum(axis=0)
    while len(m) < len(names):   # 붙어 있는 두 조각: 가장 넓은 덩어리를 가운데쯤 가장 얇은 세로줄에서 나눔
        w = max(range(len(m)), key=lambda i: m[i][1] - m[i][0])
        x0, x1 = m[w]
        lo, hi = x0 + (x1 - x0) * 3 // 10, x0 + (x1 - x0) * 7 // 10
        sx = lo + int(np.argmin(colsum[lo:hi]))
        m[w:w + 1] = [[x0, sx], [sx, x1]]
    if len(m) != len(names):
        raise RuntimeError(f"조각 {len(m)}개 ≠ 이름 {len(names)}개: {sheet}")
    # 흰 테두리 없애기 (2026-11-19 사용자: "그림을 누끼 딸 때 흰부분이 있는점")
    # ① 가장자리를 1px 안으로 ② 가장자리 몇 px 는 '배경색과 얼마나 다른가'로 투명도를 다시 셈
    # ③ 반투명 픽셀에 섞인 배경색을 빼서 원래 색으로 (색 되돌리기)
    fg_in = cv2.erode(fg, np.ones((3, 3), np.uint8), iterations=1)
    soft = cv2.GaussianBlur(fg_in.astype(np.float32), (0, 0), 0.7)
    dist = cv2.distanceTransform(fg_in, cv2.DIST_L2, 3)
    diff = np.abs(rgb - bg).max(axis=2).astype(np.float32)
    est = np.clip((diff - 8) / 100.0, 0, 1)
    alpha = np.where(dist < 3.5, soft * est, soft)
    alpha = np.where(dist >= 3.5, np.maximum(alpha, soft), alpha)
    out = a.copy()
    al = np.clip(alpha, 0, 1)[..., None]
    col = (a[..., :3].astype(np.float32) - (1 - al) * bg.reshape(1, 1, 3)) / np.maximum(al, 0.05)
    out[..., :3] = np.where(al > 0.02, np.clip(col, 0, 255), a[..., :3]).astype(np.uint8)
    out[..., 3] = (al[..., 0] * 255).clip(0, 255).astype(np.uint8)
    outdir.mkdir(parents=True, exist_ok=True)
    res = []
    for (x0, x1), nm in zip(m, names):
        # 옆 조각에서 넘어온 작은 부스러기 지우기: 이 칸에서 가장 큰 덩어리의 3% 보다 작은 덩어리는 투명하게
        sub = (fg[:, x0:x1] > 0).astype(np.uint8)
        kn, kl, ks, _ = cv2.connectedComponentsWithStats(sub, connectivity=8)
        if kn > 2:
            big = ks[1:, cv2.CC_STAT_AREA].max()
            for j in range(1, kn):
                if ks[j, cv2.CC_STAT_AREA] < big * 0.03:
                    blk = kl == j
                    out[:, x0:x1, 3][blk] = 0
                    fg[:, x0:x1][blk] = 0
        ys = np.where(fg[:, x0:x1].any(axis=1))[0]
        y0, y1 = max(0, ys[0] - 6), min(a.shape[0], ys[-1] + 6)
        p = outdir / f"{nm}.png"
        lx = max(0, x0 - 6)
        crop = out[y0:y1, lx:x1 + 6].copy()
        crop[:, :x0 - lx, 3] = 0          # 여백(양옆 6px)에 들어온 옆 조각은 투명하게
        crop[:, x1 - lx:, 3] = 0
        cv2.imencode('.png', crop)[1].tofile(str(p))
        res.append(p)
    return res


if __name__ == "__main__":
    print([p.name for p in cut(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3].split(","))])
