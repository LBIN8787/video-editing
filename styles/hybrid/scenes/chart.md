<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `chart` — 시세 선 그래프

**언제:** 주가·지수·환율의 최근 흐름 (시장 채널)

**무엇:** 실제 시세 선이 그려지고 마지막 구간 강조 + 값

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `chart` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/chart.jpg`, 영상 `ytflow/looks/scenes/clips/chart.mp4`

## 화면 구성·움직임 원리

- 실제 시세(marketdata, ticker·period)를 최근 60일로 잘라 먹색 선을 그림, 오른쪽 가격 눈금
- 마지막 n일(focus_last)을 강조색 굵은 선 + 동그라미, 마지막 값은 선과 안 겹치는 빈자리에
- 다음 박자 stamp → 도장. 시장 채널은 확대 없음(zoom off)

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.20초 | 「2026.11.06 · 야후 파이낸스 (11/6 종…」 아래에서 떠오름 |
| 0.20초 | 「코스피, 선거 뒤 이틀」 아래에서 떠오름 |
| 0.30초 | 선 그려짐 |
| 0.50초 | 손그림 선 그려짐 |
| 1.55초 | 선 그려짐 |
| 2.05초 | 손그림 선 그려짐 |
| 2.25초 | 「4,869.96」 아래에서 떠오름 |
| 2.55초 | 「5,683 → 5,059」 아래에서 떠오름 |
| 5.55초 | 「외국인 -6.2조」 크게서 찍힘(도장) |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "chart", "ticker": ...`

```json
{
 "type": "chart",
 "label": "2026.11.06 · 야후 파이낸스 (11/6 종가는 뉴스 보도)",
 "ticker": "^KS11",
 "period": "3mo",
 "title": "코스피, 선거 뒤 이틀",
 "beats": [
  {
   "say": "11월 6일, 코스피가 이틀 만에 11% 가까이 떨어졌습니다.",
   "focus_last": 3,
   "mark": "5,683 → 5,059"
  },
  {
   "say": "외국인은 그 이틀 동안 6조 원 넘게 팔았습니다.",
   "stamp": "외국인 -6.2조"
  }
 ],
 "append": [
  {
   "date": "2026-11-06",
   "close": 5059.69,
   "source": "11/6 종가: 뉴스 보도 (팩트시트 F19)"
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `append, label, period, ticker, title` · 박자: `focus_last, mark` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only chart --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/hybrid.py:261` `s_chart`
