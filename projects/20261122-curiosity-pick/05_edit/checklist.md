# 체크리스트 — 20261122-curiosity-pick

매뉴얼 v98 · 2026-11-22T13:08:57 · **MUST 실패 2개**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ✅ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 몇십 년 된 주차장에도 금이 가는데, 철근도 없는 1,900년 된 돔은 어떻게 버텼을까? |
| G1 | MUST | 트리거·왜 지금 | ✅ | 2026-11-22 정기 작업: 호기심 채널 일 1편(매일 18:00) — 분야를 가리지 않는 이야기 채널로 바뀐 첫 주제 카드. 후보 3개는  |
| G1 | MUST | 욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3) | ✅ | 강도 3 · 자료 2 |
| G1 | 참고 | 욕망 점수 합계 (후보끼리 비교할 때 씀) | ✅ | 합계 15 {'desire': 3, 'clarity': 3, 'timeliness': 1, 'demand': 3, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 2 |
| G1 | SHOULD | 후보 3개 비교 기록 | ✅ | 3 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | '옛날 것이 더 튼튼하다'가 아니다. 판테온 돔은 실제로 금이 가 있다. 금이 가도 무너지지 않게 무게를 덜었고(두께·가벼운 돌·빈 꼭대기),  |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ✅ | 각도 · 누구나 아는 '로마 콘크리트는 튼튼하다'를 '사실 금이 가 있다'로 뒤집 |
| G2 | MUST | 자료 화면마다 credit·url | ✅ | 1개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | 참고 | 자료 화면 소스 종류 (한 곳에서만 가져오면 화면이 단조로워짐) | ℹ️ | 1종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ✅ | 링크 6개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |
| G4 | SHOULD | 목적 분간: intent.md 에 '목적:' 정보 습득형/즐길거리형 + 세 질문 (11 §2-4) | ✅ |  |
| G4 | MUST | core_message·question·logic | ✅ |  |
| G4 | MUST | 근거 검수표: 모든 주장에 근거·비약·괴리·착각 확인 (02_script/script_review.md '근거 검수', 13 §4-1, 2026-11-22 사용자) | ✅ |  |
| G4 | SHOULD | 대본 구성요소 대조표: 채널 대본 공식의 요소마다 있음/없음·어느 장 (02_script/script_review.md '구성요소', 13 §7) | ✅ |  |
| G4 | SHOULD | curiosity: 비유와 대비가 되는 숫자 — 사실은 이야기 속에서 (04 §0-6) | ✅ | {'compare_to': 3, 'analogies': 2, 'past_cases': 2, 'glossary': 1} |
| G4 | MUST | 투자 권유 표현 0개 | ✅ | [] |
| G4 | MUST | 레퍼런스 채널 이름 0개 | ✅ | [] |
| G4 | MUST | 미완성 표시 0개 | ✅ | [] |
| G4 | SHOULD | 과장 단어 0개 | ✅ | [] |
| G4 | SHOULD | 진행 말투: '~였고요.' 같은 이어 붙인 끝맺음 없음 (README §2-2, 2026-11-20 사용자: 필수 아님) | ✅ | [] |
| G4 | SHOULD | 여는 부분에 이 영상의 질문 하나 (시청자가 무엇을 따라가는지 알게) | ✅ |  |
| G1 | MUST | curiosity: 훅 먼저 정하기 (topic_brief.hook: type·line·gap) | ✅ | 나와의 연결 |
| G4 | MUST | curiosity: 여는 장면이 곧 훅 — 소개·순서 예고·설명보다 앞 (04 §0) | ✅ | 훅 박자 0 · 순서 예고 None |
| G4 | MUST | curiosity: 훅의 질문(gap)이 나옴 (답은 숨김) | ✅ | 철근도 없는 이 돔은 어떻게 1,900년을 버텼을까요? |
| G1 | MUST | curiosity: 시청자 조사 01_research/audience.md (주 시청자·유입 경로·유입 이유·끝까지 보는 이유) | ✅ | docs/29 |
| G4 | MUST | curiosity: 편집 전에 대본만 사용자 검토 통과 (02_script/script_review.md '통과', 04 §0-6) | ✅ |  |
| G6 | SHOULD | curiosity: 제목이 훅에서 나옴 (훅과 같은 낱말) | ✅ | 3/4 |
| G4 | MUST | 인트로 없음: 첫 장면이 intro 가 아니고 인사·채널 소개·순서 예고·구독 부탁 없음 (README §2-1) | ✅ | [] |
| G4 | SHOULD | 말투: 말 걸기·감탄 표현 없음 (README §2-3, 참고용) | ✅ | [] |
| G4 | 참고 | 말투(호기심): '~습니다/~니다' 끝맺음 몫·평균 문장 길이 (차분한 이야기 내레이터인지) | ✅ | 85% · 36자 |
| G6 | 참고 | 길이(측정값만 — 시간 기준 없음, 구성요소가 정함, README §2-4) | ✅ | 0.0분 |
| G5 | SHOULD | 배경: 한 가지 바탕으로 고정하지 않음 — 장면이 하는 일이 바뀌면 바탕도 바뀜 (05 §0-2) | ⚠️ | ['film'] |
| G5 | 참고 | 배경: 같은 바탕이 이어지는 구간 | ✅ | [] |
| G5 | 참고 | 반복 피로: 글씨·도형뿐인 장면이 이어지는 구간 — 자료·지도·그림으로 보여 줄 수 있는지 다시 볼 곳 (05 §0-3) | ℹ️ | 최장 6연속 (장면 s6) |
| G5 | 참고 | 장식 효과(dust·leak)를 쓴 장면 — 내용이 담긴 볼거리 대신 쓰지 않았는지 (05 §0-4) | ✅ | [] |
| G5 | 참고 | 반복 피로: 볼거리(자료·지도·그림)가 있는 장면의 몫 | ℹ️ | 0/6 |
| G5 | 참고 | 반복 피로: 같은 시각 효과가 이어지는 구간 (효과 종류 수는 채우지 않음 — 05 §0-5) | ✅ | [] 연속 [] |
| G5 | 참고 | 바탕 계열: 같은 채널 직전 두 편과 같은 바탕 계열인지 (바꿔도 되고 이어 써도 됨 — 카테고리 얼굴 05 §0-7 이 먼저) | ✅ | 이번 cream · 직전 [] |
| G5 | SHOULD | v15: 카테고리 개성 — hybrid.json 에 brand (장 표지·인과 지도·듀오톤이 카테고리답게) | ⚠️ |  |
| G5 | SHOULD | v15: 장 표지 사진은 주제에 맞게 — 같은 사진 두 번 없음, 한 출처로 표지를 모두 때우지 않음 | ✅ | 표지 [] · 가장 많은 출처 ('', 0) |
| G5 | 참고 | 반복 피로: 같은 채널 직전 편과 화면 구성이 얼마나 겹치나 | ✅ | 0% |
| G5 | 참고 | 같은 장면 type 이 이어지는 구간 — 하는 일이 바뀌었는데 화면이 같지 않나 | ℹ️ | [None, None, None, None] |
| G5 | SHOULD | 스타일 조합: 한 스타일로만 만들지 않음 — 장면이 하는 일에 맞춰 섞음 (05 §0-1) | ⚠️ | 1종 ['?None'] |
| G5 | 참고 | 스타일 조합: 가장 많이 쓴 스타일의 몫·겹친 장면·같은 스타일 연속 | ℹ️ | ?None 1.0 · 겹침 0 · 최장 연속 6 |
| G5 | 참고 | 강조 횟수·강조가 겹친 장면 — 기억할 숫자·반전·결론에만 썼는지 (05 §0-1) | ✅ | 0번 [] · 겹친 장면 [] |
| G5 | SHOULD | 핵심 단어 띄우기에 문장을 쓰지 않음 — 자막과 같은 내용을 위에 반복하지 않음 (v3) | ✅ | [] |
| G5 | SHOULD | 그래픽 팩이 브랜드에 맞는 스타일 등록부 안 (styles/recipes) | ✅ | paper-sketch / 등록부 ['chalkboard', 'clean-flat', 'clean-white', 'crumpled-paper', |
| G5 | SHOULD | style-pick 기록 (상황에 맞춘 스타일 선택) | ⚠️ | python -m ytflow style-pick <프로젝트> |
| G5 | SHOULD | edit-plan 기록 (메인·주제 레포에서 이 영상의 상황별 장면·기법을 채움) | ⚠️ | python -m ytflow edit-plan <프로젝트> → 02_script/EDIT_CONTEXT.md |
| G6 | MUST | final.mp4 | ✅ |  |
| G6 | MUST | 레이아웃 결함 없음 (겹침·잘림·대비·장면 의도 goal/why) | ❌ | {} |
| G6 | SHOULD | 글자 겹침 점검 기록 (05_edit/overlap_qa.json) | ⚠️ | python scripts/overlap_scan.py <프로젝트> |
| G6 | 참고 | 무대 화면: 한꺼번에 보이는 것·글자·멈춘 박자 (한 화면 한 생각인지 눈으로, 04 §0-5) | ✅ | {} |
| G6 | MUST | 싱크 (0.5초 안 ≥95%, 화면−소리 ≤0.1초, 중앙값 ≤0.2초) | ❌ | {'within_0_5s': 0.968, 'p95_abs_offset': 0.43, 'median_abs_offset': 0.26, 'video |
| G6 | SHOULD | 납품 점검(음량 등) | ⚠️ | None |
| G6 | SHOULD | 최종 목소리 ElevenLabs | ✅ |  |
| G7 | MUST | 제목 후보 3개 + 이유 | ✅ |  |
| G7 | MUST | 썸네일 A/B/C + 점검 ok | ✅ |  |
| G7 | 참고 | 제목 앞부분에 질문·핵심 (목록에서 잘려도 무슨 영상인지 보이게) | ✅ | 철근 하나 없는 1,900년 된 돔은 왜 |
| G8 | MUST | 완성본 보관 기록 — Drive(drive.json·drive_archive.json) 또는 공개 가능한 것만 GitHub Release(release.json) | ✅ |  |
| G8 | MUST | episodes.md 기록 | ✅ | ch-knowledge |

**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.
사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
