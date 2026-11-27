"""대사별 무료 음성(edge-tts) → 이어 붙인 voice.wav + 박자 시간표.
사용: python voice.py <lines.json> <작업폴더> [--voice ko-KR-InJoonNeural] [--rate +32%]
lines.json 옆에 timeline.json 을 쓴다. 장 첫 줄(`ch` 가 있는 줄) 앞에는 쉼을 조금 더 둔다."""
import argparse, asyncio, json, pathlib, subprocess
import edge_tts
ap = argparse.ArgumentParser(); ap.add_argument("lines"); ap.add_argument("out")
ap.add_argument("--voice", default="ko-KR-InJoonNeural"); ap.add_argument("--rate", default="+32%")
ap.add_argument("--gap", type=float, default=0.24); ap.add_argument("--chgap", type=float, default=0.9); ap.add_argument("--lead", type=float, default=0.8)
a = ap.parse_args(); LP = pathlib.Path(a.lines); OUT = pathlib.Path(a.out); OUT.mkdir(parents=True, exist_ok=True)
lines = json.loads(LP.read_text(encoding="utf-8"))
def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode())
async def main():
    t, tl, parts = a.lead, [], []
    for i, l in enumerate(lines):
        p = OUT / f"{l['id']}.mp3"
        meta = OUT / f"{l['id']}.txt"
        if not p.exists() or not meta.exists() or meta.read_text(encoding="utf-8") != l["t"] + a.voice + a.rate:
            await edge_tts.Communicate(l["t"], a.voice, rate=a.rate).save(str(p)); meta.write_text(l["t"] + a.voice + a.rate, encoding="utf-8")
        if "ch" in l and i > 0: t += a.chgap
        d = dur(p); tl.append({**l, "start": round(t, 3), "end": round(t + d, 3)}); parts.append((p, t)); t += d + a.gap
    total = t + 2.5
    inputs, filt = [], []
    for k, (p, st) in enumerate(parts):
        inputs += ["-i", str(p)]; filt.append(f"[{k}]adelay={int(st*1000)}|{int(st*1000)}[a{k}]")
    filt.append("".join(f"[a{k}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad=whole_dur={total}[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "44100", "-ac", "2", str(OUT / "voice.wav")], check=True)
    (LP.parent / "timeline.json").write_text(json.dumps({"total": round(total, 2), "lines": tl}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("total", round(total, 1), "s")
asyncio.run(main())
