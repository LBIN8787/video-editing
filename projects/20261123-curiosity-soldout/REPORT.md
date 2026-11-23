# REPORT — 호기심 「'품절 임박'을 보면 왜 손이 먼저 나갈까」 (2026-11-23)

## S0 착수 메모
- 직전 편: 판테온(비공개 보관 — "주제가 애매 … 이야기를 풀어나가는게 재밌냐 하면 잘 모르겠구요", v1 "지식나열같아요"), 의지력·흰 곰(심리 실험 문법).
- 이번 편에서 피할 것 3개: ① 실험 소개가 줄기가 되는 구성(D1 카드의 약점) ② 사실 항목 차례로 들려주기 ③ 구매 권유·비권유, 특정 쇼핑몰 비난.

## 단계
| 단계 | 상태 |
|---|---|
| D1 주제 | 통과 — 사용자 11-23 "둘 다 진행해줘" (우선순위 1, 블프 11-27 전 공개 목표) |
| S2 조사 | 완료 — `01_research/factsheet.md`(F1~F36)·`sources.md`(S1~S29)·`audience.md`(인식 지도) |
| S3 의도 | 완료 — `02_script/intent.md` |
| S4 대본 | 완료 — `02_script/script_v1.md`, 근거 검수 53줄(`_evidence_review_v1.md`) → 8건 반영, `script_review.md` |
| D2 대본 | **사용자 결정 기다림** — `inbox/decisions/20261123-20261123-curiosity-soldout-D2.md` |

- 한 일: 위 산출물. `check --upto G4` 대본 단계 항목 통과(남은 MUST 2개는 S5 장면표 칸).
- 혼자 판단한 것: 지우 화면의 문구를 '27명이 보는 중'에서 '방금 2명이 구매'로 정함(실험에서 효과가 확인된 것은 '남들이 이미 가져가서 줄어듦'). 결말은 '샀다/안 샀다' 없이 열어 둠. 영국 조사는 확인된 94%만 씀.
- 막힌 것: 미국 PMC(봇 확인)·미시간대 저장소(403) — 우회하지 않음. '하루 미루면 덜 산다' 연구는 원문을 못 열어 대본에 쓰지 않음. 같은 소재 한국어 영상 조회수·검색 자동완성 미확인.


## 2026-11-23 정기 작업 (S5 마무리 → S7 렌더 → S8 포장 → D4 요청)
| 단계 | 상태 |
|---|---|
| S5 원화 | 완료 — GPT room1~6·cookie1~4·office 11시트(base 판 — `_r1` 은 처음 판이라 쓰지 않음), Drive `영상/20261123-curiosity-soldout/art/` |
| S7 렌더 | 완료 — Drive `영상/20261123-curiosity-soldout/05_edit/soldout_v1.mp4` (10:37, = final), edge-tts 초안 목소리, 배경음 없음. 프레임 44장 눈으로 확인(`soldout_v1_frames_1·2.jpg`) |
| 자막 싱크 | sync-qa — 0.5초 안 98.8%·중앙값 0.26초·화면−소리 −0.13초 (`05_edit/sync_qa.json`, `subs.ass` 는 v1 타임라인에서; ffprobe 길이 해석 오류는 감싸서 우회, 코드 미수정) |
| S8 포장 | 제목 3·설명란·태그 `05_edit/youtube.md`, 썸네일 A/B/C(Drive 같은 폴더, `thumbnail_qa.json`), 요약 `02_script/hybrid.json`, 보관 기록 `drive_archive.json` |
| D4 | **사용자 결정 기다림** — `inbox/decisions/20261123-20261123-curiosity-soldout-D4.md` |

다시 만들기 (02_script 에서):
```
python beats.py script_v2.md beats.json && python make_spec.py
BEATS=beats.json python full_voice.py <TTS 폴더>
python cut_sheets.py <시트 폴더(_r2 가 있으면 그 판을 <시트>.png 로)> <조각 폴더>
python make_evidence.py <PDF 폴더> <조각 폴더>  # worchel·barton·mathur PDF (sources.md S1·S2·S5)
python detect_screens.py <조각 폴더> room1_bl room1_br room2_tl room2_tr room2_br room5_bl room6_tr   # 가림막 mask_*.png (screens.json 은 git 판 그대로)
SPEC=soldout.json OVERLAY=soldout_overlay.html TIMELINE=soldout_timeline.json python render_full.py <TTS 폴더> <조각 폴더> <작업 폴더> <출력.mp4> 6
python thumbnails.py <조각 폴더> <출력 폴더>
```
