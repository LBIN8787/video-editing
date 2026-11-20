---
from: claude-code
type: final-render
project: 20261120-curiosity-trend
status: pending
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
