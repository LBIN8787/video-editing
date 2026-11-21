<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# 겹치기 — 다른 장면 위에 얹는 것

실사·인과 지도 같은 장면 위에 박자 키 하나로 얹는 연출.

예시 영상: [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP)

## `footage@chips` — 실사 위 말 칩

**언제:** 사람들이 저마다 무엇을 원하나 / 같은 틀 사례 나열

**무엇:** 실사 위에 부탁·메시지 칩이 0.6초 간격으로 하나씩 떠오름

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `footage@chips` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/footage_chips.jpg`, 영상 `ytflow/looks/scenes/clips/footage_chips.mp4`
  - 예시와 실제의 차이: 예시의 바탕은 '실사 자리' 색 그라데이션

### 화면 구성·움직임 원리

- 실사 위 정해진 자리 6곳(CHIP_SLOTS) 또는 x·y 에 흰 둥근 칩(색 점 + 굵은 글자)이 chip_gap(0.6초) 간격으로 튀어나오고 위아래로 살짝 둥실, 칩마다 pop

### 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.00초 | 영상 움직임 |
| 0.20초 | 「실사 자리」 아래에서 떠오름 |
| 0.65초 | 「프로틴 싸게 사 줘」 튀어나옴 |
| 1.10초 | 「프로틴 싸게 사 줘」 둥실 움직임(반복) |
| 1.25초 | 「메일 좀 정리해 줘」 튀어나옴 |
| 1.70초 | 「메일 좀 정리해 줘」 둥실 움직임(반복) |
| 1.85초 | 「미용실 예약해 줘」 튀어나옴 |
| 2.30초 | 「미용실 예약해 줘」 둥실 움직임(반복) |

### 대본(`02_script/hybrid.json`)에 쓰는 법

`footage 박자 "chips": ["…", …]`

```json
{
 "type": "footage",
 "clip": {
  "src": "ph",
  "start": 0,
  "frame": "full"
 },
 "label": "실사 자리",
 "beats": [
  {
   "say": "출근길 사람들은 저마다 AI 에게 부탁을 겁니다.",
   "chips": [
    "프로틴 싸게 사 줘",
    "메일 좀 정리해 줘",
    "미용실 예약해 줘"
   ]
  }
 ]
}
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

읽는 키 — 장면: `clip, label` · 박자: `chip_gap, chips, lower, vox` (렌더러 코드에서 자동)

### 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only footage@chips --force` (그림·영상·이 명세가 함께 갱신)

### 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/hybrid.py:222` `s_footage`

## `chapter@noir` — 누아르 장 표지

**언제:** 누아르 스킨 영상의 장 나누기 — 날짜가 이야기의 뼈대일 때 (오신트형 큰 날짜 표지의 구조)

**무엇:** 검은 바탕에 작은 빨간 줄(날짜·기간) → 큰 회백색 명조 제목 → 짧은 빨간 선, 화면이 살짝 물러남

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `chapter@noir` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/chapter_noir.jpg`, 영상 `ytflow/looks/scenes/clips/chapter_noir.mp4`
  - 예시와 실제의 차이: 누아르 스킨에서 look 을 안 정하고 자료 화면도 없으면 이 표지 (빨간 전면 대신 — 빨강은 한 곳만). 자료 화면이 있으면 사진 표지가 되므로 look 을 noir 로 고정

### 화면 구성·움직임 원리

- kicker(없으면 date·num)가 넓은 자간에서 좁혀지며 빨갛게 → 0.45초 뒤 큰 명조 제목 → 1초에 제목 아래 짧은 빨간 선
- sub 가 있으면 아래 회색 작은 줄, 화면 전체는 1.04배에서 천천히 제자리로

### 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.00초 | 장면 전체 확대·이동 |
| 0.15초 | 「월요일 → 금요일」 아래에서 떠오름 |
| 0.45초 | 「닷새 동안 무슨 일이 있었나」 아래에서 떠오름 |
| 1.00초 | 선 그려짐 |
| 1.20초 | 「가상의 예시」 아래에서 떠오름 |

### 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "chapter", "look": "noir", "kicker": "월요일 → 금요일"`

