# 체크리스트 — 20261107-knowledge-스페인독감

매뉴얼 v1 · 2026-11-08T14:02:58 · **MUST 실패 6개**

| 게이트 | 등급 | 항목 | 결과 | 내용 |
|---|---|---|---|---|
| G0 | MUST | 기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음) | ✅ |  |
| G1 | MUST | topic_brief.json 있음 | ❌ | 01_research/topic_brief.json (schemas/topic_brief.schema.json) |
| G1 | MUST | 브랜드(ai/market/curiosity) | ✅ | curiosity |
| G1 | MUST | 욕망·시청자 질문 | ❌ |  |
| G1 | MUST | 트리거·왜 지금 | ❌ |  |
| G1 | MUST | 욕망 점수 ≥12, 욕망 강도·보여 줄 자료 ≥2 | ❌ | 합계 0 {} |
| G1 | MUST | 수요 증거 1개 이상 | ❌ | 0 |
| G1 | SHOULD | 후보 3개 비교 기록 | ⚠️ | 0 |
| G1 | SHOULD | 우리만의 답(our_angle) | ⚠️ |  |
| G2 | MUST | 자료 화면마다 credit·url | ✅ | 13개, 빠짐 [] |
| G2 | MUST | 금지 라이선스(SA·NC·ND) 없음 | ✅ | [] |
| G2 | SHOULD | 자료 화면 소스 3종 이상 (롱폼) | ✅ | 10종 |
| G3 | MUST | 팩트시트 + 출처 링크 3개 이상 | ❌ | 링크 0개 |
| G3 | SHOULD | 확인 상태 표시(✅/⚠️) | ✅ |  |
| G3 | SHOULD | '쓰지 않는 것' 목록 | ✅ |  |
| G4 | MUST | core_message·question·logic | ✅ |  |
| G4 | MUST | 비교 기준≥1·비유≥2·과거 사례≥1·풀이≥1 | ✅ | {'compare_to': 4, 'analogies': 2, 'past_cases': 2, 'glossary': 4} |
| G4 | MUST | 투자 권유 표현 0개 | ✅ | [] |
| G4 | MUST | 레퍼런스 채널 이름 0개 | ✅ | [] |
| G4 | MUST | 미완성 표시 0개 | ✅ | [] |
| G4 | SHOULD | 과장 단어 0개 | ✅ | [] |
| G4 | SHOULD | 첫 3장면 안에 질문 | ✅ |  |
| G5 | MUST | 같은 type 3연속 없음 | ✅ | [] |
| G5 | SHOULD | 자료 화면 공백 ≤45초 | ⚠️ | 최장 155초 |
| G5 | SHOULD | 장 표지 간격 ≤200초 | ✅ | 최장 92초 |
| G5 | SHOULD | 그래픽 팩이 브랜드 추천 안 | ✅ | paper-sketch |
| G6 | MUST | final.mp4 | ✅ |  |
| G6 | MUST | 레이아웃 점검 비어 있음 | ✅ | {} |
| G6 | MUST | 싱크 (0.5초 안 ≥95%, 화면−소리 ≤0.1초, 중앙값 ≤0.2초) | ✅ | {'within_0_5s': None, 'p95_abs_offset': 0.37, 'median_abs_offset': 0.06, 'video_ |
| G6 | SHOULD | 납품 점검(음량 등) | ✅ | completed |
| G6 | SHOULD | 최종 목소리 ElevenLabs | ✅ |  |
| G7 | MUST | 제목 후보 3개 + 이유 | ✅ |  |
| G7 | MUST | 썸네일 A/B/C + 점검 ok | ✅ |  |
| G7 | SHOULD | 제목 앞 22자 안에 질문/핵심 | ✅ | 스페인 독감은 왜 '스페인' 독감일까?  |
| G8 | MUST | GitHub Release 업로드 | ✅ |  |
| G8 | MUST | episodes.md 기록 | ✅ | ch-knowledge |

사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요.
