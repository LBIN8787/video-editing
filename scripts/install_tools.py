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
    if t["kind"] == "skill":  # 본체 없이 skill 폴더만 (저장소가 크고 skill 이 곧 도구일 때)
        return install_skill_only(t, force)
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


def set_description(skill_md: Path, desc: str) -> None:
    """SKILL.md 머리(frontmatter)의 description 만 바꿈 (여러 줄 description 도 통째로)."""
    import re
    text = skill_md.read_text(encoding="utf-8")
    head, sep, body = text[4:].partition("\n---")
    lines, out, skip = head.split("\n"), [], False
    for ln in lines:
        if skip and (ln.startswith((" ", "\t")) or not ln.strip()):
            continue
        skip = False
        if re.match(r"^description\s*:", ln):
            out.append("description: " + json.dumps(desc, ensure_ascii=False))
            skip = True
            continue
        out.append(ln)
    skill_md.write_text("---\n" + "\n".join(out) + sep + body, encoding="utf-8")


def install_skill_only(t: dict, force: bool) -> None:
    """고정 태그를 임시로 얕게 받아 skill 폴더의 include 만 복사 (tools/ 에 본체를 두지 않음)."""
    outs = [sd / Path(rel).name for rel in t["skills"] for sd in SKILL_DIRS]
    if all(o.exists() for o in outs) and not force:
        print(f"= {t['name']} (설치돼 있음)")
        return
    print(f"+ {t['name']} ({t.get('ref') or t['commit']})")
    tmp = Path(tempfile.mkdtemp())
    try:
        if t.get("ref"):  # 태그
            run(["git", "clone", "-q", "--depth", "1", "--branch", t["ref"], t["repo"], str(tmp / "r")])
        else:  # 태그 없는 저장소는 커밋으로
            run(["git", "clone", "-q", "--filter=blob:none", "--no-checkout", t["repo"], str(tmp / "r")])
            run(["git", "checkout", "-q", t["commit"]], cwd=tmp / "r")
        got = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=tmp / "r", capture_output=True, text=True).stdout.strip()
        if t.get("commit") and not t["commit"].startswith(got) and not got.startswith(t["commit"]):
            raise SystemExit(f"  ! {t['name']}: 태그 {t['ref']} 가 {got} 를 가리킴 (고정값 {t['commit']}) — 다시 검토하세요")
        for rel in t["skills"]:
            src = tmp / "r" / rel
            for sd in SKILL_DIRS:
                out = sd / Path(rel).name
                if out.exists():
                    shutil.rmtree(out)
                out.mkdir(parents=True)
                for name in t.get("include") or [p.name for p in src.iterdir()]:
                    (shutil.copytree if (src / name).is_dir() else shutil.copy)(src / name, out / name)
                desc = (t.get("description_override") or {}).get(Path(rel).name)
                if desc:  # 호출 조건이 너무 넓은 skill 은 설명을 좁혀 우리 skill 과 겹치지 않게
                    set_description(out / "SKILL.md", desc)
            print(f"  skill → {Path(rel).name}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main(force: bool) -> None:
    spec = json.loads((TOOLS / "external.json").read_text(encoding="utf-8"))
    for t in spec["tools"]:
        install(t, force)
    print("완료. 확인: python -m ytflow tools")


if __name__ == "__main__":
    main("--force" in sys.argv)
