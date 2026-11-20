<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# 장면 전환 — 렌더러에 있는 전환

장면 사이 넘어가는 법. 대본의 다음 장면에 `"tr": "<id>"`(기본 fade, 장 표지는 push). 모양 매치 아이리스만 앞 장면에 `iris_out`.

예시 영상: [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP)

## `fade` — 겹치며 바뀜 (기본)

**언제:** 보통 장면 사이

**무엇:** 앞 장면이 사라지며 다음 장면이 나타남

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `fade` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/tr_fade.jpg`, 영상 `ytflow/looks/scenes/clips/tr_fade.mp4`

### 화면 구성·움직임 원리

- 앞 장면 마지막 0.3초 #root 불투명도 1→0, 다음 장면 처음 0.35초 0→1 (edit10.apply)

### 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| **장면 1** (`bignum`) | |
| 0.55초 | 「앞 장면」 아래에서 떠오름 |
| 0.85초 | 「1」 아래에서 떠오름 |
| 0.85초 | 숫자가 1.0 까지 세어 올라감 |
| 1.50초 | 장면 전체 사라짐 |
| 1.95초 | 손그림 선 그려짐 |
| **장면 2** (`bignum`) | |
| 0.00초 | 장면 전체 아래에서 떠오름 |
| 0.55초 | 「다음 장면」 아래에서 떠오름 |
| 0.85초 | 「2」 아래에서 떠오름 |
| 0.85초 | 숫자가 2.0 까지 세어 올라감 |
| 1.95초 | 손그림 선 그려짐 |

### 대본(`02_script/hybrid.json`)에 쓰는 법

`기본 — 쓰지 않아도 됨`

```json
[
 {
  "type": "bignum",
  "small": "앞 장면",
  "value": "1",
  "beats": [
   {
    "say": "앞 장면입니다."
   }
  ]
 },
 {
  "type": "bignum",
  "small": "다음 장면",
  "value": "2",
  "beats": [
   {
    "say": "다음 장면입니다."
   }
  ],
  "tr": "fade"
 }
]
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

### 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only transitions --force` (그림·영상·이 명세가 함께 갱신)

### 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/edit10.py:apply (전환) · ytflow/stages/uiflow.py:iris_out (모양 매치)` ``

## `push` — 밀기

**언제:** 장이 바뀔 때

**무엇:** 다음 장면이 옆에서 밀려 들어옴

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `push` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/tr_push.jpg`, 영상 `ytflow/looks/scenes/clips/tr_push.mp4`

### 화면 구성·움직임 원리

- 앞 장면이 왼쪽으로 12% 밀리며 사라지고, 다음 장면이 오른쪽 12%에서 밀려 들어옴(0.5초), whoosh-short

### 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| **장면 1** (`bignum`) | |
| 0.55초 | 「앞 장면」 아래에서 떠오름 |
| 0.85초 | 「1」 아래에서 떠오름 |
| 0.85초 | 숫자가 1.0 까지 세어 올라감 |
| 1.50초 | 장면 전체 사라짐 |
| 1.95초 | 손그림 선 그려짐 |
| **장면 2** (`bignum`) | |
| 0.00초 | 장면 전체 옆에서 밀려 들어옴 |
| 0.55초 | 「다음 장면」 아래에서 떠오름 |
| 0.85초 | 「2」 아래에서 떠오름 |
| 0.85초 | 숫자가 2.0 까지 세어 올라감 |
| 1.95초 | 손그림 선 그려짐 |

### 대본(`02_script/hybrid.json`)에 쓰는 법

`"tr": "push" (장 표지는 기본)`

```json
[
 {
  "type": "bignum",
  "small": "앞 장면",
  "value": "1",
  "beats": [
   {
    "say": "앞 장면입니다."
   }
  ]
 },
 {
  "type": "bignum",
  "small": "다음 장면",
  "value": "2",
  "beats": [
   {
    "say": "다음 장면입니다."
   }
  ],
  "tr": "push"
 }
]
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

### 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only transitions --force` (그림·영상·이 명세가 함께 갱신)

### 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/edit10.py:apply (전환) · ytflow/stages/uiflow.py:iris_out (모양 매치)` ``

## `wipe` — 색 판 닦기

