"""화풍·구성요소 목록용 '실제 렌더' 예시 만들기 — 지금까지 영상에 쓴 장면 종류마다 한 장면을 진짜 렌더러(hybrid → HyperFrames)로.

python scripts/looks_catalog.py [--only bars,quote] [--workers 3] [--sec 6]
  → ~/.cache/ytflow/looks/scenes/<종류>.mp4 (640px 미리보기) + scenes.json (어느 프로젝트의 어느 장면인가)
예시는 projects/*/02_script/hybrid.json 에서 그 종류를 처음 쓴 장면을 그대로(박자는 앞 3개만, 박자당 --sec/3 초).
자료 사진·원본 영상이 이 컴퓨터에 없으면 렌더러의 대체 화면이 나온다(그대로 기록).
"""
from __future__ import annotations

import argparse
import copy
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = Path.home() / ".cache" / "ytflow" / "looks" / "scenes"
SKIP = {"intro"}   # 사용자 판정으로 쓰지 않는 장면 (README §2-1 v24)


def samples(only: set[str] | None = None) -> dict:
    """장면 종류 → (프로젝트, 장면) — 가장 최근 프로젝트의 것을 우선."""
    got: dict = {}
    for f in sorted(ROOT.glob("projects/*/02_script/hybrid.json"), reverse=True):
        try:
            spec = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for sc in spec.get("scenes", []):
            t = sc.get("type")
            if not t or t in SKIP or t in got or (only and t not in only):
                continue
            got[t] = (f.parents[1].name, sc)
    return got


# 같은 장면을 바꿔 렌더 — 장 표지 모양·카테고리 구조(증거판·칠판)·그래픽 팩의 그림 슬롯(막대/그림 기호, 사람/네모 칸/도넛 …)
VARIANTS = [
    # (키, 프로젝트, 장면 종류, 바꿀 값)
    ("chapter-board", "20261120-market-deep", "chapter", {"look": "board"}),
    ("chapter-dash", "20261120-market-deep", "chapter", {"look": "dash"}),
    ("chapter-photo", "20261107-knowledge-스페인독감", "chapter", {"look": "photo", "bg": "duotone"}),
    ("chapter-chalk", "20261111-curiosity-hallucination", "chapter", {"look": "chalk"}),
    ("chapter-window", "20261120-market-deep", "chapter", {"look": "window"}),
    ("chapter-paper", "20261107-knowledge-스페인독감", "chapter", {"look": "plain", "skin": "paper-sketch"}),
    ("chapter-type", "20261120-market-deep", "chapter", {"look": "plain", "skin": "clean-flat"}),
    ("board-evidence", "20261120-market-deep", "map_causal", {}),
    ("chalk-causal", "20261111-curiosity-hallucination", "map_causal", {"look": "", "bg": "chalk", "skin": "chalkboard"}),
    ("map_causal-paper", "20261107-knowledge-스페인독감", "map_causal", {}),
    ("compare-bars", "20261120-market-deep", "bars", {"skin": "clean-flat"}),
    ("compare-pictogram", "20261120-market-deep", "bars", {"skin": "dark-doc"}),
    ("proportion-people", "20261107-knowledge-스페인독감", "people", {}),
    ("proportion-waffle", "20261107-knowledge-스페인독감", "people", {"skin": "newsprint"}),
    ("proportion-donut", "20261107-knowledge-스페인독감", "people", {"skin": "midnight"}),
    ("flow-sticky", "20261107-knowledge-스페인독감", "map_causal", {"skin": "dark-doc"}),
    ("flow-pill", "20261107-knowledge-스페인독감", "map_causal", {"skin": "slate"}),
]


def variant_samples(only: set[str] | None = None) -> dict:
    got = {}
    for key, name, typ, over in VARIANTS:
        if only and key not in only:
            continue
        f = ROOT / "projects" / name / "02_script" / "hybrid.json"
        try:
            spec = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        sc = next((x for x in spec.get("scenes", []) if x.get("type") == typ), None)
        if sc:
            sc = copy.deepcopy(sc)
            for k, v in over.items():
                if v == "":
                    sc.pop(k, None)
                else:
                    sc[k] = v
            got[key] = (name, sc)
    return got


def _features(sc: dict) -> list[str]:
    ks = []
    for l in sc.get("layers") or []:
        if isinstance(l, dict) and l.get("kind"):
            ks.append("layer-" + l["kind"])
    fx = sc.get("fx")
    for f in (fx if isinstance(fx, list) else [fx] if isinstance(fx, (str, dict)) else []):
        k = f if isinstance(f, str) else (f or {}).get("kind")
        if k:
            ks.append("fx-" + k)
    for b in sc.get("beats") or []:
        ms = b.get("motion")
        for m in (ms if isinstance(ms, list) else [ms] if isinstance(ms, dict) else []):
            if isinstance(m, dict) and m.get("do"):
                ks.append("motion-" + m["do"])
    return ks


