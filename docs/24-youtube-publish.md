# 24. 유튜브 올리기·관리 자동화 (2026-11-13)

> 사용자 요청: "유튜브 관리까지 — 업로드랑 설정, 더보기(설명란) 세팅 등등".
> 방법: **공식 YouTube Data API v3** (`ytflow/stages/ytpublish.py`). 브라우저 자동 조작(Studio 화면을 로봇이 누르기)은 쓰지 않는다 — 화면이 바뀌면 깨지고 약관상 위험.

## 0. 무엇이 자동인가
| 항목 | 자동 | 어디서 정함 |
|---|---|---|
| 영상 업로드 | ✅ | `05_edit/final.mp4` (GitHub Release 에서 받음) |
| 제목 | ✅ 1번 후보 | `05_edit/youtube.md` (yt-pack) |
| 설명란(더보기): 요약·기준 시각·챕터·출처·면책·해시태그 | ✅ | `youtube.md` 설명란 블록 |
| 태그 | ✅ | `youtube.md` 태그 |
| 카테고리·언어·아동용 아님·라이선스·퍼가기·통계 공개 | ✅ | `channels/ch-market-daily/channel.yaml` → `youtube:` |
| 공개 예약 (평일 08:00 KST, 지났으면 바로 공개) | ✅ | `youtube.publish_time` 또는 `--at` |
| 썸네일 | ✅ 한 장(A) | `--thumb A|B|C` · **채널 전화 인증 필요** |
| 자막(한국어 트랙) | ✅ | `subs.ass` → SRT |
| 재생목록 (아침 브리핑/심층/주간/주말 분석, 없으면 만듦) | ✅ | `youtube.playlists` |
| '변경되거나 합성된 콘텐츠' 고지 | ✅ (기본 '아니요') | `youtube.synthetic_media` |
| 결과 기록 (영상 주소·Studio 주소·한 일·경고) | ✅ | `05_edit/youtube_publish.json` (main 에 자동 커밋) |
| 썸네일 테스트 및 비교(A/B/C) · 댓글 고정 · 최종 화면·카드 · 수익 창출 | ❌ API 미지원 | Studio 에서 (1~2분) |

## 1. 한 번만 하는 준비 (사용자 PC, 약 15분)
1. **구글 클라우드 프로젝트** — https://console.cloud.google.com → 새 프로젝트 (예: `ytflow`).
2. **API 켜기** — 'API 및 서비스 → 라이브러리' → **YouTube Data API v3** → 사용.
3. **OAuth 동의 화면** — 외부(External) · 앱 이름 `ytflow` · 내 이메일 → 범위는 건너뛰어도 됨 → **테스트 사용자에 내 구글 계정 추가**.
   그다음 **'앱 게시(In production)'** 로 바꾼다 — 테스트 상태로 두면 권한이 **7일마다 만료**된다. (확인되지 않은 앱 경고는 나 혼자 쓰므로 '계속' 누르면 됨)
4. **사용자 인증 정보** — 'OAuth 클라이언트 ID 만들기' → 유형 **데스크톱 앱** → JSON 내려받기 → `D:\ytflow\video-editing\client_secret.json` (커밋 안 됨, .gitignore).
5. **권한 받기** — PC 에서 (gh CLI 로그인돼 있어야 함: `gh auth login`):
   ```bash
   cd D:\ytflow\video-editing
   python scripts/youtube_auth.py client_secret.json --to-github
   ```
   브라우저가 열리면 이미 로그인된 계정 → **채널 '이어읽는시장'(브랜드 계정)을 고른다** → 허용.
   끝에 "권한을 준 채널: 이어읽는시장" 이 나오면 성공 — 토큰은 화면·채팅에 나오지 않고 GitHub 저장소 비밀값 3개(YT_CLIENT_ID · YT_CLIENT_SECRET · YT_REFRESH_TOKEN)로 바로 들어간다.
6. **API 감사(audit) 신청** — ⚠ 확인 안 된 API 프로젝트로 올린 영상은 **비공개로 잠긴다**(유튜브 정책, 2020-07 이후 만든 프로젝트). 
   YouTube API Services 감사 양식(https://support.google.com/youtube/contact/yt_api_form)으로 '내 채널에 내 영상을 올리는 개인용 도구' 라고 신청. 통과 전까지는:
   업로드·설명란·자막·재생목록은 자동으로 되고, **공개 전환만 Studio 에서 손으로**(또는 통과 뒤 자동).

## 2. 매일 쓰는 법
```bash
python -m ytflow upload <프로젝트>                 # 영상 → GitHub Release (기존)
python -m ytflow yt-publish <프로젝트> --dry-run    # 무엇을 올릴지 미리 보기 (제목·공개 상태·예약 시각·재생목록)
python -m ytflow yt-publish <프로젝트>              # GitHub Actions 가 올림 → 몇 분 뒤 05_edit/youtube_publish.json
python -m ytflow yt-publish <프로젝트> --at 2026-11-17T08:00 --thumb B   # 시각·썸네일 지정
```
- 같은 프로젝트를 두 번 올리지 않는다(`youtube_publish.json` 에 video_id 가 있으면 멈춤).
- 썸네일이 거절되면(전화 인증 안 된 채널) 영상은 그대로 두고 `warnings` 에 남긴다.
- 자동 제작 일정(매일 06:05)도 마지막에 이 명령을 부른다.

## 3. 목소리 (같은 날 정함)
- 채널 목소리는 `channel.yaml` 의 `tts`(Teo, ElevenLabs)를 렌더가 바로 쓴다. 키는 클라우드 환경의 네트워크 비밀값(api.elevenlabs.io, `xi-api-key`).
- 키가 안 먹거나 크레딧이 없으면 **영상은 멈추지 않고 edge 초안 목소리로** 만들고 로그에 남긴다 — 그 날은 올리기 전에 확인.
- 강제로 초안 목소리: `YTFLOW_TTS=edge python -m ytflow hybrid <프로젝트>`.
