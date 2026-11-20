# 체크리스트 — 20261120-curiosity-nextlane

매뉴얼 v62 · 2026-11-20T08:05:17 · **MUST 실패 2개**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ✅ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 마트 계산대에서도 도로에서도, 왜 늘 내 옆 줄이 더 빨라 보일까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 2026-11-20 D1 주제 카드에서 사용자 선택(A). |
| G1 | MUST | 욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3) | ✅ | 강도 3 · 자료 3 |
| G1 | 참고 | 욕망 점수 합계 (후보끼리 비교할 때 씀) | ✅ | 합계 15 {'desire': 3, 'clarity': 3, 'timeliness': 1, 'demand': 2, 'visuals': 3, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 1 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 착각이라는 답(Nature 1999)과 '실제로 느린 줄에 서 있을 때가 많다'는 반론(Bostrom)을 둘 다 따라가, 둘이 서로 다른 것을  |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 각도 · 같은 장면(옆 줄을 보는 눈)을 두 연구가 다르게 설명한다. |
| G2 | MUST | 자료 화면마다 credit·url | ❌ | 0개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | 참고 | 자료 화면 소스 종류 (한 곳에서만 가져오면 화면이 단조로워짐) | ℹ️ | 0종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ✅ | 링크 7개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |
| G4 | SHOULD | 목적 분간: intent.md 에 '목적:' 정보 습득형/즐길거리형 + 세 질문 (11 §2-4) | ✅ |  |
| G4 | MUST | core_message·question·logic | ❌ |  |
| G4 | SHOULD | curiosity: 비유와 대비가 되는 숫자 — 사실은 이야기 속에서 (04 §0-6) | ⚠️ | {'compare_to': 0, 'analogies': 0, 'past_cases': 0, 'glossary': 0} |
| G4 | MUST | 투자 권유 표현 0개 | ✅ | [] |
| G4 | MUST | 레퍼런스 채널 이름 0개 | ✅ | [] |
| G4 | MUST | 미완성 표시 0개 | ✅ | [] |
| G4 | SHOULD | 과장 단어 0개 | ✅ | [] |
| G4 | MUST | 진행 말투: '~였고요.' 같은 이어 붙인 끝맺음 없음 (README §2-2) | ✅ | [] |
| G4 | SHOULD | 여는 부분에 이 영상의 질문 하나 (시청자가 무엇을 따라가는지 알게) | ⚠️ |  |
| G4 | MUST | 인트로 없음: 첫 장면이 intro 가 아니고 인사·채널 소개·순서 예고·구독 부탁 없음 (README §2-1) | ✅ | [] |
| G4 | SHOULD | 말투: 말 걸기·감탄 표현 없음 (README §2-3, 참고용) | ✅ | [] |
| G4 | 참고 | 말투(호기심): '~습니다/~니다' 끝맺음 몫·평균 문장 길이 (차분한 이야기 내레이터인지) | ℹ️ | 0% · 0자 |

**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.
사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
