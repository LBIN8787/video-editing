# 06. 체크리스트와 검사안 — 반드시 지킬 것

## 검사 방법
```bash
python -m ytflow check <프로젝트>              # 모든 게이트 (만든 단계까지)
python -m ytflow check <프로젝트> --upto G4    # 대본까지만
```
결과: `05_edit/checklist.md`(사람이 읽는 표) + `05_edit/checklist.json`. **MUST 가 하나라도 실패하면 종료 코드 1** — 다음 단계로 가지 않습니다.
- **MUST** = 반드시. 실패하면 고치기 전에는 렌더·업로드 금지.
- **SHOULD** = 권고. 실패하면 이유를 `REPORT.md` 에 적고 진행 가능.
- **EYE** = 사람(또는 에이전트)이 눈으로 확인. 자동 검사 불가 → 확인 후 `05_edit/checklist_eye.md` 에 체크.

> **시사(issues) 채널**은 아래에 더해 `manual/08-issues.md` §6 의 전용 항목(기준 시각·양쪽 입장·단정 금지어·출처 다양성)을 `check` 가 함께 검사합니다.

## G1 주제 (`01_research/topic_brief.json`, 스키마 `schemas/topic_brief.schema.json`)
| 등급 | 항목 | 자동 |
|---|---|---|
| MUST | `brand` 가 ai/market/curiosity 중 하나, `desire` 와 `viewer_question` 이 채워짐 | ✅ |
| MUST | `trigger` (무엇이 이 주제를 지금 건드렸나)와 `why_now` 가 있음 | ✅ |
| MUST | 욕망 점수 합계 ≥ 12, 욕망 강도 ≥ 2, 보여 줄 자료 ≥ 2 (01-desire-map §3) | ✅ |
| MUST | 수요 증거 1개 이상 (`demand_evidence`: 검색·아웃라이어·뉴스 순위) | ✅ |
| SHOULD | 후보 3개를 비교한 기록 (`candidates`) | ✅ |
| SHOULD (issues 는 MUST) | `driver`: 이 영상을 무엇이 띄우나 — 소재·각도·형식 + 근거 (manual/01 §4-1). 소재가 약하면 각도(반대 결과·생활 체감·추억·사람)를 적음 | ✅ |
| SHOULD | `our_angle` (남들 영상보다 깊은 것) | ✅ |

## G2 소스
| 등급 | 항목 | 자동 |
|---|---|---|
| MUST | 쓰는 자료 화면마다 `credit` 과 `url` (라이선스 포함) | ✅ |
| MUST | 라이선스가 CC BY·CC0·퍼블릭 도메인·공식 자료·직접 제작 (CC BY-SA·NC·ND, 다른 유튜버 영상 금지) | ✅ (credit 단어 검사) + EYE |
| MUST | 봇 확인·차단 우회 안 함 | EYE |
| SHOULD | 롱폼은 자료 화면 소스 3종 이상 | ✅ |

## G3 사실 (`01_research/factsheet.md`)
| 등급 | 항목 | 자동 |
|---|---|---|
| MUST | 팩트시트가 있고 출처 링크가 3개 이상 (롱폼) | ✅ |
| MUST | ❌(확인 실패) 사실이 대본에 없음 | EYE |
| SHOULD | ✅/⚠️ 상태 표시가 있음 | ✅ |
| SHOULD | '쓰지 않는 것' 목록 | ✅ |

## G4 대본 (`02_script/hybrid.json`)
| 등급 | 항목 | 자동 |
|---|---|---|
| MUST | `core_message`, `question`, `logic` 이 있음 | ✅ |
| MUST | 숫자 비교 기준 `compare_to` ≥ 1, 비유 `analogies` ≥ 2, 과거 사례 `past_cases` ≥ 1, `glossary` ≥ 1 | ✅ |
| MUST | **투자 권유 표현 0개** (사세요·매수 추천·지금이 기회·무조건 오른다·수익 보장 …) | ✅ |
| MUST | 레퍼런스 채널 이름 0개 | ✅ |
| MUST | '재확인 필요'·'TODO' 같은 미완성 표시 0개 | ✅ |
| SHOULD | 과장 단어 0개 (충격·소름·경악·역대급) | ✅ |
| SHOULD | 첫 장면이 30초 안에 질문을 던짐 (`question` 단어가 첫 3장면 안에 or 질문형 문장) | ✅ |
| SHOULD | market: 마지막 2장면 안에 확인할 신호(checklist) | ✅ |
| SHOULD | issues: 말하듯 쓴 대본 — 묻는 문장(?) 3개 이상, 보도문 말투('~것으로 알려졌다') 비율 낮게 (08 §0-1) | ✅ |

