<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `journey` — 지도 여정

**언제:** 어디서 어디로 — 전파·이동·공급망

**무엇:** 세계 지도 위를 카메라가 이동·확대, 경로선이 그려지고 핀

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `journey` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/journey.jpg`, 영상 `ytflow/looks/scenes/clips/journey.mp4`

## 화면 구성·움직임 원리

- 세계 지도(직사각형, 화면 꽉)를 places 좌표로 → 박자 goto(+zoom)로 카메라 이동·확대, route 로 경로 곡선이 그려지고 pin 으로 핀·이름
- highlight 나라 칠하기, seas 바다 이름

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.00초 | 「<path d="M-53.333,1190.631L-…」 나타남 |
| 0.20초 | 「지도 · world-atlas (ISC)」 아래에서 떠오름 |
| 0.30초 | 「병이 지나간 길, 1918」 아래에서 떠오름 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "journey"`

```json
{
 "type": "journey",
 "places": {
  "kansas": [
   -96.8,
   39.1
  ],
  "brest": [
   -4.49,
   48.39
  ],
  "glasgow": [
   -4.25,
   55.86
  ],
  "madrid": [
   -3.7,
   40.42
  ],
  "seoul": [
   126.98,
   37.57
  ],
  "brevig": [
   -166.49,
   65.33
  ]
 },
 "title": "병이 지나간 길, 1918",
 "label": "지도 · world-atlas (ISC)",
 "start": {
  "goto": null,
  "zoom": 1
 },
 "beats": [
  {
   "say": "미리 말씀드리면, 답은 전쟁에 있습니다. 1차 세계대전이 병을 실어 날랐고,"
  },
  {
   "say": "같은 전쟁이 신문의 입을 막았습니다. 그리고 입을 막지 않은 단 한 나라가, 병의 이름을 뒤집어썼습니다."
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `center, drawn, highlight, label, pins, places, projection, seas, start, title` · 박자: `goto, pin, route, zoom` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only journey --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/directions.py:132` `s_journey`
