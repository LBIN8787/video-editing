# `bars` — 막대 비교

**언제:** 같은 단위의 값 2~6개를 한눈에 비교 (지수 등락·업종·종목). 음수는 기준선 아래로

**예시 영상 (움직임):** [bars.mp4](https://drive.google.com/file/d/1pnlWsrvCke45fr1kE6UkvVUm9OVZFfxx/view) — Drive `ytflow/style-examples/` · 원본: `projects/20261120-market-deep` 완성본 0:29~1:00

## 박자표 — 무엇이 언제 나타나나
| 언제 | 화면 |
|---|---|
| 박자 1 시작 +0.1초 | 기준선이 그어짐(0.5초) |
| 각 항목의 `t` 낱말을 말하는 순간 | 그 막대가 자라남(0.6초, 연필 소리) — `t` 가 없으면 0.4초 + 순서×0.6~0.9초 |
| 막대가 선 뒤 +0.4초 | 값이 막대 끝에 세어 올라감 / 이름은 막대와 동시에 |
| `emph` 번호의 막대 | 강조색(빨강·금색), 나머지는 잉크색 빗금 |
| 다음 박자의 `t` 낱말 | 오른쪽에 숫자 카드(`motion`) |

## 대본(`02_script/hybrid.json`)에 쓰는 법
```json
{"type":"bars","title":"19일(목) 미국 장 (%)","emph":0,
 "items":[{"label":"반도체 지수","value":-2.41,"text":"-2.41","t":"반도체"},
          {"label":"나스닥","value":-2.25,"text":"-2.25","t":"나스닥은"}, …],
 "beats":[{"say":"나스닥은 2.25%, 다우는 …"},{"say":"…","motion":[{"t":"변동성","do":"count","value":"28.44","label":"VIX"}]}]}
```

## 만들기
`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

## 확인할 것
막대가 말보다 늦지 않은지(`t` 를 대사의 실제 낱말로) · 음수가 아래로 그려졌는지 · 4개 이상이면 이름이 겹치지 않는지

코드: `ytflow/stages/hybrid.py `s_bars``
