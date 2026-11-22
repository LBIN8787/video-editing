# 스타일 고르기 — 20261121-market-deep-ai-chips

브랜드 **market** · 질문 "칩이 모자란다는 회사 주가가 한 달에 3분의 1이 빠졌다. AI 수요가 꺾인 걸까, 아니면 다른 무엇일까?" (역설) · 분위기 ['궁금', '경계']

| 자리 | 스타일 | 그래픽 팩 | 뼈대 장면 | 이유 |
|---|---|---|---|---|
| 영상 전체(기본) | `issue-dark-montage` 시사 심층 (어두운 영화 톤 + 실사 사진 몽타주 + 지도·인과 결론) (approved) | dark-doc | kb, journey, choropleth, map_causal, card_type, quote | 소스 있음(archive), 소스 있음(map) |
| 훅 (첫 30초) | `archive-doc` 아카이브 다큐 (자료 화면 켄 번스 + 타자기 문장) (demo) | dark-doc | kb, card_type, footage, quote | 소스 있음(archive) |
| 결론 | `kinetic-type` 키네틱 타이포 (말하는 순간 단어가 튀어나옴) (demo) | kinetic-poster | kinetic, card_type |  |

**기본 그래픽 팩**은 `edit.yaml` 의 `skin: dark-doc`. 특정 구간만 다른 팩이 맞으면 그 장면에 `"skin": "<팩>"` (예: 지도 장면만 newsprint, 인용 한 줄만 dark-doc).

후보 순위:

- `explain-stage` 5.0점 — 소스 있음(statement), 소스 있음(price)
- `issue-dark-montage` 5.0점 — 소스 있음(archive), 소스 있음(map)
- `news-desk` 4.5점 — 소스 있음(statement), 소스 있음(price)
- `data-report` 4.0점 — 소스 있음(price)
- `statement-brief` 4.0점 — 소스 있음(statement)

## 조합 계획 (한 스타일로만 만들지 않습니다)

| 구간 | 쓸 스타일 (2개 이상 섞기) |
|---|---|
| 훅 (첫 30초) | - |
| 본론 | explain-stage → issue-dark-montage → news-desk (장면마다 번갈아) |
| 결론 | - |

한 장면 안에서 겹치기 (`layers`) — 영상마다 3장면 이상, **강조가 아니라 내용**(사진·지도·도장)으로:

- `kb` + `locator`: 자료 화면 + 위치 미니 지도 (아카이브 × 지도)
- `kb` + `number`: 자료 화면 + 큰 숫자 카드 (아카이브 × 데이터)
- `journey` + `photo`: 지도 이동 + 그곳의 자료 사진 액자 (지도 × 아카이브)
- `footage` + `stamp`: 원본 영상 + 날짜·장소 타자기 (하이브리드 × 아카이브)
- `bars` + `photo`: 막대 비교 + 비교 대상의 사진 (데이터 × 아카이브)
- `chart` + `number`: 주가 그래프 + 그날의 숫자 하나 (데이터, 영상에서 가장 중요한 숫자에만)

규칙(롱폼): 스타일 4종 이상 · 한 스타일이 40% 넘지 않게 · 겹친 장면 3개 이상 · 같은 스타일 3장면 연속을 넘지 않는 쪽 · 강조는 기억할 곳에만 (모두 `check` 참고값, 05 §0-0) · 자막과 같은 문장 반복 금지
