# 팩트시트 — AI 가 다음 AI 를 만들기 시작했다 (2026-11-25 조사)

형식: 기술·산업 트렌드 + 원리 해설(11 §3-1). 회사 주장과 독립 시각을 나눕니다.
표시: ✅ 1차 출처 · ⚠️ 보도·2차 · 💬 해석 · 🏢 회사 자체 측정(회사 주장)

## A. 앤트로픽 원문 — 'When AI builds itself' (앤트로픽 인스티튜트, 2026, '9/18 업데이트' 포함) https://www.anthropic.com/institute/recursive-self-improvement
| # | 내용 | 표시 |
|---|---|---|
| A1 | 정의: 재귀적 자기개선 = AI 가 자기 후계 모델을 "fully autonomously designing and developing" 하는 것. "We are not there yet, and recursive self-improvement is not inevitable." | ✅ |
| A2 | 2026년 5월 기준, 회사 코드베이스에 합쳐진 코드의 80% 넘게를 Claude 가 씀(경영진 추정은 90% 이상) — 단 "lines of code is an imperfect measure"(양이지 질 아님) | ✅🏢 |
| A3 | 엔지니어 1인당 하루 합친 코드: 2026년 2분기가 2024년의 8배 — 회사가 "almost certainly an overstatement"라고 스스로 적음 | ✅🏢 |
| A4 | 최적화 과제(속도 올리기): Claude Opus 4(2025-05) 약 3배 → Mythos Preview(2026-04) 약 52배. 숙련자는 4~8시간에 약 4배 | ✅🏢 |
| A5 | 자율 연구 시연(2026-04): 에이전트가 성능 격차의 97% 를 메움(사람 둘은 23%), 누적 800시간·연산비 약 1만 8천 달러 — 단 "didn't transfer cleanly to production-scale models", "humans still chose the problem and created the scoring rubric" | ✅🏢 |
| A6 | '연구 감각' 시험(n=129): 사람 선택보다 낫다고 판정된 비율 Opus 4.5 51%(2025-11) → Mythos Preview 64%(2026-04). 단 사람이 개선할 여지가 있던 장면을 골랐고, 대조 묶음(127개)에선 약 20% | ✅🏢 |
| A7 | 외부 측정(METR): AI 가 해내는 과제 길이가 약 4개월마다 두 배. "In 2027, AI systems could be capable of tasks that take a person weeks." | ✅(회사가 인용한 외부 측정) |
| A8 | 시나리오 셋: ① 추세가 멈춤 ② 사람이 방향을 정한 채 효율이 복리로 쌓임("likely heading into") ③ 완전한 재귀적 자기개선("least certain"). 시간표의 마지막 칸은 "20XX?" | ✅ |
| A9 | 제안: 최전선 AI 개발을 늦추거나 잠시 멈출 "option"이 있는 게 세상에 좋다 — 멈춤을 확인할 검증 체계 제안 | ✅ |

## B. 보도
| # | 내용 | 출처 | 표시 |
|---|---|---|---|
| B1 | AP(2026-09-17): 앤트로픽 발표에 따르면 Claude 가 회사 모델 연구개발의 **26% 를 '주도'**(높은 수준 지시만으로 대부분을 끝까지, 사람 감독 아래), 약 90% 는 '협업'(사람이 가까이서 지휘). 주도 비율은 2월 0 → 8월 4분의 1 | https://www.click2houston.com/business/2026/09/18/anthropic-says-its-model-claude-is-helping-to-build-the-next-version-of-itself/ | ⚠️ 회사 발표의 보도(원문 공지는 못 찾음) |
| B2 | AP: 8월 기준 약 3만 개의 에이전트가 연구·엔지니어링 작업 | 같은 기사 | ⚠️ 쓰지 않음(원문 미확인) |

