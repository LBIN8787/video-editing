# 체크리스트 — 20261122-curiosity-pick2

매뉴얼 v113 · 2026-11-22T23:04:12 · **통과**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ✅ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 올림픽 마라톤에서 어떻게 차를 타고 온 선수가 1등으로 들어오고, 진짜 우승자는 쥐약 성분을 먹고 달렸을까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 2026-11-22 정기 작업: 호기심 채널 일 1편. 판테온 편이 비공개로 끝남(사용자: "주제가 애매하고 솔직히 사람들이 좋아할까? 하면 잘 |
| G1 | MUST | 욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3) | ✅ | 강도 3 · 자료 2 |
| G1 | 참고 | 욕망 점수 합계 (후보끼리 비교할 때 씀) | ✅ | 합계 16 {'desire': 3, 'clarity': 3, 'timeliness': 2, 'demand': 3, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 2 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 5 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 기묘한 일화 모음으로 끝내지 않고, '왜 물을 주지 않았나'라는 한 질문으로 묶어 오늘의 급수대·규정으로 돌아온다. (D1 뒤 S2 에서 확정) |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 소재 · 제목 한 줄('1등이 차를 타고 왔다')로 끌리고, 사람들의 사연과 반전 |

**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.
사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
