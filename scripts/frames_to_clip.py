"""캡처한 프레임 묶음(f_000250.png …)을 일정 fps 의 무음 mp4 로 묶는다.

ego lite 로 '정지 → 이동 → 찍기' 한 레퍼런스 화면을 rea-video 같은 영상 분석 도구에 넣기 위한 것.
파일 이름의 숫자(밀리초)로 정렬하고, 빠진 시각은 앞 프레임을 반복해 원래 시간축을 지킨다.

    python scripts/frames_to_clip.py %YTFLOW_DRIVE%\\refs\\<ID>\\frames --fps 4 -o ref.mp4
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("frames", type=Path, help="f_<밀리초>.png 가 든 폴더")
    ap.add_argument("--fps", type=float, default=4.0, help="캡처 간격의 역수 (0.25초 → 4)")
    ap.add_argument("-o", "--out", type=Path, required=True)
    a = ap.parse_args()

    shots = []
    for p in a.frames.iterdir():
        m = re.fullmatch(r"f_(\d+)\.(png|jpe?g)", p.name, re.I)
        if m:
            shots.append((int(m.group(1)), p))
    if not shots:
        print(f"프레임이 없습니다: {a.frames}", file=sys.stderr)
        return 1
    shots.sort()
    step = 1000.0 / a.fps
    end = shots[-1][0]
    n = int(round(end / step)) + 1

    with tempfile.TemporaryDirectory() as td:
        lst = Path(td) / "list.txt"
        lines, j = [], 0
        for i in range(n):
            t = i * step
            while j + 1 < len(shots) and shots[j + 1][0] <= t + step / 2:
                j += 1
            lines.append(f"file '{shots[j][1].resolve().as_posix()}'\nduration {1 / a.fps:.6f}")
        lines.append(f"file '{shots[j][1].resolve().as_posix()}'")
        lst.write_text("\n".join(lines) + "\n", encoding="utf-8")
        a.out.parent.mkdir(parents=True, exist_ok=True)
        ff = shutil.which("ffmpeg") or "ffmpeg"
        cmd = [ff, "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
               "-vf", f"fps={a.fps},scale=trunc(iw/2)*2:trunc(ih/2)*2", "-pix_fmt", "yuv420p",
               "-c:v", "libx264", "-crf", "18", str(a.out)]
        subprocess.run(cmd, check=True)
    print(f"{a.out}  ({n}장, {n / a.fps:.1f}초, 원본 프레임 {len(shots)}장)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
