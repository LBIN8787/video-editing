<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `isotype` — 사물 아이콘 줄

**언제:** '10통 중 3통' 같은 몫을 물건으로 느끼게

**무엇:** 아이콘 N개 중 일부가 흐려지며 빠짐

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `isotype` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/isotype.jpg`, 영상 `ytflow/looks/scenes/clips/isotype.mp4`

## 화면 구성·움직임 원리

- 아이콘(icon) total 개를 한 줄로 → 그중 lost 개가 흐려지며 빠짐
- before·after 숫자 라벨 2개가 차례로 — '10통 중 3통'을 물건으로

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.20초 | 「IEA 자료 보도 (파이낸셜뉴스)」 아래에서 떠오름 |
| 0.20초 | 「사우디 원유 생산 (하루)」 아래에서 떠오름 |
| 0.50초 | 손그림 선 그려짐 |
| 0.75초 | 요소 튀어나옴 |
| 1.65초 | 「2월 1,040만 배럴」 아래에서 떠오름 |
| 6.32초 | 요소 사라짐 |
| 7.27초 | 「3월 725만 배럴」 아래에서 떠오름 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "isotype"`

```json
{
 "type": "isotype",
 "label": "IEA 자료 보도 (파이낸셜뉴스)",
 "title": "사우디 원유 생산 (하루)",
 "icon": "fuel",
 "total": 10,
 "lost": 3,
 "before": "2월 1,040만 배럴",
 "after": "3월 725만 배럴",
 "beats": [
  {
   "say": "사우디 생산도 2월 하루 1,040만 배럴에서, 3월 725만 배럴로 줄었습니다."
  },
  {
   "say": "열 통을 팔던 나라가, 세 통을 못 팔게 된 셈입니다."
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `after, before, icon, label, lost, title, total` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only isotype --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/edit10.py:132` `s_isotype`
