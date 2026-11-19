# 체크리스트 — 20261119-curiosity-choice-blindness

매뉴얼 v44 · 2026-11-19T15:46:21 · **MUST 실패 1개**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ❌ | [2026-11-19 · 사용자 피드백 · projects/20261118-curiosity-next · 층: 작업 기준] 나중에 이 메뉴얼을  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ✅ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 내가 고르지 않은 잼을 왜 골랐다고 했을까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 2026-11-19 호기심 채널 유사 영상 추가 조사 및 D1 사용자 선택. |
| G1 | MUST | 욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3) | ✅ | 강도 3 · 자료 3 |
| G1 | 참고 | 욕망 점수 합계 (후보끼리 비교할 때 씀) | ✅ | 합계 15 {'desire': 3, 'clarity': 3, 'timeliness': 1, 'demand': 2, 'visuals': 3, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 1 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 첫 선택·바뀐 결과·이유를 한 병의 동작으로 구별하고, 즉시 말하지 않은 사람도 알아챘을 수 있는지 본다. |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 각도 · 손가락, 병의 뚜껑, 숟가락이 서로 다른 시점의 근거를 남긴다. |
| G2 | MUST | 자료 화면마다 credit·url | ✅ | 1개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | 참고 | 자료 화면 소스 종류 (한 곳에서만 가져오면 화면이 단조로워짐) | ℹ️ | 1종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ✅ | 링크 8개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |
| G4 | MUST | core_message·question·logic | ✅ |  |
| G4 | SHOULD | curiosity: 비유와 대비가 되는 숫자 — 사실은 이야기 속에서 (04 §0-6) | ✅ | {'compare_to': 1, 'analogies': 2, 'past_cases': 2, 'glossary': 1} |
| G4 | MUST | 투자 권유 표현 0개 | ✅ | [] |
| G4 | MUST | 레퍼런스 채널 이름 0개 | ✅ | [] |
| G4 | MUST | 미완성 표시 0개 | ✅ | [] |
| G4 | SHOULD | 과장 단어 0개 | ✅ | [] |
| G4 | MUST | 진행 말투: '~였고요.' 같은 이어 붙인 끝맺음 없음 (README §2-2) | ✅ | [] |
| G4 | SHOULD | 여는 부분에 이 영상의 질문 하나 (시청자가 무엇을 따라가는지 알게) | ✅ |  |
| G1 | MUST | curiosity: 훅 먼저 정하기 (topic_brief.hook: type·line·gap) | ✅ | 장면 |
| G4 | MUST | curiosity: 여는 장면이 곧 훅 — 소개·순서 예고·설명보다 앞 (04 §0) | ✅ | 훅 박자 0 · 순서 예고 None |
| G4 | MUST | curiosity: 훅의 질문(gap)이 나옴 (답은 숨김) | ✅ | 그 사이에 뭐가 달라졌을까요? |
| G1 | MUST | curiosity: 시청자 조사 01_research/audience.md (주 시청자·유입 경로·유입 이유·끝까지 보는 이유) | ✅ | docs/29 |
| G4 | 참고 | curiosity: 지식·설명 문장의 몫 (사실이 사람·사건 속에 있는지 — 판단은 대본 검토 D2, 04 §0-6) | ✅ | 25/151 = 17% (script_v2.md) |
| G4 | MUST | curiosity: 편집 전에 대본만 사용자 검토 통과 (02_script/script_review.md '통과', 04 §0-6) | ✅ |  |
| G6 | SHOULD | curiosity: 제목이 훅에서 나옴 (훅과 같은 낱말) | ⚠️ | 0/4 |
| G4 | MUST | 인트로 없음: 첫 장면이 intro 가 아니고 인사·채널 소개·순서 예고·구독 부탁 없음 (README §2-1) | ✅ | [] |
| G4 | SHOULD | 말투: 말 걸기·감탄 표현 없음 (README §2-3, 참고용) | ✅ | [] |
| G4 | 참고 | 말투(호기심): '~습니다/~니다' 끝맺음 몫·평균 문장 길이 (차분한 이야기 내레이터인지) | ℹ️ | 66% · 35자 |
| G6 | MUST | 길이: 롱폼 10분 이상 — 많이 짧으면 쇼츠로 (README §2-4) | ✅ | 12.8분 |
| G5 | SHOULD | 배경: 한 가지 바탕으로 고정하지 않음 — 장면이 하는 일이 바뀌면 바탕도 바뀜 (05 §0-2) | ⚠️ | ['film'] |
| G5 | 참고 | 배경: 같은 바탕이 이어지는 구간 | ✅ | [] |
| G5 | 참고 | 반복 피로: 글씨·도형뿐인 장면이 이어지는 구간 — 자료·지도·그림으로 보여 줄 수 있는지 다시 볼 곳 (05 §0-3) | ✅ | 최장 1연속 (장면 27) |
| G5 | 참고 | 장식 효과(dust·leak)를 쓴 장면 — 내용이 담긴 볼거리 대신 쓰지 않았는지 (05 §0-4) | ✅ | [] |
| G5 | 참고 | 반복 피로: 볼거리(자료·지도·그림)가 있는 장면의 몫 | ✅ | 34/35 |
| G5 | 참고 | 반복 피로: 같은 시각 효과가 이어지는 구간 (효과 종류 수는 채우지 않음 — 05 §0-5) | ✅ | [] 연속 [] |
| G5 | SHOULD | 바탕색 돌려 쓰기: 직전 두 편과 같은 바탕 계열(특히 미색 종이)이 아님 (05 §0-6) | ✅ | 이번 cream · 직전 ['cream'] |
| G5 | SHOULD | v15: 카테고리 개성 — hybrid.json 에 brand (장 표지·인과 지도·듀오톤이 카테고리답게) | ✅ | curiosity |
| G5 | SHOULD | v15: 장 표지 사진은 주제에 맞게 — 같은 사진 두 번·NASA 사진 2장 이상 없음 | ✅ | 표지 [] · NASA 0 |
| G5 | 참고 | 같은 장면 type 이 이어지는 구간 — 하는 일이 바뀌었는데 화면이 같지 않나 | ℹ️ | ['stage', 'stage', 'stage', 'stage', 'stage', 'stage', 'stage', 'stage', 'stage' |
| G5 | 참고 | 자료 화면 없이 그래픽만 이어지는 가장 긴 구간 | ℹ️ | 최장 771초 |
| G5 | 참고 | 장 전환 없이 이어지는 가장 긴 구간 | ℹ️ | 최장 771초 |
| G5 | SHOULD | 스타일 조합: 한 스타일로만 만들지 않음 — 장면이 하는 일에 맞춰 섞음 (05 §0-1) | ✅ | 2종 ['?screenshot', 'anim-stage'] |
| G5 | 참고 | 스타일 조합: 가장 많이 쓴 스타일의 몫·겹친 장면·같은 스타일 연속 (뼈대 스타일 영상) | ℹ️ | anim-stage 0.96 · 겹침 34 · 최장 연속 26 |
| G5 | 참고 | 강조 횟수·강조가 겹친 장면 — 기억할 숫자·반전·결론에만 썼는지 (05 §0-1) | ✅ | 0번 [] · 겹친 장면 [] |
| G5 | SHOULD | 핵심 단어 띄우기에 문장을 쓰지 않음 — 자막과 같은 내용을 위에 반복하지 않음 (v3) | ✅ | [] |
| G5 | SHOULD | 그래픽 팩이 브랜드에 맞는 스타일 등록부 안 (styles/recipes) | ✅ | paper-sketch / 등록부 ['chalkboard', 'clean-flat', 'clean-white', 'dark-doc', 'kine |
| G5 | SHOULD | style-pick 기록 (상황에 맞춘 스타일 선택) | ✅ | python -m ytflow style-pick <프로젝트> |
| G5 | SHOULD | edit-plan 기록 (메인·주제 레포에서 이 영상의 상황별 장면·기법을 채움) | ✅ | python -m ytflow edit-plan <프로젝트> → 02_script/EDIT_CONTEXT.md |
| G6 | MUST | final.mp4 | ✅ |  |
| G6 | MUST | 레이아웃 결함 없음 (겹침·잘림·대비·장면 의도 goal/why) | ✅ | {} |
| G6 | 참고 | 무대 화면: 한꺼번에 보이는 것·글자·멈춘 박자 (한 화면 한 생각인지 눈으로, 04 §0-5) | ✅ | {} |
| G6 | MUST | 싱크 (0.5초 안 ≥95%, 화면−소리 ≤0.1초, 중앙값 ≤0.2초) | ✅ | {'within_0_5s': 0.983, 'p95_abs_offset': 0.29, 'median_abs_offset': 0.02, 'video |
| G6 | SHOULD | 납품 점검(음량 등) | ✅ | completed |
| G6 | SHOULD | 최종 목소리 ElevenLabs | ✅ |  |
| G7 | MUST | 제목 후보 3개 + 이유 | ✅ |  |
| G7 | MUST | 썸네일 A/B/C + 점검 ok | ✅ |  |
| G7 | 참고 | 제목 앞부분에 질문·핵심 (목록에서 잘려도 무슨 영상인지 보이게) | ✅ | 내가 고르지 않은 잼을 왜 골랐다고 했을 |

**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.
사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
