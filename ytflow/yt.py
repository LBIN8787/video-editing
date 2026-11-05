"""yt-dlp 를 서브프로세스로 호출하는 얇은 래퍼 (API 키 불필요)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


def _run(args: list[str]) -> str:
    cmd = [sys.executable, "-m", "yt_dlp", "--no-warnings", "--ignore-errors", *args]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode not in (0, 1):
        raise RuntimeError(out.stderr[-2000:])
    return out.stdout


def flat_playlist(url: str, limit: int) -> dict:
    """채널 /videos 탭 또는 ytsearch 결과를 빠르게 목록으로."""
    raw = _run(["-J", "--flat-playlist", "--playlist-end", str(limit), url])
    return json.loads(raw) if raw.strip() else {"entries": []}


def video_info(video_id: str) -> dict:
    raw = _run(["-J", "--skip-download", f"https://www.youtube.com/watch?v={video_id}"])
    return json.loads(raw) if raw.strip() else {}


def download_subs(video_id: str, out_dir: Path, lang: str = "ko") -> Path | None:
    out_dir.mkdir(parents=True, exist_ok=True)
    _run([
        "--skip-download", "--write-subs", "--write-auto-subs",
        "--sub-langs", f"{lang}.*,{lang}", "--sub-format", "vtt",
        "-o", str(out_dir / "%(id)s.%(ext)s"),
        f"https://www.youtube.com/watch?v={video_id}",
    ])
    found = sorted(out_dir.glob(f"{video_id}*.vtt"))
    return found[0] if found else None


def download_lowres(video_id: str, out_dir: Path) -> Path | None:
    """컷 분석용 저화질 영상 (분석 후 삭제 권장)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    _run([
        "-f", "worst[height>=240][ext=mp4]/worst",
        "-o", str(out_dir / "%(id)s.%(ext)s"),
        f"https://www.youtube.com/watch?v={video_id}",
    ])
    found = sorted(out_dir.glob(f"{video_id}.*"))
    return found[0] if found else None


_TS = re.compile(r"(\d+):(\d+):(\d+)[.,](\d+)\s+-->\s+(\d+):(\d+):(\d+)[.,](\d+)")


def parse_vtt(path: Path) -> list[dict]:
    """VTT → [{start, end, text}]. 자동자막의 '굴러가는' 중복 줄을 제거한다."""
    cues: list[dict] = []
    cur = None
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = _TS.search(line)
        if m:
            g = list(map(int, m.groups()))
            cur = {"start": g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000,
                   "end": g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000, "lines": []}
            cues.append(cur)
        elif cur is not None and line.strip() and not line.startswith(("WEBVTT", "Kind:", "Language:")):
            cur["lines"].append(re.sub(r"<[^>]+>", "", line).strip())
    out: list[dict] = []
    seen_last = ""
    for c in cues:
        for t in c["lines"]:
            if t and t != seen_last:
                out.append({"start": c["start"], "end": c["end"], "text": t})
                seen_last = t
    return out
