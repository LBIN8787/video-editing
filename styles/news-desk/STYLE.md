# 뉴스 데스크 카드 (news-desk)
> 레퍼런스 분석·장단점: `docs/25-reference-2611.md` §1 · 장면 `newsdesk` (`ytflow/stages/newsdesk.py`) · 시험작 `projects/20261113-style-ref2`

**한 소식 = 한 장.** 모든 소식이 같은 틀이라 시청자가 볼 곳을 배운다.

| 칸 | 대본 키 | 규칙 |
|---|---|---|
| 순번·출처 회사 | `idx`, `total`, `source` | 'NEWS 2 / 7 — OPENAI' + 위 진행 막대 |
| 꼬리표 | `tag`, `tag_color`, `date` | 주의(red)·사례(green)·지금 할 일(yellow)·이슈·흐름 — 소식의 쓸모 |
| 제목 | `headline`, `hl` | 14자 안팎, 핵심 낱말 하나만 강조색 |
| 요약 | `sub` | 한 줄 |
| 숫자 | `stats[≤3]` (label·value·color) | 모든 숫자는 출처로 확인된 것, 비교 기준은 내레이션에서 |
| 점 목록 | `bullets[≤3]` | 짧게 |
| 증거 패널 | `panel` = shot(캡처·사진 `src`, `caption`) / bignum(`value` 세기) / stamp(`text`, `sub`) | 하나만. 캡처는 1차 출처 |
| 출처 줄 | `footer`, `handle` | 본문 아래 줄 (자막과 겹치지 않음) |

- 박자 2개 권장: 1박자 = 제목·요약, 2박자 = 숫자·증거 패널(`panel_beat`).
- 섞어 쓰기: 이 카드만 이어지면 지루함 → 2~3장마다 인과 지도·차트·원본 발언(bite)을 끼움.
