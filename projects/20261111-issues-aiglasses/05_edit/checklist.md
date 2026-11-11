# 체크리스트 — 20261111-issues-aiglasses

매뉴얼 v15 · 2026-11-11T12:41:20 · **MUST 실패 2개**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ❌ | [2026-11-11 · 20261112-bg-trials 기각] 진행 말투: 장 표지 '여기까지가 ~였고요.' 같은 끝맺음이 부자연스러워 흐름 |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | issues |
| G1 | MUST | 욕망·시청자 질문 | ✅ | AI 안경 컨닝, 수능에서 정말 막을 수 있을까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 2026-10-29 교육부 '수능 스마트안경 부정행위 대응 계획' + 11월 수능(19일)을 앞둔 현장 불안 보도 |
| G1 | MUST | 욕망 점수 ≥12, 욕망 강도·보여 줄 자료 ≥2 | ✅ | 합계 15 {'desire': 3, 'clarity': 3, 'timeliness': 3, 'demand': 2, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 1 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | '막는다'는 발표와 '구별이 어렵다'는 현장을 같은 무게로 놓고, 수험생이 실제로 알아야 할 것만 정리 |
| G1 | MUST | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 각도 · docs/18: 교육·입시는 소재만으로 약한 편 → 생활 체감 각도(내  |
| G2 | MUST | 자료 화면마다 credit·url | ✅ | 2개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | SHOULD | 자료 화면 소스 3종 이상 (롱폼) | ⚠️ | 2종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ✅ | 링크 5개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |
| G4 | MUST | core_message·question·logic | ✅ |  |
| G4 | MUST | 비교 기준≥1·비유≥2·과거 사례≥1·풀이≥1 | ✅ | {'compare_to': 2, 'analogies': 2, 'past_cases': 1, 'glossary': 3} |
| G4 | MUST | 투자 권유 표현 0개 | ✅ | [] |
| G4 | MUST | 레퍼런스 채널 이름 0개 | ✅ | [] |
| G4 | MUST | 미완성 표시 0개 | ✅ | [] |
| G4 | SHOULD | 과장 단어 0개 | ✅ | [] |
| G4 | MUST | 진행 말투: '~였고요.' 같은 이어 붙인 끝맺음 없음 (README §2-2) | ❌ | ['까지가 무슨 일이 있었는지였고요.'] |
| G4 | SHOULD | 첫 3장면 안에 질문 | ✅ |  |
| G4 | MUST | issues: 사실 기준 시각(as_of) | ✅ | 2026-11-11 09:00 KST |
| G4 | MUST | issues: 서로 다른 입장 2개 이상(각 출처) | ✅ | 2 |
| G4 | MUST | issues: 대본에 '기준' 시점 언급 | ✅ |  |
| G4 | MUST | issues: 단정·비하 금지어 없음 | ✅ | [] |
| G3 | MUST | issues: 출처 링크 5개 이상·도메인 3곳 이상 | ✅ | 5개 / 4곳 |
| G4 | SHOULD | issues: 모르는 것(unknowns) 말하기 | ✅ |  |
| G4 | SHOULD | issues: 사람의 목소리 장면 1개 이상 (quote·이름 자막) | ✅ | 2 |
| G4 | SHOULD | issues: 말하듯 쓴 대본 — 묻는 문장 3개+, 보도문 말투 10% 이하 (08 §0-1) | ✅ | 물음 6 · 보도문 0/32 |
| G1 | SHOULD | issues: 이름 붙은 시리즈(series) | ✅ | 이슈의 구조 |
| G5 | SHOULD | issues: 양쪽 입장 장면 길이 차 30% 이내 | ✅ | [14.3, 13.5] |
| G4 | MUST | 오프닝: 본론 전에 MC 오프닝(intro: 인사·오늘 이야기·순서 예고·시작 멘트, 3박자 이상) | ✅ |  |
| G5 | MUST | 배경: 장면 목적에 맞춰 3종 이상 (한 가지 바탕만 쓰면 불합격, manual 05 §0-2) | ✅ | ['film', 'grid', 'photo', 'spot', 'tint'] |
| G5 | SHOULD | 배경: 같은 바탕 3장면 연속 없음 (film 제외) | ✅ | [] |
| G5 | MUST | 반복 피로: 글씨·도형뿐인 장면 3개 연속 금지 (눈요기: 자료·지도·사진 겹치기·시각 효과, 05 §0-3) | ✅ | 최장 1연속 (장면 4) |
| G5 | SHOULD | v10: 장식 효과(dust·leak)는 2장면 이하 — 내용이 담긴 볼거리(사진·지도·사물 그림·정리판) 먼저 | ✅ | [12, 13] |
| G5 | SHOULD | 반복 피로: 눈요기 있는 장면 60% 이상 | ✅ | 10/12 |
| G5 | SHOULD | 반복 피로: 같은 시각 효과 3장면 연속 없음 · 효과 3종 이상(롱폼) | ✅ | ['fx:dust', 'fx:photofill', 'fx:scan', 'fx:tilt'] 연속 [] |
| G5 | SHOULD | 바탕색 돌려 쓰기: 직전 두 편과 같은 바탕 계열(특히 미색 종이)이 아님 (05 §0-6) | ✅ | 이번 dark:dark-doc · 직전 ['dark:midnight', 'light:clean-white'] |
| G5 | SHOULD | v15: 카테고리 개성 — hybrid.json 에 brand (장 표지·인과 지도·듀오톤이 카테고리답게) | ⚠️ |  |
| G5 | SHOULD | v15: 장 표지 사진은 주제에 맞게 — 같은 사진 두 번·NASA 사진 2장 이상 없음 | ⚠️ | 표지 ['seoul', 'seoul2', 'seoul', 'seoul2'] · NASA 4 |
| G5 | SHOULD | 반복 피로: 같은 채널 직전 편과 화면 구성 겹침 70% 이하 (Jaccard) | ✅ | 43% |
| G5 | MUST | 같은 type 3연속 없음 | ✅ | [] |
| G5 | SHOULD | 자료 화면 공백 ≤45초 | ⚠️ | 최장 224초 |
| G5 | SHOULD | 장 표지 간격 ≤200초 | ✅ | 최장 63초 |
| G5 | MUST | 스타일 조합: 4종 이상 섞기 (한 스타일로만 만들면 불합격) | ✅ | 9종 ['?isotype', '?recap', 'archive-doc', 'data-report', 'hybrid-causal', 'kineti |
| G5 | MUST | 한 스타일이 40% 넘지 않음 | ✅ | paper-column 0.36 |
| G5 | MUST | 한 장면 안에서 겹친 장면(layers) 3개 이상 | ✅ | 3 |
| G5 | MUST | 같은 스타일 3장면 연속 없음 | ✅ | 최장 2 |
| G5 | MUST | 강조는 아껴서: 1분에 1번 이하 (이 영상 4번까지) | ✅ | 1번 [(17, 'kinetic')] |
| G5 | MUST | 한 장면에 강조 1개까지 (위아래로 같은 내용 반복 금지) | ✅ | 넘친 장면 [] |
| G5 | MUST | 핵심 단어 띄우기(words)는 단어 1~3개만 | ✅ | [] |
| G5 | SHOULD | 그래픽 팩이 브랜드에 맞는 스타일 등록부 안 (styles/recipes) | ✅ | dark-doc / 등록부 ['clean-flat', 'dark-doc', 'kinetic-poster', 'newsprint', 'paper- |
| G5 | SHOULD | style-pick 기록 (상황에 맞춘 스타일 선택) | ✅ | python -m ytflow style-pick <프로젝트> |
| G6 | MUST | final.mp4 | ✅ |  |
| G6 | MUST | 레이아웃 점검 비어 있음 | ✅ | {} |
| G6 | MUST | 싱크 (0.5초 안 ≥95%, 화면−소리 ≤0.1초, 중앙값 ≤0.2초) | ✅ | {'within_0_5s': 1.0, 'p95_abs_offset': 0.07, 'median_abs_offset': 0.05, 'video_m |
| G6 | SHOULD | 납품 점검(음량 등) | ✅ | completed |
| G6 | SHOULD | 움직임: 화면 변화 ≥8회/분 · 정지 화면 비율 ≤0.5 (완성본 측정, v12 — 차분함이 우선) | ⚠️ | 변화 6.2/분 · 정지 0.65 |
| G6 | SHOULD | 최종 목소리 ElevenLabs | ✅ |  |
| G7 | MUST | 제목 후보 3개 + 이유 | ✅ |  |
| G7 | MUST | 썸네일 A/B/C + 점검 ok | ✅ |  |
| G7 | SHOULD | 제목 앞 22자 안에 질문/핵심 | ⚠️ | AI 안경 컨닝, 수능에서 정말 막을 수 |
| G8 | MUST | GitHub Release 업로드 | ✅ |  |
| G8 | MUST | episodes.md 기록 | ✅ | ch-issues |

사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
