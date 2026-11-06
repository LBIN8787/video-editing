---
name: edit-style-moneycrew
description: 머니크루 편집 스타일(무늬 없는 미색 배경 + 위쪽 자막 + 그려지는 주가 차트·가로 막대·굵은 숫자의 평면 인포그래픽 모션)로 영상을 만들거나 검토한다. 산업·공급망·실적·과거 사례 비교 같은 숫자 많은 경제 해설에 쓴다.
---

# 머니크루 스타일 (flat 렌더러)

- **규칙 원본:** `styles/moneycrew/STYLE.md` (먼저 읽기), 대본 추가 규칙: `styles/moneycrew/script.md`
- **제작:** `python -m ytflow make --style-ref moneycrew [--topic "..."]`
- **기존 프로젝트에 적용:** `cp styles/moneycrew/edit.yaml projects/<프로젝트>/edit.yaml` 후 assets → subtitles → assemble
- **대본 핵심:**
  - 카드 위주로 짭니다(70~85%).
  - 추이는 `line` 카드로, 비교는 `bars`/`number_compare` 로 보여 줍니다.
  - 문장은 한 줄 자막에 들어가게 짧게 씁니다.
- **핵심 점검:**
  - 위쪽 자막과 카드 제목이 겹치지 않는가
  - 강조 뒤 자막색이 어두운색으로 돌아오는가
  - 약 4초마다 새 요소가 나타나는가
- **아직 렌더러에 없는 기법:** 캔들 차트, 아이소메트릭 아이콘, 빨간 도장, 달력 카드. 필요한 장면은 `visual_brief` 에 지시를 남깁니다.
