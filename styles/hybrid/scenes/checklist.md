# `checklist` — 줄 목록

**언제:** 사건·조건·주장 3~5개를 차례로 쌓을 때. 줄마다 상태(확인 ✓ / 경고 △ / 아님 ✗ / 날짜)

**예시 영상 (움직임):** [checklist.mp4](https://drive.google.com/file/d/1WB0v-x5RTestBbb7_GtmIbfVX0XSvXyf/view) — Drive `ytflow/style-examples/` · 원본: `projects/20261120-market-deep` 완성본 1:46~2:18

## 박자표 — 무엇이 언제 나타나나
| 언제 | 화면 |
|---|---|
| 박자마다 | `upto` 번째 줄까지 이 박자에 나타남 |
| 줄의 `t` 낱말을 말하는 순간(-0.15초) | 네모 칸이 그려지고 글이 나타남(연필 소리) — `t` 가 없으면 박자 시작 +0.3초, 다음 줄은 0.9초 간격 |
| 줄이 나타난 뒤 +0.4~0.6초 | 상태 표시: ✓ 초록 체크 / △ 노란 경고 / ✗ 빨간 X 두 획 / 날짜는 오른쪽에 빨간 숫자 |
| 박자에 `stamp` | 박자 끝 1.2초 전 도장 |
| `motion` | 오른쪽 아래 숫자 카드 (x 150·text_w 900 으로 오른쪽을 비워 둠) |

## 대본(`02_script/hybrid.json`)에 쓰는 법
```json
{"type":"checklist","title":"그 한 달에 있었던 일","x":150,"text_w":900,"skin":"newsprint",
 "rows":[{"label":"엔비디아 젠슨 황 사임 — 리더십 질문","state":"warn","t":"사임"}, …],
 "beats":[{"say":"…젠슨 황이 물러나며…","upto":2},{"say":"…","upto":4}]}
```

## 만들기
`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

## 확인할 것
줄이 대사보다 먼저 다 뜨지 않는지(`upto`·`t`) · 글이 `text_w` 안에 맞는지 · 확인되지 않은 주장은 ✓ 대신 △

코드: `ytflow/stages/hybrid.py `s_checklist``
