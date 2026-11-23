<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `card_type` — 검은 카드 타자기

**언제:** 인용·핵심 문장, 무거운 한 마디

**무엇:** 검은 바탕에 한 줄씩 타자로 쳐짐

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `card_type` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/card_type.jpg`, 영상 `ytflow/looks/scenes/clips/card_type.mp4`

## 화면 구성·움직임 원리

- 검은 카드 바탕에 lines 가 박자마다 한 줄씩 타자기로 쳐짐, by 로 말한 사람
- 인용·무거운 한 문장

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.55초 | 요소 나타남 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "card_type"`

```json
{
 "type": "card_type",
 "lines": [
  "이 병은",
  "스페인에서 시작되지 않았다."
 ],
 "beats": [
  {
   "say": "이 병은 스페인에서 시작되지 않았습니다. 스페인이 가장 심하게 당한 나라도 아니었고요."
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `by, lines` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only card_type --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/directions.py:76` `s_card_type`
