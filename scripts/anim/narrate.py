"""대본(md) → 초안 목소리(edge-tts, 문장마다) + 낱말 시각(faster-whisper) + 자막(ASS, 어두운 상자).

    python scripts/anim/narrate.py <script.md> <출력 폴더> [--voice ko-KR-InJoonNeural] [--rate +0%]

출력: voice.mp3 · sentences.json([시작, 끝, 문장, 장 번호]) · words.json([시작, 끝, 낱말]) · captions.ass · chapters.json
대본 형식: '## n. 장 제목' 아래 문단들. '**', '---', '# ' 줄은 읽지 않는다.
초안 목소리는 edge-tts, 업로드 최종본은 ElevenLabs (AGENTS.md '목소리').
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
from pathlib import Path

GAP_SENT, GAP_PARA, GAP_CHAP = 0.32, 0.85, 1.6


def parse(md: str):
    chap, out = 0, []   # (장, 문단 시작?, 문장)
    titles = []
    for para in re.split(r"\n\s*\n", md):
        p = para.strip()
        if not p or p.startswith("**") or p.startswith("---") or p.startswith("# "):
            continue
        m = re.match(r"##\s*(\d+)\.\s*(.+)", p)
        if m:   # 제목 줄 바로 아래 문단이 빈 줄 없이 붙어 있어도 읽음
            chap = int(m.group(1))
            head, _, rest = p.partition("\n")
            titles.append(re.match(r"##\s*\d+\.\s*(.+)", head).group(1).strip())
            p = rest.strip()
            if not p:
                continue
        if chap == 0:
            continue
        sents = re.findall(r"[^.?!]+[.?!]+[’'\"」]?|[^.?!]+$", p.replace("\n", " "))
        merged = []   # 따옴표 속 물음표 뒤('…때렸지?' 대신 '…있었어?'라고 …)는 한 문장으로
        for x in (x.strip() for x in sents if x.strip()):
            if merged and re.search(r"[?!]['’\"]$", merged[-1]):
                merged[-1] += " " + x
            else:
                merged.append(x)
        for i, s in enumerate(merged):
            out.append((chap, i == 0, s))
    return out, titles


async def tts(text, path, voice, rate):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=rate).save(str(path))


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout.strip())


def ass_t(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def chunks(s, n=26):
    """자막 한 줄 길이로 끊기(띄어쓰기 기준)."""
    words, out, cur = s.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    # 마지막 조각이 너무 짧으면 앞에 붙임
    if len(out) > 1 and len(out[-1]) < 8:
        last = out.pop()
        out[-1] += " " + last
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--voice", default="ko-KR-InJoonNeural")
    ap.add_argument("--rate", default="+0%")
    a = ap.parse_args()
    out = a.out
    seg = out / "seg"
    seg.mkdir(parents=True, exist_ok=True)
    items, titles = parse(a.script.read_text(encoding="utf-8"))

    async def run_all():
        sem = asyncio.Semaphore(6)

        async def one(i, s):
            p = seg / f"{i:03d}.mp3"
            if not p.exists():
                async with sem:
                    await tts(s, p, a.voice, a.rate)
        await asyncio.gather(*(one(i, s) for i, (_, _, s) in enumerate(items)))
    asyncio.run(run_all())

    # 이어 붙이기: 문장 사이·문단 사이·장 사이 쉼
    t, sents, lst, chap_t = 0.4, [], [], {}
    sil = {}
    def silence(d):
        if d not in sil:
            p = seg / f"sil_{int(d*1000)}.mp3"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(d),
                            "-c:a", "libmp3lame", "-b:a", "48k", str(p)], check=True)
            sil[d] = p
        return sil[d]
    lst.append(silence(0.4))
    prev = None
    for i, (c, first, s) in enumerate(items):
        if prev is not None:
            g = GAP_CHAP if c != prev else (GAP_PARA if first else GAP_SENT)
            lst.append(silence(g))
            t += g
        p = seg / f"{i:03d}.mp3"
        d = dur(p)
        chap_t.setdefault(c, t)
        sents.append([round(t, 3), round(t + d, 3), s, c])
        lst.append(p)
        t += d
        prev = c
    lst.append(silence(1.5))
    t += 1.5
    (out / "concat.txt").write_text("".join(f"file '{p.as_posix()}'\n" for p in lst), encoding="utf-8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(out / "concat.txt"),
                    "-ar", "48000", "-c:a", "libmp3lame", "-b:a", "160k", str(out / "voice.mp3")], check=True)
    total = dur(out / "voice.mp3")
    (out / "sentences.json").write_text(json.dumps(sents, ensure_ascii=False, indent=0), encoding="utf-8")
    (out / "chapters.json").write_text(json.dumps([[round(chap_t[i + 1], 2), ttl] for i, ttl in enumerate(titles)],
                                                  ensure_ascii=False), encoding="utf-8")

    # 낱말 시각 (받아쓰기)
    if (out / "words.json").exists() and (out / "words.json").stat().st_mtime > (out / "voice.mp3").stat().st_mtime:
        words = json.loads((out / "words.json").read_text(encoding="utf-8"))
    else:
        words = whisper(out, " ".join(s for _, _, s in items[:3]))
    write_captions(out, sents)
    print(f"ok {len(sents)} sentences, {len(words)} words, {total:.1f}s")


def whisper(out, prompt=""):
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    import numpy as np   # PyAV 판 차이로 파일 직접 열기가 깨질 때가 있어 ffmpeg 로 16k 배열을 만들어 넘김
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(out / "voice.mp3"), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    segs, _ = m.transcribe(np.frombuffer(raw, np.float32), language="ko", word_timestamps=True, vad_filter=False,
                           initial_prompt=prompt)
    words = [[round(w.start, 3), round(w.end, 3), w.word.strip()] for sg in segs for w in (sg.words or [])]
    (out / "words.json").write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    return words


def write_captions(out, sents):

    # 자막: 문장을 줄 길이로 나누고 글자 수 비율로 시간 배분
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,NanumGothic ExtraBold,50,&H00FFFFFF,&H00FFFFFF,&H64101012,&H64101012,0,0,0,0,100,100,0,0,3,14,0,2,80,80,58,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    for s0, s1, s, _ in sents:
        parts = chunks(s)
        L = sum(len(p) for p in parts)
        x = s0
        for p in parts:
            y = x + (s1 - s0) * len(p) / L
            ev.append(f"Dialogue: 0,{ass_t(x)},{ass_t(y + 0.05)},Sub,,0,0,0,,{p}")
            x = y
    (out / "captions.ass").write_text(head + "\n".join(ev) + "\n", encoding="utf-8-sig")
    print(f"ok {len(sents)} sentences, {len(words)} words, {total:.1f}s")


if __name__ == "__main__":
    main()
