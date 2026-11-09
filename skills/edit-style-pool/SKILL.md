---
name: edit-style-pool
description: 스타일 풀에 추가된 장면·겹치기(AI 대화 화면, 터미널 타자, 화면 자동 줌, 손그림 표시, 나라 색칠 지도, 세로 쇼츠 Claude 판)를 대본에 넣어 쓴다. AI 사용법·도구 설명, 화면의 한 곳을 가리켜야 할 때, 여러 나라가 나오는 이야기, 실제 화면이 있는 쇼츠에 쓴다.
---

# 스타일 풀 (등록부 `styles/recipes/*.yaml`, 코드 `ytflow/stages/directions.py`·`shorts_hf.py`)

먼저 `python -m ytflow style-pick <프로젝트>` 로 추천을 보고, 영상 하나에 여러 스타일을 섞습니다 (`manual/05-style-matching.md` §0-1, 강조는 1분에 1번 이하).

| 장면 type / 겹치기 | 필드 | 쓸 때 |
|---|---|---|
| `chat` | `app`(창 제목), `turns[{role: user|ai, text, beat, delay}]` | 프롬프트와 답을 보여 줄 때. 상표·로고 없이 'AI 대화 · 재구성 예시'. 실제로 쓴 대화나 공식 절차만 |
| `terminal` | `title`, `lines[{cmd|out, beat, delay}]` | 설치·실행 명령. **실제 실행 기록만** |
| `zoomshot` | `clip{src,start}`, `focus[{beat, box:[x,y,w,h], label}]` 또는 `{beat, out:true}` | 화면의 한 곳을 가리킬 때. box 는 1920×1080 기준 — 렌더 후 프레임으로 꼭 확인 |
| layers `mark` | `{beat, box, shape: circle|underline|arrow}` | 가장 중요한 한 곳에만 (강조 예산 포함) |
| `choropleth` | `values{나라 영문명: 값}`, 박자 `show[]`, `title`, `legend` | 여러 나라. 값이 없으면 legend 에 '값 아님' |
| 세로 쇼츠 | `02_script/short.json` → `python -m ytflow short <프로젝트>` | 실제 화면이 있는 쇼츠 (Claude 판). 설명 카드형은 Codex 'AI 실전노트' 보관본 |

시험작: `projects/20261109-pool-ai`(`styles/demos/pool_ai.json`), `projects/20261109-pool-map`, `projects/20261109-short-unslop`.
