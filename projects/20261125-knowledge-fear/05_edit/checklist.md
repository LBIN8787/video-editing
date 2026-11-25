# 체크리스트 — 20261125-knowledge-fear

매뉴얼 v135 · 2026-11-25T21:24:58 · **MUST 실패 2개**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ❌ | [2026-11-25 · 20261125-curiosity-riemann 기각] 불합격 입니다. 전부 이미지느낌보다는 글씨느낌에 애니메이션효과  |
| G0 | SHOULD | 매뉴얼 그래프가 최신 (python -m ytflow manual-graph) | ✅ | manual/graph.json |
| G1 | MUST | topic_brief.json 있음 | ✅ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ✅ | 안전한 줄 알면서도, 왜 몸은 먼저 놀랄까 |
| G1 | MUST | 트리거·왜 지금 | ✅ | 2026-11-03 Nature Neuroscience(맥길대·토론토대 스카버러): 공포를 배우면 해마에서 '위험한 곳'과 '안전한 곳'의 기억 |
| G1 | MUST | 욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3) | ✅ | 강도 3 · 자료 2 |
| G1 | 참고 | 욕망 점수 합계 (후보끼리 비교할 때 씀) | ✅ | 합계 16 {'desire': 3, 'clarity': 3, 'timeliness': 3, 'demand': 2, 'visuals': 2, 'a |
| G1 | MUST | 수요 증거 1개 이상 | ✅ | 2 |
| G1 | SHOULD | 후보 3개 비교 기록 | ⚠️ | 0 |
| G1 | SHOULD | 우리만의 답(our_angle) | ✅ | 불안을 '고장'이 아니라 '정확함 대신 속도를 고른 설계'로 다시 보기 — 새 실험 + 진화 의학 + 반론 |
| G1 | SHOULD | 무엇이 띄우나(driver: 소재·각도·형식 + 근거) | ⚠️ | 새 연구 · '불안은 생존 본능'은 흔하지만, 기억이 겹쳐서 빨라진다는 기제와 그 대 |
| G2 | MUST | 자료 화면마다 credit·url | ❌ | 0개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | 참고 | 자료 화면 소스 종류 (한 곳에서만 가져오면 화면이 단조로워짐) | ℹ️ | 0종 |

**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.
사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
