# 체크리스트 — 20261113-curiosity-moravec

매뉴얼 v20 · 2026-11-13T16:31:36 · **통과**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 체스 챔피언을 이긴 AI는 왜 빨래를 못 갤까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 집안일 로봇 영상(빨래 개기)이 계속 화제 — 2024년 10월 π0 공개 이후 '로봇은 언제 빨래를 개 주나' 질문 증가 |
| G1 | MUST | 욕망 점수 ≥12, 욕망 강도·보여 줄 자료 ≥2 | ✅ | 합계 15 {'desire': 3, 'clarity': 3, 'timeliness': 2, 'demand': 2, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 1 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 'AI는 어려운 걸 못 한다'는 통념 대신 '우리가 쉽다고 느끼는 게 기계에겐 어렵다' — 체스와 빨래 두 장면으로 |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 각도 · AI 소재 + 일상(빨래) 반전 |
| G2 | MUST | 자료 화면마다 credit·url | ✅ | 0개, 빠짐 [] · 직접 그린 그림판 |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | SHOULD | 자료 화면 소스 3종 이상 (롱폼) | ⚠️ | 0종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ✅ | 링크 9개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |
| G4 | MUST | core_message·question·logic | ✅ |  |
| G4 | MUST | 비교 기준≥1·비유≥2·과거 사례≥1·풀이≥1 | ✅ | {'compare_to': 3, 'analogies': 3, 'past_cases': 2, 'glossary': 3} |
| G4 | MUST | 투자 권유 표현 0개 | ✅ | [] |
| G4 | MUST | 레퍼런스 채널 이름 0개 | ✅ | [] |
| G4 | MUST | 미완성 표시 0개 | ✅ | [] |
| G4 | SHOULD | 과장 단어 0개 | ✅ | [] |
| G4 | MUST | 진행 말투: '~였고요.' 같은 이어 붙인 끝맺음 없음 (README §2-2) | ✅ | [] |
| G4 | SHOULD | 첫 3장면 안에 질문 | ✅ |  |
| G1 | MUST | curiosity: 훅 먼저 정하기 (topic_brief.hook: type·line·gap) | ✅ | 장면 |
| G4 | MUST | curiosity: 짧은 인사·소개 뒤 곧바로 훅 (첫 두 장면 안, 순서 예고보다 앞) (04 §0) | ✅ | 훅 박자 3 · 순서 예고 None |
| G4 | MUST | curiosity: 훅의 질문(gap)이 나옴 (답은 숨김) | ✅ | 체스 챔피언을 이긴 기계는 왜 티셔츠 한 장을 못 갰을까? |
| G6 | SHOULD | curiosity: 제목이 훅에서 나옴 (훅과 같은 낱말) | ✅ | 3/4 |
| G4 | MUST | 오프닝: 본론 전에 MC 오프닝(intro: 인사·오늘 이야기·순서 예고·시작 멘트, 3박자 이상) | ✅ |  |

사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
