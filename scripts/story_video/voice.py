"""대본(script.md) → 무료 edge-tts 낭독(문장별 단어 시각 포함) + timeline.json.
python voice.py <script.md> <out_dir> [voice]
timeline: {"duration", "events":[{"kind":"say","i","text","start","end","words":[[w,s,e],..]}, {"kind":"chapter","title","start","end"}, {"kind":"section","name","start"}]}
"""
import asyncio, json, re, subprocess, sys, pathlib
import edge_tts

SRC = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2]); VOICE = sys.argv[3] if len(sys.argv) > 3 else "ko-KR-InJoonNeural"
PARTS = OUT / "parts"; PARTS.mkdir(parents=True, exist_ok=True)
RATE = {"가장 느리게": "-12%", "느리게": "-8%", "또박또박": "-6%", "차분하게": "-6%", "보통": "+0%", "빠르게": "+6%"}
SR = 24000

def parse():
    text = SRC.read_text(encoding="utf-8").split("## 대본 점검")[0]
    items, rate = [], "+0%"
    for line in text.split("\n"):
        s = line.strip()
        if not s: continue
        if s.startswith("### "):
            tempo = s.split("·")[-1]
            rate = next((v for k, v in RATE.items() if k in tempo.split("→")[0]), "+0%")
            items += [("section", s[4:].split("(")[0].strip()), ("gap", 0.8)]; continue
        if s.startswith("⟪"):
            items.append(("chapter", s.strip("⟪⟫ ").replace("페이지 넘김 — ", ""), 1.6)); continue
        if s.startswith(("🎨", "📷", "🗺", "📄", "---", "#", "템플릿:", "표기:", "화풍:", "|")): continue
        m = re.match(r"\((?:쉼|무음) (\d+)초\)(.*)", s)
        if m:
            items.append(("gap", float(m.group(1))))
            if "빠르게" in m.group(2): rate = RATE["빠르게"]
            elif "느리게" in m.group(2): rate = RATE["느리게"]
            continue
        if s.startswith("("): continue
        if s.startswith("▣"):
            q = re.search(r"(검은 화면 한 줄|밑줄 인용[^:]*): \"(.+)\"", s)
            if q: items += [("gap", 0.6), ("say", q.group(2), rate), ("gap", 0.8)]
            continue
        s = re.sub(r"\s*\[F[^\]]*\]|\s*🔍", "", s); s = re.sub(r"\s*·\s*(느리게|빠르게|보통).*$", "", s)
        if s: items.append(("say", s, rate))
    return items

async def tts(i, t, r):
    mp3, js = PARTS / f"{i:03d}.mp3", PARTS / f"{i:03d}.json"
    if mp3.exists() and js.exists(): return mp3, json.loads(js.read_text(encoding="utf-8"))
    words, audio = [], bytearray()
    async for ch in edge_tts.Communicate(t, VOICE, rate=r, boundary="WordBoundary").stream():
        if ch["type"] == "audio": audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            words.append([ch["text"], ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7])
    mp3.write_bytes(bytes(audio)); js.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    return mp3, words

def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)

async def main():
    items = parse(); events = []; t = 0.0; rows = []; n = 0
    def gap(sec):
        nonlocal t
        g = PARTS / f"gap_{sec:.2f}.wav"
        if not g.exists(): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{sec}", str(g)], check=True)
        rows.append(g); t += sec
    for it in items:
        if it[0] == "section": events.append({"kind": "section", "name": it[1], "start": round(t, 3)})
        elif it[0] == "chapter":
            events.append({"kind": "chapter", "title": it[1], "start": round(t, 3), "end": round(t + it[2], 3)}); gap(it[2])
        elif it[0] == "gap": gap(it[1])
        else:
            mp3, words = await tts(len(rows), it[1], it[2])
            wav = mp3.with_suffix(".wav")
            if not wav.exists(): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3), "-ar", str(SR), "-ac", "1", str(wav)], check=True)
            d = dur(wav)
            events.append({"kind": "say", "i": n, "text": it[1], "start": round(t, 3), "end": round(t + d, 3),
                           "words": [[w, round(t + s, 3), round(t + e, 3)] for w, s, e in words]})
            rows.append(wav); t += d; n += 1
            gap(0.35)
    gap(1.0)
    lst = OUT / "list.txt"; lst.write_text("\n".join(f"file '{r.resolve().as_posix()}'" for r in rows), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "pcm_s16le", str(OUT / "narration.wav")], check=True)
    real = dur(OUT / "narration.wav")
    (OUT / "timeline.json").write_text(json.dumps({"duration": round(real, 3), "events": events}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"sentences={n} computed={t:.1f}s wav={real:.1f}s words_missing={sum(1 for e in events if e['kind']=='say' and not e['words'])}")

asyncio.run(main())
