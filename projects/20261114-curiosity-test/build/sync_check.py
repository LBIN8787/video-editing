"""완성본 싱크 점검 — 받아쓰기(faster-whisper base)로 자막이 말보다 얼마나 앞/뒤에 뜨는지 잰다.

`python -m ytflow sync-qa` 와 같은 목적이지만, 이 컨테이너의 PyAV 판이 faster-whisper 의
decode_audio 와 맞지 않아(metadata_errors 인자) ffmpeg 로 16kHz 를 직접 만들어 넘긴다.
결과: 05_edit/sync_qa.json
"""
from __future__ import annotations

import difflib
import json
import re
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJ = ROOT / "projects" / "20261114-curiosity-test"
ED = PROJ / "05_edit"
FF = "ffmpeg"


def t_sec(s: str) -> float:
    h, m, x = s.split(":")
    return int(h) * 3600 + int(m) * 60 + float(x)


def audio(path: Path) -> np.ndarray:
    raw = subprocess.run([FF, "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def dur(path: Path, stream: str) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream, "-show_entries", "stream=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def main() -> None:
    from faster_whisper import WhisperModel
    final = ED / "final.mp4"
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(audio(final), language="ko", word_timestamps=True, vad_filter=False, beam_size=5)
    words = []
    for sg in segs:
        for w in sg.words or []:
            words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)})
    hyp, times = "", []
    for w in words:
        wt = re.sub(r"\s+", "", w["w"])
        for i, ch in enumerate(wt):
            hyp += ch
            times.append(w["s"] + (w["e"] - w["s"]) * (i / max(len(wt), 1)))
    lines = []
    for ln in (ED / "subs.ass").read_text(encoding="utf-8").splitlines():
        if not ln.startswith("Dialogue:") or "SubBox" not in ln:
            continue
        parts = ln.split(",", 9)
        lines.append({"start": t_sec(parts[1]), "end": t_sec(parts[2]), "text": parts[9].strip()})
    rows = []
    for r in lines:
        tgt = re.sub(r"\s+", "", r["text"])
        sm = difflib.SequenceMatcher(None, tgt, hyp, autojunk=False)
        best = None
        for a, b, n in sm.get_matching_blocks():
            if n >= max(3, int(len(tgt) * 0.6)):
                best = times[b + (0 if a == 0 else 0)]
                break
        if best is None:
            m = sm.find_longest_match(0, len(tgt), 0, len(hyp))
            best = times[m.b + max(0, min(m.size - 1, 0))] if m.size >= 2 else None
        if best is None:
            continue
        rows.append({"sub": r["text"], "t_sub": round(r["start"], 2), "t_say": round(best, 2),
                     "diff": round(r["start"] - best, 2)})
    diffs = [abs(r["diff"]) for r in rows]
    res = {
        "lines": len(rows),
        "median_abs": round(float(np.median(diffs)), 3) if diffs else None,
        "max_abs": round(max(diffs), 3) if diffs else None,
        "within_0.5": round(sum(d < 0.5 for d in diffs) / max(len(diffs), 1), 3),
        "over_0.3": [r for r in rows if abs(r["diff"]) > 0.3],
        "video": round(dur(final, "v:0"), 3),
        "audio": round(dur(final, "a:0"), 3),
        "rows": rows,
    }
    (ED / "sync_qa.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[sync] {res['lines']}줄 · 중앙 {res['median_abs']}초 · 최대 {res['max_abs']}초 · "
          f"0.5초 이내 {res['within_0.5'] * 100:.0f}% · 화면 {res['video']}s / 소리 {res['audio']}s")


if __name__ == "__main__":
    main()
