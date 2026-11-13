# 스타일 고르기 — 20261113-curiosity-moravec

브랜드 **curiosity** · 질문 "체스 챔피언을 이긴 AI는 왜 빨래를 못 갤까?" (행동의 이유) · 분위기 ['차분', '과거', '미래']

| 자리 | 스타일 | 그래픽 팩 | 뼈대 장면 | 이유 |
|---|---|---|---|---|
| 영상 전체(기본) | `paper-column` 종이 칼럼 (구겨진 종이 + 손그림 + 콜라주) (approved) | paper-sketch | analogy, map_causal, bignum, timeline | 질문 유형 행동의 이유, 분위기 차분 |
| 훅 (첫 30초) | `story-board` 이야기 그림판 (말하는 순간 종이 위에 사람·사물이 그려지고 카메라가 따라감) (demo) | paper-sketch | story | 질문 유형 행동의 이유, 분위기 차분·과거·미래 |
| 결론 | `story-board` 이야기 그림판 (말하는 순간 종이 위에 사람·사물이 그려지고 카메라가 따라감) (demo) | paper-sketch | story | 질문 유형 행동의 이유, 분위기 차분·과거·미래 |

**기본 그래픽 팩**은 `edit.yaml` 의 `skin: paper-sketch`. 특정 구간만 다른 팩이 맞으면 그 장면에 `"skin": "<팩>"` (예: 지도 장면만 newsprint, 인용 한 줄만 dark-doc).

후보 순위:

- `story-board` 8.5점 — 질문 유형 행동의 이유, 분위기 차분·과거·미래
- `chalk-lesson` 8.0점 — 질문 유형 행동의 이유, 분위기 차분·과거
- `paper-column` 7.0점 — 질문 유형 행동의 이유, 분위기 차분
- `illustrated` 6.5점 — 질문 유형 행동의 이유, 분위기 차분·과거·미래, 소스 확인 필요(art)
- `hybrid-causal` 5.0점 — 질문 유형 행동의 이유, 분위기 차분, 소스 확인 필요(footage)

## 조합 계획 (한 스타일로만 만들지 않습니다)

| 구간 | 쓸 스타일 (2개 이상 섞기) |
|---|---|
| 훅 (첫 30초) | story-board + illustrated |
| 본론 | story-board → chalk-lesson → paper-column (장면마다 번갈아) |
| 결론 | story-board + illustrated |

한 장면 안에서 겹치기 (`layers`) — 영상마다 3장면 이상, **강조가 아니라 내용**(사진·지도·도장)으로:

- `kb` + `locator`: 자료 화면 + 위치 미니 지도 (아카이브 × 지도)
- `kb` + `number`: 자료 화면 + 큰 숫자 카드 (아카이브 × 데이터)
- `journey` + `photo`: 지도 이동 + 그곳의 자료 사진 액자 (지도 × 아카이브)
- `footage` + `stamp`: 원본 영상 + 날짜·장소 타자기 (하이브리드 × 아카이브)
- `bars` + `photo`: 막대 비교 + 비교 대상의 사진 (데이터 × 아카이브)
- `chart` + `number`: 주가 그래프 + 그날의 숫자 하나 (데이터, 영상에서 가장 중요한 숫자에만)

규칙(롱폼): 스타일 4종 이상 · 한 스타일이 40% 넘지 않게 · 겹친 장면 3개 이상 · 같은 스타일 3장면 연속 금지 · 강조는 1분에 1번 이하, 자막과 같은 문장 반복 금지 (`check` G5 가 검사)
