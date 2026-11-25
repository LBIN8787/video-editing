# 체크리스트 — 20261125-pilot-psych

매뉴얼 v135 · 2026-11-25T23:35:33 · **MUST 실패 1개**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ❌ | [2026-11-25 · 20261125-curiosity-riemann 기각] 불합격 입니다. 전부 이미지느낌보다는 글씨느낌에 애니메이션효과  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ✅ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 사람이 많을수록 아무도 돕지 않는다는 방관자 효과, 정말일까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 교과서·SNS 에 계속 돌아다니는 '38명의 목격자' 이야기 — 원 보도의 정정과 CCTV 연구가 한국어로는 거의 다뤄지지 않음 (방관자 효과  |
| G1 | MUST | 욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3) | ✅ | 강도 3 · 자료 3 |
| G1 | 참고 | 욕망 점수 합계 (후보끼리 비교할 때 씀) | ✅ | 합계 15 {'desire': 3, 'clarity': 3, 'timeliness': 1, 'demand': 2, 'visuals': 3, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 2 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 한 실험을 이야기로 따라가되, 원 보도 → 정정 → 재현 연구 순으로 '배운 것'을 시청자가 직접 다시 판단하게 한다. 시리즈 틀: '다시 돌려 |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 각도 · 누구나 아는 실험을 원 자료로 다시 돌려 보는 반전 각도가 시리즈로 반복 |

**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.
사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
