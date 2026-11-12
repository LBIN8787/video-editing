# 체크리스트 — 20261112-market-call

매뉴얼 v18 · 2026-11-12T13:49:37 · **통과**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | market |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 실적이 좋아서만이 아니라면, 이번 어닝콜은 무엇이 달랐을까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 코어위브 3분기 어닝콜(11/10) 다음 날 코어위브 +24.7%, 반도체 지수 +5.7% — '어닝콜을 잘했다'는 평가 |
| G1 | MUST | 욕망 점수 ≥12, 욕망 강도·보여 줄 자료 ≥2 | ✅ | 합계 16 {'desire': 3, 'clarity': 3, 'timeliness': 3, 'demand': 2, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 1 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 있던 말을 옮기는 데서 끝내지 않고 '무엇으로 이어지나 · 무슨 뜻인가'까지 — 사실과 해석을 나눠서 |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 각도 · 어닝콜 해설은 숫자 요약이 대부분 → 걱정-답-의미 구조로 차별화 |
| G2 | MUST | 자료 화면마다 credit·url | ✅ | 2개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | SHOULD | 자료 화면 소스 3종 이상 (롱폼) | ⚠️ | 2종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ✅ | 링크 4개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |
| G4 | MUST | core_message·question·logic | ✅ |  |
| G4 | MUST | 비교 기준≥1·비유≥2·과거 사례≥1·풀이≥1 | ✅ | {'compare_to': 4, 'analogies': 2, 'past_cases': 1, 'glossary': 5} |
| G4 | MUST | 투자 권유 표현 0개 | ✅ | [] |
| G4 | MUST | 레퍼런스 채널 이름 0개 | ✅ | [] |
| G4 | MUST | 미완성 표시 0개 | ✅ | [] |
| G4 | SHOULD | 과장 단어 0개 | ✅ | [] |
| G4 | MUST | 진행 말투: '~였고요.' 같은 이어 붙인 끝맺음 없음 (README §2-2) | ✅ | [] |
| G4 | SHOULD | 첫 3장면 안에 질문 | ✅ |  |
| G3 | MUST | 연결·의미: 팩트시트에 '## 해석'(근거 번호와 함께) — 사실만 옮기지 않기 (03 §0-1) | ✅ |  |
| G4 | SHOULD | 연결·의미: 대본에서 해석을 해석이라고 밝힘 ('해석'·'의미'·'로 볼 수 있') | ✅ |  |
| G1 | MUST | 매일 브리핑: daily_brief.json 있음 (python -m ytflow daily) | ✅ | 01_research/daily_brief.json |
| G4 | MUST | 매일 브리핑: 오프닝에 기준 시각('○일 마감 기준' / '○시 기준') | ✅ |  |
| G3 | MUST | 매일 시장: 이야기마다 원인 종류(이슈·보고서·전망·실적)와 1차 출처를 팩트시트에 | ✅ | ['보고서', '실적'] |
| G4 | SHOULD | market: 끝에 확인할 신호(checklist) | ✅ | ['kinetic', 'checklist', 'outro'] |
| G4 | MUST | 오프닝: 본론 전에 MC 오프닝(intro: 인사·오늘 이야기·순서 예고·시작 멘트, 3박자 이상) | ✅ |  |
| G5 | MUST | 배경: 장면 목적에 맞춰 3종 이상 (한 가지 바탕만 쓰면 불합격, manual 05 §0-2) | ✅ | ['film', 'grid', 'photo', 'spot', 'tint'] |
| G5 | SHOULD | 배경: 같은 바탕 3장면 연속 없음 (film 제외) | ⚠️ | ['spot', 'spot', 'spot'] |
| G5 | MUST | 반복 피로: 글씨·도형뿐인 장면 3개 연속 금지 (눈요기: 자료·지도·사진 겹치기·시각 효과, 05 §0-3) | ✅ | 최장 1연속 (장면 19) |
| G5 | SHOULD | v10: 장식 효과(dust·leak)는 2장면 이하 — 내용이 담긴 볼거리(사진·지도·사물 그림·정리판) 먼저 | ✅ | [] |
| G5 | SHOULD | 반복 피로: 눈요기 있는 장면 60% 이상 | ✅ | 16/18 |
| G5 | SHOULD | 반복 피로: 같은 시각 효과 3장면 연속 없음 · 효과 3종 이상(롱폼) | ✅ | ['fx:dolly', 'fx:scan', 'fx:tilt'] 연속 [] |
| G5 | SHOULD | 바탕색 돌려 쓰기: 직전 두 편과 같은 바탕 계열(특히 미색 종이)이 아님 (05 §0-6) | ✅ | 이번 cream · 직전 ['light:slate', 'dark:dark-doc'] |
| G5 | SHOULD | v15: 카테고리 개성 — hybrid.json 에 brand (장 표지·인과 지도·듀오톤이 카테고리답게) | ✅ | market |
| G5 | SHOULD | v15: 장 표지 사진은 주제에 맞게 — 같은 사진 두 번·NASA 사진 2장 이상 없음 | ✅ | 표지 ['dc'] · NASA 0 |
| G5 | MUST | 같은 type 3연속 없음 | ✅ | [] |
| G5 | SHOULD | 자료 화면 공백 ≤45초 | ⚠️ | 최장 369초 |
| G5 | SHOULD | 장 표지 간격 ≤200초 | ✅ | 최장 120초 |
| G5 | MUST | 스타일 조합: 4종 이상 섞기 (한 스타일로만 만들면 불합격) | ✅ | 8종 ['?recap', 'archive-doc', 'data-report', 'hybrid-causal', 'kinetic-type', 'ma |
| G5 | MUST | 한 스타일이 40% 넘지 않음 | ✅ | paper-column 0.32 |
| G5 | MUST | 한 장면 안에서 겹친 장면(layers) 3개 이상 | ✅ | 4 |
| G5 | MUST | 같은 스타일 3장면 연속 없음 | ✅ | 최장 2 |
| G5 | MUST | 강조는 아껴서: 1분에 1번 이하 (이 영상 6번까지) | ✅ | 1번 [(22, 'kinetic')] |
| G5 | MUST | 한 장면에 강조 1개까지 (위아래로 같은 내용 반복 금지) | ✅ | 넘친 장면 [] |
| G5 | MUST | 핵심 단어 띄우기(words)는 단어 1~3개만 | ✅ | [] |
| G5 | SHOULD | 그래픽 팩이 브랜드에 맞는 스타일 등록부 안 (styles/recipes) | ✅ | paper-sketch / 등록부 ['blueprint', 'clean-flat', 'clean-white', 'corkboard', 'dark |
| G5 | SHOULD | style-pick 기록 (상황에 맞춘 스타일 선택) | ✅ | python -m ytflow style-pick <프로젝트> |

사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
