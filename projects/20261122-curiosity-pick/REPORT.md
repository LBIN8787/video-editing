# REPORT — 호기심 「철근 하나 없는 1,900년 된 돔은 왜 아직 서 있을까?」 (2026-11-22, v2 최종 확인 대기)

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

## v2 영상 (2026-11-22 정기 작업) — D2 v2 통과("영상 한번 생성해주세요", 샘플 없이) → D4 요청
| 단계 | 상태 |
|---|---|
| S5 장면표 | `02_script/shotlist_v2.md`, 명세 `pantheon_v2.json` ← `make_spec_v2.py` ← `beats_v2.json`(41박자, `beats.py` 에 🎮 시청자 참여 박자 추가) |
| 원화 | 새 GPT 시트 4장(build1·build2·build3·lime — 지우가 짓는 과정, `art_sheets_v2.json`·`art_orders.md` v2 절) + v1 7장 재사용 → Drive `영상/20261122-curiosity-pick/art/` |
| 모션그래픽 | **돔 단면 도식 `MG.dome`**(실제 비율 1m=14px, `pantheon_v2_overlay.html`) — 같은 단면이 박자마다 고쳐 지어짐(크기 비교·누름/벌어짐·금·밑단 두께·어른 셋·계단 고리·돌 세 층·블록 탑·천장 홈·'전부 무거웠다면'·꼭대기 열림·비·배수구) |
| S7 렌더 | Drive `영상/20261122-curiosity-pick/05_edit/pantheon_v2.mp4` (11:04, edge-tts 초안, 배경음 없음). 프레임 확인 후 도식 글 2곳(버스·배수구)이 자막과 겹쳐 위로 옮겨 다시 렌더 |
| 자막 싱크 | sync-qa 통과 — 154/155줄, 0.3초 안 95.5%, 95% 0.30초, 화면−소리 -0.09초 (`05_edit/sync_qa.json`, `subs.ass` 는 v2 타임라인에서). 렌더러 `word_times` 를 difflib 글자 맞춤으로 바꿈(edge-tts 경계가 글자를 빠뜨리거나 겹쳐 박자 7·24 자막이 최대 2초 일렀음) |
| S8 포장 | 썸네일 v2 A/B/C(C 를 '철근 없이 / 지어 봤더니 쩍'으로), `05_edit/youtube.md` v2(챕터·제목 3번 교체) |
| D4 | **사용자 결정 기다림** — `inbox/decisions/20261122-20261122-curiosity-pick-D4v2.md` |

다시 만들기:
```
cd projects/20261122-curiosity-pick/02_script
python beats.py script_v2.md beats_v2.json && python make_spec_v2.py
BEATS=beats_v2.json python full_voice.py <TTS 폴더>
python cut_sheets.py "<YTFLOW_DRIVE>/영상/20261122-curiosity-pick/art" <조각 폴더>   # + photo_dome·photo_oculus.jpg (Commons Special:FilePath?width=1920 에서 잘라 냄)
SPEC=pantheon_v2.json OVERLAY=pantheon_v2_overlay.html TIMELINE=pantheon_v2_timeline.json python render_full.py <TTS 폴더> <조각 폴더> <작업 폴더> <출력.mp4> 6
python thumbnails.py <조각 폴더> <출력 폴더>
```
- 알아 둘 것: GPT 시트 두 칸(build1 왼쪽 위·build2 오른쪽 위)에 완성된 판테온 현관이 배경에 함께 그려짐(짓는 중인데 완성 건물이 보임) — 짧게 지나가는 칸이라 그대로 둠, 거슬리면 그 칸만 다시 그림.
- `check`: MUST 미통과 2개는 v1 과 같은 성격 — G6 레이아웃 QA 는 hybrid 렌더러 전용 기록(이 렌더러는 프레임을 눈으로 확인), G6 싱크 중앙값 0.26초(기준 0.2) — 측정 쉼 보정 차이로 v1(0.26)과 같음.
- 길이 11:04 로 v1(8:50)보다 김 — 짓는 과정 장(2~6장)이 늘어난 몫.
- 막힌 것: Wikimedia upload 서버 429 → Commons `Special:FilePath` 로 받음. `codex exec -i` 가 뒤 인자를 그림 경로로 먹어 프롬프트는 stdin 으로.

