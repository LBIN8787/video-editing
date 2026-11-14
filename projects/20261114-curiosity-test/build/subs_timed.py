"""자막을 '말한 시각'으로 다시 박는다 — 03_voice/timings.json (받아쓰기 단어 정렬) 사용.

`ytflow ... subtitles` 단계는 장면 길이를 글자 수 비례로 나눠 자막 시각을 잡는다.
이야기 그림판은 그림·자막이 모두 '그 낱말을 말하는 순간'에 맞아야 하므로,
같은 줄 나눔(media.chunk_text)으로 줄을 만들되 시작·끝 시각은 글자별 시각표에서 가져온다.
스타일 머리글은 `subtitles` 단계가 만든 subs.ass 에서 그대로 가져와 쓴다.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJ = ROOT / "projects" / "20261114-curiosity-test"
SRC = PROJ / "02_script" / "scenes.json"
TIM = PROJ / "03_voice" / "timings.json"
ASS = PROJ / "05_edit" / "subs.ass"
SRT = PROJ / "05_edit" / "subs.srt"
EMPH = "&H0066D9FF"      # paper 스타일 강조색(연노랑) — config/pipeline.yaml
SUB = "&H00FFFFFF"


def ts_ass(t: float) -> str:
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def ts_srt(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def chunk(text: str, mx: int = 24) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > mx:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
        if re.search(r"[.?!]$", cur):
            lines.append(cur)
            cur = ""
    if cur:
        lines.append(cur)
    return lines


def main() -> None:
    scenes = json.loads(SRC.read_text(encoding="utf-8"))["scenes"]
    tim = json.loads(TIM.read_text(encoding="utf-8"))
    header = ASS.read_text(encoding="utf-8").split("[Events]")[0] + "[Events]\n"
    ev, srt, n = [], [], 1
    t_scene = 0.0
    for s in scenes:
        d = tim[str(s["id"])]["dur"]
        ct = tim[str(s["id"])]["chars"]
        nar = re.sub(r"\s+", "", s["narration"])
        # 글자 index → 시각
        cmap = {i: v for i, v in ct}
        lines = chunk(s["narration"], 24)
        # 줄의 첫 글자 위치(공백 제외 기준 누적)
        pos, spans = 0, []
        for ln in lines:
            flat = re.sub(r"\s+", "", ln)
            idx = nar.find(flat, pos)
            idx = pos if idx < 0 else idx
            spans.append((idx, idx + len(flat)))
            pos = idx + len(flat)
        for li, ln in enumerate(lines):
            a0, a1 = spans[li]
            t0 = cmap.get(a0, t_scene)
            t1 = cmap.get(a1, t_scene + d) if li + 1 < len(lines) else t_scene + d
            if t1 <= t0:
                t1 = t0 + max(0.6, len(ln) * 0.12)
            t0 = t_scene + max(0.0, t0 - 0.04)
            t1 = t_scene + min(d, t1 + 0.12)
            styled = ln
            for w in sorted(s.get("emphasis") or [], key=len, reverse=True):
                if w and w in styled:
                    styled = styled.replace(w, f"{{\\c{EMPH}}}{w}{{\\c{SUB}}}", 1)
            ev.append(f"Dialogue: 0,{ts_ass(t0)},{ts_ass(t1)},SubBox,,0,0,0,,{ln}")
            ev.append(f"Dialogue: 1,{ts_ass(t0)},{ts_ass(t1)},SubText,,0,0,0,,{styled}")
            srt.append(f"{n}\n{ts_srt(t0)} --> {ts_srt(t1)}\n{ln}\n")
            n += 1
        t_scene += d + 0.12
    ASS.write_text(header + "\n".join(ev) + "\n", encoding="utf-8")
    SRT.write_text("\n".join(srt) + "\n", encoding="utf-8")
    print(f"[subs] {n - 1}줄 · 마지막 {t_scene:.2f}s → {ASS.name}, {SRT.name}")


if __name__ == "__main__":
    main()
