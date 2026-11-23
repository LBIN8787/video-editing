# 편집 스타일 라이브러리

> **지금 고르는 법 (2026-11-20):** 영상마다 상황에 맞춰 고릅니다 — 스타일 등록부·추천 `python -m ytflow recipes` · `style-pick <프로젝트>` (`styles/recipes/`), 박자별 장면 `edit-plan <프로젝트>`, 화풍 `looks` · `look <프로젝트>` (`styles/looks.yaml`), 구성요소 조합 `look <프로젝트> --set 카테고리=스타일` (`styles/components.yaml`), 눈으로 보는 목록은 `skills/looks-gallery`.
> 새 시각효과는 **목록 + 움직이는 예시 + 제작 명세**를 함께 둡니다 (manual/12 §0-1, v66). 아래 계열 표는 폴더 스타일의 길잡이입니다.

스타일 하나는 폴더 하나입니다. 어떤 에이전트(Claude Code, Codex)든 같은 파일을 읽고 같은 결과를 냅니다.

스타일은 **계열(family)** 로 나뉩니다. 계열이 다르면 대본의 화면 문법, 소스를 찾는 방법, 점검 기준이 다릅니다.
계열은 `styles/<id>/edit.yaml` 의 `edit.family` 에 적습니다.

### A. 원본 소스형 (`family: source`)
인터뷰·실적발표(어닝콜)·키노트·방송 출연에서 **CEO·CFO·업계 사람이 직접 말하는 원본 영상**이 뼈대입니다.
원래 목소리에 원문·번역 자막을 달고, 발언 2~3개마다 **핵심 요약 애니메이션 카드**로 편집점을 넣습니다.
- 대본 화면 문법: `prompts/script_source.md`
- 화면 비율: 원본 영상 40~55% · 요약·숫자 카드 30~40% · 기사 캡처 10~20%
- 소스 확보가 품질을 좌우합니다: YouTube 원본 구간은 `clip-order`(클라우드) → 사용자 PC `clip-fetch` 로 받습니다 (docs/50).

| id | 이름 | 렌더러 | 상태 | 쓰는 곳 |
|---|---|---|---|---|
| `hybrid` | 하이브리드 (사용자 요청 조합) | hybrid (원본 영상 + 인과 지도 + 손그림 도식) | draft | 원본 영상이 있는 경제·산업 분석 롱폼 |
| `sixsigma` | 식스시그마 | sixsigma (카드는 검은 배경 애니메이션) | reviewed | 기업·투자 뉴스, 실적·지분·딜 해설 (`ch-source-brief`) |
| `source-cut` | 원본 발언 컷편집 | hybrid 장면 `bite` (`cutedit.py`) | — | 어닝콜·기자회견에서 대본과 맞는 문장만 그 사람의 목소리로 |

### B. 자체 제작 인포그래픽형 (`family: infographic`)
**직접 그린 도식·차트·비유 그림**이 뼈대입니다. 원본 영상은 분위기용으로만 조금 씁니다. 클립 다운로드가 필요 없어 클라우드에서 끝까지 완성됩니다.
- 대본 화면 문법: `prompts/script_infographic.md`
- 화면 비율: 카드 70~85% · 문서·기사 캡처 10~20% · 원본 영상 0~15%

| id | 이름 | 렌더러 | 상태 | 쓰는 곳 |
|---|---|---|---|---|
| `mijudiary` | 미주일기 | paper | reviewed | 개념·원리·역사 해설 (종이 콜라주 + 손그림 애니메이션) |
| `moneycrew` | 머니크루 | flat | reviewed | 산업·공급망·실적 해설 (평면 인포그래픽 모션, 차트) |
| `explain-stage` | 설명 무대 | hybrid 장면 `afterline`·`spread`·`share`·`motionboard` (`explain.py`) | demo | 상황 설명 박자 — 시장 채널 상황 설명 기본 |
| `news-desk` | 뉴스 데스크 카드 | hybrid 장면 `newsdesk` | — | 한 소식 = 한 장 (주간 정리·매일 소식 2~3개) |
| `story-board` | 이야기 그림판 | hybrid 장면 `story` | demo | 호기심 — 이야기 자리, 여러 장소·인물을 한 장으로 (04 §0-7) |
| `illustrated` | 손그림 삽화 | hybrid 장면 `illust` | — | 재구성 삽화 (자료가 없을 때, 그림은 `art-gen`·사람) |
| `anim-stage` | 애니메이션 무대 | hybrid 장면 `stage` | — | 한 화면 한 생각 — 자료가 없는 구간의 인물 행동 |
| `motion-metaphor` | 움직이는 비유 | hybrid 장면 `metaphor` | — | 사용자가 고를 때만 (매뉴얼 기준 아님) |