## v3 영상 (2026-11-22 정기 작업) — v2 D4 기각("지우의 이미지화풍이 너무달라서 확 깨") + 추가("인포그래픽 설명도 삽화로") → D4 요청
| 단계 | 상태 |
|---|---|
| 지우 화풍 | 지우 기준 그림 `art/jiwoo_ref.png`(v1 지우 네 칸) + v1 `dome.png` 만 참조로 build1·build2·build3·lime 다시 그림(`art/<시트>_v3.png`, 흰 곰 편 night.png 뺌). 지우 칸 모아 보기 `art/jiwoo_lineup_v3.jpg` 확인 |
| 설명 삽화 | 돔 단면 도식(MG.dome·블록 탑) 14박자 → 새 GPT 시트 plan1~4(지우가 그린 설계 스케치, `art_sheets_v3.json`·`art_orders.md` v3 절). 명세 `make_spec_v3.py` → `pantheon_v3.json`(대본·박자 = v2 그대로, 도식 박자 0) |
| S7 렌더 | Drive `영상/20261122-curiosity-pick/05_edit/pantheon_v3.mp4` (11:03, edge-tts 초안, 배경음 없음). 매뉴얼 v105 따라 오른쪽 위 사진 출처 상자 끔(`pantheon_v3_overlay.html`, 출처는 설명란). 설명 박자 프레임 확인 `pantheon_v3_sketch_frames.jpg` — 이름표·자막 겹침 없음 |
| 자막 싱크 | sync-qa 통과 — 155/155줄, 중앙값 0.26초·95% 0.35초, 화면−소리 -0.09초 (`subs.ass` 는 v3 타임라인에서; ffprobe 길이 해석 오류는 감싸서 우회, 코드 미수정) |
| S8 포장 | 썸네일 v3 A/B/C(`thumbnail_v3_*.png`), 제목·설명란은 v2 `youtube.md` 그대로 |
| D4 | **사용자 결정 기다림** — `inbox/decisions/20261122-20261122-curiosity-pick-D4v3.md` |

다시 만들기: v2 와 같고 `python make_spec_v3.py` → `SPEC=pantheon_v3.json OVERLAY=pantheon_v3_overlay.html TIMELINE=pantheon_v3_timeline.json python render_full.py …` (조각 폴더에는 build1·build2·build3·lime 을 `_v3` 시트에서, plan1~4 를 `plan<n>_v3.png` 에서 자름).

