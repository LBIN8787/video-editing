# 체크리스트 — 20261127-curiosity-pick

매뉴얼 v145 · 2026-11-27T07:17:37 · **통과**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ⚠️ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 비밀번호는 언제, 왜 생겼고 — 왜 지금도 우리는 그걸 수첩에 적고 있을까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 일본 '비밀번호 수첩' 품절 대란(11-24·25 보도) |
| G1 | MUST | 욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3) | ✅ | 강도 3 · 자료 3 |
| G1 | 참고 | 욕망 점수 합계 (후보끼리 비교할 때 씀) | ✅ | 합계 17 {'desire': 3, 'clarity': 3, 'timeliness': 3, 'demand': 2, 'visuals': 3, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 2 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 10 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | '비밀번호는 보안을 위해 생겼다'에서 멈추지 않고, 첫 비밀번호가 컴퓨터 시간을 나누려고 생겼고 곧바로 털렸다는 실화로 '비밀번호는 처음부터 사 |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 각도 · 이번 주 '손으로 적는 비밀번호' 화제를 보안 팁이 아니라 1960년대의 |

**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.
사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
