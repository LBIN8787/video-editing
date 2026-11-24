"""다큐 장면 시범 렌더 — 이미 목소리가 있는 프로젝트의 한 장면만 다시 렌더해 '전(완성본에서 잘라 냄) / 후(새 장면)'를 나란히 (docs/65).

  python scripts/docu_pilot.py <프로젝트 폴더> <장면 id> <출력 폴더> [--spec 새장면.json] [--final 완성본.mp4]

<프로젝트 폴더> 에는 02_script/hybrid.json·03_voice/hb_<id>_<k>.wav 가 있어야 합니다(원본을 건드리지 않게 복사본에서 실행).
--spec 을 주면 그 장면을 이 JSON 으로 바꿔 렌더합니다(id·chapter 는 원래 것 유지).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def dur_of(p: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project"); ap.add_argument("scene", type=int); ap.add_argument("out")
    ap.add_argument("--spec"); ap.add_argument("--final")
    a = ap.parse_args()
    from ytflow.project import Project
    from ytflow.stages import hybrid
    proj = Project(Path(a.project).resolve())
    spec = json.loads((proj.dir("script") / "hybrid.json").read_text(encoding="utf-8"))
    idx = next(i for i, s in enumerate(spec["scenes"]) if s.get("id") == a.scene)
    old = spec["scenes"][idx]
    if a.spec:
        new = json.loads(Path(a.spec).read_text(encoding="utf-8"))
        for k in ("id", "chapter"):
            new[k] = old.get(k)
        spec["scenes"][idx] = new
    sc = spec["scenes"][idx]
    chapters = {s["chapter"]: s for s in spec["scenes"] if s["type"] == "chapter"}
    ch = chapters.get(sc.get("chapter"))
    if ch:
        sc["_chnum"], sc["_chtitle"] = ch["num"], ch["title"]
    sc["_project_dir"] = str(proj.path)
    vdir = proj.dir("voice")
    durs = {f"{a.scene:03d}_{k}": dur_of(vdir / f"hb_{a.scene:03d}_{k}.wav") for k in range(len(sc["beats"]))}
    bt, dur = hybrid.timing(sc, durs)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    work = out / f"scene_{a.scene:03d}"
    D = hybrid.build_scene(proj, spec, sc, bt, dur, work)
    if sc.get("type") == "docu":   # 검토용: 이 장면의 목표·움직임별 의도 (2026-11-24 사용자: "쓸거면 그 이유와 의도가 명확해야")
        from ytflow.stages import docu
        (out / f"docu_intent_{a.scene:03d}.md").write_text(docu.intents(sc) + "\n", encoding="utf-8")
    if D.qa:
        print("점검:", *D.qa, sep="\n  ")
        if any(str(q).startswith("docu/") for q in D.qa):
            print("의도가 분명하지 않은 다큐 장면은 렌더하지 않습니다 — goal·why_docu·움직임별 why 를 채우세요")
            return 1
    silent = out / f"after_{a.scene:03d}_silent.mp4"
    err = hybrid.render_scene(work, silent)
    if err:
        print("렌더 실패:", err)
        return 1
    # 목소리: 박자 시작 시각에 각 wav 를 놓음
    inputs, filt = [], []
    for k, (t0, _) in enumerate(bt):
        inputs += ["-i", str(vdir / f"hb_{a.scene:03d}_{k}.wav")]
        filt.append(f"[{k + 1}:a]adelay={int(t0 * 1000)}|{int(t0 * 1000)}[a{k}]")
    mix = "".join(f"[a{k}]" for k in range(len(bt))) + f"amix=inputs={len(bt)}:normalize=0[aout]"
    after = out / f"after_{a.scene:03d}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), *inputs, "-filter_complex", ";".join(filt + [mix]),
                    "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-shortest", str(after)], check=True)
    print("후:", after, f"{dur:.1f}초")
    if a.final:   # 전: 완성본에서 같은 장면 구간
        tl = json.loads((proj.dir("edit") / "hybrid_timeline.json").read_text(encoding="utf-8"))
        t = 0.0
        for row in tl:
            if row["scene"] == a.scene:
                before = out / f"before_{a.scene:03d}.mp4"
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", a.final, "-t", f"{row['dur']:.3f}",
                                "-c:v", "libx264", "-crf", "20", "-c:a", "aac", str(before)], check=True)
                side = out / f"compare_{a.scene:03d}.mp4"
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(before), "-i", str(after), "-filter_complex",
                                "[0:v]scale=960:540[l];"
                                "[1:v]scale=960:540[r];"
                                "[l][r]hstack[v]", "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-crf", "22", "-c:a", "aac", "-shortest", str(side)],
                               check=True)
                print("비교:", side)
                break
            t += row["dur"]
    return 0


if __name__ == "__main__":
    sys.exit(main())
