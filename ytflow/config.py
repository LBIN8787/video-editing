from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
PROMPT_DIR = ROOT / "prompts"
DATA_DIR = ROOT / "data"          # 벤치마킹 원자료 / 스타일 프로필
PROJECTS_DIR = ROOT / "projects"  # 영상 1편 = 프로젝트 폴더 1개
STYLES_DIR = ROOT / "styles"      # 편집 스타일 라이브러리 (스타일 1개 = 폴더 1개)


_OVERRIDE: dict = {}


def set_project_override(path: Path) -> None:
    """프로젝트 폴더의 edit.yaml 을 pipeline.yaml 위에 덮어쓴다 (예: style: paper)."""
    global _OVERRIDE
    _OVERRIDE = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}) if path.exists() else {}


def _merge(a: dict, b: dict) -> dict:
    out = dict(a)
    for k, v in b.items():
        out[k] = _merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def load(name: str) -> dict:
    with open(CONFIG_DIR / f"{name}.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if name == "pipeline":
        data = _merge(data, _OVERRIDE)
        style = (data.get("edit") or {}).get("style", "sixsigma")
        # styles.<이름> 블록이 있으면 edit 위에 겹친다 → 스타일 전환이 한 줄로 끝난다
        data["edit"] = _merge(data.get("edit") or {}, (data.get("styles") or {}).get(style) or {})
        data["edit"]["style"] = style
    return data


def prompt(name: str) -> str:
    return (PROMPT_DIR / f"{name}.md").read_text(encoding="utf-8")


def style_profile() -> dict:
    """benchmark 단계가 만든 스타일 프로필. 없으면 빈 dict."""
    import json

    p = DATA_DIR / "style_profile.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


# 편집 스타일 계열: 대본의 화면 문법과 점검 기준이 계열마다 다르다
FAMILIES = {
    "source": "원본 소스형 — 인터뷰·실적발표·키노트 원본 영상 + 자막 + 중간 핵심요약 애니메이션 (식스시그마)",
    "infographic": "자체 제작 인포그래픽형 — 도식·차트·비유 그림을 직접 그려 설명 (미주일기, 머니크루)",
    "shorts": "세로 쇼츠 — 9:16, 고정 훅 + 큰 자막",
}
_RENDERER_FAMILY = {"sixsigma": "source", "paper": "infographic", "flat": "infographic", "shorts": "shorts"}


def style_family(edit: dict | None = None) -> str:
    """edit.family 가 있으면 그것, 없으면 렌더러로 추정 (sixsigma→source, paper·flat→infographic)."""
    edit = edit if edit is not None else (load("pipeline").get("edit") or {})
    return edit.get("family") or _RENDERER_FAMILY.get(edit.get("style", ""), "source")