## v4 영상 (2026-11-22 정기 작업) — v3 D4 기각 + 바로잡음("되살리고 튀는 지우칸만 고쳐쥬세요") → D4 요청
| 단계 | 상태 |
|---|---|
| 되살림 | build1·build2·build3·lime 은 v2 시트(`art/<시트>.png`)로 되돌림, v1 시트 그대로. `jiwoo_ref.png`·`*_v3` 짓는 시트는 쓰지 않음 |
| 나란히 보기 | 지우 칸 전부를 `garage_tr`(주차장 지우)와 한 장에 → `art/jiwoo_lineup_v4.jpg` |
| 튀는 칸만 다시 | `dome_bl`(반실사 클로즈업)·`build2_bl`(만화풍 얼굴) 한 칸씩 새로(`art/dome_bl_v4.png`·`build2_bl_v4.png`), 설계 스케치 plan1~4 는 v3 시트를 고치기(구성 그대로, 지우만) → `art/plan<n>_v4.png`. 참조는 garage.png + 잼 편 tasting.png 만(Codex `$imagegen`, `-m gpt-6-sol`, 프롬프트 `art/*_v4.txt`) |
| 그대로 둔 칸 | build1_tr·build3_tl 은 고칠 후보였지만 나란히 보기에서 같은 화풍이라 v2 그대로 |
| S7 렌더 | Drive `영상/20261122-curiosity-pick/05_edit/pantheon_v4.mp4` (11:03, = final.mp4) — 타임라인이 v3 과 같아 자막 싱크(v3 sync-qa 통과)·subs.ass 그대로 유효. 명세·오버레이는 v3 그대로(`pantheon_v3.json`·`pantheon_v3_overlay.html`), 타임라인 `05_edit/pantheon_v4_timeline.json` |
| 바뀐 것 | `05_edit/pantheon_v4_changes.jpg`(전·후), 표는 `inbox/decisions/20261122-20261122-curiosity-pick-D4v4.md` |
| S8 포장 | 썸네일 v4 A/B/C(C 는 v2 build1_br 로 돌아감), 제목·설명란 그대로 |
| D4 | **사용자 결정 기다림** — `inbox/decisions/20261122-20261122-curiosity-pick-D4v4.md` |

다시 만들기 (조각 폴더):
```
# 시트 폴더에 garage dome end history lab rust struct build1 build2 build3 lime .png 와 plan<n>_v4.png → plan<n>.png
python cut_sheets.py <시트 폴더> <조각 폴더>
# dome_bl_v4.png·build2_bl_v4.png 는 16:9 가운데 자르기 → 1920×1080 으로 <조각 폴더>/dome_bl.jpg·build2_bl.jpg 덮어쓰기
# photo_dome·photo_oculus: Commons "Oculus, Dome, Pantheon (31565206097).jpg" ?width=1920 (1920×2560) 에서 오쿨루스 중심(985,1184) 기준 1920×1080 / 960×540→확대
BEATS=beats_v2.json python full_voice.py <TTS 폴더>
SPEC=pantheon_v3.json OVERLAY=pantheon_v3_overlay.html TIMELINE=pantheon_v4_timeline.json python render_full.py <TTS 폴더> <조각 폴더> <작업 폴더> <출력.mp4> 6
```

## v5 화풍 샘플 (2026-11-22 정기 작업) — v4 D4 기각("거의 전구간이 전부 이전 영상들 화풍이랑 달라 실사풍에 눈은 작고 완전 다른 화풍과 캐릭터가됐어") → 샘플만, D3 요청
| 단계 | 상태 |
|---|---|
| 진단 | 기준으로 삼던 `garage.png`(v1 주차장 지우)부터 이전 영상 화풍이 아님 → 판테온 편 기존 그림은 어떤 것도 참조로 쓰지 않음 |
| 샘플 | 참조 = 흰 곰 편 `night.png` + 잼 편 `tasting.png` 두 장만. 4칸 시트 1장(주차장 녹물·판테온 올려다봄·공사장 돔 가리킴·설계 스케치 설명) → Drive `art/style_sample_v5.png`, 프롬프트 `art/style_sample_v5.txt` (Codex `$imagegen`, `-m gpt-6-sol`, 한 번에 그림) |
| 나란히 보기 | `art/style_sample_v5_compare.jpg` — 둥근 얼굴·큰 눈·단발·굵은 선·평면 채색이 이전 영상과 같은 계열. 다른 점: 조금 더 어려 보임, 머리색이 짙은 갈색 |
| 렌더 | 하지 않음 (샘플 통과 뒤) |
| D3 | **사용자 결정 기다림** — `inbox/decisions/20261122-20261122-curiosity-pick-D3v5.md` |

통과하면: 지우가 나오는 모든 시트 + 사람·배경 시트 전부를 같은 참조 두 장 + 이 샘플 프롬프트의 화풍 문단으로 다시 그려 v5 렌더(대본 v2·박자·자막·설명 삽화 방향·실제 사진 그대로).
