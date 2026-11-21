---
from: claude-code
type: browser-task
url: https://www.youtube.com/watch?v=6r3D-CMJkuI
status: done
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

## 결과

**네 클립 모두 받지 못했습니다.** 비공개 Drive `ytflow/cache/clips/20261120-market-deep-druckenmiller/` 에는 올릴 파일이 없어 아무것도 올리지 않았습니다.

| 파일 이름 | 구간 | 결과 |
|---|---|---|
| `druck_qa.mp4` | 1:58.5 ~ 2:11.0 | **미확보** |
| `druck_notlose.mp4` | 8:10.5 ~ 8:16.8 | **미확보** |
| `druck_break.mp4` | 9:15.5 ~ 9:22.8 | **미확보** |
| `druck_2027.mp4` | 12:00.5 ~ 12:07.8 | **미확보** |

### 사유

1. **`yt_dlp` 실행이 유튜브 봇 확인으로 차단** — 2026-11-21 19:00 KST, `python3 -m yt_dlp --simulate "https://www.youtube.com/watch?v=6r3D-CMJkuI"` → `ERROR: [youtube] 6r3D-CMJkuI: Sign in to confirm you're not a bot`. yt-dlp 2026.10.26. 플레이어 클라이언트를 `tv`·`mweb`·`web_safari`·`web_embedded`·`ios`·`android_vr` 로 바꿔도 모두 같은 응답이었습니다. 클라우드에서 쿠키·로그인으로 봇 확인을 우회하는 것은 하지 않았습니다.
2. **`ffmpeg`/`ffprobe` 미설치** — PATH에 없어 구간 자르기·병합과 해상도 확인을 할 수 없습니다(`imageio-ffmpeg` 번들 바이너리만 존재, CLI 없음).
3. **원격 브라우저로도 영상 파일 저장 불가** — 페이지는 정상 재생되지만 플레이어는 스트림만 재생할 뿐 mp4 파일로 내려받는 경로가 없습니다. 게다가 이 브라우저 세션은 음소거·오디오 출력 장치가 없는 헤드리스 환경입니다.

### 다음에 필요한 것

사용자 PC에서 `python -m ytflow clip-fetch 20261120-market-deep-druckenmiller` 실행이 필요합니다. 같은 네 구간을 받아 `04_assets/clip_manifest.json` 을 만들고 Drive에 올리는 경로입니다. 참고로 yt-dlp 오류 메시지 자체가 `--cookies-from-browser` 사용을 안내하고 있으니, PC에서도 같은 봇 확인이 나오면 사용자 본인 브라우저 세션으로 실행하는 방법을 검토해야 합니다.
