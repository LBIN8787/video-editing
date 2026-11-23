<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `motionboard` — 자유 무대

**언제:** 정해진 틀에 안 맞는 설명 — 사람과 물건 사이 관계가 움직일 때

**무엇:** 인물·카드·글자·화살표를 놓고 박자마다 나타남·이동·강조·바꿈

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `motionboard` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/motionboard.jpg`, 영상 `ytflow/looks/scenes/clips/motionboard.mp4`

## 화면 구성·움직임 원리

- els 에 요소를 미리 선언(person·card·img·text·arrow·brush·ban·dashed, 위치 x·y)
- 박자 do 에 나올 요소와 동작(move·hide·hi·dim·swap)을 적으면 그대로 연기 — 정해진 틀이 없는 관계 설명용
- theme: paper(구겨진 종이)·light·dark

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.15초 | 「보호예수가 풀리면」 아래에서 떠오름 |
| 0.50초 | 「초기 투자자」 튀어나옴 |
| 0.95초 | 「주식」 튀어나옴 |
| 1.40초 | 「묶여 있음」 튀어나옴 |
| 3.34초 | 「보호예수 해제」 튀어나옴 |
| 3.79초 | 「묶여 있음」 사라짐 |
| 4.24초 | 「주식」 움직임 |
| 5.66초 | 「새 투자자」 튀어나옴 |
| 6.11초 | 선 그려짐 |
| 6.41초 | 「매도」 아래에서 떠오름 |
| 6.51초 | 선 그려짐 |
| 6.56초 | 요소 튀어나옴 |
| 6.56초 | 「주식」 둥실 움직임(반복) |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "motionboard"`

```json
{
 "type": "motionboard",
 "title": "보호예수가 풀리면",
 "theme": "paper",
 "els": {
  "inv": {
   "kind": "person",
   "x": 420,
   "y": 600,
   "name": "초기 투자자",
   "role": "상장 전에 산 사람",
   "tone": "gray"
  },
  "buy": {
   "kind": "person",
   "x": 1500,
   "y": 600,
   "name": "새 투자자",
   "role": "시장에서 사는 사람"
  },
  "stock": {
   "kind": "card",
   "x": 700,
   "y": 640,
   "icon": "files",
   "label": "주식"
  },
  "free": {
   "kind": "text",
   "x": 960,
   "y": 260,
   "text": "보호예수 해제",
   "size": 64,
   "color": "red"
  },
  "note": {
   "kind": "text",
   "x": 700,
   "y": 480,
   "text": "묶여 있음",
   "pen": true,
   "color": "red"
  },
  "sell": {
   "kind": "arrow",
   "from": "inv",
   "to": "buy",
   "label": "매도",
   "color": "red",
   "bend": 0.2
  }
 },
 "beats": [
  {
   "say": "상장 전에 산 주식은 한동안 묶여 있습니다.",
   "do": [
    "inv",
    "stock",
    "note"
   ]
  },
  {
   "say": "보호예수가 풀리면 팔 수 있게 됩니다.",
   "do": [
    "free",
    {
     "hide": "note"
    },
    {
     "move": "stock",
     "to": [
      1180,
      640
     ]
    }
   ]
  },
  {
   "say": "그 물량이 시장으로 나옵니다.",
   "do": [
    "buy",
    "sell",
    {
     "hi": "stock"
    }
   ]
  }
 ]
}
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

읽는 키 — 장면: `els` · 박자: `at, do` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only motionboard --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/explain.py:522` `s_board`