**언제:** 분위기가 확 바뀔 때 (자주 쓰면 정신없음)

**무엇:** 강조색 판이 화면을 쓸고 지나감

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `wipe` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/tr_wipe.jpg`, 영상 `ytflow/looks/scenes/clips/tr_wipe.mp4`

### 화면 구성·움직임 원리

- 강조색 판이 왼쪽에서 화면을 덮고(앞 장면 끝 0.3초) 다음 장면에서 오른쪽으로 빠져나감(0.4초)

### 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| **장면 1** (`bignum`) | |
| 0.55초 | 「앞 장면」 아래에서 떠오름 |
| 0.85초 | 「1」 아래에서 떠오름 |
| 0.85초 | 숫자가 1.0 까지 세어 올라감 |
| 1.50초 | 「화면 덮개」 옆에서 밀려 들어옴 |
| 1.95초 | 손그림 선 그려짐 |
| **장면 2** (`bignum`) | |
| 0.00초 | 「화면 덮개」 옆에서 밀려 들어옴 |
| 0.55초 | 「다음 장면」 아래에서 떠오름 |
| 0.85초 | 「2」 아래에서 떠오름 |
| 0.85초 | 숫자가 2.0 까지 세어 올라감 |
| 1.95초 | 손그림 선 그려짐 |

### 대본(`02_script/hybrid.json`)에 쓰는 법

`"tr": "wipe"`

```json
[
 {
  "type": "bignum",
  "small": "앞 장면",
  "value": "1",
  "beats": [
   {
    "say": "앞 장면입니다."
   }
  ]
 },
 {
  "type": "bignum",
  "small": "다음 장면",
  "value": "2",
  "beats": [
   {
    "say": "다음 장면입니다."
   }
  ],
  "tr": "wipe"
 }
]
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

### 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only transitions --force` (그림·영상·이 명세가 함께 갱신)

### 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/edit10.py:apply (전환) · ytflow/stages/uiflow.py:iris_out (모양 매치)` ``

## `zoom` — 확대 흐림

**언제:** 한 부분으로 '들어가는' 느낌

**무엇:** 앞 장면이 커지며 흐려지고 다음 장면이 선명해짐

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `zoom` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/tr_zoom.jpg`, 영상 `ytflow/looks/scenes/clips/tr_zoom.mp4`

### 화면 구성·움직임 원리

- 앞 장면이 1.2배 커지며 흐려지고(blur 14px), 다음 장면이 0.82배·흐림에서 제자리로 선명해짐

### 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| **장면 1** (`bignum`) | |
| 0.55초 | 「앞 장면」 아래에서 떠오름 |
| 0.85초 | 「1」 아래에서 떠오름 |
| 0.85초 | 숫자가 1.0 까지 세어 올라감 |
| 1.50초 | 장면 전체 사라짐 |
| 1.95초 | 손그림 선 그려짐 |
| **장면 2** (`bignum`) | |
| 0.00초 | 장면 전체 확대·이동 |
| 0.55초 | 「다음 장면」 아래에서 떠오름 |
| 0.85초 | 「2」 아래에서 떠오름 |
| 0.85초 | 숫자가 2.0 까지 세어 올라감 |
| 1.95초 | 손그림 선 그려짐 |

### 대본(`02_script/hybrid.json`)에 쓰는 법

`"tr": "zoom"`

```json
[
 {
  "type": "bignum",
  "small": "앞 장면",
  "value": "1",
  "beats": [
   {
    "say": "앞 장면입니다."
   }
  ]
 },
 {
  "type": "bignum",
  "small": "다음 장면",
  "value": "2",
  "beats": [
   {
    "say": "다음 장면입니다."
   }
  ],
  "tr": "zoom"
 }
]
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

### 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only transitions --force` (그림·영상·이 명세가 함께 갱신)

### 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/edit10.py:apply (전환) · ytflow/stages/uiflow.py:iris_out (모양 매치)` ``

## `iris` — 원으로 열기

**언제:** 가벼운 장 전환