## G5 연출
| 등급 | 항목 | 자동 |
|---|---|---|
| MUST | 같은 type 3연속 없음 (chapter 제외) | ✅ |
| MUST | **강조 아껴 쓰기**: 강조(words·number·vox·kinetic) 1분에 1번 이하, 한 장면에 1개까지, words 는 핵심 단어 1~3개만 — 자막과 같은 문장을 위에 반복하면 불합격 | ✅ |
| MUST | **스타일 조합**: 롱폼 4종 이상(쇼츠 2종), 한 스타일 40% 이하(쇼츠 60%), 겹친 장면(`layers`) 3개 이상(쇼츠 1개), 같은 스타일 3장면 연속 없음 — 한 스타일로만 만들면 불합격 | ✅ |
| SHOULD | 자료 화면 공백 ≤ 45초 (렌더 후 `hybrid_timeline.json` 으로 계산) | ✅ |
| SHOULD | 약 3분마다 장 표지/질문 (최장 간격 ≤ 200초) | ✅ |
| SHOULD | 그래픽 팩이 브랜드에 맞는 등록부 레시피의 팩 (`styles/recipes`, `edit.yaml` 의 skin) | ✅ |
| SHOULD | `style-pick` 기록이 있음 (`01_research/style_pick.json`) — 상황에 맞춰 골랐다는 증거 | ✅ |

## G6 완성본
| 등급 | 항목 | 자동 |
|---|---|---|
| MUST | `final.mp4` 있음 | ✅ |
| MUST | 레이아웃 점검 비어 있음 (`04_assets/layout_qa.json`: 화살표·글자 겹침) | ✅ |
| MUST | 싱크: 자막 0.5초 안 ≥ 95%, 화면−소리 ≤ 0.1초 (`sync_qa.json`), 중앙값 ≤ 0.2초 | ✅ |
| MUST | 프레임 시트를 눈으로 확인 (`final_sheet.png`): 잘린 글자·겹침·빈 화면 | EYE |
| SHOULD | 음량 −14 LUFS 근처 (`delivery_check.json`) | ✅ |
| SHOULD | 업로드 최종본은 ElevenLabs 목소리 (edge-tts 는 초안) | ✅ (`03_voice/el` 또는 channel tts) |

## G7 포장
| 등급 | 항목 | 자동 |
|---|---|---|
| MUST | 제목 후보 3개 + 각 이유 | ✅ |
| MUST | 썸네일 A/B/C 파일 + `thumbnail_qa.json` 모두 ok (시간 표시 겹침 없음) | ✅ |
| MUST | 제목·썸네일에 영상에 없는 숫자·사실 없음 | EYE |
| SHOULD | 제목 앞 22자 안에 질문/핵심 | ✅ |

## G8 보관·기록
| 등급 | 항목 | 자동 |
|---|---|---|
| MUST | GitHub Release 업로드 (`05_edit/release.json`) | ✅ |
| MUST | 채널 `episodes.md` 에 회차 한 줄 | ✅ |
| SHOULD | 기획 문서(md/json/yaml) 커밋, 미디어는 커밋 안 함 | EYE (`git status`) |
| SHOULD | `REPORT.md` 의 남은 일을 사용자에게 보고 | EYE |

## 마지막 사람 눈 검사 (EYE) — 3분 안에
1. 첫 30초를 소리 켜고 본다: 질문이 들리는가? 화면이 말보다 늦지 않은가?
2. 프레임 시트에서 잘린 글자·겹친 선·빈 화면을 찾는다.
3. 숫자 하나를 골라 팩트시트의 출처를 직접 열어 본다.
4. 썸네일을 휴대폰 크기로 본다(`thumbnail_preview.png`): 3초 안에 무슨 영상인지 아는가?
5. market: "이 영상을 보고 누가 특정 종목을 사야 한다고 느낄까?" → 그렇다면 고친다.
