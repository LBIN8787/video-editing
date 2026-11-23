<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `studio3d` — 3D 무대

**언제:** 물건 하나를 입체로 보여 줄 때 (시안)

**무엇:** 어두운 스튜디오의 3D 물체가 움직임

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `studio3d` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/studio3d.jpg`, 영상 `ytflow/looks/scenes/clips/studio3d.mp4`

## 화면 구성·움직임 원리

- 어두운 스튜디오에 3D 물체(object·preset)를 그리고 메인 시간축이 매 프레임 다시 그림
- in·out·n·left·right 로 물체 수·좌우 이름. 시안 단계

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.20초 | 「코어위브 3분기 어닝콜 공식 녹취록 (2026.11…」 아래에서 떠오름 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "studio3d"`

```json
{
 "type": "studio3d",
 "preset": "stack",
 "left": "공급 가능한 용량",
 "right": "검증된 수요",
 "n": 10,
 "label": "코어위브 3분기 어닝콜 공식 녹취록 (2026.11.10) · 회사 발표",
 "beats": [
  {
   "say": "코어위브 CEO는 2027년 말까지 공급할 수 있는 용량보다,"
  },
  {
   "say": "검증된 수요가 10배 많다고 했습니다."
  }
 ]
}
```
대본 공통 키: `edit_v10` (예: map_causal 의 `map`)

읽는 키 — 장면: `in, label, left, n, object, out, preset, right, tag` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only studio3d --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/studio3d.py:157` `s_studio3d`
