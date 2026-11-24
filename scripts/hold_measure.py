"""화면이 멈춘 시간 재기 — 레퍼런스 측정(docs/68)과 같은 방법.

0.25초마다 64×36 흑백으로 줄인 화면의 평균 밝기 차이가 0.6(0~255) 미만인 구간이
1.5초 이상 이어지면 '정지'로 센다. 브라우저에서 YouTube 레퍼런스를 잰 것과 같은 계산이라
내 영상과 레퍼런스를 같은 잣대로 맞댈 수 있다.

python scripts/hold_measure.py 영상.mp4 [영상2.mp4 ...] [--from 0 --to 999]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

W, H, FPS, EPS, MIN = 64, 36, 4, 0.6, 1.5


def measure(path: str, t0: float = 0.0, t1: float | None = None) -> dict:
    cmd = ["ffmpeg", "-v", "error", "-ss", str(t0)] + (["-to", str(t1)] if t1 else []) + [
        "-i", path, "-vf", f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    n = len(raw) // (W * H)
    frames = [raw[i * W * H:(i + 1) * W * H] for i in range(n)]
    diffs = [0.0] + [sum(abs(a - b) for a, b in zip(frames[i], frames[i - 1])) / (W * H) for i in range(1, n)]
    holds, start = [], None
    for i, d in enumerate(diffs):
        t = i / FPS
        if d < EPS:
            start = t if start is None else start
        else:
            if start is not None and t - start >= MIN:
                holds.append((start, t))
            start = None
    if start is not None and n / FPS - start >= MIN:
        holds.append((start, n / FPS))
    dur = n / FPS
    tot = sum(b - a for a, b in holds)
    return {"file": path, "dur": round(dur, 1), "holds_n": len(holds), "hold_share": round(tot / dur, 2) if dur else 0,
            "longest": round(max((b - a for a, b in holds), default=0), 1),
            "holds": [(round(a + t0, 1), round(b + t0, 1)) for a, b in holds if b - a >= 4]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--from", dest="t0", type=float, default=0.0)
    ap.add_argument("--to", dest="t1", type=float, default=None)
    a = ap.parse_args()
    for f in a.files:
        print(json.dumps(measure(f, a.t0, a.t1), ensure_ascii=False))
    sys.exit(0)
