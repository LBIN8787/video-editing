---
name: video-research
description: 영상 주제의 자료조사를 한다. 웹 검색으로 1차 출처(공시, 보도자료, 정부 발표)와 주요 언론을 교차 확인해 출처·날짜·확인상태가 붙은 팩트시트(01_research/factsheet.md)와 인용 기사 목록(articles.json)을 만든다.
---

# 자료조사 (research 단계)

## 자동
`python -m ytflow stage <프로젝트> research` 를 실행합니다. 백엔드가 웹 검색으로 조사합니다(claude-cli: WebSearch/WebFetch, codex-cli: `codex --search exec`, api: 서버 웹 검색 도구).

## 직접 할 때 (manual 모드, 또는 결과를 고칠 때)
입력은 `00_source/shortlist.json` 의 선택된 주제(`state.json` 의 `pick` 번호)와 `01_research/my_notes.md`(있으면)입니다.

1. **조사:** 검색 도구로 조사합니다.
   - 1차 출처를 우선합니다: DART·SEC 공시, 회사 IR·보도자료, 정부 발표(정책브리핑).
   - 그다음 주요 언론(국내·해외)입니다.
   - 숫자(금액·지분율·날짜·실적)는 서로 다른 출처 2곳 이상으로 맞춥니다. 다르면 둘 다 적고 차이를 설명합니다.
   - 오늘 날짜 기준 최신 정정·후속 보도를 확인합니다.
2. **팩트시트 작성:** `01_research/factsheet.md` 를 `prompts/research.md` 형식으로 씁니다.
   - 모든 팩트에 `[F번호] 내용 — 출처: [매체](URL) (YYYY-MM-DD) — 확인상태` 를 붙입니다.
   - '인물 발언'에는 누가·언제·어디서·원문을 적습니다. 확인된 것만 씁니다. 이것이 대본에서 원본 발언(quote) 장면의 근거가 됩니다.
3. **기사 목록 작성:** `01_research/articles.json` 을 씁니다(스키마 `schemas/articles.schema.json`). 팩트시트에 URL 이 있는 기사·공시만 넣습니다.

## 품질 기준
- 추측한 숫자는 넣지 않습니다. 모르면 '확인 필요'로 적습니다.
- 잘못된 보도를 찾으면 팩트시트 맨 위 '주의' 상자에 적습니다(대본에 쓰지 않기 위해).
- '다음에 볼 것'에는 날짜가 정해진 일정만 넣습니다.
