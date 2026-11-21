# 체크리스트 — 20261121-curiosity-willpower

매뉴얼 v81 · 2026-11-21T12:58:54 · **통과**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ✅ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 야식 앞에서 무너진 것은 정말 의지가 바닥났기 때문일까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 2026-11-21 사용자 요청: 위 피드백(반전 먼저·근거 한정·문제 제기 뒤 해법까지)을 반영해 새 주제로 대본·영상 제작. 주제는 에이전트 |
| G1 | MUST | 욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3) | ✅ | 강도 3 · 자료 2 |
| G1 | 참고 | 욕망 점수 합계 (후보끼리 비교할 때 씀) | ✅ | 합계 14 {'desire': 3, 'clarity': 3, 'timeliness': 1, 'demand': 2, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 1 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 원 실험(쿠키·무) → 대규모 재검증(2016·2021)에서 효과가 일관되게 나오지 않음 → 대안 설명과 일상 자료 → 참는 힘 대신 상황을 미 |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 각도 · 같은 질문을 '실험 → 재검증 → 일상 자료'로 세 번 다른 방법으로 확 |

**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.
사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
