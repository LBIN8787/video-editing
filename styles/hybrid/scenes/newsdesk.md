<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `newsdesk` — 뉴스 데스크 카드

**언제:** 여러 소식을 차례로 (AI 뉴스 정리, 브리핑)

**무엇:** 한 소식 = 한 장 — 꼬리표·큰 제목·숫자 3칸·증거 패널

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `newsdesk` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/newsdesk.jpg`, 영상 `ytflow/looks/scenes/clips/newsdesk.mp4`
  - 예시와 실제의 차이: 예시의 오른쪽 증거 패널은 캡처가 없어 비어 있음

## 화면 구성·움직임 원리

- 한 소식 = 한 장 고정 틀: 위 진행 막대(idx/total)·출처 → 꼬리표·날짜 → 큰 제목(hl 강조) → 요약 → 숫자 3칸(stats) → 점 목록
- 오른쪽 증거 패널(panel: 캡처 shot·큰 숫자·도장)이 panel_beat 박자에
- 아래 출처·채널 주소. 색은 그래픽 팩 색을 따름

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.20초 | 「진행 막대」 움직임 |
| 0.25초 | 「이슈」 아래에서 떠오름 |
| 0.35초 | 「창업자가」 아래에서 떠오름 |
| 0.70초 | 「젠슨 황, 사장·CEO·이사직에서 즉시 사임」 아래에서 떠오름 |
| 8.06초 | 「주가 (11/12)」 아래에서 떠오름 |
| 8.06초 | 「이사회 의장은 하비 존스」 옆에서 밀려 들어옴 |
| 8.21초 | 「임시 CEO」 아래에서 떠오름 |
| 8.26초 | 「정식 CEO는 안팎에서 찾는 중」 옆에서 밀려 들어옴 |
| 8.26초 | 요소 옆에서 밀려 들어옴 |
| 8.36초 | 「첫 실적」 아래에서 떠오름 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "newsdesk"`

```json
{
 "type": "newsdesk",
 "idx": 1,
 "total": 3,
 "source": "NVIDIA",
 "tag": "이슈",
 "tag_color": "red",
 "date": "11월 11일 공시",
 "headline": "창업자가 물러났다",
 "hl": "물러났다",
 "sub": "젠슨 황, 사장·CEO·이사직에서 즉시 사임",
 "stats": [
  {
   "label": "주가 (11/12)",
   "value": "-4.34%",
   "color": "red"
  },
  {
   "label": "임시 CEO",
   "value": "크레스 CFO",
   "color": "white"
  },
  {
   "label": "첫 실적",
   "value": "11/17",
   "color": "yellow"
  }
 ],
 "bullets": [
  "이사회 의장은 하비 존스",
  "정식 CEO는 안팎에서 찾는 중"
 ],
 "panel": {
  "kind": "shot",
  "src": "footage/nvidia.jpg",
  "caption": "엔비디아 본사 간판 · CC BY 2.0 Will Buckner",
  "pos": "50% 40%"
 },
 "footer": "출처: 엔비디아 8-K 공시·보도자료 (SEC, 2026.11.11)",
 "beats": [
  {
   "say": "첫 번째 소식, 엔비디아입니다. 젠슨 황이 사장과 CEO, 이사직에서 즉시 물러났습니다."
  },
  {
   "say": "주가는 4.34% 내렸고, 콜레트 크레스 CFO가 임시 CEO를 맡습니다. 첫 시험대는 11월 17일 실적입니다."
  }
 ]
}
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

읽는 키 — 장면: `accent, brand, bullets, date, footer, handle, headline, hl, idx, panel, panel_beat, source, stats, sub, tag, tag_color, total` · 박자: `motion` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only newsdesk --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/newsdesk.py:33` `s_newsdesk`
