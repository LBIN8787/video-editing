from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
PROMPT_DIR = ROOT / "prompts"
DATA_DIR = ROOT / "data"          # 벤치마킹 원자료 / 스타일 프로필
PROJECTS_DIR = ROOT / "projects"  # 영상 1편 = 프로젝트 폴더 1개


def load(name: str) -> dict:
    with open(CONFIG_DIR / f"{name}.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def prompt(name: str) -> str:
    return (PROMPT_DIR / f"{name}.md").read_text(encoding="utf-8")


def style_profile() -> dict:
    """benchmark 단계가 만든 스타일 프로필. 없으면 빈 dict."""
    import json

    p = DATA_DIR / "style_profile.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
