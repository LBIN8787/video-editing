# 체크리스트 — 20261109-style-combo

매뉴얼 v3 · 2026-11-09T07:39:58 · **MUST 실패 7개**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ❌ | [2026-11-09 · 20261109-style-combo 기각] 같은 이유: 강조(키네틱 단어 띠 등) 남용, 자막과 같은 내용 반복; [ |
| G1 | MUST | topic_brief.json 있음 | ❌ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ❌ |  |
| G1 | MUST | 트리거·왜 지금 | ❌ |  |
| G1 | MUST | 욕망 점수 ≥12, 욕망 강도·보여 줄 자료 ≥2 | ❌ | 합계 0 {} |
| G1 | MUST | 수요 증거 1개 이상 | ❌ | 0 |
| G1 | SHOULD | 후보 3개 비교 기록 | ⚠️ | 0 |
| G1 | SHOULD | 우리만의 답(our_angle) | ⚠️ |  |
| G2 | MUST | 자료 화면마다 credit·url | ✅ | 8개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | SHOULD | 자료 화면 소스 3종 이상 (롱폼) | ✅ | 6종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ❌ | 링크 0개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ⚠️ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ⚠️ |  |
| G4 | MUST | core_message·question·logic | ✅ |  |
| G4 | MUST | 비교 기준≥1·비유≥2·과거 사례≥1·풀이≥1 | ✅ | {'compare_to': 4, 'analogies': 2, 'past_cases': 2, 'glossary': 4} |
| G4 | MUST | 투자 권유 표현 0개 | ✅ | [] |
| G4 | MUST | 레퍼런스 채널 이름 0개 | ✅ | [] |
| G4 | MUST | 미완성 표시 0개 | ✅ | [] |
| G4 | SHOULD | 과장 단어 0개 | ✅ | [] |
| G4 | SHOULD | 첫 3장면 안에 질문 | ✅ |  |
| G5 | MUST | 같은 type 3연속 없음 | ✅ | [] |
| G5 | SHOULD | 자료 화면 공백 ≤45초 | ✅ | 최장 39초 |
| G5 | SHOULD | 장 표지 간격 ≤200초 | ✅ | 최장 116초 |
| G5 | MUST | 스타일 조합: 4종 이상 섞기 (한 스타일로만 만들면 불합격) | ✅ | 6종 ['archive-doc', 'data-report', 'hybrid-causal', 'kinetic-type', 'map-journey' |
| G5 | MUST | 한 스타일이 40% 넘지 않음 | ✅ | archive-doc 0.26 |
| G5 | MUST | 한 장면 안에서 겹친 장면(layers) 3개 이상 | ✅ | 6 |
| G5 | MUST | 같은 스타일 3장면 연속 없음 | ✅ | 최장 2 |
| G5 | MUST | 강조는 아껴서: 1분에 1번 이하 (이 영상 3번까지) | ✅ | 3번 [(2, 'kinetic'), (7, 'vox'), (14, 'kinetic')] |
| G5 | MUST | 한 장면에 강조 1개까지 (위아래로 같은 내용 반복 금지) | ✅ | 넘친 장면 [] |
| G5 | MUST | 핵심 단어 띄우기(words)는 단어 1~3개만 | ✅ | [] |
| G5 | SHOULD | 그래픽 팩이 브랜드에 맞는 스타일 등록부 안 (styles/recipes) | ✅ | paper-sketch / 등록부 ['clean-flat', 'dark-doc', 'kinetic-poster', 'newsprint', 'pa |
| G5 | SHOULD | style-pick 기록 (상황에 맞춘 스타일 선택) | ⚠️ | python -m ytflow style-pick <프로젝트> |

사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
