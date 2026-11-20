---
from: claude-code
type: final-render
project: 20261120-curiosity-trend
status: failed
---

넘기기 편 v3 를 **ElevenLabs 최종 목소리**로 다시 렌더해 주세요 (사용자 2026-11-20: "ElevenLabs 목소리로 최종 렌더해줘").
목소리는 클라우드에서 만들어 GitHub Release 에 올렸습니다 — 원화는 PC·Drive 에만 있어(클라우드 Drive 커넥터로는 PC 동기화 파일이 보이지 않음) 렌더는 PC 에서.

```
git pull
gh release download video-20261120-curiosity-trend -p v3_voice_elevenlabs.zip -D <작업>/voice   # 또는 GitHub 웹에서 받기
unzip <작업>/voice/v3_voice_elevenlabs.zip -d <작업>/voice/el
# 장면별 s<장면>_0.mp3 (30문단, 5분 38초, Nobel Butler YBRudLRm83BV5Mazcr42 · eleven_v4 · ko, 대본 v3 와 글자 일치 확인)
cd projects/20261120-curiosity-trend/02_script
python build_v3.py <ARTDIR>
ARTDIR=<ARTDIR> python render_v3.py <클립 폴더> <작업>/voice/el none <작업>/final <작업>/final_v3.mp4
```

- 끝나면 프레임 확인 → `05_edit/youtube.md` 챕터를 새 `timeline.json` 시각으로 → 최종 MP4 를 Drive `영상/20261120-curiosity-trend/05_edit/final_v3.mp4` 로.
- D4(사용자 최종 승인) 뒤 '한겹 더 보면' 일부 공개 업로드 (HANDOFF.md §다시 렌더하고 업로드할 때).
- 이 파일 status 를 done 으로, 결과(길이·Drive 경로)를 아래에 적어 main 에 푸시.

## 추가 (2026-11-21, 사용자: "영상 유튜브에 일부공개 미리 올려줘 내가 그거로 보게")
렌더가 끝나면 **바로 '한겹 더 보면' 채널에 일부 공개(unlisted)로 미리 올려** 사용자가 유튜브에서 보게 해 주세요 (최종 승인 전 검토용).
- ElevenLabs 판 렌더가 아직이면, 이미 있는 `v3_art_review.mp4`(초안 목소리)라도 먼저 올리고 나중에 바꿔도 됩니다.
- 방법 ①(원본 화질): PC 에 YouTube 권한이 있으면 `final.mp4` 를 `05_edit/` 에 두고 `python -m ytflow yt-publish projects/20261120-curiosity-trend --via here --privacy unlisted`
- 방법 ②: `python -m ytflow upload projects/20261120-curiosity-trend --to github` → `python -m ytflow yt-publish projects/20261120-curiosity-trend --privacy unlisted` (GitHub Actions, Release 는 100MB 아래로 다시 압축됨)
- `channels/ch-knowledge/channel.yaml` 의 `expected_channel: "한겹 더 보면"` — 권한이 다른 채널이면 올리지 않고 멈춤(`youtube_publish.json` 의 `blocked`). 그때는 `scripts/youtube_auth.py` 로 '한겹 더 보면' 권한을 받아야 함.
- 올린 주소를 `05_edit/youtube_publish.json` 과 이 파일 아래에 적어 main 에 푸시.

> pc-worker 2026-11-21 01:13: 1번째 시도 시작 (브랜치 main)

> pc-worker 2026-11-21 01:14: 1번째 시도가 끝나지 않음 (종료 코드 1) — 다음 차례에 다시

> pc-worker 2026-11-21 01:23: 3번째 시도 시작 (브랜치 main)

> pc-worker 2026-11-21 01:23: 3번 시도했지만 끝나지 않음 (종료 코드 1) — 로그: G:\내 드라이브\ytflow\_local\pc-worker\pc_worker.log
