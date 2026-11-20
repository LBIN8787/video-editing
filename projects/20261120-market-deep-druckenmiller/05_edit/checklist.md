# 체크리스트 — 20261120-market-deep-druckenmiller

매뉴얼 v77 · 2026-11-20T16:31:21 · **통과**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ✅ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | market |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 전설적인 투자자가 '지금은 안 한다'고 했다. 왜, 그리고 실제로는 무엇을 했을까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 대담 영상 41만 회 + 13F 보도 '구글 0, 금광주' |
| G1 | MUST | 욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3) | ✅ | 강도 3 · 자료 2 |
| G1 | 참고 | 욕망 점수 합계 (후보끼리 비교할 때 씀) | ✅ | 합계 16 {'desire': 3, 'clarity': 3, 'timeliness': 3, 'demand': 2, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 2 |
| G1 | SHOULD | 후보 3개 비교 기록 | ⚠️ | 1 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 영어 원문 발언 + 13F 숫자를 하나씩 + 번역본은 요지로만 표시 |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ⚠️ | 인물 · 투자 대가의 공개 발언 + 공시 |
| G2 | MUST | 시장: SAVE(오선) 시장 소식 알림 확인 기록 — 상태 '확인함' 또는 '확인 못 함: 이유' (01_research/save_check.md) | ✅ | 확인함 (inbox/save/20261117.md · 20261120.md · 20261121.md 에서 '드러켄밀러' 검색) |
| G2 | SHOULD | 시장: SAVE 실제로 확인함 (항목 1개 이상) | ✅ | 확인함 (inbox/save/20261117.md · 20261120.md · 20261121.md 에서 '드러켄밀러' 검색) · 항목 1 |
| G2 | MUST | 자료 화면마다 credit·url | ✅ | 1개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | 참고 | 자료 화면 소스 종류 (한 곳에서만 가져오면 화면이 단조로워짐) | ℹ️ | 1종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ✅ | 링크 13개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |

**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.
사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
