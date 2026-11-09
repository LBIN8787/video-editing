# 체크리스트 — 20261107-knowledge-스페인독감

매뉴얼 v2 · 2026-11-09T00:51:04 · **MUST 실패 5개**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ❌ | [2026-11-09 · 20261107-style-archive 기각] 스타일 자체는 합격. 그러나 한 스타일로만 영상 전체를 만들면 불합격  |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 스페인 독감은 왜 '스페인'일까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 수요 분석(2026-11-07): 교양 분야에서 '누구나 아는 것 + 모르는 이유' 질문형 제목이 아웃라이어 상위. 1918년 대유행 기록이 미 |
| G1 | MUST | 욕망 점수 ≥12, 욕망 강도·보여 줄 자료 ≥2 | ✅ | 합계 14 {'desire': 3, 'clarity': 3, 'timeliness': 1, 'demand': 2, 'visuals': 3, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 1 |
| G1 | SHOULD | 후보 3개 비교 기록 | ⚠️ | 2 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 이름의 이유에서 끝나지 않고 '숨길수록 커진다'(필라델피아 vs 세인트루이스)와 한국(무오년 독감, 조선인 치사율)까지 연결 |
| G2 | MUST | 자료 화면마다 credit·url | ✅ | 13개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | SHOULD | 자료 화면 소스 3종 이상 (롱폼) | ✅ | 10종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ❌ | 링크 0개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |
| G4 | MUST | core_message·question·logic | ✅ |  |
| G4 | MUST | 비교 기준≥1·비유≥2·과거 사례≥1·풀이≥1 | ✅ | {'compare_to': 4, 'analogies': 2, 'past_cases': 2, 'glossary': 4} |
| G4 | MUST | 투자 권유 표현 0개 | ✅ | [] |
| G4 | MUST | 레퍼런스 채널 이름 0개 | ✅ | [] |
| G4 | MUST | 미완성 표시 0개 | ✅ | [] |
| G4 | SHOULD | 과장 단어 0개 | ✅ | [] |
| G4 | SHOULD | 첫 3장면 안에 질문 | ✅ |  |
| G5 | MUST | 같은 type 3연속 없음 | ✅ | [] |
| G5 | SHOULD | 자료 화면 공백 ≤45초 | ⚠️ | 최장 155초 |
| G5 | SHOULD | 장 표지 간격 ≤200초 | ✅ | 최장 92초 |
| G5 | MUST | 스타일 조합: 4종 이상 섞기 (한 스타일로만 만들면 불합격) | ✅ | 5종 ['data-report', 'hybrid-causal', 'map-journey', 'paper-column', 'statement-br |
| G5 | MUST | 한 스타일이 40% 넘지 않음 | ❌ | hybrid-causal 0.54 |
| G5 | MUST | 한 장면 안에서 겹친 장면(layers) 3개 이상 | ❌ | 0 |
| G5 | MUST | 같은 스타일 3장면 연속 없음 | ❌ | 최장 3 |
| G5 | SHOULD | 그래픽 팩이 브랜드에 맞는 스타일 등록부 안 (styles/recipes) | ✅ | paper-sketch / 등록부 ['clean-flat', 'dark-doc', 'kinetic-poster', 'newsprint', 'pa |
| G5 | SHOULD | style-pick 기록 (상황에 맞춘 스타일 선택) | ✅ | python -m ytflow style-pick <프로젝트> |

사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
