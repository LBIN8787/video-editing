# 스타일 고르기 — 20261109-ai-unslop

브랜드 **ai** · 질문 "AI가 만든 티, 어떻게 지워?" (방법) · 분위기 ['실용', '미래']

| 자리 | 스타일 | 그래픽 팩 | 뼈대 장면 | 이유 |
|---|---|---|---|---|
| 영상 전체(기본) | `blueprint-explainer` 청사진 설명 (남색 모눈 + 흰 선 구조도) (demo) | blueprint | map_causal, analogy, bars, checklist | 질문 유형 방법, 분위기 미래 |
| 훅 (첫 30초) | `kinetic-type` 키네틱 타이포 (말하는 순간 단어가 튀어나옴) (demo) | kinetic-poster | kinetic, card_type | 질문 유형 방법, 분위기 실용 |
| 결론 | `kinetic-type` 키네틱 타이포 (말하는 순간 단어가 튀어나옴) (demo) | kinetic-poster | kinetic, card_type | 질문 유형 방법, 분위기 실용 |

**기본 그래픽 팩**은 `edit.yaml` 의 `skin: blueprint`. 특정 구간만 다른 팩이 맞으면 그 장면에 `"skin": "<팩>"` (예: 지도 장면만 newsprint, 인용 한 줄만 dark-doc).

후보 순위:

- `blueprint-explainer` 6.5점 — 질문 유형 방법, 분위기 미래
- `kinetic-type` 6.5점 — 질문 유형 방법, 분위기 실용
- `screen-demo` 6.0점 — 질문 유형 방법, 분위기 실용, 소스 있음(screen)
- `hybrid-causal` 4.0점 — 소스 있음(footage)
- `data-report` 1.0점 — 소스 확인 필요(price)

## 조합 계획 (한 스타일로만 만들지 않습니다)

| 구간 | 쓸 스타일 (2개 이상 섞기) |
|---|---|
| 훅 (첫 30초) | kinetic-type |
| 본론 | blueprint-explainer → screen-demo → hybrid-causal (장면마다 번갈아) |
| 결론 | kinetic-type |

한 장면 안에서 겹치기 (`layers`) — 영상마다 3장면 이상:

- `kb` + `words`: 자료 화면 + 그 순간의 핵심 단어 (아카이브 × 키네틱)
- `kb` + `locator`: 자료 화면 + 위치 미니 지도 (아카이브 × 지도)
- `kb` + `number`: 자료 화면 + 큰 숫자 카드 (아카이브 × 데이터)
- `journey` + `photo`: 지도 이동 + 그곳의 자료 사진 액자 (지도 × 아카이브)
- `footage` + `stamp`: 원본 영상 + 날짜·장소 타자기 (하이브리드 × 아카이브)
- `footage` + `words`: 원본 영상 + 핵심 단어 (하이브리드 × 키네틱)
- `bars` + `photo`: 막대 비교 + 비교 대상의 사진 (데이터 × 아카이브)
- `chart` + `words`: 주가 그래프 + 핵심 단어 (데이터 × 키네틱)

규칙(롱폼): 스타일 4종 이상 · 한 스타일이 40% 넘지 않게 · 겹친 장면 3개 이상 · 같은 스타일 3장면 연속 금지 (`check` G5 가 검사)

## 추천과 다르게 고른 이유
- 추천 기본 팩은 blueprint 였지만, 이 영상의 뼈대는 '직접 실행 화면'(화면 따라 하기)이라 밝은 clean-flat 을 기본으로 두고, 원리 구간(왜 비슷한가·스킬은 어떻게 일하나: 장면 10·14·15)만 blueprint 로 바꿨다. 화면 녹화는 어두운 대시보드라 남색 바탕 위에서는 구분이 약하다.
- 화면 따라 하기(screen-demo)와 청사진(blueprint-explainer)은 이 영상으로 첫 검증 (사용자 승인 2026-11-09).