```json
{
 "type": "chapter",
 "skin": "noir",
 "look": "noir",
 "kicker": "월요일 → 금요일",
 "title": "닷새 동안 무슨 일이 있었나",
 "sub": "가상의 예시",
 "beats": [
  {
   "say": "닷새 동안 무슨 일이 있었는지 따라가 봅니다."
  }
 ]
}
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

읽는 키 — 장면: `icon, title` · 박자: `—` (렌더러 코드에서 자동)

### 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only chapter@noir --force` (그림·영상·이 명세가 함께 갱신)

### 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/hybrid.py:334` `s_chapter`

## `map_causal@cut` — 선 끊김 (빨간 점선 + X)

**언제:** 막혔다·차단됐다·끊겼다

**무엇:** 그려 둔 연결선을 지우지 않고 빨간 점선 + X 로 바꿈

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `map_causal@cut` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/map_causal_cut.jpg`, 영상 `ytflow/looks/scenes/clips/map_causal_cut.mp4`

### 화면 구성·움직임 원리

- 그린 화살표(<g> 로 묶임)를 0.3초에 흐리게(12%) → 같은 경로에 빨간 점선(16·14)이 나타나 흐르고 → 가장 긴 구간 가운데 빨간 원 X 가 크게서 찍힘, pop

### 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.20초 | 「부탁에서 결제까지」 아래에서 떠오름 |
| 0.35초 | 요소 아래에서 떠오름 |
| 0.50초 | 손그림 선 그려짐 |
| 0.50초 | 요소 튀어나옴 |
| 0.55초 | 「사용자 부탁」 아래에서 떠오름 |
| 0.60초 | 요소 아래에서 떠오름 |
| 0.75초 | 요소 튀어나옴 |
| 0.80초 | 「AI 비서」 아래에서 떠오름 |
| 0.85초 | 요소 아래에서 떠오름 |
| 0.95초 | 손그림 선 그려짐 |
| 1.00초 | 요소 튀어나옴 |
| 1.05초 | 「쇼핑몰 결제」 아래에서 떠오름 |
| 1.10초 | 요소 아래에서 떠오름 |
| 1.25초 | 요소 튀어나옴 |
| 1.30초 | 「메신저」 아래에서 떠오름 |
| 1.30초 | 손그림 선 그려짐 |
| 4.45초 | 선 묶음 사라짐 |
| 4.45초 | 선 나타남 |
| 4.45초 | 선 점선이 흐름 |
| 4.60초 | 「✕」 크게서 찍힘(도장) |
| 4.85초 | 요소 아래에서 떠오름 |
| 5.00초 | 요소 튀어나옴 |
| 5.05초 | 「쇼핑몰 결제」 아래에서 떠오름 |

### 대본(`02_script/hybrid.json`)에 쓰는 법

`map_causal·statecard 박자 "cut"`

```json
{
 "type": "map_causal",
 "title": "부탁에서 결제까지",
 "map": {
  "nodes": {
   "ask": {
    "label": "사용자 부탁",
    "icon": "user",
    "x": 400,
    "y": 420
   },
   "bot": {
    "label": "AI 비서",
    "icon": "bot",
    "x": 960,
    "y": 420
   },
   "shop": {
    "label": "쇼핑몰 결제",
    "icon": "shopping-cart",
    "x": 1520,
    "y": 420
   },
   "msg": {
    "label": "메신저",
    "icon": "smartphone",
    "x": 960,
    "y": 760
   }
  }
 },
 "beats": [
  {
   "say": "부탁은 AI 비서를 거쳐 결제와 메시지로 이어집니다.",
   "reveal": [
    "ask",
    "bot",
    "shop",
    "msg"
   ],
   "draw": [
    [
     "ask",
     "bot"
    ],
    [
     "bot",
     "shop"
    ],
    [
     "bot",
     "msg"
    ]
   ]
  },
  {
   "say": "그런데 메시지 쪽 길은 막혔습니다.",
   "cut": [
    [
     "bot",
     "msg"
    ]
   ],
   "active": "shop"
  }
 ]
}
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

읽는 키 — 장면: `label, title` · 박자: `active, cut, draw, instant, reveal, tag` (렌더러 코드에서 자동)

### 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only map_causal@cut --force` (그림·영상·이 명세가 함께 갱신)

### 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/hybrid.py:455` `s_map_causal`