## C. 독립·반대 시각 (이름 있는 사람만)
| # | 누가 | 말 | 출처 | 표시 |
|---|---|---|---|---|
| C1 | 드와케시 파텔(AI 인터뷰 진행자·작가) | 최고 수준 AI 연구자를 완전히 자동화하는 해의 중앙값 "2028", 2027년 초지능은 아니라고 봄 · METR 의 가속 증거는 약하다는 반론을 소개 | https://www.dwarkesh.com/p/rsiobjections (2026-11-24) | ✅(본인 글) |
| C2 | 세브 크리에(같은 글에서 인용된 반론) | AI 장악 시나리오는 '부엉이 그리는 법' 같다 — 중간 단계가 빠져 있다 | 같은 글 | ⚠️(인용의 인용) |
| C3 | 같은 글이 정리한 병목 | 비싼 GPU(연산), 사람이 고리 안에 남음, 연구 성과 측정의 어려움 | 같은 글 | ⚠️(요약) |
| C4 | 데이비드 색스(백악관 AI 자문) 등 | 회사들의 안전 경고는 정교한 "regulatory capture"(규제를 자기에게 유리하게) 시도라는 비판 | AP 2026-09-27 https://abcnews.com/Technology/wireStory/anthropic-openai-sound-alarm-ai-safety-seek-shape-136794636 | ⚠️(보도) |
| C5 | 장링화·리윈허(arXiv, 2026-11-22) | 모델이 자기 가중치 수정 프로그램을 직접 써서 다섯 세대 반복 — 수학 문제 정확도 73.95% → 76.45%. 27B 모델 하나, 수학 하나의 작은 결과 | https://arxiv.org/abs/2611.29513 | ✅(논문 초록, 동료 심사 전) |

## 인사이트 (11 §3-3 — 통찰을 뒷받침 / 반박하는 이름 있는 시각)
**통찰(이 영상의 주장, 💬):** AI 가 AI 를 만드는 고리에서 사람에게 남은 마지막 칸은 '무엇을 풀지 고르는 일'이다. 그리고 지금 업계의 진짜 질문은 그 칸마저 넘어가느냐다.
| 쪽 | 누가 (소속) | 날짜 | 원문 한 줄 | 근거 | 출처 |
|---|---|---|---|---|---|
| 뒷받침 | 앤트로픽 (회사 원문) | 2026 | "humans still chose the problem and created the scoring rubric" | 자율 연구 시연의 단서 | A5 |
| 뒷받침 | 고팔 사르마 외 (랜드연구소) | 2026-10-12 | "no disclosed system sets its own research agenda or designs its own successors" | 공개된 연구소 발표 검토 · 자동화 비율을 체계적으로 보고하지 않는 문제 | https://www.rand.org/pubs/perspectives/PEA5068-1.html |
| 반박 (그 칸도 넘어간다) | 드와케시 파텔 (AI 인터뷰 진행자) | 2026-11-24 | 최고 AI 연구자 완전 자동화 중앙값 "2028" | 추세 외삽 | C1 |
| 반박 | 앤트로픽 (회사 측정) | 2026-04 | 연구 감각 판정 64% (대조 20%) | 갈림길 선택 비교 | A6 |
| 반박 | 드루브 스리칸스 외 (arXiv) | 2026-09-22 | 에이전트가 자기 연구 코드를 고쳐 "seven successive improvements" (8일, 자율) | 작은 규모·동료 심사 전 | https://arxiv.org/abs/2609.26457 |
| 다른 축 (경고 자체를 의심) | 데이비드 색스 (백악관 AI 자문) 등 | 2026-09 | 안전 경고는 "regulatory capture" 시도 | 정치적 비판 | C4 ⚠️ |
| 측정 | METR (외부 평가 기관) | 2026 | 과제 길이 약 4개월마다 두 배 | 외부 측정 | A7 |

## 💬 우리 해석
- I1. 고리(연구 → 더 나은 모델 → 더 빠른 연구)의 여러 칸에 AI 가 들어갔지만, **문제를 고르고 채점 기준을 정하는 칸은 아직 사람**입니다 — 근거 A5(회사 스스로 인정), A8.
- I2. 공개된 숫자 대부분은 회사 자체 측정이고, 회사가 스스로 붙인 단서(A2·A3·A6)가 숫자만큼 중요합니다.
- I3. 그래서 지금은 '닫힌 고리'가 아니라 '사람 손이 점점 짧아지는 고리'로 보입니다 — 근거 A8 시나리오 ②.

## 쓰지 않는 것
- "곧 인간을 넘는다", "통제 불능" 같은 단정. 3만 에이전트(B2). 미토스의 사이버 능력 세부(다른 주제).
- 공정성: 이 채널은 제작에 AI(앤트로픽 Claude 포함)를 씁니다 → 설명란에 밝힘, 비판 시각을 같은 무게로.
