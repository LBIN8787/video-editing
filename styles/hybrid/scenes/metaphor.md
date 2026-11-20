<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `metaphor` — 움직이는 비유

**언제:** 사용자가 고를 때만 (따로 쓰는 스타일)

**무엇:** 무리가 한쪽으로 옮겨 가고 의태어가 튀어나옴

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `metaphor` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/metaphor.jpg`, 영상 `ytflow/looks/scenes/clips/metaphor.mp4`

## 화면 구성·움직임 원리

- 무리(crowd)가 한쪽(target)으로 옮겨 가고 의태어(words)가 튀어나오는 비유 장면, 화살표·강조(hl)·꼬리표(tag)
- 사용자가 고를 때만 쓰는 따로 스타일

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.20초 | 「코어위브 3분기 어닝콜 공식 녹취록 (2026.11…」 아래에서 떠오름 |
| 0.35초 | 요소 움직임 |
| 0.45초 | 「수요가 용량의」 아래에서 떠오름 |
| 0.55초 | 「공급 가능한 용량」 튀어나옴 |
| 0.65초 | 요소 아래에서 떠오름 |
| 0.75초 | 「AI 연구소」 튀어나옴 |
| 0.75초 | 요소 아래에서 떠오름 |
| 0.90초 | 「기업」 튀어나옴 |
| 0.90초 | 요소 아래에서 떠오름 |
| 0.95초 | 선 그려짐 |
| 0.96초 | 요소 아래에서 떠오름 |
| 1.05초 | 「금융사」 튀어나옴 |
| 1.70초 | 선 나타남 |
| 7.60초 | 요소 움직임 |
| 8.24초 | 「줄 서는 중」 튀어나옴 |
| 8.26초 | 요소 움직임 |
| 8.94초 | 「공급 가능한 용량」 둥실 움직임(반복) |
| 8.95초 | 요소 움직임 |
| 9.24초 | 「바글바글」 튀어나옴 |
| 9.25초 | 요소 움직임 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "metaphor"`

```json
{
 "type": "metaphor",
 "mode": "migrate",
 "label": "코어위브 3분기 어닝콜 공식 녹취록 (2026.11.10) · 회사 발표",
 "title": "수요가 용량의 10배",
 "hl": "10배",
 "target": {
  "label": "공급 가능한 용량",
  "color": "#D9412B",
  "kind": "bus"
 },
 "sources": [
  {
   "label": "AI 연구소",
   "color": "#2F6FB3"
  },
  {
   "label": "기업",
   "color": "#2E9D6A"
  },
  {
   "label": "금융사",
   "color": "#E0A82E"
  }
 ],
 "crowd": {
  "icon": "person",
  "n": 40,
  "start": "right",
  "beat": 1,
  "board": 0.85
 },
 "words": [
  {
   "text": "바글바글",
   "side": "left",
   "beat": 1
  },
  {
   "text": "줄 서는 중",
   "side": "right",
   "beat": 1
  }
 ],
 "arrow": {
  "beat": 0
 },
 "beats": [
  {
   "say": "코어위브 CEO는 2027년 말까지 공급할 수 있는 용량보다, 검증된 수요가 10배 많다고 했습니다."
  },
  {
   "say": "버스 한 대에 손님이 열 배 몰린 셈이죠. 회사는 다 태우지 않고, 더 좋은 조건을 기다린다고까지 했습니다."
  }
 ]
}
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

읽는 키 — 장면: `arrow, crowd, hl, label, mode, object, sources, tag, target, title, words` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only metaphor --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/motion.py:125` `s_metaphor`
