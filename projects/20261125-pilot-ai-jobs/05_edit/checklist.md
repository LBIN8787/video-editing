# 체크리스트 — 20261125-pilot-ai-jobs

매뉴얼 v135 · 2026-11-25T23:35:30 · **MUST 실패 1개**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ❌ | [2026-11-25 · 20261125-curiosity-riemann 기각] 불합격 입니다. 전부 이미지느낌보다는 글씨느낌에 애니메이션효과  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ✅ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | ai |
| G1 | MUST | 욕망·시청자 질문 | ✅ | AI 가 정말 신입의 첫 출근을 빼앗고 있을까, 그렇다면 어떤 일의 신입일까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 한국은행 이슈노트 '청년고용 위축, AI 탓인가?'·스탠퍼드 '탄광의 카나리아' 8월 개정(22~25세 격차 19%)·20대 임금근로 일자리 1 |
| G1 | MUST | 욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3) | ✅ | 강도 3 · 자료 2 |
| G1 | 참고 | 욕망 점수 합계 (후보끼리 비교할 때 씀) | ✅ | 합계 17 {'desire': 3, 'clarity': 3, 'timeliness': 3, 'demand': 3, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 2 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 출처 없는 'AI 가 못 바꾸는 직업 TOP7' 대신, 기관 원문 숫자마다 비교 기준을 달고 회사·기관 주장과 반대 해석(채용 경기·금리 탓)을 |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 각도 · 수요는 이미 큼(방송사·작은 채널 모두 터짐). 우리 몫은 같은 소재를  |

**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.
사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
