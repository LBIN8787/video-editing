"""ElevenLabs 문단 음성(b<번호>.mp3) → 단어별 시각(b<번호>.words.json, render_full.py 형식).
ElevenLabs 커넥터는 글자 시각을 주지 않으므로 받아쓰기(faster-whisper) 단어 시각을 원고 글자에 맞춘다(difflib). 자막 비례 배분 금지(2026-11-21 사용자).
python el_align.py <음성 폴더> <beats.json>  → 같은 폴더에 words.json + align_report.json(문단마다 원고·받아쓰기 일치율)"""
import difflib, json, re, subprocess, sys
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

SAY = {"e가": "이가", "텍사스A&M": "텍사스에이앤엠"}   # render_full.py 와 같게(글자 수 맞춤용)
norm = lambda s: re.sub(r"[^0-9A-Za-z가-힣]", "", s)


def pcm(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def main(folder, beats_path):
    folder = Path(folder)
    beats = json.loads(Path(beats_path).read_text(encoding="utf-8"))
    m = WhisperModel("small", device="cpu", compute_type="int8")
    report = []
    for b in beats:
        if b.get("silent"):
            continue
        f = folder / f"b{b['id']:02d}.mp3"
        segs, _ = m.transcribe(pcm(f), language="ko", word_timestamps=True, vad_filter=False)
        ww = [(w.start, w.end, w.word) for s in segs for w in s.words]
        hyp, ht = "", []   # 받아쓰기 글자열과 글자마다 시각
        for a, e, w in ww:
            n = norm(w)
            for k, ch in enumerate(n):
                hyp += ch; ht.append(a + (e - a) * (k + .5) / max(len(n), 1))
        words = []
        for w in b["text"].split():
            for k, v in SAY.items():
                w = w.replace(k, v)
            words.append(w)
        ref = "".join(norm(w) for w in words)
        rt = [None] * len(ref)
        sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
        for i, j, n in sm.get_matching_blocks():
            for k in range(n):
                rt[i + k] = ht[j + k]
        known = [i for i, v in enumerate(rt) if v is not None]
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                   capture_output=True, text=True).stdout)
        for i in range(len(rt)):   # 맞지 않은 글자는 앞뒤 아는 글자 사이를 고르게
            if rt[i] is None:
                lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
                if lo is None and hi is None: rt[i] = dur * i / max(len(rt), 1)
                elif lo is None: rt[i] = rt[hi] * i / max(hi, 1)
                elif hi is None: rt[i] = rt[lo] + (dur - rt[lo]) * (i - lo) / max(len(rt) - lo, 1)
                else: rt[i] = rt[lo] + (rt[hi] - rt[lo]) * (i - lo) / (hi - lo)
        out, p = [], 0
        for w in words:
            n = len(norm(w))
            if n == 0:
                continue
            seg = rt[p:p + n]; p += n
            out.append([round(seg[0] - .06, 3), round(seg[-1] + .06, 3), w])
        f.with_suffix(".words.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
        report.append({"id": b["id"], "match": round(sm.ratio(), 3), "heard": hyp[:200], "text": ref[:200]})
        print(b["id"], round(sm.ratio(), 3), flush=True)
    (folder / "align_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")


main(*sys.argv[1:3])
