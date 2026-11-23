# 스타일 고르기 — 20261112-market-call

브랜드 **market** · 질문 "실적이 좋아서만이 아니라면, 이번 어닝콜은 무엇이 달랐을까?" (원인) · 분위기 ['긴장']

| 자리 | 스타일 | 그래픽 팩 | 뼈대 장면 | 이유 |
|---|---|---|---|---|
| 영상 전체(기본) | `data-report` 데이터 리포트 (실제 시세·막대·비교표) (approved) | clean-flat | chart, bars, compare, bignum | 질문 유형 원인, 분위기 긴장, 소스 있음(price) |
| 훅 (첫 30초) | `archive-doc` 아카이브 다큐 (자료 화면 켄 번스 + 타자기 문장) (demo) | dark-doc | kb, card_type, footage, quote | 분위기 긴장, 소스 있음(archive) |
| 결론 | `kinetic-type` 키네틱 타이포 (말하는 순간 단어가 튀어나옴) (demo) | kinetic-poster | kinetic, card_type |  |

**기본 그래픽 팩**은 `edit.yaml` 의 `skin: clean-flat`. 특정 구간만 다른 팩이 맞으면 그 장면에 `"skin": "<팩>"` (예: 지도 장면만 newsprint, 인용 한 줄만 dark-doc).

후보 순위:

- `data-report` 8.0점 — 질문 유형 원인, 분위기 긴장, 소스 있음(price)
- `dash-cover` 7.0점 — 질문 유형 원인, 분위기 긴장
- `evidence-board` 7.0점 — 질문 유형 원인, 분위기 긴장
- `issue-dark-montage` 6.0점 — 질문 유형 원인, 분위기 긴장, 소스 있음(archive), 소스 확인 필요(map)
- `paper-column` 6.0점 — 질문 유형 원인

## 조합 계획 (한 스타일로만 만들지 않습니다)

| 구간 | 쓸 스타일 (2개 이상 섞기) |
|---|---|
| 훅 (첫 30초) | - |
| 본론 | data-report → dash-cover → evidence-board (장면마다 번갈아) |
| 결론 | - |

한 장면 안에서 겹치기 (`layers`) — 영상마다 3장면 이상, **강조가 아니라 내용**(사진·지도·도장)으로:

- `kb` + `locator`: 자료 화면 + 위치 미니 지도 (아카이브 × 지도)
- `kb` + `number`: 자료 화면 + 큰 숫자 카드 (아카이브 × 데이터)
- `journey` + `photo`: 지도 이동 + 그곳의 자료 사진 액자 (지도 × 아카이브)
- `footage` + `stamp`: 원본 영상 + 날짜·장소 타자기 (하이브리드 × 아카이브)
- `bars` + `photo`: 막대 비교 + 비교 대상의 사진 (데이터 × 아카이브)
- `chart` + `number`: 주가 그래프 + 그날의 숫자 하나 (데이터, 영상에서 가장 중요한 숫자에만)

규칙(롱폼): 스타일 4종 이상 · 한 스타일이 40% 넘지 않게 · 겹친 장면 3개 이상 · 같은 스타일 3장면 연속 금지 · 강조는 1분에 1번 이하, 자막과 같은 문장 반복 금지 (`check` G5 가 검사)
