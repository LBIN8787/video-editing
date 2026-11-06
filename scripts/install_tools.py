"""외부 영상편집 도구·skill 설치 (고정 버전). 목록은 tools/external.json.

    python scripts/install_tools.py          # 설치 (이미 있으면 건너뜀)
    python scripts/install_tools.py --force  # 다시 설치

- 도구 본체는 tools/<이름>/ 에 (저장소에 올리지 않음, .gitignore)
- 그 도구의 agent skill 은 .claude/skills/ 와 .agents/skills/ 에 복사 (Claude Code·Codex 가 같이 읽음)
- 버전은 2주 이상 지난 릴리스로 고정합니다. 올릴 때는 tools/external.json 을 고치고 SKILL.md 를 다시 읽어 봅니다.
- HyperFrames 사용 통계는 ytflow 가 HYPERFRAMES_NO_TELEMETRY=1 로 끕니다.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
SKILL_DIRS = [ROOT / ".claude" / "skills", ROOT / ".agents" / "skills"]


def run(cmd, cwd=None):
    print("  $", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def install(t: dict, force: bool) -> None:
    dst = TOOLS / t["name"]
    if dst.exists() and not force:
        print(f"= {t['name']} (설치돼 있음)")
    else:
        if dst.exists():
            shutil.rmtree(dst)
        dst.mkdir(parents=True)
        print(f"+ {t['name']}")
        if t["kind"] == "npm":
            (dst / "package.json").write_text(json.dumps({"name": f"ytflow-{t['name']}", "private": True}), encoding="utf-8")
            run(["npm", "install", "--no-audit", "--no-fund", "--ignore-scripts", *t["packages"]], cwd=dst)
        elif t["kind"] == "git":
            run(["git", "clone", "-q", "--filter=blob:none", "--no-checkout", t["repo"], str(dst)])
            run(["git", "checkout", "-q", t["commit"]], cwd=dst)
    # agent skill 복사 (git 저장소의 skill 폴더, npm 도구는 skills_repo 의 태그에서)
    src_root = dst
    tmp = None
    if t.get("skills_repo"):
        tmp = Path(tempfile.mkdtemp())
        run(["git", "clone", "-q", "--depth", "1", "--branch", t["skills_ref"], t["skills_repo"], str(tmp / "r")],)
        src_root = tmp / "r"
    for rel in t.get("skills", []):
        src = src_root / rel
        for sd in SKILL_DIRS:
            out = sd / Path(rel).name if rel != "." else sd / t["name"]
            if out.exists():
                shutil.rmtree(out)
            if t.get("include"):  # 저장소 전체가 skill 인 경우 필요한 것만
                out.mkdir(parents=True)
                for name in t["include"]:
                    (shutil.copytree if (src / name).is_dir() else shutil.copy)(src / name, out / name)
            else:
                shutil.copytree(src, out, ignore=shutil.ignore_patterns(".git", "tests", "evals", "node_modules"))
        print(f"  skill → {Path(rel).name if rel != '.' else t['name']}")
    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)


def main(force: bool) -> None:
    spec = json.loads((TOOLS / "external.json").read_text(encoding="utf-8"))
    for t in spec["tools"]:
        install(t, force)
    print("완료. 확인: python -m ytflow tools")


if __name__ == "__main__":
    main("--force" in sys.argv)
