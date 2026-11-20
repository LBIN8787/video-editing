<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `kb` — 자료 사진 켄 번스

**언제:** 역사·사건의 자료 사진 (아카이브 다큐)

**무엇:** 자료 사진 가득 + 천천히 움직임 + 필름 가장자리 + 타자기 날짜·장소

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `kb` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/kb.jpg`, 영상 `ytflow/looks/scenes/clips/kb.mp4`
  - 예시와 실제의 차이: 예시는 사진 없이 렌더해 어두운 바탕만 — 실제는 자료 사진이 천천히 움직임

## 화면 구성·움직임 원리

- 자료 사진·영상을 화면 가득 + 켄 번스(move 방향으로 천천히 확대·이동) + 필름 가장자리 어둡게
- 타자기 날짜·장소 도장(stamp), 박자 lower 로 이름 자막

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.00초 | 영상 움직임 |
| 0.20초 | 「자료 화면 · 미국 의회도서관」 아래에서 떠오름 |
| 0.30초 | 요소 아래에서 떠오름 |
| 0.50초 | 요소 나타남 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "kb"`

```json
{
 "type": "kb",
 "clip": {
  "src": "march",
  "start": 0
 },
 "move": "in",
 "stamp": "1918 · 프랑스 서부전선",
 "label": "자료 화면 · 미국 의회도서관",
 "beats": [
  {
   "say": "1918년, 전 세계 사람 세 명 중 한 명이 같은 병에 걸렸습니다."
  },
  {
   "say": "우리는 이 병을 '스페인 독감'이라고 부르죠. 그런데 이상한 점이 하나 있습니다."
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `label, move, stamp` · 박자: `lower` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only kb --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/directions.py:57` `s_kb`
