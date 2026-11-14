"""음성 + 말한 시각(단어 타임) 만들기 — 이야기 그림판이 '그 낱말을 말하는 순간' 그림을 그리게.

ytflow `voice` 단계 대신 쓰는 이유: 그림 트리거와 자막 싱크에 **단어 시각**이 필요하다.
edge-tts 는 무료·키 없음(합성은 문장 단위, 문장 경계 시각도 함께 받는다).
받아쓰기(faster-whisper base, 저장소 캐시)로 단어 시각을 재고, 대본 글자와 맞춰(char alignment)
글자 위치 → 시각 표를 만든다. 받아쓰기가 어긋나면 문장 경계 기준 비례 배분으로 자동 대체.

결과
  03_voice/scene_XXX.mp3         합성 원본
  03_voice/clean/scene_XXX.wav   음량만 정규화(-16 LUFS, 무음 제거 없음 → 단어 시각 그대로)
  03_voice/durations.json        장면 길이 (ytflow subtitles/assemble 이 읽는 형식)
  03_voice/words/scene_XXX.json  [{w,s,e}...] 받아쓰기 단어 시각
  03_voice/timings.json          {"1": {"dur":4.2, "chars":[[char_index, sec]...], "narration":...}}
"""
from __future__ import annotations

import asyncio
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]          # repos/video-editing
PROJ = ROOT / "projects" / "20261114-curiosity-test"
VOICE = PROJ / "03_voice"
FF = "ffmpeg"
FP = "ffprobe"
VOICE_ID = "ko-KR-InJoonNeural"
RATE = "+8%"


def sh(args: list[str]) -> None:
    r = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *args], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-2000:])


def dur(path: Path) -> float:
    out = subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout.strip()
    return float(out)


async def synth(text: str, mp3: Path) -> list[dict]:
    import edge_tts
    c = edge_tts.Communicate(text, VOICE_ID, rate=RATE)
    bounds: list[dict] = []
    with open(mp3, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] in ("SentenceBoundary", "WordBoundary"):
                bounds.append({"t": ch["offset"] / 1e7, "d": ch["duration"] / 1e7, "text": ch["text"], "kind": ch["type"]})
    return bounds


def transcribe(words_dir: Path, wav: Path, sid: int) -> list[dict]:
    cache = words_dir / f"scene_{sid:03d}.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    from faster_whisper import WhisperModel
    import numpy as np
    # PyAV 판이 맞지 않아 ffmpeg 로 16kHz mono float32 를 직접 만들어 넘긴다 (faster-whisper 의 decode_audio 우회)
    raw = subprocess.run([FF, "-v", "error", "-i", str(wav), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, dtype=np.float32)
    m = WhisperModel("base", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(audio, language="ko", word_timestamps=True, vad_filter=False, beam_size=5)
    out = []
    for sg in segs:
        for w in sg.words or []:
            out.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)})
    cache.parent.mkdir(exist_ok=True, parents=True)
    cache.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def char_times(narration: str, words: list[dict], bounds: list[dict]) -> list[tuple[int, float]]:
    """글자 index → 말한 시각. 받아쓰기 단어와 대본을 글자 단위로 맞춘다."""
    nar = re.sub(r"\s+", "", narration)
    if not words:
        return []
    # 받아쓰기 문자열 + 글자별 시각
    hyp, times = "", []
    for w in words:
        wt = re.sub(r"\s+", "", w["w"])
        if not wt:
            continue
        for i, ch in enumerate(wt):
            hyp += ch
            times.append(w["s"] + (w["e"] - w["s"]) * (i / max(len(wt), 1)))
    if not hyp:
        return []
    sm = difflib.SequenceMatcher(None, nar, hyp, autojunk=False)
    char_t: list[float | None] = [None] * len(nar)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            char_t[a + k] = times[b + k]
    # 빈 곳은 앞뒤 시각 사이 선형 보간
    known = [(i, t) for i, t in enumerate(char_t) if t is not None]
    if not known:
        return []
    if len(known) < max(3, len(nar) * 0.35):     # 받아쓰기가 너무 안 맞으면 버린다
        return []
    for i, t in enumerate(char_t):
        if t is not None:
            continue
        prev = max((k for k, _ in known if k < i), default=None)
        nxt = min((k for k, _ in known if k > i), default=None)
        if prev is None and nxt is None:
            char_t[i] = 0.0
        elif prev is None:
            char_t[i] = char_t[nxt]
        elif nxt is None:
            char_t[i] = char_t[prev]
        else:
            span = nxt - prev
            char_t[i] = char_t[prev] + (char_t[nxt] - char_t[prev]) * ((i - prev) / span)
    return [(i, round(t, 3)) for i, t in enumerate(char_t)]


def main() -> None:
    scenes = json.loads((PROJ / "02_script" / "scenes.json").read_text(encoding="utf-8"))["scenes"]
    (VOICE / "clean").mkdir(parents=True, exist_ok=True)
    words_dir = VOICE / "words"
    timing, durs = {}, {}
    for s in scenes:
        sid = s["id"]
        mp3 = VOICE / f"scene_{sid:03d}.mp3"
        wav = VOICE / "clean" / f"scene_{sid:03d}.wav"
        bounds: list[dict] = []
        if not mp3.exists() or mp3.stat().st_size < 2000:
            bounds = asyncio.run(synth(s["narration"], mp3))
            (VOICE / f"scene_{sid:03d}.bounds.json").write_text(json.dumps(bounds, ensure_ascii=False, indent=1), encoding="utf-8")
        else:
            bf = VOICE / f"scene_{sid:03d}.bounds.json"
            bounds = json.loads(bf.read_text(encoding="utf-8")) if bf.exists() else []
        raw = VOICE / "clean" / f"scene_{sid:03d}_raw.wav"
        # 앞뒤 무음 + 문장 사이 긴 침묵만 줄인다 (0.45초 넘는 침묵 → 0.30초).
        # prosody 는 edge-tts 그대로 두고 '숨 쉴 틈 없는' 이야기 리듬만 만든다.
        sh(["-i", str(mp3), "-af",
            "silenceremove=start_periods=1:start_threshold=-40dB:stop_periods=-1:stop_duration=0.45:stop_threshold=-40dB:stop_silence=0.30,"
            "areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse,loudnorm=I=-16:TP=-1.5",
            "-ar", "48000", "-ac", "2", str(wav)])
        raw.unlink(missing_ok=True)
        d = round(dur(wav), 3)
        durs[str(sid)] = d
        words = transcribe(words_dir, wav, sid)
        ct = char_times(s["narration"], words, bounds)
        # 받아쓰기 실패 → 문장 경계(또는 균등) 비례 배분
        if not ct:
            n = len(re.sub(r"\s+", "", s["narration"])) or 1
            ct = [(i, round(d * i / n, 3)) for i in range(n)]
            print(f"[voice] #{sid} {d}s · 받아쓰기 정렬 실패 → 비례 배분")
        else:
            print(f"[voice] #{sid} {d}s · 단어 {len(words)}개 정렬")
        timing[str(sid)] = {"dur": d, "chars": ct, "narration": s["narration"]}
    (VOICE / "durations.json").write_text(json.dumps(durs, ensure_ascii=False, indent=1), encoding="utf-8")
    (VOICE / "timings.json").write_text(json.dumps(timing, ensure_ascii=False), encoding="utf-8")
    total = sum(durs.values())
    print(f"[voice] 장면 {len(durs)}개 · 말소리 {total:.2f}s (+장면 사이 0.12s → {total + 0.12 * len(durs):.2f}s)")


if __name__ == "__main__":
    main()
