---
from: claude-code
type: curiosity-build
project: 20261120-curiosity-whitebear-v2
branch: ccr-8d1b9648-0fm4oq
after: 20261120-2327-art-whitebear.md
status: done
---

흰 곰 편 v4(약 9분 25초) 완성 영상 자동 빌드 — 원화 할 일(`20261120-2327-art-whitebear.md`)이 done 이 되면 PC 일꾼이 시작합니다.
`python scripts/curiosity_build.py projects/20261120-curiosity-whitebear-v2` (설정 `02_script/build.json`):
원화 시트 9장(YTFLOW_DRIVE/영상/20261120-curiosity-whitebear-v2/art) → 논문 3쪽·루이스 캐럴 사진 받기 → 칸 자르기 → 목소리(ElevenLabs 채널 목소리, 키 없으면 초안) → 장면(ep_whitebear_v4.py) → 렌더 → Drive `영상/20261120-curiosity-whitebear-v2/05_edit/whitebear_v4.mp4` + 프레임 시트.

## PC 작업 결과 (2026-11-21)

- Drive `ytflow/영상/20261120-curiosity-whitebear-v2/05_edit/whitebear_v4.mp4` 및 `whitebear_v4_frames.jpg`를 만들었습니다. 9분 25초, 1920×1080, 30fps입니다. 동일 폴더에 썸네일 A/B/C가 있습니다.
- 음성 MP3가 작업 브랜치에 없어 v4 대본 114문장을 Edge TTS로 읽힌 검토본입니다. 모든 문장의 음성, 전체 영상 디코딩, 주요 장면의 자막 배치를 확인했습니다. [자막과 쪽지·논문 영역을 보정한 렌더 소스](https://github.com/LBIN8787/video-editing/commit/868c76345dc353468bc8904e32a882d3c210fe9c)
