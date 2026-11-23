"""skills/ (원본) → .claude/skills/ (Claude Code) · .agents/skills/ (Codex) 로 복사한다.

    python scripts/sync_skills.py          # 복사
    python scripts/sync_skills.py --check  # 어긋났는지만 확인 (CI·커밋 전)

심볼릭 링크 대신 복사하는 이유: Windows 에서 git 심볼릭 링크가 일반 파일로 풀리는 문제를 피하려고.
"""
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "skills"
TARGETS = [ROOT / ".claude" / "skills", ROOT / ".agents" / "skills"]


def external() -> set:
    """scripts/install_tools.py 가 넣은 외부 skill 은 지우지 않는다 (tools/external.json)."""
    import json
    f = ROOT / "tools" / "external.json"
    if not f.exists():
        return set()
    out = set()
    for t in json.loads(f.read_text(encoding="utf-8"))["tools"]:
        out |= {t["name"] if r == "." else Path(r).name for r in t.get("skills", [])}
    return out


def main(check: bool) -> int:
    bad = 0
    for tgt in TARGETS:
        for skill in sorted(p for p in SRC.iterdir() if (p / "SKILL.md").exists()):
            dst = tgt / skill.name
            same = dst.exists() and not filecmp.dircmp(skill, dst).diff_files and \
                not filecmp.dircmp(skill, dst).left_only and not filecmp.dircmp(skill, dst).right_only
            if check:
                if not same:
                    print(f"어긋남: {dst.relative_to(ROOT)}")
                    bad += 1
                continue
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(skill, dst)
        if not check:
            for old in tgt.iterdir() if tgt.exists() else []:
                if not (SRC / old.name / "SKILL.md").exists() and old.name not in external():
                    shutil.rmtree(old)
            print(f"동기화: {tgt.relative_to(ROOT)} ({len(list(tgt.iterdir()))}개)")
    if check:
        print("✓ 동기화됨" if not bad else f"✗ {bad}개 어긋남 → python scripts/sync_skills.py")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