### C. 쇼츠 (`family: shorts`)
| id | 이름 | 렌더러 | 상태 | 쓰는 곳 |
|---|---|---|---|---|
| `shorts-aitips` | AI 꿀팁 쇼츠 | shorts | reviewed | 9:16: GitHub·AI 활용 소재 (`python -m ytflow shorts`) |
| `hook-shorts` (레시피) | 훅 쇼츠 (얼굴 없이) | `python -m ytflow hookshort` | — | 실제 화면 꽉 채움·훅 제목·큰 자막 |
| `presenter-shorts` | 말하는 사람 쇼츠 | `python -m ytflow presenter` | — | 본인 촬영 영상이 있을 때만 |

### 어느 계열을 쓸까
| 주제 | 계열 |
|---|---|
| 실적발표·인터뷰·청문회처럼 **당사자의 말**이 핵심 | 원본 소스형 |
| 개념·구조·역사·숫자 비교처럼 **설명**이 핵심, 또는 원본 영상이 부족 | 인포그래픽형 |

### 모든 계열 공통: 일반인용 대본
`prompts/script.md` 의 원칙(핵심 한 문장, 논리 구조, 숫자 + 비교 기준, 비유 2개 이상, 과거 사례 1개 이상, 어려운 말 풀이)을 따르고,
`python -m ytflow validate` 가 이를 점검합니다. 어려운 말 목록은 `data/jargon.json` 입니다.

## 렌더러
| renderer | 코드 | 겉모습 |
|---|---|---|
| `hybrid` | `ytflow/stages/hybrid.py` | HyperFrames 장면별 렌더: 원본 영상·이름 자막·인과 지도·빗금 도식 |
| `sixsigma` | `ytflow/stages/cards.py` | 검은 배경 정지 카드 + 원본 영상 |
| `paper` | `ytflow/stages/paper.py` | 종이 질감 + 손그림 애니메이션 |
| `shorts` | `ytflow/stages/shorts.py` | 9:16: 고정 훅 + 가운데 창(페이지 스크롤·카드·큰 글씨) + 큰 자막 |
| `flat` | `ytflow/stages/flat.py` | paper 애니메이션 엔진 + 평면 프로필 (단색 배경, 곧은 선, 굵은 고딕) |

카드 종류(chart · line · number_compare · bars · flow · table · headline · text · analogy)는 모든 렌더러가 공통으로 따릅니다.
`analogy` 는 '실제 숫자 ≈ 일상 비유' 두 칸 카드, `chart` 에 `start`/`end` 를 주면 과거 기간(예: 2000년 시스코)의 실제 시세를 그립니다.

## 폴더 구성
| 파일 | 역할 | 만드는 방법 |
|---|---|---|
| `STYLE.md` | 스타일 문서: 화면 문법, 구현 상태, 체크리스트 | `ytflow style` 이 초안을 쓰고 사람이 다듬음 |
| `edit.yaml` | 렌더러 설정: 색, 속도, 자막 방식 | `ytflow style` 측정값으로 자동 생성 |
| `script.md` | 이 스타일로 대본을 쓸 때 추가 규칙 | 초안 자동 생성 후 사람이 다듬음 |
| `rules.json` / `metrics.json` | 분석 원자료 | `ytflow style` |
| `work/` | 장면 미리보기 이미지 | 타 채널 화면이라 저장소에 올리지 않음 |

## 쓰는 법
```bash
python -m ytflow styles                                         # 목록
python -m ytflow make --style-ref mijudiary                     # 이 스타일로 영상 제작
python -m ytflow style <id> ref1.mp4 ref2.mp4 --title <이름>    # 새 스타일 추가
```
새 스타일을 추가하는 절차는 `skills/edit-style-new/SKILL.md` 에 있습니다.

## 연출과 그래픽 (2026-11-07~) — docs/13-direction-vs-graphics.md
편집 스타일 = **연출 문법**(장면 종류·편집점·편집 포인트·리듬, 대본 hybrid.json) + **그래픽 스킨**(`skins/<id>/skin.yaml`: 색·글꼴·배경·선 질감·사진 톤·자막 상자).
연출은 그대로 두고 스킨만 갈아 끼울 수 있다: `paper-sketch`(종이 손그림, 기본) · `clean-flat`(평면 인포그래픽) · `dark-doc`(어두운 다큐).
