# REPORT — 호기심 「정말 남들은 나보다 더 재밌게 살까? — 포모의 정체」 (2026-11-26)

## S0 착수 메모
- 읽은 것: manual/04-curiosity·11-workflow·13-script, channel.yaml(주인공·화풍 = 지우), episodes.md, 직전 편 '품절 임박'(soldout) 주제 기록.
- 주제: 사용자 지정 — "주제는 fomo로 해주세요" (11-24 후보 10개 밖). 11-24 D1 요청은 이 답으로 닫음.
- 같은 날 정정: 리만가설 편은 채널 밖 시험작 → 채널 공개 대상에서 뺌(`projects/20261125-curiosity-riemann/REPORT.md` 맨 위).
- 이번 편에서 피할 것 3개
  1. '품절 임박' 편과 겹치는 것 (희소성·쇼핑) → 이번 편은 물건이 아니라 '남의 삶과의 비교'. 쇼핑 포모는 다루지 않음.
  2. 지식 나열·연구 해설 (판테온 v1, 의지력 v1~v15) → 지우의 금요일 밤이 줄기, 연구는 그 밤을 다시 읽는 근거, 장마다 결론 한 문장(04 §0-8).
  3. 'SNS 끊으세요' 훈계 결말 → 2026 재현 실패까지 보여 주고, 결말은 지우의 메시지 한 통.

## 단계
| 단계 | 상태 |
|---|---|
| D1 주제 | 사용자 지정 (11-26) |
| S2 조사 | `01_research/factsheet.md`(자료 지도 A1~D2·해석의 지도·쓰지 않는 것), `sources.md`, `audience.md`(인식 지도). 원문 확인 ✅: Przybylski 2013, Whillans 2017, APS 2026 재현 보도 / ⚠️: McGinnis 2004 칼럼, Deri 2017(원문 열람 실패), Hunt 2018(보도로 교차) |
| S3 의도 | `02_script/intent.md` (생활·사회 트렌드형, 지우의 행동을 따라가는 흐름, 기억할 장면 = 식당 창과 기숙사 방) |
| S4 대본 | `02_script/script_v1.md` (약 3,600자·10분) · 근거 검수 `02_script/script_review.md` |
| D2 대본 | 사용자 "우선은 제작하고 나서 검수할게요" → 완성본 검수와 합침 |

## 혼자 판단한 것
- 각도: '포모 = 보이는 장면만 세는 착각' (핵심 근거 Whillans 2017 신입생 1,099명). 쇼핑·주식 포모는 '지금의 고리' 한 줄로만.
- 막힌 곳: PubMed(쿠키), Psychology Today(봇 확인), CBC(403) — 우회하지 않음. Deri 2017 은 원문을 못 열어 대본에 숫자 없이 한 줄씩만.

## 검사 (`check --upto G4`)
- G1·G3·G4 의 대본 단계 MUST 는 통과. 남은 ❌ 두 개는 장면 기획(S5) 때 생기는 파일의 몫: G2 '자료 화면 credit·url'(04_assets 없음), G4 'core_message·question·logic'(hybrid.json 없음). D2 결정 뒤 S5 에서 채웁니다.
- 판단 티어 최종 점검(필수 5·선택 3) 반영 — 원문과 다르던 '첫 학기'(실제 2월), 평균 논리, 상관을 원인처럼 쓴 말투, 재현 연구 인원 등.
- ⚠️ 렌더 전 원문 대조 남음: McGinnis 2004 칼럼, Deri 2017 초록, Hunt 2018 포모 결과.

## 2026-11-26 제작 (S5 → S7 → S8, 사용자: "우선은 제작하고 나서 검수할게요")
| 단계 | 상태 |
|---|---|
| S5 장면 | `02_script/make_spec.py` → `fomo.json` (44박자), 연출 결정 `hybrid.json` direction · `DIRECTION_LOG.md` |
| 원화 | 30칸 한 칸씩 — 지우 11칸은 품절 임박 편의 승인된 침실 칸 + 지우 기준판 조각에서 고쳐 그림(`E:/ytflow-local/fix-jiwoo/fix_frames.py`), 지우 없는 19칸은 잼 편 tasting.png + 커닝 편 고친 칸 참조(`E:/ytflow-local/fomo/gen_other.py`). Codex 내장 이미지 생성(ChatGPT 구독). 더 귀여운 쪽으로 간 2칸(타자·답장)과 생각 풍선 속 동기들이 지우를 닮은 1칸은 다시 그림. Drive `영상/20261126-curiosity-fomo/art/` |
| 증거 화면 | Przybylski 2013·Whillans 2017 논문 첫 쪽 (`02_script/make_evidence.py`) |
| S7 렌더 | Drive `…/05_edit/fomo_v1.mp4` (10:43), edge-tts 초안, 배경음 없음. 프레임 71장 확인 → 고친 뒤 다시 렌더 |
| 싱크 | 중앙값 0.26초 · 0.5초 안 98.8% · 화면−소리 0.01초 (sync-qa 판정 통과, ffprobe 길이 해석 오류는 감싸서 우회 — 코드 미수정) |
| S8 포장 | 제목 3·설명란·태그 `05_edit/youtube.md`, 썸네일 A/B/C(`thumbnail_qa.json`), 보관 기록 `drive_archive.json` |
| D4 | **사용자 검수 기다림** (대본 + 완성본) — `inbox/decisions/20261126-20261126-curiosity-fomo-D4.md` |

- `check` MUST 남은 2개: G6 레이아웃(이 렌더러는 hybrid 의 layout_qa 를 만들지 않음 — 프레임 직접 확인으로 대신), G6 싱크 기준(중앙값 0.2초 이하) — 유행 20년 편(공개됨)과 같은 상태.
- 매뉴얼과 다르게 한 것: 04 §0-7 '인물 칸 모음은 렌더 전에 사용자 통과' — 사용자 지시("제작하고 나서 검수")로 렌더 뒤 검수에 함께 냄(`art/jiwoo_check.jpg`).
- ⚠️ 원문 대조 남음: McGinnis 2004 칼럼, Deri 2017 초록, Hunt 2018 포모 결과 — 확인되지 않으면 해당 문장을 빼고 다시 렌더.

다시 만들기 (02_script 에서):
```
python beats.py script_v1.md beats.json && python make_spec.py
BEATS=beats.json python full_voice.py <TTS 폴더>
python make_evidence.py <PDF 폴더> <조각 폴더>
SPEC=fomo.json OVERLAY=fomo_overlay.html TIMELINE=fomo_timeline.json python render_full.py <TTS 폴더> <조각 폴더> <작업 폴더> <출력.mp4> 6
python thumbnails.py <조각 폴더> <출력 폴더>
```
