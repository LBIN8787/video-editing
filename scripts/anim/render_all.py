"""긴 장면을 구간으로 나눠 동시에 렌더 → 이어 붙임 → 목소리·효과음·자막 입혀 검토본.

    python render_all.py <out 폴더> <html> <voice> <ass> <끝 초> <결과.mp4> [--parts 3] [--jobs N]
여러 편을 한꺼번에: 이 스크립트를 편마다 따로 실행(각각 --parts 만큼 node 프로세스).
"""
import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

H = Path(__file__).resolve().parent
NODE_PATH = str(H.parents[1] / "tools/playwright/node_modules")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("html")
    ap.add_argument("voice")
    ap.add_argument("ass")
    ap.add_argument("end", type=float)
    ap.add_argument("result")
    ap.add_argument("--parts", type=int, default=3)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    n = a.parts
    cuts = [round(a.end * i / n * 30) / 30 for i in range(n + 1)]   # 프레임 경계에 맞춤
    import os
    env = dict(os.environ, NODE_PATH=NODE_PATH)

    def part(i):
        o = a.out / f"part{i}.mp4"
        subprocess.run(["node", str(H / "render.js"), a.html, str(o), str(cuts[i]), str(cuts[i + 1])], check=True, env=env)
        return o

    with ThreadPoolExecutor(n) as ex:
        parts = list(ex.map(part, range(n)))
    lst = a.out / "parts.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    silent = a.out / "video.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(silent)], check=True)
    subprocess.run([sys.executable, str(H / "finish.py"), str(silent), a.voice, a.ass, str(Path(a.html).with_suffix(".sfx.json")), str(a.end), a.result], check=True)


if __name__ == "__main__":
    main()
