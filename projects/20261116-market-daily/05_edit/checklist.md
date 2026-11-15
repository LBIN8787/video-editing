# 체크리스트 — 20261116-market-daily

매뉴얼 v34 · 2026-11-15T21:45:19 · **통과**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ✅ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | market |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 회사 안의 일이던 엔비디아 사태가, 왜 이번 주 미국 재무장관과 의회의 일이 됐을까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 금요일 반도체 -3.43% · 주말 재무장관 '10일 안에 답' · 의회 수출 규제 법안 · 18일 실적 · 앤트로픽 상장 |
| G1 | MUST | 욕망 점수 ≥12, 욕망 강도·보여 줄 자료 ≥2 | ✅ | 합계 17 {'desire': 3, 'clarity': 3, 'timeliness': 3, 'demand': 3, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 1 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 주말의 발언·법안을 엔비디아 10-Q 원문(지역 매출 기준·수출 규제 위험)과 맞대고, 이번 주 일정으로 잇기 |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 소재 · 주말 사이 새로 생긴 정책 압력 + 이번 주 실적·상장 |
| G2 | MUST | 시장: SAVE(오선) 소식 확인 기록 — 상태 '확인함' 또는 '확인 못 함: 이유' (01_research/save_check.md) | ✅ | 확인함 (사용자 메모: 20261116.md) |
| G2 | SHOULD | 시장: SAVE 실제로 확인함 (항목 1개 이상) | ✅ | 확인함 (사용자 메모: 20261116.md) · 항목 4 |
| G2 | MUST | 자료 화면마다 credit·url | ✅ | 4개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | SHOULD | 자료 화면 소스 3종 이상 (롱폼) | ✅ | 4종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ✅ | 링크 12개 |
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
| G4 | MUST | 매일 브리핑: 첫 두 장면 안에 기준 시각('○일 마감 기준' / '○시 기준') — 인트로 없이 (README §2-1) | ✅ |  |
| G3 | MUST | 매일 시장: 이야기마다 원인 종류(이슈·보고서·전망·실적)와 1차 출처를 팩트시트에 | ✅ | ['이슈', '전망', '실적'] |
| G1 | SHOULD | v26: topic_brief 에 known(이미 알려진 것)·new_angle(자료를 엮어야 보이는 것) — 제목·훅은 new_angle 에서 (03 §0-2) | ✅ | 질문이 '누가 이끄나'에서 '무엇을 팔았나'로 바뀌었다 — 그런데 10- |
| G3 | SHOULD | v26: 팩트시트 '## 자료 지도' — 보고서·발언·행동 각 2줄+, 합계 6줄+, 자료마다 의미 칸 (03 §0-2) | ⚠️ | 0줄 {'보고서': 0, '발언': 0, '행동': 0} 의미✓ |
| G3 | SHOULD | v33: 팩트시트 '## 직접 계산' 1개+ (식·출처 숫자) — 연결 비율·민감도 (03 §0-4) | ✅ | 3개 |
| G3 | SHOULD | v33: 팩트시트 '## 틀리는 경우' 3개 (03 §0-4) | ✅ | 3개 |
| G3 | SHOULD | v33: 팩트시트 '## 신호' 숫자 기준선·날짜 3개+ (03 §0-4) | ✅ | 3개 |
| G1 | SHOULD | v28: topic_brief hub_event — 그 기간 시장을 가장 크게 흔든 사건이 중심축 (03 §0-3) | ✅ | 베선트 재무장관 '10일 안에 답' 요구 + 의회 수출 규제 추진 (엔비 |
| G3 | SHOULD | v28: 팩트시트 '## 파급 경로'·'## 주의할 점' (03 §0-3) | ⚠️ |  |
| G4 | SHOULD | v28: 대본 앞 3장면 안에 중심 사건 (03 §0-3) | ✅ | 10일 |
| G3 | SHOULD | v26: 팩트시트 '## 매체 프레임' — 매체 4곳+ (국내 2·해외 2), 제목·강조점·빠진 것 (03 §0-2) | ⚠️ | 0곳 |
| G3 | SHOULD | v28: 매체 프레임에 '입장' 칸 (낙관·우려·중립, 03 §0-3) | ⚠️ |  |
| G4 | SHOULD | v26: 대본에 매체가 어떻게 다뤘나 + 말과 행동 맞대기 (03 §0-2) | ⚠️ |  |
| G4 | MUST | v27: 화면에 없는 숫자를 2개+ 말하면서 그 순간 생기는 그림(motion)이 없는 박자 0개 (manual/09 §6) | ✅ | [] |
| G6 | MUST | 제목·썸네일에 채널 이름(이어 읽는 시장) 없음 — 날짜만 (manual/09 §7) | ✅ | [] |
| G4 | SHOULD | market: 끝에 확인할 신호(checklist) | ✅ | ['checklist', 'kinetic', 'outro'] |
| G4 | MUST | 인트로 없음: 첫 장면이 intro 가 아니고 인사·채널 소개·순서 예고·구독 부탁 없음 (README §2-1) | ✅ | [] |
| G4 | SHOULD | 말투: 말 걸기·감탄 표현 없음 (README §2-3, 참고용) | ✅ | [] |
| G4 | SHOULD | 말투: '~습니다/~니다·~까요' 80% 이상, 평균 문장 35자 이상 (미주일기 96~100%·62~71자) | ✅ | 100% · 43자 |
| G5 | SHOULD | 배경: 장면 목적에 맞춰 여러 가지 (권고 3종, 05 §0-2 — v34 유동) | ✅ | ['film', 'grid', 'photo', 'spot', 'tint'] |
| G5 | SHOULD | 배경: 같은 바탕 3장면 연속 없음 (film 제외) | ✅ | [] |
| G5 | SHOULD | 반복 피로: 글씨·도형뿐인 장면이 길게 이어지지 않게 (권고 2장면까지, 05 §0-3 — v34 유동) | ⚠️ | 최장 4연속 (장면 15) |
| G5 | SHOULD | v10: 장식 효과(dust·leak)는 2장면 이하 — 내용이 담긴 볼거리(사진·지도·사물 그림·정리판) 먼저 | ✅ | [] |
| G5 | SHOULD | 반복 피로: 눈요기 있는 장면 60% 이상 | ⚠️ | 8/17 |
| G5 | SHOULD | 반복 피로: 같은 시각 효과 3장면 연속 없음 · 효과 3종 이상(롱폼) | ⚠️ | [] 연속 [] |
| G5 | SHOULD | 바탕색 돌려 쓰기: 직전 두 편과 같은 바탕 계열(특히 미색 종이)이 아님 (05 §0-6) | ✅ | 이번 cream · 직전 [] |
| G5 | SHOULD | v15: 카테고리 개성 — hybrid.json 에 brand (장 표지·인과 지도·듀오톤이 카테고리답게) | ✅ | market |
| G5 | SHOULD | v15: 장 표지 사진은 주제에 맞게 — 같은 사진 두 번·NASA 사진 2장 이상 없음 | ✅ | 표지 ['nyse', 'capitol', 'seoul'] · NASA 0 |
| G5 | SHOULD | 반복 피로: 같은 채널 직전 편과 화면 구성 겹침 70% 이하 (Jaccard) | ✅ | 69% |
| G5 | SHOULD | 같은 type 3연속 없음 (권고, v34 유동) | ✅ | [] |
| G5 | SHOULD | 자료 화면 공백 ≤45초 | ⚠️ | 최장 527초 |
| G5 | SHOULD | 장 표지 간격 ≤200초 | ✅ | 최장 145초 |
| G5 | SHOULD | 스타일 조합: 상황에 맞춰 섞기 (권고 4종, v34 유동) | ✅ | 7종 ['archive-doc', 'data-report', 'hybrid-causal', 'kinetic-type', 'map-journey' |
| G5 | SHOULD | 한 스타일이 40% 넘지 않음 (권고, v34 유동) | ✅ | paper-column 0.33 |
| G5 | SHOULD | 한 장면 안에서 겹친 장면(layers) 3개 안팎 (권고, v34 유동) | ⚠️ | 2 |
| G5 | SHOULD | 같은 스타일 3장면 연속 없음 (권고, v34 유동) | ✅ | 최장 2 |
| G5 | SHOULD | 강조는 아껴서: 1분에 1번 안팎 (이 영상 9번, v34 유동) | ✅ | 1번 [(22, 'kinetic')] |
| G5 | SHOULD | 한 장면에 강조 1개까지 (위아래로 같은 내용 반복 피하기, v34 유동) | ✅ | 넘친 장면 [] |
| G5 | SHOULD | 핵심 단어 띄우기(words)는 단어 1~3개 (v34 유동) | ✅ | [] |
| G5 | SHOULD | 그래픽 팩이 브랜드에 맞는 스타일 등록부 안 (styles/recipes) | ✅ | paper-sketch / 등록부 ['blueprint', 'clean-flat', 'clean-white', 'corkboard', 'dark |
| G5 | SHOULD | style-pick 기록 (상황에 맞춘 스타일 선택) | ✅ | python -m ytflow style-pick <프로젝트> |
| G5 | SHOULD | edit-plan 기록 (메인·주제 레포에서 이 영상의 상황별 장면·기법을 채움) | ✅ | python -m ytflow edit-plan <프로젝트> → 02_script/EDIT_CONTEXT.md |

사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
