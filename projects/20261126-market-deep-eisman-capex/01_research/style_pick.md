# 스타일 고르기 — 20261126-market-deep-eisman-capex

브랜드 **market** · 질문 "AI 투자가 꺾이면 반도체 주문은 언제, 무엇 때문에 멈추나 — 내 하이닉스·삼성은?" (전망) · 분위기 ['경계', '궁금']

| 자리 | 스타일 | 그래픽 팩 | 뼈대 장면 | 이유 |
|---|---|---|---|---|
| 영상 전체(기본) | `statement-brief` 발언 원본 브리핑 (원본 인터뷰 + 원문·번역 자막 + 요약 카드) (approved) | dark-doc | footage, quote, bignum | 소스 있음(statement) |
| 훅 (첫 30초) | `source-cut` 원본 발언 컷편집 (그 사람이 직접 말하는 부분만 잘라 넣기) (demo) | clean-flat | bite | 질문 유형 전망, 소스 확인 필요(footage), 소스 있음(statement) |
| 결론 | `source-cut` 원본 발언 컷편집 (그 사람이 직접 말하는 부분만 잘라 넣기) (demo) | clean-flat | bite | 질문 유형 전망, 소스 확인 필요(footage), 소스 있음(statement) |

**기본 그래픽 팩**은 `edit.yaml` 의 `skin: dark-doc`. 특정 구간만 다른 팩이 맞으면 그 장면에 `"skin": "<팩>"` (예: 지도 장면만 newsprint, 인용 한 줄만 dark-doc).

후보 순위:

- `source-cut` 4.5점 — 질문 유형 전망, 소스 확인 필요(footage), 소스 있음(statement)
- `statement-brief` 4.0점 — 소스 있음(statement)
- `dash-cover` 3.0점 — 
- `evidence-board` 3.0점 — 
- `paper-column` 3.0점 — 

## 조합 계획 (한 스타일로만 만들지 않습니다)

| 구간 | 쓸 스타일 (2개 이상 섞기) |
|---|---|
| 훅 (첫 30초) | source-cut |
| 본론 | source-cut → statement-brief → dash-cover (장면마다 번갈아) |
| 결론 | source-cut |

한 장면 안에서 겹치기 (`layers`) — 영상마다 3장면 이상, **강조가 아니라 내용**(사진·지도·도장)으로:

- `kb` + `locator`: 자료 화면 + 위치 미니 지도 (아카이브 × 지도)
- `kb` + `number`: 자료 화면 + 큰 숫자 카드 (아카이브 × 데이터)
- `journey` + `photo`: 지도 이동 + 그곳의 자료 사진 액자 (지도 × 아카이브)
- `footage` + `stamp`: 원본 영상 + 날짜·장소 타자기 (하이브리드 × 아카이브)
- `bars` + `photo`: 막대 비교 + 비교 대상의 사진 (데이터 × 아카이브)
- `chart` + `number`: 주가 그래프 + 그날의 숫자 하나 (데이터, 영상에서 가장 중요한 숫자에만)

규칙(롱폼): 스타일 4종 이상 · 한 스타일이 40% 넘지 않게 · 겹친 장면 3개 이상 · 같은 스타일 3장면 연속을 넘지 않는 쪽 · 강조는 기억할 곳에만 (모두 `check` 참고값, 05 §0-0) · 자막과 같은 문장 반복 금지