def feature_samples(only: set[str] | None = None) -> dict:
    """겹치기(layers)·장면 효과(fx)·박자 motion 마다 그것을 처음 쓴 장면 (가장 최근 프로젝트부터)."""
    got = {}
    for f in sorted(ROOT.glob("projects/*/02_script/hybrid.json"), reverse=True):
        try:
            spec = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for sc in spec.get("scenes", []):
            for k in _features(sc):
                if k not in got and (not only or k in only):
                    c = copy.deepcopy(sc)
                    if k.startswith("motion-"):   # 그 박자가 잘리지 않게: 그 박자와 앞 박자만
                        bs = c.get("beats") or []
                        i = next((j for j, b in enumerate(bs) if k[7:] in json.dumps(b.get("motion"), ensure_ascii=False)), 0)
                        c["beats"] = bs[max(0, i - 1):i + 1]
                    got[k] = (f.parents[1].name, c)
    return got


def build(name: str, sc: dict, sec: float, work: Path):
    from ytflow.project import Project
    from ytflow.stages import hybrid
    project = Project.open(name)
    spec = json.loads((project.dir("script") / "hybrid.json").read_text(encoding="utf-8"))
    sc = copy.deepcopy(sc)
    beats = (sc.get("beats") or [{"say": ""}])[:3]
    sc["beats"] = beats
    per = sec / max(1, len(beats))
    bt, t = [], hybrid.LEAD
    for _ in beats:
        bt.append((round(t, 2), per - hybrid.GAP))
        t += per
    dur = round(t - hybrid.GAP + hybrid.TAIL, 2)
    chapters = {x["chapter"]: x for x in spec["scenes"] if x.get("type") == "chapter"}
    ch = chapters.get(sc.get("chapter"))
    if ch and sc["type"] != "chapter":
        sc["_chnum"], sc["_chtitle"] = ch.get("num", ""), ch.get("title", "")
    if sc.get("type") == "bite":   # 원본 발언: 원본이 없으면 렌더러처럼 인용 카드로
        spec["scenes"] = [sc]
        hybrid.bite_fallback(project, spec)
        if sc.get("type") == "quote":
            sc.pop("clip", None)
    # 이 컴퓨터에 자료 영상·사진이 없으면 대체 영상(Mixkit 무료 클립)으로 — 예시에 '대체 자료' 표시
    fdir = project.dir("assets") / "footage"
    placeholder = None
    if spec.get("footage"):
        missing = [k for k, v in spec["footage"].items() if not (fdir / str(v.get("file", ""))).exists()]
        if missing:
            src = Path.home() / ".cache" / "ytflow" / "looks" / "footage_src.mp4"
            fdir.mkdir(parents=True, exist_ok=True)
            placeholder = fdir / "_catalog_placeholder.mp4"
            shutil.copy(src, placeholder)
            for k in missing:
                spec["footage"][k] = dict(spec["footage"][k], file=placeholder.name)
            sc["_placeholder"] = True
    try:
        hybrid.build_scene(project, spec, sc, bt, dur, work)
    finally:
        if placeholder and placeholder.exists():
            placeholder.unlink()
    return bool(sc.get("_placeholder"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--sec", type=float, default=6.0)
    ap.add_argument("--variants", action="store_true", help="장 표지 모양·카테고리 구조·그림 슬롯 변형만")
    ap.add_argument("--features", action="store_true", help="겹치기·장면 효과·박자 motion 마다 그것을 쓴 장면")
    a = ap.parse_args()
    from ytflow.stages import hybrid
    OUT.mkdir(parents=True, exist_ok=True)
    only = set(a.only.split(",")) if a.only else None
    todo, meta = [], {}
    mp = OUT / "scenes.json"
    if mp.exists():
        meta = json.loads(mp.read_text(encoding="utf-8"))
    for t, (name, sc) in (variant_samples(only) if a.variants else feature_samples(only) if a.features else samples(only)).items():
        work = OUT / "work" / t
        if work.exists():
            shutil.rmtree(work)
        try:   # 장면 HTML 은 한 번에 하나씩 (그래픽 팩·글꼴이 전역 설정)
            ph = build(name, sc, a.sec, work)
            todo.append((t, name, work))
            meta.setdefault("_placeholder", {})[t] = ph
            print(f"[catalog] {t:12s} ← {name}")
        except Exception as e:   # noqa: BLE001
            print(f"[catalog] {t:12s} ✗ 만들기: {e}")
            meta[t] = {"project": name, "error": str(e)[:200]}

    def render(item):
        t, name, work = item
        full = work / "full.mp4"
        err = hybrid.render_scene(work, full)
        if err or not full.exists():
            return t, name, err or "렌더 실패"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(full), "-vf", "scale=640:-2,fps=24", "-an",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "30", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                        str(OUT / f"{t}.mp4")], check=True)
        return t, name, ""

    with ThreadPoolExecutor(a.workers) as ex:
        for t, name, err in ex.map(render, todo):
            meta[t] = {"project": name, "file": f"{t}.mp4", "placeholder": meta.get("_placeholder", {}).get(t, False)} if not err else {"project": name, "error": err[:200]}
            print(f"[catalog] {t:12s} {'✗ ' + err[:120] if err else 'ok'}")
    meta.pop("_placeholder", None)
    mp.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
