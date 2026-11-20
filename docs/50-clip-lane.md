# 50. 원본 발언 영상 — 필요할 때만 PC 에서 받기 (2026-11-20)

> 사용자 (2026-11-20): "앞으로 그럼 클라우드에서 제 계정으로 로그인하던지 클라우드가 아니라 다운로드가 필요할 때만 뭐 따로 다운로드 하던지 할 수 있도록 해주세요" · "아 우선 피클에게 요청한거 좋아요"
> 계기: 11/20 심층에 인터뷰·방송 원본을 넣지 못함 (클라우드는 유튜브 봇 확인으로 막힘, 우회 금지).

## 0. 왜 '클라우드 로그인'이 아니라 'PC 에서 받기'인가
| 길 | 결론 | 이유 |
|---|---|---|
| 클라우드에 내 유튜브 계정 로그인(쿠키) | **쓰지 않음** | 클라우드 세션은 일회용이고 여러 작업이 거쳐 감 → 계정 세션이 새면 채널까지 위험. 봇 확인을 계정으로 넘는 것은 '우회 금지'(AGENTS.md 소스 규칙)와 부딪힘 |
| **PC 에서 그 구간만 받기** | **기본** | PC 는 사용자 본인의 브라우저 로그인으로 평소처럼 봄(`clips.cookies_from_browser`). 받는 것은 대본이 쓰는 20초 이내 구간뿐 |

## 1. 흐름 — 찾기(피클) → 주문(클라우드) → 받기(PC) → 렌더
```
① 피클 (휴대폰 브라우저)  inbox/requests/<KST>-<slug>.md      → 공식 채널 영상 주소·구간·원문 (내려받지 않음)
② 클라우드               python -m ytflow clip-order <프로젝트>  → 02_script/clip_orders.json + inbox/pc-tasks/<KST>-clip-fetch-<프로젝트>.md (main 에 푸시)
③ PC (Codex·Claude)      python -m ytflow clip-fetch <프로젝트>  → 04_assets/footage/<파일> + Drive ytflow/cache/clips/<프로젝트>/ + 04_assets/clip_manifest.json
                          python -m ytflow hybrid <프로젝트>       → 원본이 들어간 판 (bite 장면: 그 사람의 목소리 + 번역 자막)
                          python -m ytflow upload <프로젝트> → yt-publish
④ (선택) 클라우드        python -m ytflow clip-pull <프로젝트>    → Drive 가 붙은 환경(YTFLOW_DRIVE 폴더 또는 rclone 리모트 YTFLOW_RCLONE_REMOTE)이면 manifest 의 sha256 대로 가져와 클라우드에서 렌더
```
- 2026-11-20 확인: 이 클라우드 환경은 Google Drive API 에 인증되지 않음(401) → 지금은 ③에서 **PC 가 렌더까지** 한다(11/20 Codex 가 한 방식). Drive 커넥터·rclone 이 붙으면 ④로 클라우드가 이어서 렌더.
- `hybrid` 는 렌더 전에 `clip-pull` 을 자동으로 시도하고, 원본이 없으면 멈추지 않고 인용 카드로 그린다(`bite_fallback`).

## 2. 대본에 적는 법 (`hybrid.json`)
```json
"footage": {"meeks": {"file": "meeks_cnbc_20261119.mp4", "url": "https://www.youtube.com/watch?v=i58L0YVXq_w",
                      "start": "3:29", "end": "3:45", "who": "폴 미크스",
                      "credit": "CNBC Television 공식 채널 (YouTube) · 2026.11.19 Squawk Box"}},
{"type": "bite", "who": "폴 미크스", "insight": true, "beats": [{"say": "앞 내레이션 (누가·언제·어디서)"}],
 "clip": {"src": "meeks", "lang": "en", "cuts": [{"find": "영어 원문 그대로", "ko": "번역"}]}}
```
- `url`·`start`·`end` 가 있는 footage 를 bite 가 쓰면 `clip-order` 가 주문서에 올린다. 구간은 피클 결과(자막 큐 타임)에서 앞뒤 0.5초 여유.
- 받은 구간 안에서 `cut`(받아쓰기 정렬)이 문장을 다시 찾아 단어 단위로 자른다(styles/source-cut).
- 11/20 처럼 클라우드판과 원본판을 나눠야 하면 대본 스크립트에 `--bites` 같은 스위치를 둔다(`scripts/daily_20261120/make.py`).

## 3. 지킬 것
- **구간만:** 한 구간 20초 이내, 한 편 60초 안팎(manual/09 §3-5). `clip-order` 가 넘으면 ⚠️.
- **공식 채널만:** 본인·기관(나스닥·연준·회사 IR) → 방송사 공식(CNBC Television·Bloomberg Television …). 해설 유튜버 영상 금지.
- **어디에 두나:** 받은 원본은 **Drive**(비공개)에만. git·공개 GitHub Release 에 원본 구간을 올리지 않는다 — git 에는 `clip_manifest.json`(파일 이름·크기·sha256·주소·구간)만.
- **로그인 정보:** 쿠키·토큰·비밀번호를 git·요청 파일·클라우드 환경 변수에 두지 않는다.
- **자동 더빙 주의:** CNBC 일부 영상은 한국어 자동 더빙 트랙이 기본 — `yt-dlp` 기본 형식은 원음(영어)을 고르지만, 받은 뒤 한 번 들어 확인.

## 4. 파일
| 파일 | 내용 |
|---|---|
| `ytflow/stages/cliplane.py` | `order` · `fetch` · `pull` |
| `02_script/clip_orders.json` | 주문서 (git) |
| `04_assets/clip_manifest.json` | 받은 결과 (git, 미디어 없음) |
| `inbox/pc-tasks/` | PC 에이전트 할 일 (한 파일 = 한 편) |
| `inbox/research/source-backlog.md` | 당일 못 넣은 원본 — 다음 회차에 |
