"""화풍 목록 (styles/looks.yaml): 모션그래픽·삽화·실사 색보정을 영상마다 고르는 자리.

무엇으로 보여 줄지(실사·모션그래픽·삽화)는 박자가 하는 일이 정하고(manual/12 §0-1), 여기서는 '어떻게 보일지'만 고릅니다.
프로젝트 edit.yaml 의  look: {motion: <id>, illust: <id>, footage: <id>}
  motion  → 그래픽 스킨 (config.load('pipeline') 이 edit.skin 으로 바꿈, edit.yaml 에 skin 을 직접 적으면 그것이 우선)
  illust  → 그림 주문서 화풍 문장 (imagegen.run, art_plan.json 의 style 이 우선)
  footage → 실사 클립 색보정 ffmpeg 필터 (footage_vf)
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
FILE = ROOT / "styles" / "looks.yaml"
KINDS = {"motion": "모션그래픽 화풍", "illust": "삽화 화풍", "footage": "실사 색보정"}
STATUS = {"approved": "합격", "trial": "시안", "available": "사용 가능"}


def load() -> dict:
    return yaml.safe_load(FILE.read_text(encoding="utf-8")) or {}


def get(kind: str, look_id: str) -> dict | None:
    return (load().get(kind) or {}).get(look_id)


def skin_for(look_id: str) -> str:
    d = get("motion", look_id) or {}
    return d.get("skin") or ""


def project_look(project_dir: Path) -> dict:
    p = Path(project_dir) / "edit.yaml"
    d = (yaml.safe_load(p.read_text(encoding="utf-8")) or {}) if p.exists() else {}
    return d.get("look") or (d.get("edit") or {}).get("look") or {}


def illust_prompt(project_dir: Path) -> str:
    lid = project_look(project_dir).get("illust")
    return ((get("illust", lid) or {}).get("prompt") or "") if lid else ""


def footage_vf(project_dir: Path, default: str = "warm-doc") -> str:
    lid = project_look(project_dir).get("footage") or default
    return (get("footage", lid) or {}).get("vf", "")


def listing(kind: str | None = None) -> str:
    data = load()
    out = []
    for k, title in KINDS.items():
        if kind and k != kind:
            continue
        out += [f"## {title} ({k})", "", "| id | 이름 | 모습 | 어울리는 상황 | 피할 때 | 상태 |", "|---|---|---|---|---|---|"]
        for lid, d in (data.get(k) or {}).items():
            out.append(f"| `{lid}` | {d.get('name', '')} | {d.get('look', '')} | {d.get('fits', '')} | {d.get('avoid', '')} | "
                       f"{STATUS.get(d.get('status', ''), d.get('status', ''))} |")
        out.append("")
    out.append("고르기: python -m ytflow look <프로젝트> --motion <id> --illust <id> --footage <id>")
    return "\n".join(out)


def choose(project_dir: Path, motion: str = "", illust: str = "", footage: str = "") -> dict:
    """edit.yaml 의 look 을 바꾸고 지금 값을 돌려줌. 없는 id 는 거절."""
    data = load()
    for k, v in (("motion", motion), ("illust", illust), ("footage", footage)):
        if v and v not in (data.get(k) or {}):
            raise SystemExit(f"[look] '{v}' 는 {KINDS[k]} 목록에 없습니다 — python -m ytflow looks --kind {k}")
    p = Path(project_dir) / "edit.yaml"
    d = (yaml.safe_load(p.read_text(encoding="utf-8")) or {}) if p.exists() else {}
    lk = dict(d.get("look") or {})
    for k, v in (("motion", motion), ("illust", illust), ("footage", footage)):
        if v:
            lk[k] = v
    if motion or illust or footage:
        d["look"] = lk
        p.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return lk
