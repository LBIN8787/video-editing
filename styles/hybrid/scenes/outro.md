# `outro` — 마무리 카드

**언제:** 영상 끝. 실사·자료 영상 위에 흐린 막 + 종이 카드 한 장

**예시 영상 (움직임):** [outro.mp4](https://drive.google.com/file/d/1LELn4La13CQ7QoulbhPu619tz6UtT8lp/view) — Drive `ytflow/style-examples/` · 원본: `projects/20261120-market-deep` 완성본 14:58~15:14

## 박자표 — 무엇이 언제 나타나나
| 언제 | 화면 |
|---|---|
| 0초 | 바탕 영상(`clip`)이 천천히 밀려 들어옴 |
| 0.6초 | 영상 위에 흐린 막(0.8초) |
| 0.7초 | 종이 카드가 떠오름 |
| 0.9초 | 제목 |
| 1.4초 | 빨간 밑줄 |
| 1.8초 | 작은 글(`sub`) |

## 대본(`02_script/hybrid.json`)에 쓰는 법
```json
{"type":"outro","title":"20일 낮까지의 소식","sub":"출처는 설명란에","clip":{"src":"racks","start":0},
 "beats":[{"say":"딱 하나만 기억한다면 이것입니다…"}]}
```

## 만들기
`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

## 확인할 것
바탕 영상 라이선스·출처 · 카드 글이 바탕과 대비되는지

코드: `ytflow/stages/hybrid.py `s_outro``
