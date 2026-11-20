<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `afterline` — 사건 이후 누적

**언제:** 제재·발표 '이후에도' 계속된 일

**무엇:** 시간선 위 사건 표식 → '이후' 구간이 붉게 열림 → 카드가 쌓임 → 수량 문구

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `afterline` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/afterline.jpg`, 영상 `ytflow/looks/scenes/clips/afterline.mp4`

## 화면 구성·움직임 원리

- 시간선 위 사건 표식(event: 이름·날짜·금지 아이콘) → '이후' 구간이 붉게 열림 → 카드(items.count 개, 아이콘)가 하나씩 쌓임 → headline(앞말 + 강조 문구)
- explain 무대: show 에 적은 부품만 나오고 앞 것은 남음

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.15초 | 「제재 뒤에도 계속 나온 것」 아래에서 떠오름 |
| 0.40초 | 선 그려짐 |
| 0.85초 | 「어느 회사」 아래에서 떠오름 |
| 1.00초 | 선 그려짐 |
| 1.00초 | 「2025년 3월 제재」 아래에서 떠오름 |
| 2.85초 | 선 그려짐 |
| 3.15초 | 「제재 뒤」 아래에서 떠오름 |
| 3.35초 | 「1」 튀어나옴 |
| 3.75초 | 「2」 튀어나옴 |
| 4.15초 | 「3」 튀어나옴 |
| 4.55초 | 「4」 튀어나옴 |
| 4.95초 | 「5」 튀어나옴 |
| 5.35초 | 「6」 튀어나옴 |
| 5.79초 | 「새 버전」 아래에서 떠오름 |
| 5.99초 | 「6개 이상」 아래에서 떠오름 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "afterline"`

```json
{
 "type": "afterline",
 "title": "제재 뒤에도 계속 나온 것",
 "event": {
  "name": "어느 회사",
  "date": "2025년 3월 제재",
  "tag": "제재 뒤",
  "mark": "ban"
 },
 "items": {
  "count": 6,
  "icon": "cpu"
 },
 "headline": {
  "pre": "새 버전",
  "emph": "6개 이상"
 },
 "beats": [
  {
   "say": "한 회사가 제재 명단에 올랐습니다.",
   "show": [
    "event"
   ]
  },
  {
   "say": "그런데 제재 뒤에도 새 버전은 계속 나왔습니다.",
   "show": [
    "after",
    "items"
   ]
  },
  {
   "say": "여섯 개가 넘습니다.",
   "show": [
    "headline"
   ]
  }
 ]
}
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

읽는 키 — 장면: `event, headline, id, items` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only afterline --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/explain.py:208` `s_afterline`
