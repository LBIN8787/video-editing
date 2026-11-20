<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `bite` — 원본 발언 컷

**언제:** CEO·연준·정부의 실제 발언 (원본이 있을 때만)

**무엇:** 긴 원본에서 대본과 맞는 문장만 잘라 그 사람 목소리로 + 원문·번역 2단

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `bite` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/bite.jpg`, 영상 `ytflow/looks/scenes/clips/bite.mp4`
  - 예시와 실제의 차이: 원본 영상이 없으면 인용 카드로 바뀌어 그려짐

## 화면 구성·움직임 원리

- 앞 내레이션 동안 원본 첫 화면을 멈춘 사진처럼(어둡게, 천천히 당김) + 이름 카드
- 이어서 cut 으로 찾은 구간만 이어 붙인 원본 목소리·영상 + 원문·번역 2단 자막
- 원본이 없으면 인용 카드(quote)로 바뀌어 그려짐 (bite_fallback)

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "bite" + python -m ytflow cut`

```json
{
 "type": "bite",
 "who": "제롬 파월",
 "role": "연준 의장 · 2023년 6월 14일 FOMC 기자회견",
 "label": "FOMC 기자회견 2023.6.14",
 "beats": [
  {
   "say": "파월 의장의 설명을 직접 들어 보겠습니다."
  }
 ],
 "clip": {
  "src": "fomc",
  "lang": "en",
  "cuts": [
   {
    "from": "We've covered a lot of ground",
    "to": "have yet to be felt",
    "ko": "우리는 많이 왔고, 긴축의 효과는 아직 다 나타나지 않았습니다."
   },
   {
    "from": "today we decided to leave",
    "to": "policy interest rate unchanged",
    "ko": "그래서 오늘, 정책금리를 그대로 두기로 했습니다."
   }
  ]
 }
}
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

읽는 키 — 장면: `label, role, show_en, who` · 박자: `credit, dur, segs, video` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only bite --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/cutedit.py:154` `s_bite`
