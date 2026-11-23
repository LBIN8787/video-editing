# `versus` — 맞대기

**언제:** 엇갈린 두 시각·주장 vs 부인·기대 vs 현실

**예시 영상 (움직임):** [versus.mp4](https://drive.google.com/file/d/1uze0c79ORRf8IRmXsjG541SM-n_fSjn9/view) — Drive `ytflow/style-examples/` · 원본: `projects/20261120-market-deep` 완성본 10:28~10:50

## 박자표 — 무엇이 언제 나타나나
| 언제 | 화면 |
|---|---|
| 박자 1 +0.2초 | 왼쪽 아이콘 → 큰 글자 → 설명 |
| +1.2초 | 가운데 'vs' |
| +1.4초 | 오른쪽 (강조색) 같은 순서 |
| 박자 2 +0.3초 | 오른쪽 큰 글자에 동그라미 |
| +1.0초 | `question` 이 있으면 아래 질문 한 줄('톡') |

## 대본(`02_script/hybrid.json`)에 쓰는 법
```json
{"type":"versus","insight":true,
 "left":{"value":"주장","label":"헌터브룩: 명단 뒤에도 펌웨어가 갔다","icon":"file-text"},
 "right":{"value":"부인","label":"AMD: 사업 관행을 왜곡했다","icon":"shield"},
 "beats":[{"say":"…"},{"say":"…","question":"(선택) 남는 질문"}]}
```

## 만들기
`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

## 확인할 것
양쪽 근거·출처가 `label` 에 · 한쪽 편을 드는 말투가 아닌지 · 큰 글자는 두 글자 안팎

코드: `ytflow/stages/hybrid.py `s_versus``
