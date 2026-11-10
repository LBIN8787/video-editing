"""완성 영상의 자막·목소리·화면 싱크 점검 (사람 귀 대신 받아쓰기로 잰다).

    python -m ytflow sync-qa <프로젝트>

1. final.mp4 의 소리를 faster-whisper 로 받아써서 단어마다 실제 말한 시각을 얻는다.
2. subs.ass 의 자막 줄마다 '그 줄 첫 글자를 실제로 말하기 시작한 시각'을 찾는다 (글자 단위 맞추기, difflib).
3. 자막이 뜨는 시각 − 말하기 시작한 시각 = 어긋남. +면 자막이 늦음, −면 자막이 빠름.
4. 영상 길이와 소리 길이 차이(화면 밀림)도 잰다.
결과: 05_edit/sync_qa.json — 중앙값·최대·0.3초 넘게 어긋난 줄. 기준: |어긋남| ≤ 0.5초가 95% 이상 + 화면−소리 0.1초 이내면 통과 (받아쓰기 시각 오차 감안).
"""
from __future__ import annotations

import difflib
import json
import re
import subprocess

from ..project import Project
from . import align


def _t(s: str) -> float:
    h, m, x = s.split(":")
    return int(h) * 3600 + int(m) * 60 + float(x)


def _dur(path, stream: str) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream, "-show_entries", "stream=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def _words_windowed(wav, win: float = 25.0) -> list[dict]:
    """긴 소리는 VAD 를 켜면 시각이 밀리는 경우가 있어, 25초 창으로 잘라 VAD 없이 받아쓰고 시각을 더한다."""
    from faster_whisper import WhisperModel
    audio = align._audio(wav)
    c = align._cfg()
    key = (c["model"], c["compute_type"])
    if key not in align._models:
        align._models[key] = WhisperModel(c["model"], device="cpu", compute_type=c["compute_type"])
    model, out, sr = align._models[key], [], 16000
    step, lead = int((win - 6) * sr), 3.0   # 6초 겹치게 자르고, 창 앞 3초·뒤 3초 단어는 옆 창 것을 씀 (창 경계에서 시각이 틀어짐)
    for k in range(0, len(audio), step):
        segs, _ = model.transcribe(audio[k:k + int(win * sr)], language="ko", word_timestamps=True, vad_filter=False)
        lo = k / sr + (lead if k else 0.0)
        hi = k / sr + win - lead
        for sg in segs:
            for w in (sg.words or []):
                t = k / sr + float(w.start)
                if lo <= t < hi or (k + step >= len(audio) and t >= lo):
                    out.append({"start": t, "end": k / sr + float(w.end), "word": w.word.strip()})
    return out


def run(project: Project) -> dict:
    edir = project.dir("edit")
    final = edir / "final.mp4"
    lines = []
    for ln in (edir / "subs.ass").read_text(encoding="utf-8").splitlines():
        if ln.startswith("Dialogue:"):
            f = ln.split(",", 9)
            lines.append((_t(f[1]), _t(f[2]), f[9]))
    wav = edir / "hb_work" / "final_audio.wav"
    wav.parent.mkdir(parents=True, exist_ok=True)
    voice = edir / "hb_work" / "voice.wav"   # 배경음이 있으면 쉼이 묻혀 받아쓰기·쉼 찾기가 흔들림 → 섞기 전 내레이션으로 잼 (시간축은 완성본과 같음)
    src = voice if voice.exists() and voice.stat().st_mtime >= final.stat().st_mtime - 3600 else final
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
    words = _words_windowed(wav)
    norm = align._norm
    R, owner = "", []
    for wi, w in enumerate(words):
        t = norm(w["word"])
        R += t
        owner += [wi] * len(t)
    S, starts = "", []
    for a, b, text in lines:
        starts.append(len(S))
        S += norm(text)
    sm = difflib.SequenceMatcher(None, S, R, autojunk=False)
    m = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            m[blk.a + k] = blk.b + k
    # 받아쓰기는 문장 앞의 쉼(무음) 속으로 시작점을 당겨 잡는 일이 있다 → 실제 말소리 시작(무음 끝)으로 보정
    sil = []
    pr = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(wav), "-af", "silencedetect=n=-35dB:d=0.2", "-f", "null", "-"],
                        capture_output=True, text=True)
    st = None
    for ln in pr.stderr.splitlines():
        if "silence_start:" in ln:
            st = float(ln.split("silence_start:")[1].split()[0])
        elif "silence_end:" in ln and st is not None:
            sil.append((st, float(ln.split("silence_end:")[1].split()[0])))
            st = None

    def onset(t):
        for s0, e0 in sil:
            if s0 - 0.3 <= t < e0 - 0.05 and e0 - t <= 1.5:
                return e0
        return t

    rows = []
    for (a, b, text), p in zip(lines, starts):
        n = len(norm(text))
        hit = next((m[q] for q in range(p, p + min(n, 4)) if q in m), None)  # 줄 앞 4글자 안에서 맞는 글자
        if hit is None:
            continue
        spoken = float(words[owner[hit]]["start"])
        spoken = onset(spoken)
        rows.append({"sub": round(a, 2), "spoken": round(spoken, 2), "off": round(a - spoken, 2), "text": text[:30]})
    offs = sorted(abs(r["off"]) for r in rows)
    res = {
        "lines": len(lines), "measured": len(rows),
        "median_abs_offset": offs[len(offs) // 2] if offs else None,
        "p95_abs_offset": offs[int(len(offs) * 0.95)] if offs else None,
        "within_0_3s": round(sum(o <= 0.3 for o in offs) / len(offs), 3) if offs else None,
        "video_minus_audio_s": round(_dur(final, "v:0") - _dur(final, "a:0"), 3),
        "worst": sorted(rows, key=lambda r: -abs(r["off"]))[:8],
    }
    res["within_0_5s"] = round(sum(o <= 0.5 for o in offs) / len(offs), 3) if offs else None
    # 받아쓰기 단어 시각 자체가 음악·효과음이 섞인 완성본에서 ±0.3~0.5초 흔들림 → 0.5초 이내 95% 를 기준으로
    res["pass"] = bool(res["within_0_5s"] and res["within_0_5s"] >= 0.95 and abs(res["video_minus_audio_s"]) <= 0.1)
    (edir / "sync_qa.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[sync-qa] 자막 {res['measured']}/{res['lines']}줄 · 어긋남 중앙값 {res['median_abs_offset']}s · 95% {res['p95_abs_offset']}s · "
          f"0.3초 이내 {res['within_0_3s']} · 화면−소리 {res['video_minus_audio_s']}s → {'통과' if res['pass'] else '확인 필요'}")
    return res
