"""대사별 edge-tts → 이어 붙인 내레이션 + 박자 시간표(timeline.json). 사용: python make_voice.py <출력폴더>"""
import asyncio, json, subprocess, sys, pathlib
import edge_tts
HERE = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
VOICE, RATE, GAP, LEAD = "ko-KR-InJoonNeural", "+32%", 0.24, 0.8
lines = json.loads((HERE / "lines.json").read_text(encoding="utf-8"))

async def tts(i, t):
    p = OUT / f"l{i:02d}.mp3"
    if not p.exists():
        await edge_tts.Communicate(t, VOICE, rate=RATE).save(str(p))
    return p

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode())

async def main():
    paths = [await tts(i, l["t"]) for i, l in enumerate(lines)]
    t, tl, parts = LEAD, [], []
    for l, p in zip(lines, paths):
        d = dur(p); tl.append({"id": l["id"], "t": l["t"], "start": round(t, 3), "end": round(t + d, 3)}); parts.append((p, t)); t += d + GAP
    total = t + 2.0
    inputs, filt = [], []
    for k, (p, st) in enumerate(parts):
        inputs += ["-i", str(p)]; filt.append(f"[{k}]adelay={int(st*1000)}|{int(st*1000)}[a{k}]")
    filt.append("".join(f"[a{k}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad=whole_dur={total}[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "44100", "-ac", "2", str(OUT / "voice.wav")], check=True)
    (HERE / "timeline.json").write_text(json.dumps({"total": round(total, 2), "lines": tl}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("total", round(total, 1), "s")
asyncio.run(main())
