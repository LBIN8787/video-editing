"""Dispatch an opted-in project to its saved visual edit, irrespective of LLM backend."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from .. import config

ENGINE=Path(__file__).resolve().parents[2]/"scripts"/"script_motion"
MODULES=("render_saved.py","stage_layers.py")

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def render(project):
    script=project.path/"02_script"
    source=script/"motion_source.json"
    manifest=script/"motion_edition.json"
    if not source.exists():
        if manifest.exists():
            raise ValueError("고정 장면표에 대응하는 02_script/motion_source.json이 필요합니다.")
        return None
    spec=json.loads(source.read_text(encoding="utf-8-sig"))
    if not config.DRIVE_DIR:
        raise ValueError("이 편의 매체 묶음에 접근하려면 YTFLOW_DRIVE에 ytflow 폴더 경로를 지정하세요.")
    drive=config.DRIVE_DIR.resolve()
    root=(drive/spec["bundle"]).resolve()
    edition=spec["edition"]
    if not root.is_relative_to(drive) or Path(edition).name!=edition or edition in (".","..",""):
        raise ValueError("잘못된 매체 묶음의 상대 경로")
    if digest(manifest)!=digest(root/edition/"edition.json"):
        raise ValueError("프로젝트와 Drive의 장면표가 서로 다른 판본입니다.")
    runtime=root/"runtime.json"
    if digest(runtime)!=spec["runtime_sha256"]:
        raise ValueError("렌더 입력 목록의 판본이 다릅니다.")
    pins=json.loads(runtime.read_text(encoding="utf-8-sig"))
    for name in MODULES:
        data=(ENGINE/name).read_text(encoding="utf-8-sig").encode()
        if hashlib.sha256(data).hexdigest()!=pins["renderer"][name]:
            raise ValueError(f"렌더러 판본 확인 필요: {name}")
    for rel,h in pins["fonts"].items():
        if digest(root/"fonts"/rel)!=h: raise ValueError(f"글꼴 판본 확인 필요: {rel}")
    subprocess.run([sys.executable,str(ENGINE/"render_saved.py"),str(root),edition],check=True)
    output=root/edition/"review.mp4"
    print(f"[hybrid] 고정 장면표 검토본 → {output}")
    return output
