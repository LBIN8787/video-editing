<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `people` — 100명 그림

**언제:** 비율을 '사람'으로 (3명 중 1명)

**무엇:** 사람 아이콘 100개 중 일부가 빨갛게

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `people` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/people.jpg`, 영상 `ytflow/looks/scenes/clips/people.mp4`

## 화면 구성·움직임 원리

- 사람 아이콘 100개(10×10, scatter 면 흩어짐) → count 명이 강조색으로 채워짐
- 오른쪽 큰 숫자(세어 올라감) + 설명·출처 줄

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.20초 | 「CDC · 1918 Pandemic (H1N1 vi…」 아래에서 떠오름 |
| 0.20초 | 「세계 인구 100명으로 줄이면」 아래에서 떠오름 |
| 0.50초 | 손그림 선 그려짐 |
| 0.65초 | 요소 나타남 |
| 3.56초 | 「33명」 아래에서 떠오름 |
| 3.56초 | 숫자가 33.0 까지 세어 올라감 |
| 3.86초 | 「이 병에 걸렸다」 아래에서 떠오름 |
| 4.06초 | 「약 5억 명 = 당시 세계 인구의 3분의 1」 아래에서 떠오름 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "people"`

```json
{
 "type": "people",
 "label": "CDC · 1918 Pandemic (H1N1 virus)",
 "title": "세계 인구 100명으로 줄이면",
 "count": 33,
 "value": "33명",
 "caption": "이 병에 걸렸다",
 "sub": "약 5억 명 = 당시 세계 인구의 3분의 1",
 "beats": [
  {
   "say": "당시 세계 인구를 100명으로 줄여 볼까요."
  },
  {
   "say": "그중 33명이 이 병에 걸렸습니다. 약 5억 명, 세계 인구의 3분의 1입니다.",
   "fill": true
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `caption, count, id, label, scatter, sub, title, value` · 박자: `fill` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only people --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/hybrid.py:884` `s_people`
