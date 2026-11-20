# `chapter` — 장 표지

**언제:** 장이 바뀌는 순간. 번호 + 짧은 제목 한 줄

**예시 영상 (움직임):** [chapter.mp4](https://drive.google.com/file/d/1Aa_JCX4AKbPSD5BaeLtZ6r2s4VHtYhM5/view) — Drive `ytflow/style-examples/` · 원본: `projects/20261120-market-deep` 완성본 1:10~1:18

## 박자표 — 무엇이 언제 나타나나
| 언제 | 화면 |
|---|---|
| 0초 | 종이 한 장이 오른쪽에서 밀려 들어옴(0.7초, '휙' 소리) — `type` 판이면 강조색 판이 왼쪽→오른쪽으로 덮음 |
| 0.6초 | 아이콘 |
| 0.7초 | 장 번호 |
| 0.9초 | 장 제목 |
| 1.3초 | 제목 밑 빨간 밑줄(0.45초) |

## 대본(`02_script/hybrid.json`)에 쓰는 법
```json
{"type":"chapter","num":"1","title":"한 달 사이, 갈라진 AI","icon":"trending-down","look":"board",
 "beats":[{"say":"하루만 보면 놓치는 것이 있습니다. 한 달 전으로 돌아가 보겠습니다."}]}
```

## 만들기
`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

## 확인할 것
제목은 한 줄로 · 장 표지 사진을 쓰면 주제와 맞는지(같은 사진 반복 없음, 06 G5)

코드: `ytflow/stages/hybrid.py `s_chapter` · graphics.py `chapter_type``
