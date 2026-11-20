<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `usmap` — 미국 주 지도

**언제:** 미국 주별 이야기 (선거·규제)

**무엇:** 손으로 그린 미국 지도 + 주 강조 + 숫자

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `usmap` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/usmap.jpg`, 영상 `ytflow/looks/scenes/clips/usmap.mp4`

## 화면 구성·움직임 원리

- 손그림 미국 주 경계 → 박자 highlight 주 칠하기 → counter 큰 숫자(세어 올라감)·note 메모, counter2 로 두 번째 숫자

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.20초 | 「2026.11.05 · The Next Web, G…」 아래에서 떠오름 |
| 0.20초 | 「데이터센터 주민투표 41건」 아래에서 떠오름 |
| 0.20초 | 요소 그려짐 |
| 0.50초 | 손그림 선 그려짐 |
| 0.65초 | 「41건」 아래에서 떠오름 |
| 0.65초 | 숫자가 41.0 까지 세어 올라감 |
| 0.85초 | 「주민투표」 아래에서 떠오름 |
| 6.71초 | 선 아래에서 떠오름 |
| 7.01초 | 손그림 선 그려짐 |
| 7.21초 | 「오하이오 21건」 아래에서 떠오름 |
| 11.01초 | 「형광펜」 옆으로 펼쳐짐 |
| 11.11초 | 「40 / 41」 아래에서 떠오름 |
| 11.31초 | 「제한 쪽 승리」 아래에서 떠오름 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "usmap"`

```json
{
 "type": "usmap",
 "label": "2026.11.05 · The Next Web, GovTech",
 "title": "데이터센터 주민투표 41건",
 "beats": [
  {
   "say": "11월 3일 미국 중간선거 날, 데이터센터를 두고 주민투표가 41건 열렸습니다.",
   "counter": {
    "value": 41,
    "suffix": "건",
    "label": "주민투표"
   }
  },
  {
   "say": "열 개 주에서 열렸는데, 오하이오 한 곳에서만 21건이었습니다.",
   "highlight": [
    "Ohio"
   ],
   "note": {
    "state": "Ohio",
    "text": "오하이오 21건"
   }
  },
  {
   "say": "결과는 41건 중 40건, '짓지 말자' 쪽의 승리였습니다.",
   "counter2": {
    "value": 40,
    "of": 41,
    "label": "제한 쪽 승리"
   }
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `label, title` · 박자: `counter, counter2, highlight, note` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only usmap --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/hybrid.py:500` `s_usmap`
