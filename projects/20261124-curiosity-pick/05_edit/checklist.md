# 체크리스트 — 20261124-curiosity-pick

매뉴얼 v124 · 2026-11-24T07:16:54 · **통과**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ✅ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 왜 우리는 동그란 눈·큰 머리 캐릭터를 보면 새벽부터 줄을 설까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 캐릭터 굿즈 새벽 오픈런·리셀 기사(11월 셋째 주) + 연말 굿즈 철 |
| G1 | MUST | 욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3) | ✅ | 강도 3 · 자료 2 |
| G1 | 참고 | 욕망 점수 합계 (후보끼리 비교할 때 씀) | ✅ | 합계 17 {'desire': 3, 'clarity': 3, 'timeliness': 3, 'demand': 3, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 2 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 10 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | '아기 얼굴이라 귀엽다'에서 멈추지 않고, 만화가들이 50년 동안 모르는 사이 캐릭터를 아기 쪽으로 바꿔 왔다는 측정 이야기로 '귀여움은 우리가 |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 각도 · 이번 주 오픈런 화제를 '왜 귀여운가' 설명이 아니라 측정된 변화의 이야 |

**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.
사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
