#!/usr/bin/env python3
"""매뉴얼 한 명만 고치기 — hook 에서 부르는 가벼운 검사 (docs/35).
  python scripts/manual_guard.py claude-hook   < Claude Code PreToolUse JSON   (막으면 종료 코드 2)
  python scripts/manual_guard.py pre-commit                                      (막으면 종료 코드 1)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ytflow.stages import governance as g  # noqa: E402

mode = sys.argv[1] if len(sys.argv) > 1 else ""
if mode == "claude-hook":
    sys.exit(g.hook_check_stdin())
if mode == "pre-commit":
    sys.exit(g.precommit())
print(g.status())
