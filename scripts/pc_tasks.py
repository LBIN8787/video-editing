"""PC 할 일 알림 — 로컬(PC) 세션이 시작될 때 inbox/pc-tasks 의 pending 을 보여 줌 (클라우드 세션에서는 조용히).
python scripts/pc_tasks.py [--all]"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def pending() -> list[tuple[str, str]]:
    out = []
    for f in sorted((ROOT / "inbox" / "pc-tasks").glob("*.md")):
        if f.name == "README.md":
            continue
        t = f.read_text(encoding="utf-8")
        if re.search(r"^status:\s*pending", t, re.M):
            ty = (re.search(r"^type:\s*(\S+)", t, re.M) or [None, "?"])[1]
            out.append((f.name, ty))
    return out


if __name__ == "__main__":
    if os.environ.get("CLAUDE_CODE_REMOTE") == "true" and "--all" not in sys.argv:
        sys.exit(0)   # 클라우드는 PC 할 일을 처리하지 못함
    p = pending()
    if p:
        print(f"PC 할 일 {len(p)}건 (inbox/pc-tasks) — 먼저 처리할 수 있으면 처리: " + ", ".join(f"{n} [{t}]" for n, t in p))
