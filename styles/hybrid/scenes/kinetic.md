# `kinetic` — 키네틱 글자

**언제:** 결론 한 문장·장 전환 한 줄. 목소리가 말하는 순간 낱말이 박힘 (화면 글자가 곧 자막)

**예시 영상 (움직임):** [kinetic.mp4](https://drive.google.com/file/d/10QIVmNXXiB_opqz4RQsLb9J-HeiepuTS/view) — Drive `ytflow/style-examples/` · 원본: `projects/20261120-market-deep` 완성본 14:55~15:00

## 박자표 — 무엇이 언제 나타나나
| 언제 | 화면 |
|---|---|
| 말하는 낱말마다 | 그 순간 낱말이 화면에 나타남 — 덩어리(한 줄) 단위로 위로 밀려 올라가며 바뀜 |
| `hit` 낱말·숫자 | 크게, 강조색 |
| 마지막 덩어리 | 옅어지며 끝남 |
| `note` | 아래 작은 설명(+0.6초) |

## 대본(`02_script/hybrid.json`)에 쓰는 법
```json
{"type":"kinetic","beats":[{"say":"새 주식이 들어설 자리를, 시장 전체가 내줬습니다.","hit":["자리를","전체가"]}]}
```

## 만들기
`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

## 확인할 것
아래 자막은 자동으로 끔(화면 글자가 자막) · 한 편에 몇 번만(롱폼 전체를 키네틱으로 하지 않음) · `hit` 은 1~3개

코드: `ytflow/stages/directions.py `s_kinetic` · `_kinetic_beat``
