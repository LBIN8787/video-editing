<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `illust` — 손그림 삽화 카메라

**언제:** 사람들의 생각·행동·상황, 옛 사례 재현 (그림은 사람이 준비)

**무엇:** 삽화 한 장 위를 카메라가 박자마다 옮겨 가며 표시·생각 풍선

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `illust` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/illust.jpg`, 영상 `ytflow/looks/scenes/clips/illust.mp4`
  - 예시와 실제의 차이: 예시는 삽화 없이 렌더해 빈 틀 — 실제는 준비한 삽화 위를 카메라가 옮겨 감

## 화면 구성·움직임 원리

- 삽화 한 장(art)을 붓 쓸기로 드러냄(reveal) → 박자마다 카메라가 moves 의 자리로 옮겨 감
- marks: 손그림 동그라미·화살표·생각 풍선, boil 로 선이 살아 움직임. 그림은 사람이 준비(art-brief)

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.00초 | 「화면 덮개」 움직임 |
| 0.00초 | 요소 나타남 |
| 0.20초 | 「임시 그림: 카미유 피사로 「르아브르 광장」 189…」 아래에서 떠오름 |
| 5.45초 | 요소 움직임 |
| 6.95초 | 「또 올랐네…」 튀어나옴 |
| 12.65초 | 요소 움직임 |
| 12.80초 | 「또 올랐네…」 사라짐 |
| 14.05초 | 요소 움직임 |
| 14.35초 | 「금리 +5%p」 아래에서 떠오름 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "illust"`

```json
{
 "type": "illust",
 "art": "havre.jpg",
 "reveal": "paint",
 "credit": "임시 그림: 카미유 피사로 「르아브르 광장」 1893 · 시카고 미술관 CC0",
 "brief": "1950년대풍 미국 거리, 장바구니를 든 사람들이 가게 앞 가격표를 보며 한숨 (오른쪽 위는 은행 건물)",
 "moves": [
  {
   "beat": 0,
   "focus": [
    0,
    0,
    1,
    1
   ]
  },
  {
   "beat": 1,
   "focus": [
    0.0,
    0.42,
    0.55,
    0.58
   ]
  },
  {
   "beat": 2,
   "focus": [
    0.45,
    0.35,
    0.55,
    0.65
   ]
  }
 ],
 "marks": [
  {
   "beat": 1,
   "kind": "bubble",
   "at": [
    1380,
    230
   ],
   "text": "또 올랐네…"
  },
  {
   "beat": 2,
   "kind": "note",
   "at": [
    1180,
    200
   ],
   "text": "금리 +5%p"
  }
 ],
 "beats": [
  {
   "say": "2023년 6월, 미국 사람들은 1년 넘게 오른 물가에 지쳐 있었습니다."
  },
  {
   "say": "5월 소비자물가는 1년 전보다 4% 올랐습니다. 연준이 목표로 하는 2%의 두 배죠."
  },
  {
   "say": "연준은 그사이 금리를 5%포인트나 올렸습니다. 그리고 이날, 처음으로 인상을 멈췄습니다."
  }
 ]
}
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

읽는 키 — 장면: `art, boil, credit, mark_color, marks, moves, reveal` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only illust --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/illust.py:96` `s_illust`
