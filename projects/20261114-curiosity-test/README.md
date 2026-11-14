# 20261114-curiosity-test — 호기심 '이야기 그림판' 스타일 시험편 (약 46초)

호기심 채널(ch-knowledge)의 **이야기 그림판(story-board)** 연출이 클라우드(리눅스 컨테이너, node·chromium 없음)에서
끝까지 렌더되는지 확인하는 시험편입니다. 유튜브 업로드 없음, `main` 무관(`exp/cloud-render-test`).

- 주제: **비행기 창 아래 작은 구멍(bleed hole)은 왜 뚫려 있을까** — 사실은 FAA AC 25.775-1 · GKN/Boeing 엔지니어 인터뷰로 확인 (`01_research/factsheet.md`)
- 그림: **`build/board.py` — Pillow 벡터 그림판**(3840×2160 종이, 카메라 이동, 선이 그려지는 등장). `ytflow/stages/story.py`(HyperFrames → node·chromium)는 이 환경에서 돌지 않아 같은 문법을 Pillow 로 옮겼습니다.
- 목소리: `build/tts_timed.py` — edge-tts(ko-KR-InJoonNeural, +8%) + 무음 정리 + **받아쓰기로 단어 시각** 측정
- 그림 타이밍: `02_script/board.json` 의 `word` → 그 낱말을 말하는 순간 등장 (`03_voice/timings.json`)
- 자막: `ytflow stage subtitles` 가 만든 스타일 그대로, 줄 시각만 `build/subs_timed.py` 로 단어 시각에 다시 박음
- 마스터링: `ytflow stage assemble` → `finish.master` (ffmpeg-skill loudness -14 LUFS · check.py · look.py)

## 다시 만들기
```bash
export PATH="$PWD/../../bin:$PATH"        # 저장소 밖 ffmpeg/ffprobe (없으면 시스템 ffmpeg)
python projects/20261114-curiosity-test/build/tts_timed.py     # mp3 + clean wav + durations + 단어 시각
python projects/20261114-curiosity-test/build/board.py         # 장면 12개 → 04_assets/scene_XXX_anim.mp4 (장면당 약 20초)
python -m ytflow stage projects/20261114-curiosity-test subtitles
python projects/20261114-curiosity-test/build/subs_timed.py    # 자막 시각을 말한 시각으로
python -m ytflow stage projects/20261114-curiosity-test assemble   # draft → final.mp4 · delivery_check.json · final_sheet.png
python projects/20261114-curiosity-test/build/sync_check.py    # 받아쓰기로 싱크 실측 → sync_qa.json
```
`assets` 단계는 일부러 건너뜁니다 — 그 단계는 `scene_XXX_anim.mp4` 를 지우고 종이 카드로 바꿔 놓기 때문입니다.
그림을 한 장면만 다시 그리려면 `python .../build/board.py --scene 7`, 정지 프레임은 `--still 7:2.4`(→ `05_edit/stills/`).

## 결과 (2026-11-14 · 리눅스 컨테이너)
- 46.29초 · 1920×1080 · 30fps · h264 + AAC 48kHz 2ch · **-14.0 LUFS** · true peak -2.3 dBTP · 11.2MB
- `delivery_check.json` PASS 11 / WARN 1(자막을 화면에 구워 별도 트랙 없음 — 의도) · `ytflow qa` 겹침 없음
- `sync_qa.json`: 22줄 · 중앙값 0.05초 · 0.5초 이내 86%
- 글자 깨짐(□) 없음 — 저장소 동봉 나눔 폰트만 사용
