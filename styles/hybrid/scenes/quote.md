# `quote` — 인용 카드

**언제:** 이름 있는 사람·매체의 말 한 문장. 원문 + 번역, 핵심어 형광펜

**예시 영상 (움직임):** [quote.mp4](https://drive.google.com/file/d/1duJVu6iZNVg8qR3mvE84gWIsvGfNgq5v/view) — Drive `ytflow/style-examples/` · 원본: `projects/20261120-market-deep` 완성본 7:10~7:34

## 박자표 — 무엇이 언제 나타나나
| 언제 | 화면 |
|---|---|
| 0.15초 | 종이 카드가 아래에서 떠오름(0.5초) |
| 0.4초 | 큰 따옴표 |
| 박자 1 +0.3초부터 0.5초 간격 | 번역 문장이 줄마다 |
| +0.6초 | 아래에 이름 자막(`who`·`role`) |
| +0.9초 | 원문(영어) 한두 줄 |
| +1.6초 (`mark` 박자가 있으면 그 박자) | `keyword` 에 형광펜(연필 소리), `note` 가 있으면 그 아래 ↳ 한 줄 |

## 대본(`02_script/hybrid.json`)에 쓰는 법
```json
{"type":"quote","insight":true,"who":"헌터브룩 미디어","role":"조사 보고서 … · 11.19",
 "quote":"AMD는 정말 엔비디아보다 안전한 대안일까?","keyword":"안전한 대안",
 "orig":"Is AMD really a safer alternative to Nvidia?","beats":[{"say":"…"},{"say":"…"}]}
```

## 만들기
`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

## 확인할 것
의견이면 `insight: true`('의견' 표시) · 원문과 번역이 같은 뜻인지 · 원본 영상이 있으면 `bite`(그 사람 목소리)를 먼저

코드: `ytflow/stages/hybrid.py `s_quote``
