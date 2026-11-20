---
from: claude-code
type: curiosity-build
project: 20261120-curiosity-whitebear-v2
branch: ccr-8d1b9648-0fm4oq
status: pending
---

흰 곰 편 v4 다시 렌더 — **ElevenLabs 채널 목소리**로 (2026-11-20 사용자: "목소리 파일 드라이브로 넘겨서 다시 렌더해줘" → "권장으로").
지난 빌드(`20261120-2328-build-whitebear.md`)는 PC 에 목소리 파일이 없어 edge-tts 초안으로 만들어졌습니다.

- 목소리: 클라우드에서 만든 ElevenLabs 목소리(558.79초)를 Drive 연결 한도 때문에 세 조각으로 올림 → `YTFLOW_DRIVE/cache/whitebear_v4_voice_elevenlabs.mp3.part0~2`. `curiosity_build.py` 가 이어 붙여 sha256 을 확인하고 `03_voice/v4/voice.mp3` 로 씀 (`build.json` 의 `voice_parts`).
- 장면: 작업 브랜치의 최신 `ep_whitebear_v4.py` — PC 보정(쪽지·논문을 자막 위로, 868c763)과 클라우드 수정(색 빼기 검은 깜빡임, 1장 끝 빈 화면)을 합친 판.
- 결과: Drive `영상/20261120-curiosity-whitebear-v2/05_edit/whitebear_v4_elevenlabs.mp4` + 프레임 시트. 초안판 `whitebear_v4.mp4` 는 그대로 둠.
- 조각이 없다는 오류면 Drive 동기화를 기다렸다가 다음 차례에 다시 (일꾼이 2번까지 시도).
