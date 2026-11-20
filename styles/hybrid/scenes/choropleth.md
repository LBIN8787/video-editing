<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `choropleth` — 나라 색칠 지도

**언제:** 여러 나라의 수치 비교

**무엇:** 나라별 값으로 색칠, 박자마다 나라가 칠해짐, 범례

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `choropleth` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/choropleth.jpg`, 영상 `ytflow/looks/scenes/clips/choropleth.mp4`

## 화면 구성·움직임 원리

- 나라 경계 지도(world-atlas) → values{나라: 값}으로 색 단계, 박자 show 의 나라들이 차례로 칠해짐 + 범례(legend)

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.20초 | 「지도 · world-atlas (ISC)」 아래에서 떠오름 |
| 0.65초 | 선 나타남 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "choropleth"`

```json
{
 "type": "choropleth",
 "title": "이 이야기에 나오는 나라들",
 "legend": "색: 영상에서 다룬 나라 (값 아님)",
 "label": "지도 · world-atlas (ISC)",
 "values": {
  "United States of America": 1,
  "France": 1,
  "United Kingdom": 1,
  "Spain": 1,
  "South Korea": 1,
  "North Korea": 1
 },
 "beats": [
  {
   "show": [
    "United States of America",
    "France",
    "United Kingdom"
   ],
   "say": "미리 말씀드리면, 답은 전쟁에 있습니다. 1차 세계대전이 병을 실어 날랐고,"
  },
  {
   "show": [
    "Spain",
    "South Korea",
    "North Korea"
   ],
   "say": "같은 전쟁이 신문의 입을 막았습니다. 그리고 입을 막지 않은 단 한 나라가, 병의 이름을 뒤집어썼습니다."
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `center, label, legend, title, values` · 박자: `show` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only choropleth --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/directions.py:552` `s_choropleth`
