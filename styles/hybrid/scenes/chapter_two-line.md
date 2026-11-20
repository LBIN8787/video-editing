<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `chapter@two-line` — 두 줄 장 표지

**언제:** 문제·비판 꼭지를 나눌 때 (앞부분은 표지 없이 흐르다가)

**무엇:** 어둡게 깐 실사 위 작은 흰 줄 → 큰 강조색 줄

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `chapter@two-line` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/chapter_two-line.jpg`, 영상 `ytflow/looks/scenes/clips/chapter_two-line.mp4`
  - 예시와 실제의 차이: 예시의 바탕은 '실사 자리' 색 그라데이션

## 화면 구성·움직임 원리

- clip 이 있으면 실사 전체 화면(아주 느린 확대), 없으면 장면 바탕 위에 rgba(8,9,12,dim=0.62) 어두운 막
- 0.45초 작은 흰 줄(kicker) 떠오름 → 0.85초 큰 강조색 줄(title, 스킨 강조색을 38% 밝힘) 떠오름 + 그림자, 소리 whoosh-short
- 색은 color 로, 라임은 lime: true

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.00초 | 영상 움직임 |
| 0.45초 | 「묻지도 않고」 아래에서 떠오름 |
| 0.85초 | 「전화를 겁니다」 아래에서 떠오름 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "chapter", "look": "two-line", "kicker", "title"`

```json
{
 "type": "chapter",
 "num": "1",
 "look": "two-line",
 "kicker": "묻지도 않고",
 "title": "전화를 겁니다",
 "clip": {
  "src": "ph",
  "start": 0
 },
 "beats": [
  {
   "say": "첫 번째 문제입니다."
  }
 ]
}
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

읽는 키 — 장면: `color, dim, kicker, lime, title` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only chapter@two-line --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/uiflow.py:443` `chapter_two_line`
