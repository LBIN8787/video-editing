# 체크리스트 — 20261110-v10-after

매뉴얼 v10 · 2026-11-10T11:49:59 · **통과**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | issues |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 유가가 올랐는데 왜 사우디는 마이너스 성장? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 2026-11-01 사우디 통계청 속보: 3분기 GDP -3.8% (유가는 10월 말 배럴당 117달러까지 올랐는데) |
| G1 | MUST | 욕망 점수 ≥12, 욕망 강도·보여 줄 자료 ≥2 | ✅ | 합계 16 {'desire': 3, 'clarity': 3, 'timeliness': 3, 'demand': 3, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 2 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 유가 상승 = 산유국 호황이라는 통념의 반대 결과를, 사우디 수출 지도 하나(호르무즈 → 동서 송유관 → 얀부 → 홍해)로 설명 |
| G1 | MUST | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 소재 · docs/18 §6: 사우디·중동 1.78 · 경제 위기·몰락 2.06  |
| G2 | MUST | 자료 화면마다 credit·url | ✅ | 4개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | SHOULD | 자료 화면 소스 3종 이상 (롱폼) | ✅ | 4종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ✅ | 링크 15개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |
| G4 | MUST | core_message·question·logic | ✅ |  |
| G4 | MUST | 비교 기준≥1·비유≥2·과거 사례≥1·풀이≥1 | ✅ | {'compare_to': 3, 'analogies': 2, 'past_cases': 1, 'glossary': 5} |
| G4 | MUST | 투자 권유 표현 0개 | ✅ | [] |
| G4 | MUST | 레퍼런스 채널 이름 0개 | ✅ | [] |
| G4 | MUST | 미완성 표시 0개 | ✅ | [] |
| G4 | SHOULD | 과장 단어 0개 | ✅ | [] |
| G4 | SHOULD | 첫 3장면 안에 질문 | ✅ |  |
| G4 | MUST | issues: 사실 기준 시각(as_of) | ✅ | 2026-11-09 18:00 KST |
| G4 | MUST | issues: 서로 다른 입장 2개 이상(각 출처) | ✅ | 2 |
| G4 | MUST | issues: 대본에 '기준' 시점 언급 | ✅ |  |
| G4 | MUST | issues: 단정·비하 금지어 없음 | ✅ | [] |
| G3 | MUST | issues: 출처 링크 5개 이상·도메인 3곳 이상 | ✅ | 15개 / 14곳 |
| G4 | SHOULD | issues: 모르는 것(unknowns) 말하기 | ⚠️ |  |
| G4 | SHOULD | issues: 사람의 목소리 장면 1개 이상 (quote·이름 자막) | ⚠️ | 0 |
| G4 | SHOULD | issues: 말하듯 쓴 대본 — 묻는 문장 3개+, 보도문 말투 10% 이하 (08 §0-1) | ⚠️ | 물음 2 · 보도문 0/22 |
| G1 | SHOULD | issues: 이름 붙은 시리즈(series) | ✅ | 이슈의 구조 |
| G4 | MUST | 오프닝: 본론 전에 MC 오프닝(intro: 인사·오늘 이야기·순서 예고·시작 멘트, 3박자 이상) | ✅ |  |
| G5 | MUST | 배경: 장면 목적에 맞춰 3종 이상 (한 가지 바탕만 쓰면 불합격, manual 05 §0-2) | ✅ | ['film', 'photo', 'tint'] |
| G5 | SHOULD | 배경: 같은 바탕 3장면 연속 없음 (film 제외) | ✅ | [] |
| G5 | MUST | 반복 피로: 글씨·도형뿐인 장면 3개 연속 금지 (눈요기: 자료·지도·사진 겹치기·시각 효과, 05 §0-3) | ✅ | 최장 1연속 (장면 5) |
| G5 | SHOULD | v10: 장식 효과(dust·leak)는 2장면 이하 — 내용이 담긴 볼거리(사진·지도·사물 그림·정리판) 먼저 | ✅ | [] |
| G5 | SHOULD | 반복 피로: 눈요기 있는 장면 60% 이상 | ✅ | 6/9 |
| G5 | SHOULD | 반복 피로: 같은 시각 효과 3장면 연속 없음 · 효과 3종 이상(롱폼) | ⚠️ | [] 연속 [] |
| G5 | SHOULD | 반복 피로: 같은 채널 직전 편과 화면 구성 겹침 70% 이하 (Jaccard) | ✅ | 38% |
| G5 | MUST | 같은 type 3연속 없음 | ✅ | [] |
| G5 | SHOULD | 자료 화면 공백 ≤45초 | ✅ | 최장 38초 |
| G5 | SHOULD | 장 표지 간격 ≤200초 | ✅ | 최장 56초 |
| G5 | MUST | 스타일 조합: 4종 이상 섞기 (한 스타일로만 만들면 불합격) | ✅ | 7종 ['?isotype', '?recap', 'archive-doc', 'hybrid-causal', 'kinetic-type', 'map-j |
| G5 | MUST | 한 스타일이 40% 넘지 않음 | ✅ | hybrid-causal 0.26 |
| G5 | MUST | 한 장면 안에서 겹친 장면(layers) 3개 이상 | ✅ | 3 |
| G5 | MUST | 같은 스타일 3장면 연속 없음 | ✅ | 최장 1 |
| G5 | MUST | 강조는 아껴서: 1분에 1번 이하 (이 영상 2번까지) | ✅ | 1번 [(12, 'kinetic')] |
| G5 | MUST | 한 장면에 강조 1개까지 (위아래로 같은 내용 반복 금지) | ✅ | 넘친 장면 [] |
| G5 | MUST | 핵심 단어 띄우기(words)는 단어 1~3개만 | ✅ | [] |
| G5 | SHOULD | 그래픽 팩이 브랜드에 맞는 스타일 등록부 안 (styles/recipes) | ✅ | dark-doc / 등록부 ['clean-flat', 'dark-doc', 'kinetic-poster', 'newsprint', 'paper- |
| G5 | SHOULD | style-pick 기록 (상황에 맞춘 스타일 선택) | ⚠️ | python -m ytflow style-pick <프로젝트> |
| G6 | MUST | final.mp4 | ✅ |  |
| G6 | MUST | 레이아웃 점검 비어 있음 | ✅ | {} |
| G6 | MUST | 싱크 (0.5초 안 ≥95%, 화면−소리 ≤0.1초, 중앙값 ≤0.2초) | ✅ | {'within_0_5s': 0.956, 'p95_abs_offset': 0.42, 'median_abs_offset': 0.05, 'video |
| G6 | SHOULD | 납품 점검(음량 등) | ✅ | completed |
| G6 | MUST | 움직임(v10): 화면 변화 ≥10회/분 · 정지 화면 비율 ≤0.45 (완성본 측정) | ✅ | 변화 13.7/분 · 정지 0.18 |
| G6 | SHOULD | 최종 목소리 ElevenLabs | ⚠️ |  |

사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
