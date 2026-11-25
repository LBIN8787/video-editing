# 팩트시트 — 아무도 읽을 수 없는 증명: 리만가설과 AI (2026-11-25 조사)

표시: ✅ 1차·원문 확인 · ⚠️ 보도·2차 · 💬 해석. 기사 4곳(사이언티픽 아메리칸·피즈닷오알지(The Conversation)·알자지라·IBM Think)은 원문을 읽음. 스미스소니언은 403 으로 못 읽음.

## A. 리만가설이란 (배경 — 널리 확인된 사실)
| # | 사실 | 출처 |
|---|---|---|
| A1 | 1859년 베른하르트 리만이 소수의 개수에 관한 논문에서 제시. 리만 제타 함수의 '자명하지 않은 영점'은 모두 실수부가 1/2 인 직선(임계선) 위에 있다는 추측 | ✅ 클레이 수학연구소 https://www.claymath.org/millennium/riemann-hypothesis/ · 위키백과 https://en.wikipedia.org/wiki/Riemann_hypothesis |
| A2 | 리만은 논문에서 "sehr wahrscheinlich"(매우 그럴듯하다)라고만 적고 증명을 미뤄 둠 | ✅ 위키백과(리만 원문 인용) |
| A3 | 1900년 힐베르트의 23개 문제 중 8번, 2000년 클레이 밀레니엄 문제 7개 중 하나, 상금 100만 달러 | ✅ 클레이 · 위키백과 |
| A4 | 왜 중요한가: 소수가 얼마나 고르게 흩어져 있는지(소수 정리의 오차)를 가장 정확하게 알려 줌. 수많은 정리가 '리만가설이 참이라면'을 전제로 함 | ✅ 클레이 · 위키백과 |
| A5 | 계산으로는 처음 10조 개(10¹³) 넘는 영점이 모두 그 직선 위에 있음이 확인됨 — 그러나 계산은 증명이 아님(무한히 많음) | ✅ 위키백과 (Gourdon 2004) |

## B. 2026년 11월 20일
| # | 사실 | 출처 | 표시 |
|---|---|---|---|
| B1 | 앤트로픽 소속 수학자 레벤트 알푀게가 11월 20일(금) 자기 누리집의 4쪽짜리 글(alpo.ge/remark.pdf)로 발표: "I believe I have, working with Claude, discovered a proof of the Riemann Hypothesis" | SciAm(조셉 하울렛) · 알자지라 · IBM | ⚠️ 보도 일치 (원문 PDF 는 다시 확인) |
| B2 | 주장은 더 넓은 '일반화된 리만가설'까지 | 피즈닷오알지 · SciAm 본문 · 알자지라 | ⚠️ |
| B3 | 증명은 사람이 읽는 글이 아니라 Lean(컴퓨터가 한 단계씩 검사하는 증명 언어) 코드 약 1,700만 줄로 공개 | 피즈닷오알지 · 알자지라 | ⚠️ |
| B4 | 알푀게: AI 로 쓴 영어 설명이 "250,000+ pages" — 올리는 것은 부적절 | 피즈닷오알지 | ⚠️ |
| B5 | 알푀게: "Claude far outpaced me near the finish line" | 알자지라 | ⚠️ |
| B6 | 앤드루 서덜랜드(MIT)가 Lean 으로 따로 컴파일함: "This is indeed an historic moment." · Lean FRO 와 Mathlib 공동체가 증명이 맞다고 믿는다는 공동 성명 | SciAm · 피즈닷오알지 | ⚠️ |
| B7 | 검증의 범위: '코드가 통과했다'(컴퓨터 검사)는 확인, '사람이 논리를 이해·검토했다'는 아직 — IBM(11-23 갱신) "Independent mathematicians have yet to verify the result" · 피즈닷오알지: 진술을 Lean 으로 옮긴 방식에 문제가 있을 수 있음 | IBM · 피즈닷오알지 | ⚠️ 매체마다 '검증' 뜻이 다름 |
| B8 | 같은 날, 미국수학회 회장 라비 바킬이 스탠퍼드 수학자 알레산드로 마시울로의 일반화된 리만가설 증명 원고(940쪽, 'The Music of the Primes', "all human, with no AI")를 급히 소개 — 몇 시간 만에 문제 가능성이 지적됨 | 피즈닷오알지 | ⚠️ (12년 작업은 보도 1곳 — 쓰지 않음) |
| B9 | 발표는 앤트로픽 상장 다음 날 | SciAm · 피즈닷오알지 | ⚠️ |
| B10 | 앞선 부분 결과: 해당 값들의 적어도 67.25% 가 예측대로임을 보인 AI 보조 결과, 유네스 람주리가 AI 없이 더 짧은 증명(arXiv 2609.02882) | 알자지라 · IBM | ⚠️ |

## 인사이트 (11 §3-3)
**통찰(💬):** 수학에서 처음으로 '맞다는 것'과 '왜 맞는지 아는 것'이 갈라졌다. 컴퓨터는 맞다고 하는데, 사람은 아직 이유를 모른다.
| 쪽 | 누가 (소속) | 원문 한 줄 | 출처 |
|---|---|---|---|
| 역사적 사건 | 앤드루 서덜랜드 (MIT) | "This is indeed an historic moment." | SciAm |
| 역사적 사건 | 제임스 메이너드 (옥스퍼드, 2022 필즈상) | "If this fully checks out, it is clearly a historic milestone in mathematics." | IBM |
| 이해는 없다 | 케빈 버저드 (임페리얼 칼리지) | "At the minute, we don't even know why the theorem is true." | 알자지라 |
| 이해는 없다 | 유네스 람주리 (로렌대) | "Mathematics is mainly about understanding why something is true." | IBM |
| 이해는 없다 | 대니얼 리트 (수학자) | 맞을 가능성이 "exceedingly likely", "No human understands it yet." | 피즈닷오알지 |
| 사람에게 공을 | 아비셰크 사하 (런던 퀸메리대) | 몇 년은 남았다고 봤다, "shatters my model of reality" · 공은 사람(알푀게)에게 | 알자지라 |
| 새 길 | 엑토르 파스텐 (칠레 가톨릭대) | 맞다면 수학 분야 사이의 "Rosetta Stone" | SciAm |

## 쓰지 않는 것
- '증명 완료'·'풀렸다' 단정 — "컴퓨터 검사는 통과, 사람의 검토는 진행 중"으로.
- 상금 지급 여부(어느 기사도 말하지 않음), 마시울로 12년, 1,700만 줄이 누구 것인지에 대한 매체 간 혼선(스미스소니언 미확인).
- 이 채널은 제작에 AI(Claude 포함)를 씀 → 설명란에 밝힘.