**무엇:** 화면 가운데 원이 닫혔다가 다음 장면이 원으로 열림

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `iris` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/tr_iris.jpg`, 영상 `ytflow/looks/scenes/clips/tr_iris.mp4`

### 화면 구성·움직임 원리

- 앞 장면 끝에 clip-path 원이 가운데로 닫히고, 다음 장면이 가운데 원으로 열림

### 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| **장면 1** (`bignum`) | |
| 0.55초 | 「앞 장면」 아래에서 떠오름 |
| 0.85초 | 「1」 아래에서 떠오름 |
| 0.85초 | 숫자가 1.0 까지 세어 올라감 |
| 1.50초 | 장면 전체 원으로 닫힘 |
| 1.95초 | 손그림 선 그려짐 |
| **장면 2** (`bignum`) | |
| 0.00초 | 장면 전체 원으로 열림 |
| 0.55초 | 「다음 장면」 아래에서 떠오름 |
| 0.85초 | 「2」 아래에서 떠오름 |
| 0.85초 | 숫자가 2.0 까지 세어 올라감 |
| 1.95초 | 손그림 선 그려짐 |

### 대본(`02_script/hybrid.json`)에 쓰는 법

`"tr": "iris"`

```json
[
 {
  "type": "bignum",
  "small": "앞 장면",
  "value": "1",
  "beats": [
   {
    "say": "앞 장면입니다."
   }
  ]
 },
 {
  "type": "bignum",
  "small": "다음 장면",
  "value": "2",
  "beats": [
   {
    "say": "다음 장면입니다."
   }
  ],
  "tr": "iris"
 }
]
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

### 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only transitions --force` (그림·영상·이 명세가 함께 갱신)

### 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/edit10.py:apply (전환) · ytflow/stages/uiflow.py:iris_out (모양 매치)` ``

## `iris_out` — 모양 매치 아이리스

**언제:** 앞 장면의 원(보호 범위·주체)에서 다음 이야기로 이어질 때

**무엇:** 앞 장면 속 원 모양이 테두리째 커져 화면을 덮고, 다음 장면이 원으로 열림

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `iris_out` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/tr_iris_out.jpg`, 영상 `ytflow/looks/scenes/clips/tr_iris_out.mp4`

### 화면 구성·움직임 원리

- 앞 장면 끝 0.75초: (x,y) 반지름 r 의 강조색 테두리 원이 나타나 화면 모서리까지 커지며 안이 바탕색으로 채워짐 (uiflow.iris_out)
- 다음 장면: 같은 바탕색 위에서 clip-path 원이 0 → 1400px 로 열림(0.6초, to 로 중심) — 두 장면이 따로 렌더돼도 색이 맞게 기본은 영상 팩 바탕색
- 한계: 원 안에 다음 장면을 직접 합성하지 않고 바탕색을 거침

### 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| **장면 1** (`bignum`) | |
| 0.55초 | 「앞 장면」 아래에서 떠오름 |
| 0.85초 | 「1」 아래에서 떠오름 |
| 0.85초 | 숫자가 1.0 까지 세어 올라감 |
| 1.05초 | 「원·배지」 나타남 |
| 1.25초 | 「원·배지」 바탕 색 바뀜 (커지며 화면을 덮음) |
| 1.95초 | 손그림 선 그려짐 |
| **장면 2** (`bignum`) | |
| 0.00초 | 장면 전체 원으로 열림 |
| 0.55초 | 「다음 장면」 아래에서 떠오름 |
| 0.85초 | 「2」 아래에서 떠오름 |
| 0.85초 | 숫자가 2.0 까지 세어 올라감 |
| 1.95초 | 손그림 선 그려짐 |

### 대본(`02_script/hybrid.json`)에 쓰는 법

`앞 장면에 "iris_out": {"x", "y", "r"}`

```json
[
 {
  "type": "bignum",
  "small": "앞 장면",
  "value": "1",
  "beats": [
   {
    "say": "앞 장면입니다."
   }
  ],
  "iris_out": {
   "x": 960,
   "y": 480,
   "r": 220
  }
 },
 {
  "type": "bignum",
  "small": "다음 장면",
  "value": "2",
  "beats": [
   {
    "say": "다음 장면입니다."
   }
  ]
 }
]
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

### 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only transitions --force` (그림·영상·이 명세가 함께 갱신)

### 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/edit10.py:apply (전환) · ytflow/stages/uiflow.py:iris_out (모양 매치)` ``
