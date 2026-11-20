---
name: looks-gallery
description: 영상 구성요소·화풍·연출 목록을 눈으로 보여 준다. 사용자가 "화풍목록 보여줘", "연출 보여줘", "스타일 목록", "어떤 화풍 있어?", "조합 보여줘"처럼 말하면 쓴다. 구성요소 카테고리(화면 화풍·삽화 화풍·실사 색보정·글자 연출·그래픽 연출·카메라·장면 전환·배경음)마다 스타일 예시와, 카테고리마다 하나씩 골라 합친 결과를 재생하는 조합 판을 최신 목록으로 다시 만들어 열어 준다.
---

# 화풍 목록 보여 주기 (2026-11-20 사용자: "나중에 화풍목록 보여줘 하면 화풍목록의 예시를 볼 수 있도록 — 시각적으로")

공유 페이지: https://claude.ai/artifact/K4CRgsyTYsWGCDw5RoCtam (`ytflow/stages/looks.py` 의 `GALLERY_URL`)

## 원리 (2026-11-20 사용자)
영상 = 구성요소 카테고리마다 고른 스타일의 **조합**(`styles/components.yaml`). 화풍(어떻게 보이나)과 연출(어떻게 움직이고 보여 주나)은 다른 축이라 서로 섞는다 — 같은 모션그래픽도 연출이 다르면 전혀 다른 장면이 된다.
- 화풍: `styles/looks.yaml` (motion·illust·footage) · 연출: `styles/techniques.yaml` (group 으로 글자·그래픽·카메라·전환에 나뉨) · 배경음: `assets/bgm/bgm.yaml`
- 고르기: `python -m ytflow look <프로젝트> --set motion=chalkboard --set text=count-up --set transition=match-move …` → edit.yaml `look`. 화풍 3종은 렌더에 바로 쓰이고, 연출은 이 영상의 기본값(장면마다 바꿀 수 있음).

## 순서
1. 페이지를 최신 목록으로 다시 만든다 (모션그래픽은 화풍마다 같은 장면이 움직이는 미리보기, 실사 색보정은 같은 클립에 보정을 바꾼 실제 화면, 삽화는 예시 그림):
   ```bash
   python -m ytflow looks --gallery <스크래치>/looks.html
   ```
2. Artifact 도구로 **같은 주소**(`GALLERY_URL`)에 다시 올리고(`url` 에 그 주소, 처음 읽지 않았으면 `action: read` 먼저), 사용자에게 링크를 준다. 목록이 바뀌지 않았으면 다시 올리지 않고 `action: open` 만.
3. 터미널에도 한 줄 요약: 화풍 수(모션그래픽·삽화·실사), 삽화 예시가 몇 개 채워졌나, 고르는 법 `python -m ytflow look <프로젝트> --motion <id> --illust <id> --footage <id>`.

## 삽화 예시 그림 — 클라우드는 주문, PC 가 그림
- 클라우드 세션: `python -m ytflow looks --order` → `inbox/pc-tasks/<KST>-looks-draw.md` (main 에 올림). PC 의 Claude Code 세션은 시작할 때 이 할 일을 알림으로 봄(`.claude/settings.json` SessionStart → `scripts/pc_tasks.py`), Codex 는 AGENTS.md 의 안내로.
- PC 세션: `python -m ytflow looks --draw auto` — 이 PC 에 있는 무료 길을 차례로: ① Codex CLI(ChatGPT 구독, 로컬 Claude Code 세션도 이 명령으로 `codex exec` 를 불러 맡김) ② Gemini API 키(`GEMINI_API_KEY`, Google AI Studio) ③ 둘 다 없으면 주문서(`ORDERS.md`)만 → 사람이 ChatGPT·Gemini 앱에 붙여 그리고 같은 폴더에 `<id>.png` → `looks --register`. 끝나면 `styles/looks_examples.json` 을 커밋하고 할 일 파일을 done 으로.
- 그림은 `<예시 폴더>/<화풍 id>.png` (PC: `YTFLOW_DRIVE/looks/`, 클라우드: `~/.cache/ytflow/looks/`). 있으면 페이지에 자동으로 들어간다.
- 없는 것만 그리기: 사용자 PC 에서 `python -m ytflow looks --draw codex` (Codex 구독, 무료 길). 클라우드에서는 `--draw manual` 로 주문서(`ORDERS.md`)만 만들고, 필요하면 `inbox/requests/` 로 피클에게 요청.
- **ElevenLabs 로 그림을 만들지 않는다** (2026-11-20 사용자). 유료 그림 생성도 사용자 승인 없이 쓰지 않는다.
- 클라우드 세션은 예시 그림이 캐시에 없을 수 있다 — 그러면 Drive `ytflow/looks/` 에서 받아 `~/.cache/ytflow/looks/` 에 두고 만든다(파일당 10MB 이하). 없으면 '준비 중' 칸으로 두고 그렇다고 말한다.

## 화풍을 더하거나 판정이 바뀌면
`styles/looks.yaml` 에 항목을 더하거나 `status`(approved·trial·available)를 고친 뒤 위 1~2 를 다시 한다. 모션그래픽 화풍은 `skins/<id>/skin.yaml` 도 함께.
