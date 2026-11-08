# 05. 편집 스타일 고르기 — 영상마다, 장면마다

편집 스타일 = **연출**(무엇이 언제 어떻게 바뀌나: 장면 type·박자·편집점) + **그래픽 팩**(색·글꼴·배경·차트 모양: `skins/<id>`). 둘은 따로 고릅니다 (docs/13).
한 영상 안에서도 연출은 섞습니다. 그래픽 팩은 **한 영상에 하나**(채널 정체성).

## 0. 먼저 자동 추천을 받습니다
편집 스타일은 **등록부** `styles/recipes/*.yaml` 에 있습니다 (`python -m ytflow recipes` 로 목록). 각 레시피는 어떤 브랜드·질문 유형·분위기·소스에 맞는지(`fits`)와 영상 안에서 맡는 자리(`roles`: 전체·본론·훅·결론)를 적어 둡니다.
```bash
python -m ytflow style-pick <프로젝트>   # topic_brief.json → 영상 전체·훅·결론 스타일 + 이유 → 01_research/style_pick.md
```
추천을 출발점으로 아래 표로 장면 단위를 다듬습니다. 추천과 다르게 고르면 이유를 `style_pick.md` 끝에 적습니다. 스타일을 늘리는 법은 `07-extend.md`.

## 1. 영상 단위: 그래픽 팩 고르기
| 그래픽 팩 | 느낌 | 어울리는 브랜드·주제 |
|---|---|---|
| `paper-sketch` (기본) | 종이 + 손그림 | curiosity 전반, market 칼럼(개념·인과) |
| `clean-flat` | 미색 평면, 굵은 막대 | market 데이터 리포트, ai 비교 |
| `dark-doc` | 어두운 다큐, 필름 | curiosity 사건·전쟁·재난, market 위기·폭락 |
| `newsprint` | 누런 신문, 먹색 | curiosity 근현대사, market '그때 신문은' 과거 사례 |
| `blueprint` | 남색 모눈, 흰 선 | ai 원리 설명, market 산업·공급망 구조 |
| `kinetic-poster` | 크림 + 검정 굵은 글자 (자막 숨김) | 쇼츠, 짧은 요약 영상 |

정하는 법: **브랜드 기본값**(ai=blueprint 또는 clean-flat, market=paper-sketch 또는 clean-flat, curiosity=paper-sketch) → 주제 분위기가 확실히 다르면(재난·위기 → dark-doc, 100년 전 → newsprint) 바꿈. 같은 채널에서 3편 연속 다른 팩은 피합니다(정체성).
미리 비교: `python -m ytflow skin-preview <프로젝트> --skins paper-sketch,dark-doc,newsprint`.

## 2. 장면 단위: 연출 type 고르기 (말하는 내용 → 화면)
| 이 문장이 하는 일 | 1순위 type | 2순위 | 피할 것 |
|---|---|---|---|
| 사건의 **장면**을 연다 (사람·장소·날짜) | `kb` (자료 화면 켄 번스 + 도장) | `footage` | 글자 카드 |
| **질문·명제 한 줄**을 던진다 | `card_type` (타자기) | `chapter` | 그림 넣기 |
| 누가 **말했다** | `footage` + `lower` (원본) | `quote` (카드 + 형광펜) | 내레이션으로만 |
| **원인 → 결과**를 잇는다 | `map_causal` (같은 칸 위치 유지) | `analogy` | 장면마다 새 도식 |
| **어디서 어디로** 퍼졌다·움직였다 | `journey` (지도 여정) | `usmap` | 표 |
| 주가·지표가 **움직였다** | `chart` (실제 시세, 마지막 구간 확대) | `bignum` | 손그림 가짜 그래프 |
| 둘을 **비교**한다 | `versus` (숫자 두 개) | `bars`, `compare` | 숫자 나열 |
| **비율**을 느끼게 한다 | `people` (100명 중 N명) | `parking`, waffle | 퍼센트 글자만 |
| **시간 순서** | `timeline` | `checklist`(date) | |
| 신문·보도의 **차이** | `newspapers` | `quote` | |
| 모양·패턴 (U자·W자) | `shape` (개념도 표시) | | 숫자 축 있는 척 |
| 꼭 기억할 **한 문장** (결론·훅) | `kinetic` (단어가 말과 함께) | `card_type` | 9분 내내 kinetic |
| 따라 하기 **단계** | `footage`(화면 녹화) + `vox` 주석 | `checklist` | |

## 3. 리듬 규칙 (docs/15 근거, `check` 가 일부 자동 검사)
- 자료 화면(footage·kb·journey 사진)이 **45초 넘게 없으면 안 됨**.
- 같은 type 연속 금지 (chapter 제외 3연속은 실패).
- 첫 30초: 장면(닻) → 질문 → 오늘의 지도. 장면 길이 6~10초.
- 약 3분마다 질문형 장 표지 또는 반전 문장 (다시 붙잡기).
- 장면 평균 10~15초, 25초 넘는 장면은 박자 안에서 화면이 바뀌어야 함(reveal·focus·카메라).

## 4. 브랜드별 추천 조합 (출발점)
| 브랜드 | 훅 | 본론 | 결론 |
|---|---|---|---|
| ai | footage(결과 화면) → kinetic 한 줄 | analogy · versus · footage+vox(따라 하기) · checklist | checklist(오늘 해 볼 것) → outro |
| market | chart(급등락 확대) → card_type 질문 | timeline · map_causal · footage+lower(발언) · compare(과거) | checklist(확인할 신호·반증) → outro |
| curiosity | kb(장면) → card_type 질문 | journey · footage · versus · people · newspapers | kinetic(답 한 문장) → outro |

## 5. 시험작 (같은 이야기를 다른 연출로)
`docs/16-new-styles.md` — 아카이브 다큐(dark-doc) · 지도 여정(newsprint) · 키네틱 타이포(kinetic-poster).
새 스타일을 시험할 때도 같은 방법: `python scripts/style_demo.py <원본> <시험작> <스펙.json>` (같은 문장·목소리 재사용, 비용 0).
