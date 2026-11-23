# `analogy` — 비유 두 칸

**언제:** 어려운 구조를 생활 속 물건으로 옮길 때. 왼쪽(익숙한 것) ≈ 오른쪽(지금 일)

**예시 영상 (움직임):** [analogy.mp4](https://drive.google.com/file/d/1gntzQVakAUmd7VBrmajqud_Aa8oXgbpH/view) — Drive `ytflow/style-examples/` · 원본: `projects/20261120-market-deep` 완성본 4:16~4:42

## 박자표 — 무엇이 언제 나타나나
| 언제 | 화면 |
|---|---|
| 박자 1 +0.2초 | 왼쪽 상자 → 아이콘 → 이름 → 작은 설명 (잉크색) |
| +1.2초 | 가운데 '≈' |
| +1.4초 | 오른쪽 상자 (빨강) 같은 순서 |
| 박자 2 시작 1초 전 | 아래로 화살표 |
| 박자 2 시작 0.5초 전 | 결론 줄(`result`) 아이콘 + 글 |

## 대본(`02_script/hybrid.json`)에 쓰는 법
```json
{"type":"analogy","title":"정품이 진열되면",
 "left":{"icon":"package","label":"정품이 없을 땐 비슷한 물건을","sub":"아마존·알파벳·브로드컴"},
 "right":{"icon":"store","label":"정품이 진열되자 정품으로","sub":"앤트로픽 직접 매수"},
 "result":{"icon":"wallet","label":"지갑은 하나 — 대체품을 내놓고 정품을 산다"},
 "beats":[{"say":"이렇게 비유할 수 있습니다…"},{"say":"지갑은 하나입니다…","show_result":true}]}
```

## 만들기
`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

## 확인할 것
이름이 상자(460px)를 넘으면 두 줄로 자동 나눔 — 그래도 길면 줄이기 · 비유가 사실처럼 보이지 않게 `label` 에 '비유'

코드: `ytflow/stages/hybrid.py `s_analogy``
