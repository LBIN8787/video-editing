# 스타일 고르기 — 20261107-knowledge-스페인독감

브랜드 **curiosity** · 질문 "스페인 독감은 왜 '스페인'일까?" (이름의 이유) · 분위기 ['과거', '위기']

| 자리 | 스타일 | 그래픽 팩 | 뼈대 장면 | 이유 |
|---|---|---|---|---|
| 영상 전체(기본) | `archive-doc` 아카이브 다큐 (자료 화면 켄 번스 + 타자기 문장) (demo) | dark-doc | kb, card_type, footage, quote | 질문 유형 이름의 이유, 분위기 위기·과거, 소스 있음(archive) |
| 훅 (첫 30초) | `archive-doc` 아카이브 다큐 (자료 화면 켄 번스 + 타자기 문장) (demo) | dark-doc | kb, card_type, footage, quote | 질문 유형 이름의 이유, 분위기 위기·과거, 소스 있음(archive) |
| 결론 | `kinetic-type` 키네틱 타이포 (말하는 순간 단어가 튀어나옴) (demo) | kinetic-poster | kinetic, card_type |  |

**기본 그래픽 팩**은 `edit.yaml` 의 `skin: dark-doc`. 특정 구간만 다른 팩이 맞으면 그 장면에 `"skin": "<팩>"` (예: 지도 장면만 newsprint, 인용 한 줄만 dark-doc).

후보 순위:

- `archive-doc` 8.5점 — 질문 유형 이름의 이유, 분위기 위기·과거, 소스 있음(archive)
- `hybrid-causal` 7.0점 — 질문 유형 이름의 이유, 소스 있음(footage)
- `map-journey` 4.5점 — 분위기 과거, 소스 있음(map)
- `paper-column` 3.0점 — 
- `kinetic-type` 2.5점 — 

## 조합 계획 (한 스타일로만 만들지 않습니다)

| 구간 | 쓸 스타일 (2개 이상 섞기) |
|---|---|
| 훅 (첫 30초) | archive-doc + kinetic-type |
| 본론 | archive-doc → hybrid-causal → map-journey (장면마다 번갈아) |
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
