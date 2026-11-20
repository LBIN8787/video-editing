<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `parking` — 주차장 칸

**언제:** 공급·수요, 자리가 차고 비는 비유

**무엇:** 주차 칸이 차례로 차거나 비는 그림

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `parking` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/parking.jpg`, 영상 `ytflow/looks/scenes/clips/parking.mp4`

## 화면 구성·움직임 원리

- 주차장 칸 격자(먹색 칸) → 빈 칸만 흰색으로 남고, 오른쪽 큰 비율 숫자
- 빈자리 비율처럼 '거의 다 찼다'를 보여 줄 때

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.20초 | 「2023 상반기 · CBRE (InsideNoVa …」 아래에서 떠오름 |
| 0.20초 | 「빈자리 0.94%」 아래에서 떠오름 |
| 0.50초 | 손그림 선 그려짐 |
| 0.65초 | 요소 아래에서 떠오름 |
| 2.75초 | 「0.94%」 아래에서 떠오름 |
| 2.95초 | 손그림 선 그려짐 |
| 2.95초 | 「빈자리 비율」 아래에서 떠오름 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "parking"`

```json
{
 "type": "parking",
 "label": "2023 상반기 · CBRE (InsideNoVa 보도)",
 "title": "빈자리 0.94%",
 "beats": [
  {
   "say": "2023년 상반기 빈자리 비율이 0.94%. 100칸 주차장에 빈칸이 1칸도 안 남은 셈입니다.",
   "fill": true
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `label, title` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only parking --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/hybrid.py:822` `s_parking`
