# 체크리스트 — 20261122-curiosity-pick

매뉴얼 v91 · 2026-11-22T10:45:35 · **MUST 실패 2개**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ✅ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 몇십 년 된 주차장에도 금이 가는데, 철근도 없는 1,900년 된 돔은 어떻게 버텼을까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 2026-11-22 정기 작업: 호기심 채널 일 1편(매일 18:00) — 분야를 가리지 않는 이야기 채널로 바뀐 첫 주제 카드. 후보 3개는  |
| G1 | MUST | 욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3) | ✅ | 강도 3 · 자료 2 |
| G1 | 참고 | 욕망 점수 합계 (후보끼리 비교할 때 씀) | ✅ | 합계 15 {'desire': 3, 'clarity': 3, 'timeliness': 1, 'demand': 3, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 2 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | '옛날 것이 더 튼튼하다'가 아니다. 판테온 돔은 실제로 금이 가 있다. 금이 가도 무너지지 않게 무게를 덜었고(두께·가벼운 돌·빈 꼭대기),  |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 각도 · 누구나 아는 '로마 콘크리트는 튼튼하다'를 '사실 금이 가 있다'로 뒤집 |
| G2 | MUST | 자료 화면마다 credit·url | ❌ | 0개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | 참고 | 자료 화면 소스 종류 (한 곳에서만 가져오면 화면이 단조로워짐) | ℹ️ | 0종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ✅ | 링크 6개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |
| G4 | SHOULD | 목적 분간: intent.md 에 '목적:' 정보 습득형/즐길거리형 + 세 질문 (11 §2-4) | ✅ |  |
| G4 | MUST | core_message·question·logic | ✅ |  |
| G4 | SHOULD | 대본 구성요소 대조표: 채널 대본 공식의 요소마다 있음/없음·어느 장 (02_script/script_review.md '구성요소', 13 §7) | ✅ |  |
| G4 | SHOULD | curiosity: 비유와 대비가 되는 숫자 — 사실은 이야기 속에서 (04 §0-6) | ✅ | {'compare_to': 3, 'analogies': 2, 'past_cases': 2, 'glossary': 1} |
| G4 | MUST | 투자 권유 표현 0개 | ✅ | [] |
| G4 | MUST | 레퍼런스 채널 이름 0개 | ✅ | [] |
| G4 | MUST | 미완성 표시 0개 | ✅ | [] |
| G4 | SHOULD | 과장 단어 0개 | ✅ | [] |
| G4 | SHOULD | 진행 말투: '~였고요.' 같은 이어 붙인 끝맺음 없음 (README §2-2, 2026-11-20 사용자: 필수 아님) | ✅ | [] |
| G4 | SHOULD | 여는 부분에 이 영상의 질문 하나 (시청자가 무엇을 따라가는지 알게) | ✅ |  |
| G1 | MUST | curiosity: 훅 먼저 정하기 (topic_brief.hook: type·line·gap) | ✅ | 나와의 연결 |
| G4 | MUST | curiosity: 여는 장면이 곧 훅 — 소개·순서 예고·설명보다 앞 (04 §0) | ✅ | 훅 박자 0 · 순서 예고 None |
| G4 | MUST | curiosity: 훅의 질문(gap)이 나옴 (답은 숨김) | ✅ | 철근도 없는 이 돔은 어떻게 1,900년을 버텼을까요? |
| G1 | MUST | curiosity: 시청자 조사 01_research/audience.md (주 시청자·유입 경로·유입 이유·끝까지 보는 이유) | ✅ | docs/29 |
| G4 | MUST | curiosity: 편집 전에 대본만 사용자 검토 통과 (02_script/script_review.md '통과', 04 §0-6) | ❌ |  |
| G6 | SHOULD | curiosity: 제목이 훅에서 나옴 (훅과 같은 낱말) | ⚠️ | 0/0 |
| G4 | MUST | 인트로 없음: 첫 장면이 intro 가 아니고 인사·채널 소개·순서 예고·구독 부탁 없음 (README §2-1) | ✅ | [] |
| G4 | SHOULD | 말투: 말 걸기·감탄 표현 없음 (README §2-3, 참고용) | ✅ | [] |
| G4 | 참고 | 말투(호기심): '~습니다/~니다' 끝맺음 몫·평균 문장 길이 (차분한 이야기 내레이터인지) | ✅ | 85% · 36자 |

**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.
사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
