"""긴 내레이션 음성(ElevenLabs 웹·커넥터로 만든 mp3 등)을 대본 박자(beat)별 파일로 자른다.

    python -m ytflow voice-import <프로젝트> part1.mp3 [part2.mp3 ...]

- 파일들을 순서대로 이어 붙인 뒤 faster-whisper 로 단어 시각을 받는다.
- 대본(02_script/hybrid.json) 글자열과 받아쓰기 글자열을 글자 단위로 맞춰(difflib) 박자 끝 단어를 찾고,
  그 근처(앞뒤 2단어)에서 **가장 긴 쉼**의 가운데를 자르는 점으로 고른다 (문단 사이 쉼이 가장 길다).
- 결과: 03_voice/hb_<장면>_<박자>.wav (앞뒤 무음 정리, 48kHz 스테레오). 원래 있던 파일은 03_voice/edge/ 로 옮긴다.
- 그 뒤 `python -m ytflow hybrid <프로젝트>` 로 다시 만들면 새 목소리 길이에 맞춰 화면·자막이 따라간다.
API 키가 없어도 된다 (ElevenLabs 웹/커넥터에서 받은 파일을 넣으면 됨).
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from ..project import Project
from . import align

FF = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]


def _beats(project: Project) -> list[tuple[str, str]]:
    d = json.loads((project.dir("script") / "hybrid.json").read_text(encoding="utf-8"))
    return [(f"{sc['id']:03d}_{k}", b["say"]) for sc in d["scenes"] for k, b in enumerate(sc["beats"])]


def run(project: Project, parts: list[str], beats: list[tuple[str, str]] | None = None) -> list[str]:
    beats = beats or _beats(project)
    vdir = project.dir("voice")
    work = vdir / "el"
    work.mkdir(parents=True, exist_ok=True)
    whole = work / "whole.wav"
    lst = work / "parts.txt"
    lst.write_text("\n".join(f"file '{Path(p).resolve()}'" for p in parts), encoding="utf-8")
    subprocess.run(FF + ["-f", "concat", "-safe", "0", "-i", str(lst), "-ar", "48000", "-ac", "2", str(whole)], check=True)
    words = align.transcribe(whole, "ko")
    norm = align._norm
    wl = [(w["start"], w["end"], len(norm(w["word"]))) for w in words if norm(w["word"])]
    # 대본 글자열 S 와 받아쓰기 글자열 R 을 글자 단위로 맞춘다 (difflib). R 의 각 글자는 몇 번째 단어인지 안다.
    import difflib
    R, owner = "", []
    for wi, w in enumerate(words):
        t = norm(w["word"])
        R += t
        owner += [wi] * len(t)
    S = "".join(norm(sv) for _, sv in beats)
    ends, acc = [], 0
    for _, sv in beats:
        acc += len(norm(sv))
        ends.append(acc)
    blocks = [b for b in difflib.SequenceMatcher(None, S, R, autojunk=False).get_matching_blocks() if b.size]

    def s2r(p: int) -> int:  # 대본 글자 위치 → 받아쓰기 글자 위치 (맞는 구간 안이면 정확히, 아니면 앞뒤 구간 사이 비례)
        prev = (0, 0)
        for b in blocks:
            if b.a <= p < b.a + b.size:
                return b.b + (p - b.a)
            if b.a > p:
                a0, r0 = prev
                return r0 + int((p - a0) * max(b.b - r0, 0) / max(b.a - a0, 1))
            prev = (b.a + b.size, b.b + b.size)
        return len(R) - 1

    W = [(float(w["start"]), float(w["end"])) for w in words]
    cuts, last = [0.0], -1
    for k in range(len(beats) - 1):
        r = min(max(s2r(ends[k]) - 1, 0), len(owner) - 1)
        i = owner[r]                                  # 이 박자의 마지막 단어
        lo, hi = max(last + 1, i - 2), min(len(W) - 2, i + 2)
        if lo > hi:
            lo = hi = min(max(last + 1, i), len(W) - 2)
        best = max(range(lo, hi + 1), key=lambda j: (W[j + 1][0] - W[j][1]) - 0.05 * abs(j - i))  # 가장 긴 쉼
        last = best
        cuts.append((W[best][1] + W[best + 1][0]) / 2)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(whole)],
                               capture_output=True, text=True).stdout)
    cuts.append(dur)
    bak = vdir / "edge"
    bak.mkdir(exist_ok=True)
    out = []
    for k, (key, say) in enumerate(beats):
        wav = vdir / f"hb_{key}.wav"
        if wav.exists() and not (bak / wav.name).exists():
            shutil.move(str(wav), bak / wav.name)
        for side in (vdir / f"hb_{key}.words.json", vdir / f"hb_{key}.mp3"):
            if side.exists():
                side.unlink()
        a, b = cuts[k], cuts[k + 1]
        subprocess.run(FF + ["-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", str(whole), "-af",
                             "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                             "-ar", "48000", "-ac", "2", str(wav)], check=True)
        out.append(f"{key}\t{a:7.2f}–{b:7.2f}\t{say[:30]}")
    (work / "cuts.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"[voice-import] {len(beats)}박자로 자름 → {vdir} (자른 위치: {work / 'cuts.txt'})")
    return out
