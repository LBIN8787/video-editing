---
from: claude-code
type: art-draw
project: 20261120-curiosity-trend
status: pending
---

호기심 '넘길수록 지루해진다' 편 v3 원화 5장을 PC 의 Codex 내장 imagegen 으로 그려 주세요 (잼 편과 같은 방법·화풍). 클라우드에는 Codex 로그인이 없고, ElevenLabs 로는 그리지 않습니다(2026-11-20 사용자).

```
git pull
# projects/20261120-curiosity-trend/02_script/art_orders.md 의 다섯 시트(night1·room·lab·night2·ending)를 그대로 생성
# 화풍 참고: YTFLOW_DRIVE/영상/20261119-curiosity-choice-blindness/art/tasting.png
# 저장: YTFLOW_DRIVE/영상/20261120-curiosity-trend/art/<이름>.png  (2×2 시트, 칸 16:9)
```

- 그림은 git 에 넣지 않습니다(Drive 로 동기화). 끝나면 이 파일 status 를 done 으로 바꾸고, 그린 시트 이름·Drive 경로·실패한 칸을 아래에 적어 main 에 푸시해 주세요.
- 클라우드 세션은 Drive 에서 시트를 받아(시트당 3MB 를 넘으면 2048px 이하 JPEG 로 저장해 주세요) 칸을 잘라 렌더합니다.
