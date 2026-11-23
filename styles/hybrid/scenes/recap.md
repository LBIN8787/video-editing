<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `recap` — 장 끝 정리판

**언제:** 긴 영상의 장 끝 정리

**무엇:** 지금까지의 결론 한 줄씩 쌓임, 이전 줄은 흐리게

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `recap` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/recap.jpg`, 영상 `ytflow/looks/scenes/clips/recap.mp4`

## 화면 구성·움직임 원리

- '여기까지 정리' 제목 → 결론 한 줄씩 왼쪽에서 밀려 쌓임(번호 칩), new_from 이전 줄은 흐리게
- 장 끝에 지금까지를 다시 묶을 때

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.20초 | 「정리」 아래에서 떠오름 |
| 0.20초 | 「여기까지 정리」 아래에서 떠오름 |
| 0.50초 | 손그림 선 그려짐 |
| 0.65초 | 「1」 옆에서 밀려 들어옴 |
| 0.65초 | 「<path d="M145.541,247.603L14…」 튀어나옴 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "recap"`

```json
{
 "type": "recap",
 "title": "여기까지 정리",
 "items": [
  "길이 막혀, 팔 수 있는 양이 30% 가까이 줄었다"
 ],
 "new_from": 0,
 "beats": [
  {
   "say": "정리하면, 길이 막혀 팔 수 있는 양이 30% 가까이 줄었습니다."
  }
 ],
 "layers": [
  {
   "kind": "locator",
   "at": [
    56.4,
    26.5
   ],
   "label": "막힌 길목 · 호르무즈",
   "beat": 0,
   "side": "right",
   "top": 600,
   "scale": 2.2
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `items, label, new_from, title` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only recap --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/edit10.py:101` `s_recap`
