"""설명 무대 시험작 다시 만들기 — 대본 scenes.json → 장면 영상 → (선택) 구성요소 목록 페이지용 짧은 클립·정지 화면.

    python styles/explain-stage/demo/render.py <출력 폴더>               # 5장면 1920x1080 mp4 + 합본 explain_demo.mp4
    python styles/explain-stage/demo/render.py <출력 폴더> --ids 1,4      # 일부만
    python styles/explain-stage/demo/render.py <출력 폴더> --gallery     # + 목록 페이지 미리보기(캐시 ~/.cache/ytflow/looks/explain-*.mp4|jpg)

음성 없이 박자 길이(d)만으로 시간을 잡는다(박자 사이 쉼은 hybrid 기본값). 실제 편에서는 hybrid.json 에 같은 장면을 넣고
`python -m ytflow hybrid <프로젝트>` — 그때는 ElevenLabs/edge-tts 음성 길이와 단어 시각(at)이 쓰인다.
필요: python scripts/install_tools.py (HyperFrames·GSAP·rough.js), ffmpeg, node.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from ytflow.stages import hybrid  # noqa: E402

HERE = Path(__file__).resolve().parent
# 목록 페이지 연출 카드 ↔ 시험작 장면 (연출 id → (장면 id, 클립 시작 초, 길이))
GALLERY = {"afterline": (1, 0.0, 10.0), "spread": (2, 0.0, 13.0), "share": (3, 0.0, 9.5), "motionboard": (4, 0.0, 14.4)}
LOOK_STILL = {"crumpled-paper": (1, 9.5), "dark-stage": (5, 9.5)}   # 화풍 카드 ↔ 정지 화면 (장면 id, 초)


class _Proj:
    def __init__(self, out: Path):
        self.path = out

    def dir(self, k):
        d = self.path / k
        d.mkdir(parents=True, exist_ok=True)
        return d


def render(out: Path, ids: list[int] | None = None) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    scenes = json.loads((HERE / "scenes.json").read_text(encoding="utf-8"))
    spec = {"scenes": scenes, "brand": "market"}
    made = []
    for sc in scenes:
        if ids and sc["id"] not in ids:
            continue
        durs = {f"{sc['id']:03d}_{k}": b.get("d", 3.0) for k, b in enumerate(sc["beats"])}
        bt, dur = hybrid.timing(sc, durs)
        work = out / f"s{sc['id']}"
        hybrid.build_scene(_Proj(out), spec, sc, bt, dur, work)
        mp4 = out / f"s{sc['id']}.mp4"
        err = hybrid.render_scene(work, mp4)
        print(f"#{sc['id']} {sc['type']} {dur:.1f}s {'✗ ' + err if err else 'ok'}")
        if not err:
            made.append(mp4)
    if len(made) > 1:
        lst = out / "list.txt"
        lst.write_text("".join(f"file '{p.name}'\n" for p in made), encoding="utf-8")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-i", str(lst), "-c:v", "libx264", "-crf", "21",
                        "-pix_fmt", "yuv420p", str(out / "explain_demo.mp4")], check=True)
    return made


def gallery(out: Path) -> None:
    """구성요소 목록 페이지가 CSS 흉내 대신 실제 렌더를 보여 주도록 짧은 클립·정지 화면을 캐시에 둔다."""
    from ytflow.stages import looks
    ex = looks.examples_dir() / "scenes"   # 목록 페이지가 media: scenes/<이름>.mp4 로 찾는 곳 (looksgallery._media)
    ex.mkdir(parents=True, exist_ok=True)
    for tid, (sid, ss, t) in GALLERY.items():
        src = out / f"s{sid}.mp4"
        if src.exists():
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(t), "-i", str(src), "-an",
                            "-vf", "fps=15,scale=480:-2", "-c:v", "libx264", "-crf", "30", "-pix_fmt", "yuv420p",
                            "-movflags", "+faststart", str(ex / f"explain-{tid}.mp4")], check=True)
            print(f"  목록 클립 → {ex / f'explain-{tid}.mp4'}")
    for lid, (sid, at) in LOOK_STILL.items():   # 화풍 카드: 완성 구도 4초 (마지막 장면을 천천히)
        src = out / f"s{sid}.mp4"
        if src.exists():
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(max(at - 4, 0)), "-t", "4", "-i", str(src), "-an",
                            "-vf", "fps=15,scale=480:-2", "-c:v", "libx264", "-crf", "30", "-pix_fmt", "yuv420p",
                            "-movflags", "+faststart", str(ex / f"explain-look-{lid}.mp4")], check=True)
            print(f"  목록 화풍 클립 → {ex / f'explain-look-{lid}.mp4'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--ids", default="")
    ap.add_argument("--gallery", action="store_true")
    a = ap.parse_args()
    o = Path(a.out)
    render(o, [int(x) for x in a.ids.split(",") if x] or None)
    if a.gallery:
        gallery(o)
