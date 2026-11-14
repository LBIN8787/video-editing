"""편집 타임라인 만들기 — 장면 길이 = 말소리 + 숨 고르는 시간(gap).

`ytflow subtitles` 단계는 gap 을 0.12초로 고정하지만, v2 는 장면마다 0.4~0.8초를 숨 고르는 데 쓴다.
그래서 대본(scenes.json)의 gap 과 목소리 길이(03_voice/timings.json)를 그대로 더해
05_edit/timeline.json 을 만든다(assemble 단계가 이 파일을 읽는다).

    python3 build/timeline.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJ = ROOT / "projects" / "20261114-curiosity-test"


def main() -> None:
    scenes = json.loads((PROJ / "02_script" / "scenes.json").read_text(encoding="utf-8"))["scenes"]
    tim = json.loads((PROJ / "03_voice" / "timings.json").read_text(encoding="utf-8"))
    rows, t = [], 0.0
    for s in scenes:
        d = float(tim[str(s["id"])]["dur"]) + float(s.get("gap", 0.12))
        rows.append({"scene": s["id"], "start": round(t, 3), "duration": round(d, 3),
                     "section": s.get("section", ""), "visual_type": s.get("visual_type", "card"),
                     "visual_brief": s.get("visual_brief", ""), "sfx": ""})
        t += d
    (PROJ / "05_edit" / "timeline.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[timeline] 장면 {len(rows)}개 · 총 {t:.2f}s")


if __name__ == "__main__":
    main()
