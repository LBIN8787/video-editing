"""같은 이야기(같은 문장·같은 목소리·같은 자료 화면)를 다른 연출로 다시 짠 시험작 프로젝트를 만든다.

    python scripts/style_demo.py <원본 프로젝트> <시험작 이름> <연출 스펙.json>
    python -m ytflow hybrid <시험작 프로젝트>

스펙: {"skin": "<그래픽 팩>", "scenes": [{"type": ..., ..., "beats": [{"from": "005_1", ...}]}], "footage": ["march", ...]}
- 박자의 "from": "<원본 장면>_<박자>" → 그 문장(say)과 음성 파일(03_voice/hb_*.wav)을 그대로 가져온다 (목소리 비용 0).
- 연출 장면 type 은 기존(hybrid.py)이든 새 것(directions.py: kb·card_type·journey·kinetic)이든 쓸 수 있다.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(src_name: str, demo_name: str, spec_path: str) -> Path:
    src = ROOT / "projects" / src_name
    dst = ROOT / "projects" / demo_name
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    sh = json.loads((src / "02_script" / "hybrid.json").read_text(encoding="utf-8"))
    say = {f"{s['id']:03d}_{k}": b["say"] for s in sh["scenes"] for k, b in enumerate(s["beats"])}
    for d in ("02_script", "03_voice", "04_assets/footage", "05_edit"):
        (dst / d).mkdir(parents=True, exist_ok=True)
    scenes = []
    for i, sc in enumerate(spec["scenes"], 1):
        sc = dict(sc, id=i)
        beats = []
        for k, b in enumerate(sc["beats"]):
            b = dict(b)
            if b.get("from"):
                key = b.pop("from")
                b["say"] = say[key]
                w = src / "03_voice" / f"hb_{key}.wav"
                tgt = dst / "03_voice" / f"hb_{i:03d}_{k}.wav"
                if w.exists() and not tgt.exists():
                    shutil.copy2(w, tgt)
            beats.append(b)
        sc["beats"] = beats
        scenes.append(sc)
    out = {k: v for k, v in sh.items() if k not in ("scenes", "package")}
    out["scenes"] = scenes
    out["footage"] = {k: v for k, v in sh["footage"].items() if k in spec.get("footage", sh["footage"].keys())}
    for k, v in out["footage"].items():
        f = dst / "04_assets" / "footage" / v["file"]
        if not f.exists():
            try:
                os.link(src / "04_assets" / "footage" / v["file"], f)
            except OSError:
                shutil.copy2(src / "04_assets" / "footage" / v["file"], f)
    if spec.get("map"):
        out["map"] = spec["map"]
    (dst / "02_script" / "hybrid.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    (dst / "02_script" / "demo_spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    (dst / "edit.yaml").write_text(
        f"# 연출 시험작: {spec.get('direction', '')} · 원본 {src_name} (같은 문장·목소리·자료 화면)\n"
        f"edit:\n  style: hybrid\n  style_ref: hybrid\n  family: source\n  skin: {spec['skin']}\n"
        f"channel: {spec.get('channel', 'ch-knowledge')}\nformat: longform\n", encoding="utf-8")
    (dst / "state.json").write_text(json.dumps({"name": demo_name, "created": dt.datetime.now().isoformat(),
                                                "done": ["script"], "approved": [], "demo_of": src_name}, ensure_ascii=False, indent=2),
                                    encoding="utf-8")
    print(f"[style-demo] {dst} ({len(scenes)}장면, 그래픽 팩 {spec['skin']})")
    return dst


if __name__ == "__main__":
    main(*sys.argv[1:4])
