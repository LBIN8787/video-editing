# 체크리스트 — 20261126-market-deep-dc-funding

매뉴얼 v135 · 2026-11-26T01:38:30 · **MUST 실패 4개**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ❌ | [2026-11-25 · 20261125-curiosity-riemann 기각] 불합격 입니다. 전부 이미지느낌보다는 글씨느낌에 애니메이션효과  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ✅ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | market |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 칩을 사 주는 쪽의 돈은 언제까지 버틸까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 사용자 요청 2026-11-26: '데이터센터를 구비하는 기업들의 현재 자금상태 … 반도체를 사려는 수요자들과 그 수요자들의 자금 흐름, 실제로 |
| G1 | MUST | 욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3) | ✅ | 강도 3 · 자료 2 |
| G1 | 참고 | 욕망 점수 합계 (후보끼리 비교할 때 씀) | ✅ | 합계 16 {'desire': 3, 'clarity': 3, 'timeliness': 2, 'demand': 3, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 3 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 반전(현금 2,651억 달러 회사가 빚을 냄) → 번 돈 vs 쓴 돈 표(공시, 직접 계산) → 틈을 메우는 돈 셋(빚·주식·장부 밖) → 약한 |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ⚠️ | 구조 · 실적 공시가 한꺼번에 보여 준 자금 흐름의 변화 + 연준 두 곳의 분석 |
| G2 | SHOULD | 시장: SAVE(오선) 시장 소식 알림 확인 기록 — 상태 '확인함' 또는 '확인 못 함: 이유' (01_research/save_check.md) | ⚠️ | save_check.md 없음 (python -m ytflow daily 가 만듦) |
| G2 | SHOULD | 시장: SAVE 실제로 확인함 (항목 1개 이상) | ⚠️ |  · 항목 0 |
| G2 | MUST | 자료 화면마다 credit·url | ❌ | 0개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | 참고 | 자료 화면 소스 종류 (한 곳에서만 가져오면 화면이 단조로워짐) | ℹ️ | 0종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ✅ | 링크 15개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |
| G4 | SHOULD | 목적 분간: intent.md 에 '목적:' 정보 습득형/즐길거리형 + 세 질문 (11 §2-4) | ✅ |  |
| G4 | MUST | core_message·question·logic | ❌ |  |
| G4 | MUST | 근거 검수표: 모든 주장에 근거·비약·괴리·착각 확인 (02_script/script_review.md '근거 검수', 13 §4-1, 2026-11-22 사용자) | ✅ |  |
| G4 | SHOULD | 대본 구성요소 대조표: 채널 대본 공식의 요소마다 있음/없음·어느 장 (02_script/script_review.md '구성요소', 13 §7) | ✅ |  |
| G4 | MUST | 쉬운 대본: 숫자엔 비교 기준, 낯선 개념엔 비유, 과거 사례, 어려운 말 풀이가 있다 | ❌ | {'compare_to': 0, 'analogies': 0, 'past_cases': 0, 'glossary': 0} |
| G4 | MUST | 투자 권유 표현 0개 | ✅ | [] |
| G4 | MUST | 레퍼런스 채널 이름 0개 | ✅ | [] |
| G4 | MUST | 미완성 표시 0개 | ✅ | [] |
| G4 | SHOULD | 과장 단어 0개 | ✅ | [] |
| G4 | SHOULD | 진행 말투: '~였고요.' 같은 이어 붙인 끝맺음 없음 (README §2-2, 2026-11-20 사용자: 필수 아님) | ✅ | [] |
| G4 | SHOULD | 여는 부분에 이 영상의 질문 하나 (시청자가 무엇을 따라가는지 알게) | ⚠️ |  |
| G4 | SHOULD | market: 끝에 확인할 신호(checklist) | ⚠️ | [] |
| G4 | MUST | 인트로 없음: 첫 장면이 intro 가 아니고 인사·채널 소개·순서 예고·구독 부탁 없음 (README §2-1) | ✅ | [] |
| G4 | SHOULD | 말투: 말 걸기·감탄 표현 없음 (README §2-3, 참고용) | ✅ | [] |

**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.
사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
