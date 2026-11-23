<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `share` — 전체 중 몫

**언제:** 매출 중 지역 비중, 전체 대비 몫

**무엇:** 전체 막대(100%)에 부분이 차례로 채워지고 눈금·괄호로 합계

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `share` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/share.jpg`, 영상 `ytflow/looks/scenes/clips/share.mp4`

## 화면 구성·움직임 원리

- 가로 전체 막대(100%) 테두리 → parts 가 왼쪽부터 차례로 채워짐(색 다름)
- mark 위치에 비교 눈금(예: 3분의 1), sum 이면 묶을 구간 위에 괄호 + 합계 문구
- explain 무대: 앞 박자 요소는 남고 show 에 적은 부품만 새로 나옴, at 으로 대사 단어에 맞춤

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.15초 | 「매출 중 두 지역의 몫」 아래에서 떠오름 |
| 0.55초 | 요소 옆으로 펼쳐짐 |
| 0.95초 | 「매출 전체」 아래에서 떠오름 |
| 0.95초 | 「0」 아래에서 떠오름 |
| 0.95초 | 「100%」 아래에서 떠오름 |
| 1.05초 | 요소 옆으로 펼쳐짐 |
| 1.45초 | 「중국·홍콩」 아래에서 떠오름 |
| 2.89초 | 요소 옆으로 펼쳐짐 |
| 3.29초 | 「싱가포르」 아래에서 떠오름 |
| 4.37초 | 선 나타남 |
| 4.57초 | 「3분의 1」 아래에서 떠오름 |
| 4.87초 | 손그림 선 그려짐 |
| 5.17초 | 「합치면 3분의 1 넘게」 아래에서 떠오름 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "share"`

```json
{
 "type": "share",
 "title": "매출 중 두 지역의 몫",
 "total": "매출 전체",
 "of": 100,
 "parts": [
  {
   "label": "중국·홍콩",
   "value": 22
  },
  {
   "label": "싱가포르",
   "value": 14
  }
 ],
 "mark": {
  "value": 33.3,
  "label": "3분의 1"
 },
 "sum": {
  "parts": [
   0,
   1
  ],
  "label": "합치면 3분의 1 넘게"
 },
 "beats": [
  {
   "say": "매출 전체를 막대 하나로 놓습니다.",
   "show": [
    "total",
    "p0"
   ]
  },
  {
   "say": "싱가포르를 더합니다.",
   "show": [
    "p1"
   ]
  },
  {
   "say": "합치면 3분의 1이 넘습니다.",
   "show": [
    "mark",
    "sum"
   ]
  }
 ]
}
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

읽는 키 — 장면: `mark, of, parts, sum, total` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only share --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/explain.py:376` `s_share`
