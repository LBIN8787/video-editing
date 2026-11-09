# 체크리스트 — 20261109-ai-unslop

매뉴얼 v4 · 2026-11-09T08:00:23 · **MUST 실패 1개**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | ai |
| G1 | MUST | 욕망·시청자 질문 | ✅ | AI가 만든 티, 어떻게 지워? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 2026-10-29 공개된 Claude 스킬 heydamir/unslop 이 11일 만에 GitHub 별 12,004개 (2026-11-09,  |
| G1 | MUST | 욕망 점수 ≥12, 욕망 강도·보여 줄 자료 ≥2 | ✅ | 합계 16 {'desire': 3, 'clarity': 2, 'timeliness': 3, 'demand': 3, 'visuals': 3, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 4 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 소개에서 끝내지 않고 ① 예제 화면에 직접 적용한 전/후와 실제 측정(이모지 30개→0, 줄 높이 30~46px→32px) ② 스킬이 일하는 원 |
| G2 | MUST | 자료 화면마다 credit·url | ✅ | 6개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | SHOULD | 자료 화면 소스 3종 이상 (롱폼) | ⚠️ | 2종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ✅ | 링크 5개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |
| G4 | MUST | core_message·question·logic | ✅ |  |
| G4 | MUST | 비교 기준≥1·비유≥2·과거 사례≥1·풀이≥1 | ✅ | {'compare_to': 3, 'analogies': 2, 'past_cases': 1, 'glossary': 4} |
| G4 | MUST | 투자 권유 표현 0개 | ✅ | [] |
| G4 | MUST | 레퍼런스 채널 이름 0개 | ✅ | [] |
| G4 | MUST | 미완성 표시 0개 | ✅ | [] |
| G4 | SHOULD | 과장 단어 0개 | ✅ | [] |
| G4 | SHOULD | 첫 3장면 안에 질문 | ✅ |  |
| G5 | MUST | 같은 type 3연속 없음 | ✅ | [] |
| G5 | SHOULD | 자료 화면 공백 ≤45초 | ⚠️ | 최장 152초 |
| G5 | SHOULD | 장 표지 간격 ≤200초 | ✅ | 최장 68초 |
| G5 | MUST | 스타일 조합: 4종 이상 섞기 (한 스타일로만 만들면 불합격) | ✅ | 8종 ['archive-doc', 'blueprint-explainer', 'data-report', 'hybrid-causal', 'kinet |
| G5 | MUST | 한 스타일이 40% 넘지 않음 | ✅ | screen-demo 0.27 |
| G5 | MUST | 한 장면 안에서 겹친 장면(layers) 3개 이상 | ✅ | 3 |
| G5 | MUST | 같은 스타일 3장면 연속 없음 | ✅ | 최장 2 |
| G5 | MUST | 강조는 아껴서: 1분에 1번 이하 (이 영상 6번까지) | ✅ | 5번 [(3, 'kinetic'), (6, 'number'), (18, 'vox'), (23, 'vox'), (26, 'kinetic')] |
| G5 | MUST | 한 장면에 강조 1개까지 (위아래로 같은 내용 반복 금지) | ✅ | 넘친 장면 [] |
| G5 | MUST | 핵심 단어 띄우기(words)는 단어 1~3개만 | ✅ | [] |
| G5 | SHOULD | 그래픽 팩이 브랜드에 맞는 스타일 등록부 안 (styles/recipes) | ✅ | clean-flat / 등록부 ['blueprint', 'clean-flat', 'dark-doc', 'kinetic-poster', 'pape |
| G5 | SHOULD | style-pick 기록 (상황에 맞춘 스타일 선택) | ✅ | python -m ytflow style-pick <프로젝트> |
| G6 | MUST | final.mp4 | ✅ |  |
| G6 | MUST | 레이아웃 점검 비어 있음 | ❌ | {'21': ['contrast/contrast_aa_failure: Contrast is 1.27:1; WCAG AA requires 3:1. |
| G6 | MUST | 싱크 (0.5초 안 ≥95%, 화면−소리 ≤0.1초, 중앙값 ≤0.2초) | ✅ | {'within_0_5s': 0.976, 'p95_abs_offset': 0.42, 'median_abs_offset': 0.04, 'video |
| G6 | SHOULD | 납품 점검(음량 등) | ✅ | completed |
| G6 | SHOULD | 최종 목소리 ElevenLabs | ⚠️ |  |
| G7 | MUST | 제목 후보 3개 + 이유 | ✅ |  |
| G7 | MUST | 썸네일 A/B/C + 점검 ok | ✅ |  |
| G7 | SHOULD | 제목 앞 22자 안에 질문/핵심 | ⚠️ | AI가 만든 티 나는 화면, 스킬 하나로 |
| G8 | MUST | GitHub Release 업로드 | ✅ |  |
| G8 | MUST | episodes.md 기록 | ✅ | ch-ai-guide |

사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
