<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `apartments` — 칸 채우기 (세대 수)

**언제:** 수백~수천 단위의 몫을 한눈에

**무엇:** 작은 칸(세대) 수백 개 중 대기·취소가 색으로 채워짐

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `apartments` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/apartments.jpg`, 영상 `ytflow/looks/scenes/clips/apartments.mp4`

## 화면 구성·움직임 원리

- 작은 칸(세대) total 개를 20열 격자로 → waiting 칸이 노랗게, cancel 칸이 빨갛게 차례로 칠해짐
- 아래 범례·형광펜 설명 — 큰 수의 몫을 '아파트 동'으로

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.20초 | 「자체 정리 (서스케하나 숫자를 아파트로)」 아래에서 떠오름 |
| 0.20초 | 「아파트 148개 동으로 바꾸면」 아래에서 떠오름 |
| 0.50초 | 손그림 선 그려짐 |
| 0.55초 | 요소 아래에서 떠오름 |
| 1.35초 | 「148개 동 = 계획 전체 148GW」 아래에서 떠오름 |
| 4.25초 | 요소 움직임 |
| 4.65초 | 「형광펜」 옆으로 펼쳐짐 |
| 4.75초 | 「허가 대기 60개 동」 아래에서 떠오름 |
| 6.25초 | 요소 움직임 |
| 6.45초 | 「최악이면 취소 12개 동」 아래에서 떠오름 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "apartments"`

```json
{
 "type": "apartments",
 "label": "자체 정리 (서스케하나 숫자를 아파트로)",
 "title": "아파트 148개 동으로 바꾸면",
 "total": 148,
 "waiting": 60,
 "cancel": 12,
 "beats": [
  {
   "say": "아파트로 바꿔 보면, 148개 동을 짓기로 했는데",
   "stage": 1
  },
  {
   "say": "60개 동은 아직 구청 허가를 기다리고, 최악이면 그중 12개 동이 취소되는 셈입니다.",
   "stage": 3
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `cancel, label, title, total, waiting` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only apartments --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/hybrid.py:684` `s_apartments`
