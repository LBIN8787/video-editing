"""프로젝트(영상 1편) 폴더 구조와 상태·게이트 관리."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from . import config

STAGES = ["discover", "scout", "select", "research", "article", "script", "sources", "clips", "voice", "assets", "subtitles", "assemble", "package", "report"]
# 게이트: 이 단계가 끝난 뒤 사람이 승인해야 다음 단계 진행
GATE_AFTER = {"select": "topic", "script": "script", "assemble": "draft"}

LAYOUT = {
    "source": "00_source",
    "research": "01_research",
    "script": "02_script",
    "voice": "03_voice",
    "assets": "04_assets",
    "edit": "05_edit",
    "package": "06_package",
}


def slugify(s: str) -> str:
    s = re.sub(r"[^\w가-힣]+", "-", s).strip("-").lower()
    return s[:40] or "project"


class Project:
    def __init__(self, path: Path):
        self.path = path
        self.state_file = path / "state.json"
        self.__post_init_override()

    # ---- 생성 / 로드 -------------------------------------------------
    @classmethod
    def create(cls, name: str) -> "Project":
        stamp = datetime.now().strftime("%Y%m%d")
        path = config.PROJECTS_DIR / f"{stamp}-{slugify(name)}"
        n = 2
        while (path / "state.json").exists() and json.loads((path / "state.json").read_text(encoding="utf-8")).get("done"):
            path = config.PROJECTS_DIR / f"{stamp}-{slugify(name)}-{n}"  # 이미 진행한 프로젝트는 덮어쓰지 않는다
            n += 1
        path.mkdir(parents=True, exist_ok=True)
        for d in LAYOUT.values():
            (path / d).mkdir(exist_ok=True)
        p = cls(path)
        if not p.state_file.exists():
            p.save_state({"name": name, "created": datetime.now().isoformat(), "done": [], "approved": []})
        return p

    @classmethod
    def open(cls, name_or_path: str) -> "Project":
        p = Path(name_or_path)
        if not p.exists() and (config.PROJECTS_DIR / name_or_path).is_dir():
            p = config.PROJECTS_DIR / name_or_path  # 폴더 이름이 정확히 같으면 우선
        if not p.exists():
            exact = [m for m in config.PROJECTS_DIR.glob(f"*-{name_or_path}") if m.is_dir()]
            matches = exact or sorted(config.PROJECTS_DIR.glob(f"*{name_or_path}*"))
            if not matches:
                raise SystemExit(f"프로젝트를 찾을 수 없습니다: {name_or_path}")
            p = matches[-1]
        return cls(p)

    def __post_init_override(self):
        config.set_project_override(self.path / "edit.yaml")

    def dir(self, key: str) -> Path:
        return self.path / LAYOUT[key]

    # ---- 상태 --------------------------------------------------------
    def state(self) -> dict:
        return json.loads(self.state_file.read_text(encoding="utf-8"))

    def save_state(self, st: dict) -> None:
        self.state_file.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")

    def mark_done(self, stage: str) -> None:
        st = self.state()
        if stage not in st["done"]:
            st["done"].append(stage)
        self.save_state(st)

    def approve(self, gate: str) -> None:
        st = self.state()
        if gate not in st["approved"]:
            st["approved"].append(gate)
        self.save_state(st)

    def gate_open(self, gate: str) -> bool:
        mode = config.load("pipeline").get("gates", {}).get(gate, "manual")
        return mode == "auto" or gate in self.state()["approved"]

    # ---- 입출력 도우미 ------------------------------------------------
    def write_json(self, key: str, name: str, data) -> Path:
        f = self.dir(key) / name
        f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return f

    def read_json(self, key: str, name: str):
        f = self.dir(key) / name
        if not f.exists():
            raise SystemExit(f"필요한 파일이 없습니다: {f} (이전 단계를 먼저 실행하세요)")
        return json.loads(f.read_text(encoding="utf-8"))
