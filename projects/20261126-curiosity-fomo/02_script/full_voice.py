"""초안 목소리(edge-tts): full_beats.json → <폴더>/b<번호>.mp3 + b<번호>.words.json(단어별 시각, 자막용 — 비례 배분 금지). python full_voice.py <폴더> [목소리] [속도]"""
import asyncio, json, os, sys
from pathlib import Path
import edge_tts
HERE = Path(__file__).resolve().parent
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
VOICE = sys.argv[2] if len(sys.argv) > 2 else "ko-KR-InJoonNeural"
RATE = sys.argv[3] if len(sys.argv) > 3 else "+4%"
SAY = {"1,099명에게": "천구십구 명에게", "3.6명": "삼 점 육 명", "48퍼센트": "사십팔 퍼센트", "31퍼센트": "삼십일 퍼센트", "389명": "삼백팔십구 명", "229명": "이백이십구 명", "600명": "육백 명", "4명이": "네 명이", "ㅋㅋ'": "'"}   # 읽기만 바꿈(자막은 원문) — render_full.py 와 같게
async def one(b, sem):
    if b.get("silent"):
        return
    f = out / f"b{b['id']:02d}.mp3"
    wj = f.with_suffix(".words.json")
    if f.exists() and wj.exists(): return
    t = b["text"]
    for k, v in SAY.items(): t = t.replace(k, v)
    async with sem:
        words, audio = [], bytearray()
        async for ch in edge_tts.Communicate(t, VOICE, rate=RATE, boundary="WordBoundary").stream():
            if ch["type"] == "audio": audio += ch["data"]
            elif ch["type"] == "WordBoundary":
                words.append([round(ch["offset"] / 1e7, 3), round((ch["offset"] + ch["duration"]) / 1e7, 3), ch["text"]])
        f.write_bytes(audio); wj.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
async def main():
    sem = asyncio.Semaphore(6)
    await asyncio.gather(*[one(b, sem) for b in json.loads((HERE / os.environ.get("BEATS", "full_beats.json")).read_text(encoding="utf-8"))])
asyncio.run(main()); print("ok", len(list(out.glob("b*.mp3"))))
