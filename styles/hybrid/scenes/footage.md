<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `footage` — 실사 영상

**언제:** 실제 장면이 있을 때 — 신뢰·현장감

**무엇:** 원본 영상 전체 화면 또는 종이 위 사진처럼 + 이름 자막·쪽지 주석

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `footage` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/footage.jpg`, 영상 `ytflow/looks/scenes/clips/footage.mp4`
  - 예시와 실제의 차이: 예시는 '실사 자리' 색 그라데이션

## 화면 구성·움직임 원리

- clip 의 원본 구간을 장면 길이만큼 잘라(소리 없음) 전체 화면(frame: full, 위아래 어둡게·종이색 테두리) 또는 종이 위 사진(frame: photo, 흰 테두리·테이프·기울임)
- 박자 lower → 이름 자막(왼쪽 아래 띠), vox → 종이 쪽지 + 형광펜 + 펜 메모, chips → 말 칩

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.00초 | 영상 움직임 |
| 0.20초 | 「자료 화면 · 텍사스 코퍼스크리스티 (NASA, 2…」 아래에서 떠오름 |
| 5.06초 | 「AI 데이터센터를 멈춰야」 튀어나옴 |
| 5.51초 | 「형광펜」 옆으로 펼쳐짐 |
| 5.86초 | 손그림 선 그려짐 |
| 6.06초 | 「당선인 발언 · 아직 법은 아님」 아래에서 떠오름 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "footage", "clip": {...}`

```json
{
 "type": "footage",
 "label": "자료 화면 · 텍사스 코퍼스크리스티 (NASA, 2019)",
 "clip": {
  "src": "texas",
  "start": 18,
  "frame": "full"
 },
 "beats": [
  {
   "say": "그런데 방아쇠는 한국이 아니라 미국 텍사스에서 당겨졌습니다."
  },
  {
   "say": "선거에서 이긴 새 주지사가, AI 데이터센터를 멈춰야 한다고 말했거든요.",
   "vox": {
    "text": "AI 데이터센터를 멈춰야",
    "note": "당선인 발언 · 아직 법은 아님"
   }
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `clip, label` · 박자: `chip_gap, chips, lower, vox` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only footage --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/hybrid.py:222` `s_footage`
