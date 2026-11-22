# REPORT — 호기심 「유행은 왜 20년쯤 지나면 돌아올까」 (2026-11-23)

## S0 착수 메모
- 직전 편: 판테온(비공개 보관 — 주제·이야기의 재미, v1 "지식나열같아요").
- 이번 편에서 피할 것 3개: ① '20년 주기'를 법칙처럼 단정 ② 연구자·연도 나열 ③ 다음 유행 예측, 상표·로고.

## 단계
| 단계 | 상태 |
|---|---|
| D1 주제 | 통과 — 사용자 11-23 "둘 다 진행해줘 유행은 왜 20년쯤 지나면 돌아올까도 괜찮네" (우선순위 3) |
| S2 조사 | 완료 — `01_research/factsheet.md`(F1~F35)·`sources.md`(S1~S38)·`audience.md`(인식 지도) |
| S3 의도 | 완료 — `02_script/intent.md` |
| S4 대본 | 완료 — `02_script/script_v1.md`, 근거 검수 63줄(`_evidence_review_v1.md`) → 12건 반영, `script_review.md` |
| D2 대본 | **사용자 결정 기다림** — `inbox/decisions/20261123-20261123-curiosity-fashion20-D2.md` |

- 한 일: 위 산출물. `check --upto G4` 대본 단계 항목 통과(남은 MUST 2개는 S5 장면표 칸).
- 혼자 판단한 것: 통설과 원문이 어긋나는 곳(레이버의 표에서 20년 = '우스꽝스럽다')을 이야기의 꺾이는 곳으로 삼음. 크로버의 틀린 예측은 근거가 분명한 '치마 폭'으로 씀. D1 카드의 트리거 기사 둘(광택 가구·20년 전 신발)은 찾지 못해 `topic_brief.trigger` 에서 뺌.
- 막힌 것: 레이버 책 본문(인터넷 아카이브 대출 제한·검색 403), V&A·브리태니커 등 403 — 우회하지 않음. 표는 2차 자료 + TIME 1969 로만 확인(⚠️).


## 2026-11-23 정기 작업 (S5 마무리 → S7 렌더 → S8 포장 → D4 요청)
| 단계 | 상태 |
|---|---|
| S5 원화 | 완료 — GPT 12시트(mirror·study·today 는 `_r2`), Drive `영상/20261123-curiosity-fashion20/art/` |
| S7 렌더 | 완료 — Drive `영상/20261123-curiosity-fashion20/05_edit/fashion20_v1.mp4` (11:44, = final), edge-tts 초안 목소리, 배경음 없음. 프레임 46장 눈으로 확인(`fashion20_v1_frames_1·2.jpg`) |
| 자막 싱크 | sync-qa — 0.5초 안 96.0%·중앙값 0.26초·화면−소리 0.0초 (통과) (`05_edit/sync_qa.json`, `subs.ass` 는 v1 타임라인에서; ffprobe 길이 해석 오류는 감싸서 우회, 코드 미수정) |
| S8 포장 | 제목 3·설명란·태그 `05_edit/youtube.md`, 썸네일 A/B/C(Drive 같은 폴더, `thumbnail_qa.json`), 요약 `02_script/hybrid.json`, 보관 기록 `drive_archive.json` |
| D4 | **사용자 결정 기다림** — `inbox/decisions/20261123-20261123-curiosity-fashion20-D4.md` |

다시 만들기 (02_script 에서):
```
python beats.py script_v2.md beats.json && python make_spec.py
BEATS=beats.json python full_voice.py <TTS 폴더>
python cut_sheets.py <시트 폴더(_r2 가 있으면 그 판을 <시트>.png 로)> <조각 폴더>
python make_photos.py <kroeber.pdf(archive.org/download/jstor-660477/660477.pdf)> <조각 폴더>   # photo_ktitle·photo_kfig20
SPEC=fashion20.json OVERLAY=fashion20_overlay.html TIMELINE=fashion20_timeline.json python render_full.py <TTS 폴더> <조각 폴더> <작업 폴더> <출력.mp4> 6
python thumbnails.py <조각 폴더> <출력 폴더>
```
