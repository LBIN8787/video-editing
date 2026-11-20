<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `zoomshot` — 화면 자동 줌

**언제:** 웹페이지·앱 화면의 한 곳을 가리킬 때

**무엇:** 자료 화면 위에서 카메라가 박자마다 네모로 다가가고 선으로 표시

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `zoomshot` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/zoomshot.jpg`, 영상 `ytflow/looks/scenes/clips/zoomshot.mp4`
  - 예시와 실제의 차이: 예시는 자료 화면 없이 렌더해 빈 바탕 — 실제는 웹페이지·앱 캡처 위에서 다가감

## 화면 구성·움직임 원리

- 자료 화면(캡처·녹화)을 화면 가득 → 박자마다 focus 의 네모로 카메라가 다가가고, 그 자리를 얇은 선 테두리 + 이름표로 표시
- 다음 박자에 표시가 사라지고 다른 네모로

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.20초 | 「고치기 전 · unslop 예제 대시보드 (CC B…」 아래에서 떠오름 |
| 0.55초 | 요소 움직임 |
| 1.45초 | 요소 나타남 |
| 1.55초 | 「글자 그라데이션」 나타남 |
| 5.01초 | 요소 사라짐 |
| 5.01초 | 「글자 그라데이션」 사라짐 |
| 5.49초 | 요소 움직임 |
| 6.39초 | 요소 나타남 |
| 6.49초 | 「이모지 아이콘」 나타남 |
| 10.56초 | 요소 사라짐 |
| 10.56초 | 「이모지 아이콘」 사라짐 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "zoomshot"`

```json
{
 "type": "zoomshot",
 "clip": {
  "src": "before",
  "start": 0
 },
 "label": "고치기 전 · unslop 예제 대시보드 (CC BY 4.0)",
 "focus": [
  {
   "beat": 0,
   "box": [
    700,
    70,
    540,
    80
   ],
   "label": "글자 그라데이션"
  },
  {
   "beat": 1,
   "box": [
    395,
    230,
    300,
    330
   ],
   "label": "이모지 아이콘"
  }
 ],
 "beats": [
  {
   "say": "예제로는 언슬롭에 같이 들어 있는, 일부러 AI처럼 만든 대시보드를 썼습니다."
  },
  {
   "say": "이 영상을 만든 클로드 코드 세션에서, 설명서의 절차를 그대로 따라 적용했습니다."
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `focus, label` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only zoomshot --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/directions.py:521` `s_zoomshot`
