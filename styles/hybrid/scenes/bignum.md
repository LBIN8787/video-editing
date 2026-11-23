# `bignum` — 큰 숫자 한 개

**언제:** 오늘 이야기의 출발점이 되는 숫자 하나(종가·규모·비율). 숫자가 곧 질문일 때

**예시 영상 (움직임):** [bignum.mp4](https://drive.google.com/file/d/1yD_LnfPrK2pW6p0l_6o-t8hHcMFCzWmn/view) — Drive `ytflow/style-examples/` · 원본: `projects/20261120-market-deep` 완성본 0:00~0:28

## 박자표 — 무엇이 언제 나타나나
| 언제 | 화면 |
|---|---|
| 박자 1 시작 +0.2초 | 위쪽 작은 설명 줄(`small`)이 나타남 |
| +0.5초 | 큰 숫자(`value`)가 0에서 세어 올라가며 나타남 (빨강, 230px) |
| +1.6초 | 숫자 밑에 빨간 손그림 밑줄이 그어짐(0.4초) |
| 박자 1 중 `t` 낱말을 말하는 순간 | 오른쪽에 작은 숫자 카드(`motion`)가 튀어나와 세어짐 |
| 박자 2 시작 +0.1~0.4초 | 아래에 비교 줄(`compare`): 이름 → 형광펜 → 비교 숫자, '톡' 소리 |
| 박자 2 중 `t` 낱말 | 다음 숫자 카드가 아래에 하나 더 |

## 대본(`02_script/hybrid.json`)에 쓰는 법
```json
{"type":"bignum","small":"앤트로픽 'ANT' 첫날 종가 · 11월 19일 미국 장 마감 기준","value":"97.17달러",
 "compare":{"label":"첫 거래 (미 동부 11시 48분, 보도)","value":"111.50달러"},
 "beats":[{"say":"…97.17달러에 마쳤습니다…","motion":[{"t":"13%","do":"count","value":"-12.9%","label":"첫 거래 대비 (계산)","x":1660,"y":690}]},
          {"say":"그런데 같은 날 …","motion":[{"t":"다우","do":"count","value":"-2.19%","label":"다우"}]}]}
```

## 만들기
`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

## 확인할 것
숫자 단위·출처(`label`) 표시 · 비교 숫자가 '무엇 대비'인지 · 카드가 큰 숫자를 가리지 않는지

코드: `ytflow/stages/hybrid.py `s_bignum``
