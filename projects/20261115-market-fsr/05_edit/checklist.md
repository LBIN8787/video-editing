# 체크리스트 — 20261115-market-fsr

매뉴얼 v27 · 2026-11-15T02:24:35 · **통과**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | market |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 연준은 한 주 동안 AI 를 물가의 원인, 아직 안 보이는 생산성, 금융 위험 1순위로 세 번 말했다 — 이 셋을 이으면 무엇이 보일까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 11/13 연준 금융안정보고서(AI 위험 1순위, 헤지펀드 레버리지 최고, AI 빚 6,800억 달러+) · 같은 주 보먼(11/10)·제퍼슨( |
| G1 | MUST | 욕망 점수 ≥12, 욕망 강도·보여 줄 자료 ≥2 | ✅ | 합계 17 {'desire': 3, 'clarity': 3, 'timeliness': 3, 'demand': 3, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 1 |
| G1 | SHOULD | 후보 3개 비교 기록 | ⚠️ | 1 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 보고서 요약이 아니라, 반년 동안의 보고서·발언·행동을 날짜 순으로 엮어 고리를 보이고, 매체가 강조한 것과 빠뜨린 것을 나란히 둔다 |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 소재 · 중앙은행 공식 문서 + 같은 주 연설 원문 + 매체 보도가 모두 공개됨 |
| G2 | MUST | 시장: SAVE(오선) 소식 확인 기록 — 상태 '확인함' 또는 '확인 못 함: 이유' (01_research/save_check.md) | ✅ | 확인함 (사용자 메모: 20261115.md, 알림 4건) |
| G2 | SHOULD | 시장: SAVE 실제로 확인함 (항목 1개 이상) | ✅ | 확인함 (사용자 메모: 20261115.md, 알림 4건) · 항목 4 |
| G2 | MUST | 자료 화면마다 credit·url | ✅ | 5개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | SHOULD | 자료 화면 소스 3종 이상 (롱폼) | ✅ | 5종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ✅ | 링크 14개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |
| G4 | MUST | core_message·question·logic | ✅ |  |
| G4 | MUST | 비교 기준≥1·비유≥2·과거 사례≥1·풀이≥1 | ✅ | {'compare_to': 4, 'analogies': 2, 'past_cases': 2, 'glossary': 6} |
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
| G3 | MUST | 매일 시장: 이야기마다 원인 종류(이슈·보고서·전망·실적)와 1차 출처를 팩트시트에 | ✅ | ['이슈', '보고서', '전망', '실적'] |
| G1 | MUST | v26: topic_brief 에 known(이미 알려진 것)·new_angle(자료를 엮어야 보이는 것) — 제목·훅은 new_angle 에서 (03 §0-2) | ✅ | 같은 주 연준은 AI 를 물가의 원인(보먼)·아직 안 보이는 생산성(제퍼 |
| G3 | MUST | v26: 팩트시트 '## 자료 지도' — 보고서·발언·행동 각 2줄+, 합계 6줄+, 자료마다 의미 칸 (03 §0-2) | ✅ | 10줄 {'보고서': 4, '발언': 3, '행동': 3} 의미✓ |
| G3 | MUST | v26: 팩트시트 '## 매체 프레임' — 매체 4곳+ (국내 2·해외 2), 제목·강조점·빠진 것 (03 §0-2) | ✅ | 5곳 |
| G4 | MUST | v26: 대본에 매체가 어떻게 다뤘나 + 말과 행동 맞대기 (03 §0-2) | ✅ |  |
| G4 | MUST | v27: 화면에 없는 숫자를 2개+ 말하면서 그 순간 생기는 그림(motion)이 없는 박자 0개 (manual/09 §6) | ✅ | [] |
| G6 | MUST | 제목·썸네일에 채널 이름(이어 읽는 시장) 없음 — 날짜만 (manual/09 §7) | ✅ | [] |
| G4 | SHOULD | market: 끝에 확인할 신호(checklist) | ✅ | ['kinetic', 'checklist', 'outro'] |
| G4 | MUST | 인트로 없음: 첫 장면이 intro 가 아니고 인사·채널 소개·순서 예고·구독 부탁 없음 (README §2-1) | ✅ | [] |
| G4 | SHOULD | 말투: 말 걸기·감탄 표현 없음 (README §2-3, 참고용) | ✅ | [] |
| G4 | SHOULD | 말투: '~습니다/~니다·~까요' 80% 이상, 평균 문장 35자 이상 (미주일기 96~100%·62~71자) | ✅ | 100% · 44자 |
| G6 | MUST | 길이: 롱폼 10분 이상 (README §2-4) | ✅ | 10.4분 |
| G5 | MUST | 배경: 장면 목적에 맞춰 3종 이상 (한 가지 바탕만 쓰면 불합격, manual 05 §0-2) | ✅ | ['film', 'grid', 'photo', 'spot', 'tint'] |
| G5 | SHOULD | 배경: 같은 바탕 3장면 연속 없음 (film 제외) | ✅ | [] |
| G5 | MUST | 반복 피로: 글씨·도형뿐인 장면 3개 연속 금지 (눈요기: 자료·지도·사진 겹치기·시각 효과, 05 §0-3) | ✅ | 최장 2연속 (장면 21) |
| G5 | SHOULD | v10: 장식 효과(dust·leak)는 2장면 이하 — 내용이 담긴 볼거리(사진·지도·사물 그림·정리판) 먼저 | ✅ | [] |
| G5 | SHOULD | 반복 피로: 눈요기 있는 장면 60% 이상 | ✅ | 14/19 |
| G5 | SHOULD | 반복 피로: 같은 시각 효과 3장면 연속 없음 · 효과 3종 이상(롱폼) | ✅ | ['fx:dolly', 'fx:scan', 'fx:tilt'] 연속 [] |
| G5 | SHOULD | 바탕색 돌려 쓰기: 직전 두 편과 같은 바탕 계열(특히 미색 종이)이 아님 (05 §0-6) | ✅ | 이번 cream · 직전 ['cream'] |
| G5 | SHOULD | v15: 카테고리 개성 — hybrid.json 에 brand (장 표지·인과 지도·듀오톤이 카테고리답게) | ✅ | market |
| G5 | SHOULD | v15: 장 표지 사진은 주제에 맞게 — 같은 사진 두 번·NASA 사진 2장 이상 없음 | ✅ | 표지 ['fed', 'dc', 'nyse'] · NASA 0 |
| G5 | SHOULD | 반복 피로: 같은 채널 직전 편과 화면 구성 겹침 70% 이하 (Jaccard) | ⚠️ | 92% |
| G5 | MUST | 같은 type 3연속 없음 | ✅ | [] |
| G5 | SHOULD | 자료 화면 공백 ≤45초 | ⚠️ | 최장 599초 |
| G5 | SHOULD | 장 표지 간격 ≤200초 | ✅ | 최장 161초 |
| G5 | MUST | 스타일 조합: 4종 이상 섞기 (한 스타일로만 만들면 불합격) | ✅ | 7종 ['archive-doc', 'data-report', 'hybrid-causal', 'kinetic-type', 'map-journey' |
| G5 | MUST | 한 스타일이 40% 넘지 않음 | ✅ | paper-column 0.34 |
| G5 | MUST | 한 장면 안에서 겹친 장면(layers) 3개 이상 | ✅ | 4 |
| G5 | MUST | 같은 스타일 3장면 연속 없음 | ✅ | 최장 2 |
| G5 | MUST | 강조는 아껴서: 1분에 1번 이하 (이 영상 10번까지) | ✅ | 1번 [(24, 'kinetic')] |
| G5 | MUST | 한 장면에 강조 1개까지 (위아래로 같은 내용 반복 금지) | ✅ | 넘친 장면 [] |
| G5 | MUST | 핵심 단어 띄우기(words)는 단어 1~3개만 | ✅ | [] |
| G5 | SHOULD | 그래픽 팩이 브랜드에 맞는 스타일 등록부 안 (styles/recipes) | ✅ | paper-sketch / 등록부 ['blueprint', 'clean-flat', 'clean-white', 'corkboard', 'dark |
| G5 | SHOULD | style-pick 기록 (상황에 맞춘 스타일 선택) | ✅ | python -m ytflow style-pick <프로젝트> |
| G6 | MUST | final.mp4 | ✅ |  |
| G6 | MUST | 레이아웃 점검 비어 있음 | ✅ | {} |
| G6 | MUST | 싱크 (0.5초 안 ≥95%, 화면−소리 ≤0.1초, 중앙값 ≤0.2초) | ✅ | {'within_0_5s': 0.977, 'p95_abs_offset': 0.11, 'median_abs_offset': 0.05, 'video |
| G6 | SHOULD | 납품 점검(음량 등) | ✅ | completed |
| G6 | SHOULD | 움직임: 화면 변화 ≥8회/분 · 정지 화면 비율 ≤0.5 (완성본 측정, v12 — 차분함이 우선) | ✅ | 변화 20.7/분 · 정지 0.12 |
| G6 | MUST | 시장 움직임: 정지 화면 비율 ≤0.45 (목표 0.3, manual/09 §6) | ✅ | 정지 0.12 |
| G6 | SHOULD | 최종 목소리 ElevenLabs | ✅ |  |
| G7 | MUST | 제목 후보 3개 + 이유 | ✅ |  |
| G7 | MUST | 썸네일 A/B/C + 점검 ok | ✅ |  |
| G7 | SHOULD | 제목 앞 22자 안에 질문/핵심 | ⚠️ | 연준이 한 주에 AI를 세 번 말했다 — |
| G8 | MUST | GitHub Release 업로드 | ✅ |  |
| G8 | MUST | episodes.md 기록 | ✅ | ch-market-daily |

사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
