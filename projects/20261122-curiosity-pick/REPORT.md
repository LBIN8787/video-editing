# REPORT — 호기심 「철근 하나 없는 1,900년 된 돔은 왜 아직 서 있을까?」 (2026-11-22, 최종 확인 대기)

## S0 착수 메모 (2026-11-22)
- 채널이 '분야를 가리지 않는 호기심 이야기'로 바뀐 뒤 첫 편(channel.yaml, 2026-11-22). 직전 편: 의지력(통과·11-22 18:00 공개 예약), 흰 곰(올림·비공개).
- 직전 기각 사유: 의지력 v84 "좋은 연구 해설을 보여주는 자료에 가깝습니다 … 이야기라기보단 연구같아요", 넘기기 편 "주제 자체를 최근 시사나 유행을 바탕으로".
- 이번 편에서 피할 것 3개: ① 연구 해설 자료처럼 되는 것(이야기가 메인, 근거는 덧붙임 — 04 §0-8) ② 시사 고리 없는 주제(01 §3-1) ③ 심리 연구 연속(분야 순환).

## 단계
| 단계 | 상태 |
|---|---|
| S1 신호·주제 카드 | 완료 — `01_research/topic_card.md` (A 블랙프라이데이 / B 판테온 / C 리처드 3세) |
| D1 주제 | 결정 — B 판테온 돔 (사용자: "B로 한번 대본작성해주세요") |
| S2 조사 | 완료 — `01_research/factsheet.md`(F1~F17), `audience.md`, topic_brief 를 B 로 갱신(훅: 주차장 녹물) |
| S3·S4 의도·대본 | 완료 — `02_script/intent.md`, `script_v1.md`, 대본만 담은 `hybrid.json`(화면 미정) |
| check --upto G4 | MUST 실패 2개는 예정된 것: G2 자료 화면(S5 전) · G4 사용자 대본 검토(D2 전) |
| D2 대본 | 통과 — 사용자: "한번 영상으로 생성해주세요" (D3 샘플 없이 완성 영상까지) |
| S5 장면표·원화 | 완료 — `02_script/shotlist.md`, 명세 `pantheon.json`(`make_spec.py`), 원화 GPT 7시트(Codex `$imagegen`, `art_orders.md`·`art_sheets.json`, Drive `영상/20261122-curiosity-pick/art/`) |
| S7 렌더 | 완료 — Drive `영상/20261122-curiosity-pick/05_edit/pantheon_v1.mp4` (8:50, 35박자, edge-tts 초안 목소리, 배경음 없음). 렌더러는 의지력 편 것을 그대로(`render_full.py` + `pantheon_overlay.html`) |
| S8 포장 | 제목 3·썸네일 A/B/C(`thumbnails.py`)·설명란 `05_edit/youtube.md` (yt-pack 은 hybrid 타임라인 전용이라 손으로) · 근거 검수표 `02_script/script_review.md` |
| 자막 싱크 | sync-qa 통과 — 126/126줄, 어긋남 중앙값 0.26초·95% 0.43초, 화면−소리 -0.02초 (`05_edit/sync_qa.json`; ytflow 의 ffprobe 길이 해석 오류는 감싸서 우회 — 코드 미수정) |
| D4 최종 | **사용자 결정 기다림** — `inbox/decisions/20261122-20261122-curiosity-pick-D4.md` |

## 다시 만들기 (2026-11-22)
```
cd projects/20261122-curiosity-pick/02_script
python beats.py script_v1.md beats.json && python make_spec.py
BEATS=beats.json python full_voice.py <TTS 폴더>                       # 초안 목소리(edge-tts, 단어 시각)
python cut_sheets.py "<YTFLOW_DRIVE>/영상/20261122-curiosity-pick/art" <조각 폴더>   # + photo_dome·photo_oculus.jpg (Commons 사진, Sonse CC BY 2.0)
SPEC=pantheon.json OVERLAY=pantheon_overlay.html TIMELINE=pantheon_timeline.json python render_full.py <TTS 폴더> <조각 폴더> <작업 폴더> <출력.mp4> 6
python thumbnails.py <조각 폴더> <출력 폴더>
```
- 막힌 것: Codex 기본 모델(gpt-6.2-sol)이 ChatGPT 계정에서 거부 → `-m gpt-6-sol` 로 그림. Codex 쪽 저장 명령이 막혀 그림은 `~/.codex/generated_images` 에서 옮김. Wikimedia 이미지 서버가 한동안 요청 제한(429) — 잠시 뒤 받음. `curiosity_build.py` 는 main 에 없음(흰 곰 작업 브랜치에만) → 의지력 편 렌더러를 씀.

## v2 대본 (2026-11-22 정기 작업) — D4 기각 반영
- 기각 원문: "지식나열같아요 체감이 안된다 … 쇼츠로 건물짓는 영상 … 같이 이야기를 구경하고 공감 참여 이해를 유도"
- `02_script/script_v2.md`: 지우가 철근 없이 돔을 직접 지어 보는 과정(고르게 붓기 실패 → 아래 두껍게·고리 → 가벼운 돌·홈 → 꼭대기 비우기 → 금이 가도 섬 → 철근의 녹과 비교 → 하얀 덩어리 실험). 팩트시트 F18(돔의 힘·계단 고리·균열 위치 ⚠️)·F19(크기 비교 계산) 추가, `intent.md`·`script_review.md` v2 절.
- `check --upto G4` MUST 통과(장면 파일 hybrid.json 은 아직 v1 — D2 통과 뒤 S5 에서 v2 로 새로).
- **D2 대기:** `inbox/decisions/20261122-20261122-curiosity-pick-D2v2.md`
