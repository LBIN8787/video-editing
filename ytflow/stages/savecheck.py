"""SAVE(오선) 소식 확인 — 주식 채널 소스 확보의 기본 점검 (2026-11-14 사용자: "오선의 save 를 활용하여 여기 소식은 기본적으로 확인").

SAVE: '투자의 모든 소식, 이제 한 곳에서' (Fivelines, 앱 + 웹 https://www.saveticker.com) — 글로벌 속보·기업 리포트·경제 지표·일정 요약.

자동으로 읽지 않습니다:
- 웹은 Cloudflare 봇 확인(403 "Just a moment")이 걸려 있고, robots.txt 가 AI 수집기(ClaudeBot·anthropic-ai·GPTBot 등)를 막고 `ai-train=no, use=reference` 를 밝힘.
- → 우회·비공개 API 호출 금지. **사람이 앱/웹에서 확인**하고 그 결과를 적는다.

흐름:
1. `python -m ytflow daily --project <날짜>-market-daily` 가 `01_research/save_check.md` (확인 표) 를 만든다.
2. 사람이 SAVE 를 보고 표를 채운다. 또는 저장소 `inbox/save/<YYYYMMDD>*.md|txt` 에 메모를 올려 두면 daily 가 표에 옮긴다.
3. SAVE 소식은 **단서**: 영상에 넣을 것은 1차 출처(SEC·DART·IR·연준·통계)로 다시 확인해 factsheet 에 쓴다 (manual/09 §3).
   SAVE 의 요약 문장을 그대로 옮기지 않는다 (use=reference).
4. `check` (G2): 상태가 '확인함' 또는 '확인 못 함: 이유' 여야 함 (MUST, 빈칸이면 실패), '확인함' + 항목 1개 이상 (SHOULD).
"""
from __future__ import annotations

import re
from pathlib import Path

from .. import config

SOURCE = {"name": "SAVE (오선)", "web": "https://www.saveticker.com",
          "app": "https://apps.apple.com/kr/app/id6751139540"}
FILE = "save_check.md"
UNSET = "미확인"


def template(day: str) -> str:
    return f"""# SAVE (오선) 소식 확인 — {day}

웹 {SOURCE['web']} · 앱 {SOURCE['app']}
자동 수집 안 됨(봇 확인·AI 수집 거부) → 사람이 앱/웹에서 보고 적습니다. 영상에 쓸 소식은 1차 출처로 다시 확인합니다 (manual/09 §3-0).

상태: {UNSET}
<!-- '확인함' 또는 '확인 못 함: 이유' 로 바꾸기 -->
확인: (누가 · 몇 시)

| 구분 | 소식 (내 말로 한 줄) | 시각 | 1차 출처 확인 | 영상에 |
|---|---|---|---|---|
| 속보 |  |  |  |  |
| 리포트 |  |  |  |  |
| 경제지표·일정 |  |  |  |  |
"""


def ensure(rdir: Path, day: str) -> Path:
    """확인 표를 만든다 (있으면 그대로). inbox 메모가 있으면 표에 옮기고 '확인함 (사용자 메모)'."""
    p = rdir / FILE
    if not p.exists():
        p.write_text(template(day), encoding="utf-8")
    ymd = day.replace("-", "")
    notes = sorted((config.ROOT / "inbox" / "save").glob(f"{ymd}*")) if (config.ROOT / "inbox" / "save").exists() else []
    notes = [n for n in notes if n.suffix in (".md", ".txt")]
    if notes and UNSET in p.read_text(encoding="utf-8"):
        rows = []
        for n in notes:
            for ln in n.read_text(encoding="utf-8").splitlines():
                ln = ln.strip(" -*\t")
                core = re.sub(r"\(알림[^)]*\)", "", ln)
                core = re.sub(r"[{\[][a-z_]+[}\]]", "", core).strip(" -·:|")   # 전달 앱 변수({notification}·[notification])가 안 바뀐 줄은 버림
                if ln and not ln.startswith("#") and len(core) >= 4:
                    rows.append(f"| 메모 | {ln.replace('|', '/')} |  | (확인 전) |  |")
        if rows:   # 쓸 만한 줄이 없으면(변수만 온 알림 등) '미확인' 그대로 — 확인한 척하지 않음
            t = p.read_text(encoding="utf-8").replace(f"상태: {UNSET}", "상태: 확인함 (사용자 메모: " + ", ".join(n.name for n in notes) + ")", 1)
            p.write_text(t.rstrip("\n") + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
    return p


def read(rdir: Path) -> dict:
    """{'exists', 'status', 'done', 'items'}"""
    p = rdir / FILE
    if not p.exists():
        return {"exists": False, "status": "", "done": False, "items": 0}
    t = p.read_text(encoding="utf-8")
    m = re.search(r"^상태:\s*(.+)$", t, re.M)
    st = (m.group(1).strip() if m else "")
    items = 0
    for ln in t.splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0] not in ("구분", "---") and not set(cells[0]) <= {"-"} and cells[1]:
            items += 1
    done = bool(st) and not st.startswith(UNSET)
    return {"exists": True, "status": st, "done": done, "items": items}
