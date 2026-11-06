"""원본 발언 구간을 단어 단위로 정확히 자른다 (faster-whisper, MIT).

원본 소스형(식스시그마식) 영상의 quote 장면은 '그 말'만 들려줘야 한다. YouTube 자막 시각은 몇 초씩 어긋나므로,
받은 클립(앞뒤 여유 포함)을 받아쓰기해 단어마다 시각을 얻고, 대본의 quote_en 과 가장 잘 맞는 구간을 찾아 다시 자른다.

- 쓰는 곳: clips 단계 (사용자 PC 의 rebuild 에서 YouTube 클립을 받은 직후). 클립이 없으면 아무것도 안 한다.
- 모델: config/pipeline.yaml → align.model (기본 small, CPU int8). 처음 실행 때 Hugging Face 에서 내려받아 캐시.
- 더 정밀하게: WhisperX(BSD-2, 음소 정렬)를 쓰려면 align.engine: whisperx (선택 설치, torch 필요).
"""
from __future__ import annotations

import json
import re
import subprocess
from difflib import SequenceMatcher
from pathlib import Path

from .. import config

_models: dict = {}


def available() -> bool:
    try:
        import faster_whisper  # noqa: F401
        return True
    except Exception:
        return False


def _cfg() -> dict:
    return {"model": "small", "compute_type": "int8", "pad_before": 0.15, "pad_after": 0.30, "min_score": 0.6,
            **(config.load("pipeline").get("align") or {})}


def _audio(path: Path):
    """ffmpeg 로 16kHz 모노 파형을 직접 읽는다 (PyAV 버전 차이를 피함: 윈도우·맥·리눅스 같은 결과)."""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path), "-f", "s16le", "-ac", "1",
                          "-ar", "16000", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def transcribe(path: Path, language: str | None = None) -> list[dict]:
    """단어 단위 받아쓰기. 결과는 <파일>.words.json 으로 캐시."""
    cache = path.with_suffix(".words.json")
    if cache.exists() and cache.stat().st_mtime >= path.stat().st_mtime:
        return json.loads(cache.read_text(encoding="utf-8"))
    from faster_whisper import WhisperModel
    c = _cfg()
    key = (c["model"], c["compute_type"])
    if key not in _models:
        _models[key] = WhisperModel(c["model"], device="cpu", compute_type=c["compute_type"])
    segs, _ = _models[key].transcribe(_audio(path), language=language, word_timestamps=True, vad_filter=True)
    words = [{"start": round(float(w.start), 3), "end": round(float(w.end), 3), "word": w.word.strip()}
             for s in segs for w in (s.words or [])]
    cache.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    return words


def _norm(t: str) -> str:
    return re.sub(r"[^a-z0-9가-힣]", "", t.lower())


def find_quote(words: list[dict], quote: str) -> tuple[float, float, float] | None:
    """quote 와 가장 비슷한 연속 단어 구간 → (시작초, 끝초, 일치도 0~1)."""
    q = [_norm(t) for t in quote.split() if _norm(t)]
    w = [_norm(x["word"]) for x in words]
    if not q or not w:
        return None
    best = (0.0, 0, 0)
    n = len(q)
    for size in range(max(1, n - 3), n + 4):
        for i in range(0, max(1, len(w) - size + 1)):
            sc = SequenceMatcher(None, q, w[i:i + size]).ratio()
            if sc > best[0]:
                best = (sc, i, i + size - 1)
    sc, i, j = best
    j = min(j, len(words) - 1)
    return words[i]["start"], words[j]["end"], sc


def refine(clip: Path, quote: str, language: str | None = "en") -> tuple[bool, str]:
    """clip 을 quote 구간만 남기도록 다시 자른다. (성공 여부, 메모)"""
    if not quote or not clip.exists() or not available():
        return False, "정렬 생략"
    c = _cfg()
    hit = find_quote(transcribe(clip, language), quote)
    if not hit or hit[2] < c["min_score"]:
        return False, f"발언을 찾지 못함 (일치도 {hit[2] if hit else 0:.2f})"
    st, en, sc = hit
    st, en = max(0.0, st - c["pad_before"]), en + c["pad_after"]
    tmp = clip.with_name(clip.stem + "_aligned.mp4")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{st:.3f}", "-i", str(clip), "-t", f"{en - st:.3f}",
                    "-c:v", "libx264", "-preset", "veryfast", "-c:a", "aac", str(tmp)], check=True)
    tmp.replace(clip)
    clip.with_suffix(".words.json").unlink(missing_ok=True)
    return True, f"단어 정렬 {st:.2f}~{en:.2f}s (일치도 {sc:.2f})"
