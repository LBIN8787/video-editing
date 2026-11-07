# 11. 제작 플레이북 — 다음에도 똑같이 만드는 법 (하이브리드 롱폼 기준, 2026-11-07)

이 문서 하나만 따라 하면 Claude Code 든 Codex 든 같은 품질로 한 편을 만들고, 영상과 작업 기록을 보관할 수 있습니다.
실제 예: `projects/20261107-knowledge-스페인독감` (교양), `projects/20261106-hybrid-데이터센터` (경제).

## 0. 준비 (세션마다 한 번)
```bash
pip install -r requirements.txt && python scripts/install_tools.py   # 이미 있으면 건너뜀
```
- 클라우드 세션: edge-tts 는 프록시를 직접 안 읽음 → 코드가 `--proxy $HTTPS_PROXY` 를 자동으로 붙임.
- 렌더 도중 세션이 재시작돼도 파일은 남음 → 같은 명령을 다시 실행하면 **바뀐 장면만** 다시 렌더.

## 1. 주제 (교양 채널은 수요부터)
```bash
python -m ytflow demand --channel ch-knowledge      # → .cache/demand/<날짜>/summary.md
```
- `docs/10-knowledge-demand.md` 의 기준 6가지로 고르고 `channels/<채널>/queue.md` 에서 하나를 꺼냄.
- 질문 하나 → 답 하나 → 반전 하나를 한 줄씩 적어 보고, 못 적으면 주제를 바꿈.

## 2. 자료 화면 먼저 (소스 먼저)
```bash
python -m ytflow archive search "influenza 1918" "liberty loan parade"     # 사진
python -m ytflow archive search "world war 1918" --films                  # 영화
```
- 미국 의회도서관: 1930년 이전 발행물 = 퍼블릭 도메인, 사진은 'No known restrictions' 확인(`archive.loc_item`).
- 사진 → 영상: `archive.still_to_clip(jpg, mp4, 24)` (세로 사진은 흐린 배경 채움). 영화는 ffmpeg 로 글자 없는 구간만 자름.
- 자료 화면 파일: `projects/<p>/04_assets/footage/*.mp4` (커밋 안 함 → 보관은 6단계).
- 다른 날·장소의 화면이면 label 에 반드시 `자료 화면 · 날짜 · 장소`.

## 3. 조사 → 팩트시트 (`01_research/factsheet.md`)
- `prompts/script_knowledge.md` A절: 장면·원리·비교·규모·연결 5층. 숫자마다 1차 출처, ✅/⚠️/❌, '쓰지 않는 것' 목록.

## 4. 대본 (`02_script/hybrid.json`)
- 장면 type·필드: `prompts/script_hybrid.md` 표. 서술 규칙: `prompts/script_knowledge.md` B·C절.
- 인과 지도 칸은 2줄 × 4칸(x = 250/710/1170/1630, y = 400/720)에 둠. 화살표는 렌더러가 다른 칸을 피해 돌려 그림.
- 같은 type 연속 금지, 자료 화면 20~30초마다, 영상 8~10분.

## 4-1. 목소리 (영상 확정 후, 키 없이)
- 초안은 edge-tts(자동). 최종은 ElevenLabs: 커넥터/웹으로 장 단위 긴 음성 → `python -m ytflow voice-import <프로젝트> part1.mp3 part2.mp3` (docs/08-voice.md).
- 채널별 목소리는 `channels/<채널>/channel.yaml` 의 voice 에 적혀 있음.

## 5. 만들기와 점검
```bash
python -m ytflow hybrid <프로젝트>      # 음성 → 장면 렌더(병렬 3) → 이어 붙이기 → 자막 → 효과음 → 마스터링(final.mp4)
```
자동으로 지켜지는 것 (2026-11-07 고침):
| 문제 | 해결 |
|---|---|
| 자막이 목소리보다 빠르거나 늦음 | 박자마다 faster-whisper 로 **실제 말하는 시각**을 받아 자막 줄을 그 순간에 바꿈. 줄은 문장 끝·쉼표에서 끊음 |
| 끝으로 갈수록 화면이 소리보다 늦음 | 장면 길이를 30fps 프레임 격자에 맞춰 장면 영상 길이 = 음성 길이 |
| 화살표가 칸·글자를 가로지름 | 직선 → ㄱ자 → 줄 사이 빈 띠 순으로 다른 칸을 피하는 경로. 못 피하면 `04_assets/layout_qa.json` 에 기록 |
| 글자 대비 부족 | HyperFrames check → layout_qa.json, 영상·사진 위 메모엔 배경 띠 |
| 음량 | -14 LUFS, 실제 최대 -1.5 dBTP (`05_edit/delivery_check.json`) |
| 박자 음성이 다음 박자 자리에 들어가 한 줄씩 늦고 장면 마지막 문장이 빠짐 (2026-11-07 발견·수정) | 장면 음성 합치기에서 ffmpeg 입력 번호를 +1 (0번은 무음 바탕) |
| 렌더러가 장면 길이를 0.1초 단위로 올림 | 장면 영상의 실제 길이를 재서 음성·자막을 거기에 맞춤 |
| **싱크 최종 확인** | 끝에 `sync-qa` 자동 실행: 완성본 소리를 25초 창으로 받아써 자막 줄 시작과 실제 말 시작 차이를 잼 → `05_edit/sync_qa.json` (0.3초 이내 95% 이상 + 화면−소리 0.1초 이내면 통과) |

사람 눈 점검 (꼭):
```bash
# 장면마다 끝 프레임 한 장씩 → 4x4 시트로 보고, layout_qa.json 이 {} 인지 확인
```
- 겹침·잘림·자막 위치, 같은 화면 반복, 자료 화면 라벨을 봄. 고치면 같은 명령을 다시 → 바뀐 장면만 렌더.

## 6. 보관 (키 필요 없음)
```bash
python -m ytflow upload <프로젝트>             # GitHub Release 'video-<프로젝트>' 에 영상·자막·업로드 문구
python -m ytflow upload <프로젝트> --archive   # + 자료 화면 묶음(footage.zip)
```
- 원리: 임시 브랜치 `media/<프로젝트>` 로 push → `.github/workflows/media-release.yml` 이 릴리스에 붙이고 브랜치를 지움. git 자격 증명만 사용.
- 파일 하나 100MB 미만(넘으면 화질을 조금 낮춘 사본). 릴리스 파일은 하나 2GB 까지, 개수 제한 없음.
- 기록: `05_edit/release.json` (주소) — GitHub 에 커밋됨.
- 작업 기록(기획·팩트시트·대본·업로드 문구·이 문서)은 main 브랜치에 커밋 = **노하우 보관**.
- Google Drive: **키 없이** Apps Script 를 한 번 설치하면 릴리스가 15분 안에 Drive 채널 폴더로 자동 복사됨 (`docs/12-drive-sync.md`). 그 밖에: 작은 문서는 Drive 커넥터(10MB 이하, 키 없음)로, 영상은 `--to drive` (오래가는 rclone 토큰을 한 번 설정한 경우, docs/09-storage.md).

## 7. 마무리
- `channels/<채널>/episodes.md` 에 한 줄, `queue.md` 상태 바꿈.
- 사용자에게: 영상, 남은 일(목소리 ElevenLabs·확인 안 된 숫자), 릴리스 주소.
