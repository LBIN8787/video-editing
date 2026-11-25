"""대본 조각 → 초안 목소리(edge-tts) — 템포 표시를 소리로 옮긴다 (시범작, 2026-11-26).

    python scripts/anim/tempo_vo.py <lines_src.json> <출력 폴더>

lines_src.json: {"voice": "ko-KR-InJoonNeural", "rates": {"<장>": "-6%"}, "lines": [{"ch": 2, "text": "… (쉼) … (긴 쉼)"}]}
- 문장 안의 (쉼)·(긴 쉼)에서 조각을 나누고, 조각 뒤에 쉼을 둔다 (쉼 0.45초, 긴 쉼 1.1초, 표시 없으면 0.22초).
- 장마다 빠르기(rates)를 다르게 준다. 사용자 11-25: "영상에 따라 템포조절이 중요".
출력: <폴더>/assets/vo/p00.mp3 … · lines.json([{i, ch, text, file, dur, pause}])
"""
import asyncio, json, re, subprocess, sys
from pathlib import Path
import edge_tts

PAUSE = {"(쉼)": 0.45, "(긴 쉼)": 1.1}
BASE = 0.22


def split(text):
    out, buf = [], ""
    for tok in re.split(r"(\(긴 쉼\)|\(쉼\))", text):
        if tok in PAUSE:
            if buf.strip():
                out.append([buf.strip(), PAUSE[tok]])
            elif out:
                out[-1][1] = max(out[-1][1], PAUSE[tok])
            else:
                out.append(["", PAUSE[tok]])   # 맨 앞 쉼
            buf = ""
        else:
            buf += tok
    if buf.strip():
        out.append([buf.strip(), BASE])
    return out


async def main(src, dst):
    cfg = json.loads(Path(src).read_text(encoding="utf-8"))
    vo = Path(dst) / "assets" / "vo"; vo.mkdir(parents=True, exist_ok=True)
    L, k = [], 0
    for ln in cfg["lines"]:
        for text, pause in split(ln["text"]):
            if not text:
                if L: L[-1]["pause"] = max(L[-1]["pause"], pause)
                continue
            f = f"p{k:02d}.mp3"
            rate = cfg.get("rates", {}).get(str(ln["ch"]), cfg.get("rate", "+0%"))
            await edge_tts.Communicate(text, cfg["voice"], rate=rate).save(str(vo / f))
            d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(vo / f)],
                                     capture_output=True, text=True).stdout)
            L.append({"i": k, "ch": ln["ch"], "text": text, "file": f, "dur": round(d, 3), "pause": pause, "rate": rate})
            k += 1
    (Path(dst) / "assets" / "vo" / "lines.json").write_text(json.dumps(L, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(L), "조각", round(sum(x["dur"] + x["pause"] for x in L), 1), "초")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))
