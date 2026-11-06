# CLAUDE.md

이 저장소의 작업 규칙은 모든 에이전트 공통으로 AGENTS.md 에 있습니다.

@AGENTS.md

## Claude Code 에서만
- 스킬은 `.claude/skills/` 에서 자동으로 읽힙니다(원본 `skills/`, 동기화 `python scripts/sync_skills.py`).
- 구독으로 파이프라인을 돌리려면 `llm.backend: claude-cli` 를 쓰세요. 이 세션 안에서 직접 판단하려면 `YTFLOW_LLM_BACKEND=manual` 을 쓰세요.
