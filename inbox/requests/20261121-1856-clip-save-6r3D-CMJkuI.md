---
from: claude-code
type: browser-task
url: https://www.youtube.com/watch?v=6r3D-CMJkuI
status: pending
title: 드러켄밀러 TomorrowX 대담 — 네 구간 영상 파일로 받아 Drive 에 올리기
---

지난 요청(`done/20261121-1645-yt-times-6r3D-CMJkuI.md`)에서 찾아 주신 네 구간을 **영상 파일(mp4, 소리 포함)**로 받아 주세요. 클라우드 세션은 유튜브 봇 확인 때문에 받지 못하고, 사용자 PC 폴더도 지금 클라우드에 연결되지 않습니다. iConnections(행사 주최) 공식 채널 영상이며, 영상 속 인용에 씁니다.

| 파일 이름 | 구간 (시작 ~ 끝) | 내용 |
|---|---|---|
| `druck_qa.mp4` | 1:58.5 ~ 2:11.0 | 진행자 질문 "So, how much of that portfolio do you own today?" + 답 "Basically, almost none." |
| `druck_notlose.mp4` | 8:10.5 ~ 8:16.8 | "We're trying to not lose money, as opposed to make money." |
| `druck_break.mp4` | 9:15.5 ~ 9:22.8 | "so I'm just taking a break which could last 2 days or 6 months." |
| `druck_2027.mp4` | 12:00.5 ~ 12:07.8 | "…the second half of 27 could be economically disappointing" |

- 올릴 곳: 비공개 Google Drive `ytflow/cache/clips/20261120-market-deep-druckenmiller/` (없으면 만들어 주세요). 공개 저장소에는 올리지 않습니다.
- 가능하면 1080p(최소 720p), 소리 포함. 구간 앞뒤로 0.5초 정도 여유가 있어도 괜찮습니다.
- 받는 도구는 무엇이든 괜찮습니다(PC 에서 `python -m ytflow clip-fetch 20261120-market-deep-druckenmiller` 를 돌릴 수 있으면 그게 가장 정확합니다 — 같은 네 구간을 받아 `04_assets/clip_manifest.json` 을 만들고 Drive 에 올립니다).

결과: 받은 파일 이름·길이·해상도·Drive 위치, 받지 못한 것은 이유.
