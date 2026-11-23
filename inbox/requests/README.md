# 요청함 — 막힌 일을 피클에게 넘기는 곳

Claude Code·Codex 같은 코딩 에이전트는 **유튜브 재생·자막·댓글, 로그인이 필요한 사이트, 봇 확인이 뜨는 페이지**에서 자주 막힙니다.
**피클(Pickle)** 은 휴대폰에서 브라우저를 직접 열고 이미 로그인된 계정으로 화면을 보기 때문에 이 부분을 대신 확인할 수 있습니다.

이 폴더가 그 통로입니다. **에이전트가 요청 파일을 `main` 에 올리면, 피클이 10분마다 이 폴더를 확인해 처리하고 결과를 같은 파일에 적어 `done/` 으로 옮깁니다.** 에이전트는 결과를 기다리지 않고 자기 일을 계속해도 됩니다(비동기).

```
에이전트: requests/<YYYYMMDD-HHMM>-<slug>.md 푸시  ──▶  피클(10분 감시): 브라우저·유튜브 조회
        ◀──  requests/done/<같은 파일명> (+ ## 결과, artifacts/)
```

## 1. 요청하는 법

1. **`main` 브랜치에 바로** 파일을 만들어 커밋·푸시합니다. **PR·다른 브랜치에 올린 파일은 처리되지 않습니다**(감시는 `main` 만 봅니다).
2. 파일 이름: `inbox/requests/<YYYYMMDD-HHMM>-<slug>.md`
   - 시각은 **한국 시간(KST)**, 24시간제. 예: `20261115-2210-yt-comments-R-iAk3UtERQ.md`
   - `slug` 는 영문 소문자·숫자·하이픈. 무엇을 물었는지 파일명만 보고 알 수 있게. 유튜브 영상 ID 처럼 대소문자를 지켜야 하는 값은 그대로 씁니다(`yt-comments-R-iAk3UtERQ`).
3. **한 파일 = 한 요청.** 확인할 것이 여러 개면 파일을 여러 개 올립니다(한 파일에 몰면 하나만 실패해도 전부 밀립니다).
4. `README.md` 와 `done/` 폴더는 피클 쪽 것이므로 **만들거나 고치지 않습니다.**

```bash
git switch main && git pull --ff-only          # 다른 에이전트가 먼저 올렸을 수 있음
$EDITOR inbox/requests/20261115-2210-yt-comments-R-iAk3UtERQ.md
git add inbox/requests && git commit -m "request: 유튜브 댓글 확인 (R-iAk3UtERQ)"
git push origin main
```

> 이 저장소는 **공개**입니다. 요청 파일에 **비밀번호·OTP·개인 이메일·전화번호·주민번호 같은 비밀값을 절대 적지 마세요.** "이미 로그인되어 있는 계정으로 확인" 처럼 적으면 됩니다. 감시 절차는 비밀값이 적힌 요청을 처리하지 않습니다.

## 2. 요청 파일 형식

YAML frontmatter + 본문입니다.

```markdown
---
from: claude-code        # claude-code | codex | other
type: youtube-check      # youtube-check | web-read | browser-task | research
url: https://www.youtube.com/watch?v=R-iAk3UtERQ
status: pending
---

이 영상의 공개 상태·업로드 날짜·조회수와, 상위 댓글 5개(좋아요 수·작성 시각)를 확인해 주세요.
출력은 아래 표 형식으로, 확인 시각과 함께 주세요. 확인할 수 없으면 그 이유도 적어 주세요.
```

| 필드 | 필수 | 값 |
|---|---|---|
| `from` | O | 요청한 에이전트: `claude-code` · `codex` · `other` |
| `type` | O | `youtube-check`(영상·자막·댓글·메타데이터) · `web-read`(공개 페이지 읽기) · `browser-task`(로그인된 사이트 조작·조회) · `research`(여러 페이지 모아 정리) |
| `url` | 아니오 | 대상 URL. 여러 개면 본문에 나열 |
| `status` | O | `pending` 으로 시작 (아래 §4 의 다른 값은 피클이 씁니다) |
| `title` | 아니오 | 한 줄 제목. 없으면 본문 첫 줄을 씁니다 |

**본문에는 이 세 가지를 적습니다:** ① 구체적으로 확인할 항목 ② 뽑아야 할 데이터(칸 이름까지) ③ 원하는 출력 형식. `"요약해 줘"` 처럼 범위가 없는 요청은 결과가 쓸모없어집니다.

## 3. 피클이 하는 일 (처리·응답 규칙)

**자동으로 처리합니다**

- 유튜브 페이지·자막·댓글·채널·재생목록 등 메타데이터 확인
- 공개 웹 페이지 읽기, 표·수치·인용 추출
- **이미 로그인된** 사이트의 조회(화면에 보이는 것 확인, 스크린샷)
- 여러 페이지를 모아 정리(`research`)

**자동으로 하지 않습니다 → `status: needs_approval`**

- 돈이 나가는 일(결제·구매·구독)
- 계정·설정·비밀번호 변경, 새 OTP·비밀번호 입력이 필요한 로그인
- 외부로 나가는 발송(메일 보내기, 글·댓글 게시, 메시지 전송)

이 경우 피클은 파일을 `done/` 으로 옮기지 않고 `status` 만 `needs_approval` 로 바꾼 뒤 **사람(저장소 주인)에게 채팅으로 승인을 묻습니다.** 승인되면 다시 `pending` 으로 돌아가 처리되고, 거절되면 `cancelled` 로 남습니다. **같은 요청을 파일로 다시 올리지 마세요** — 중복 요청으로 처리됩니다.

**처리 결과는 이렇게 남습니다**

- 같은 파일 끝에 `## 결과` 섹션이 붙습니다.
- 파일은 `inbox/requests/done/<원본파일명>` 으로 **이동**합니다(원래 경로에는 남지 않음). frontmatter `status` 는 `done` 이 됩니다.
- 첨부: **작고 공개해도 되는** CSV·캡처만 `inbox/requests/done/artifacts/<slug>/` 에 함께 커밋할 수 있습니다. 크거나 민감한 것(로그인 화면·비공개 스튜디오 자료·개인정보)은 비공개 Google Drive 에 두고 `## 결과` 에는 위치만 적습니다 (`docs/09-storage.md` §0-0).

```markdown
## 결과

- 확인 시각: 2026-11-15 22:19 KST
- 결론: 영상은 비공개, 업로드 2026-11-13 21:04, 조회수 0 (비공개라 댓글 없음)
- 근거: 채널 스튜디오 콘텐츠 목록 화면 "비공개" 표시, 시청 페이지는 "비공개 동영상" 안내
- 확인하지 못한 것: 없음
- 첨부: `inbox/requests/done/artifacts/20261115-2210-yt-comments-R-iAk3UtERQ/01-studio.png`
```

`## 결과` 아래는 **확인 시각 · 결론 · 근거(수치·인용·링크) · 확인하지 못한 것 · 첨부 경로** 다섯 칸을 지킵니다. 확인에 실패해도 이유를 적어 남깁니다 — 조용히 사라지는 요청은 없습니다.

## 4. `status` 값

| 값 | 뜻 | 누가 쓰나 |
|---|---|---|
| `pending` | 처리 대기 | 요청한 에이전트 |
| `needs_approval` | 사람 승인 대기(돈·계정 변경·외부 발송) | 피클 |
| `done` | 처리 완료(파일은 `done/` 에 있음) | 피클 |
| `cancelled` | 철회·거절 | 요청한 에이전트 또는 피클 |

요청을 **철회**하려면 `status: cancelled` 로 바꿔 커밋하거나 파일을 지웁니다. 이미 `done/` 으로 옮겨진 요청은 되돌리지 않고, 필요하면 새 요청으로 정정을 받습니다.

## 5. 결과 받는 법

```bash
# 대기 중인 요청 / 끝난 요청 목록
gh api "repos/LBIN8787/video-editing/contents/inbox/requests?ref=main" --jq '.[].name'
gh api "repos/LBIN8787/video-editing/contents/inbox/requests/done?ref=main" --jq '.[].name'

# 결과 읽기(클론 없이)
gh api "repos/LBIN8787/video-editing/contents/inbox/requests/done/<파일명>" --jq '.content' | base64 -d

# 또는 클론에서
git switch main && git pull --ff-only && cat inbox/requests/done/<파일명>
```

- **기다리지 않아도 됩니다.** 나중에 `done/` 목록에서 파일명으로 찾아 읽으세요. 파일명이 같으니 자기 요청을 찾기 쉽습니다.
- 보통 **10분 안에 확인이 시작**되고, 조회 한 건은 몇 분 안에 끝납니다. 오래 걸리는 조사는 파일에 기한을 적어 주세요(예: "오늘 23:00 KST까지").
- **`done/` 은 읽기 전용으로 봅니다.** 결과를 고치지 말고, 틀렸으면 새 요청 파일로 정정을 요청합니다. 결과에는 확인 시각이 있으니 **오래된 결과를 지금 사실로 쓰지 마세요.** 영상에 넣을 숫자·발언은 1차 출처로 다시 확인합니다(`manual/09 §3-0` 과 같은 원칙).
- 결과 첨부는 `git pull` 로 `done/artifacts/` 에서 가져다 씁니다.

## 6. 한계 (미리 알아 둘 것)

- **유튜브 봇 확인·로그인 벽은 우회하지 않습니다.** 막히면 결과에 "확인 못 함 + 이유"로 남깁니다. 우회를 요구하는 요청은 처리되지 않습니다.
- **로그인이 만료된 사이트**는 비밀번호를 파일에 적지 않는 규칙 때문에 `needs_approval` 로 돌아옵니다. 그때는 사람이 휴대폰에서 한 번 로그인해 주면 다음 요청부터 됩니다.
- **피클이 처리하지 못하는 상태**(앱이 꺼져 있거나 감시가 멈춤)에서는 요청이 `pending` 으로 남습니다. 한 시간 넘게 `pending` 이면 해당 요청은 사람이 볼 수 있게 따로 알리는 것이 좋습니다.
- 이 통로는 **조회·수집**용입니다. 파일 수정·커밋·코드 변경은 이 폴더가 아니라 각자 하던 방식대로 합니다.

## 7. 예시

**youtube-check** — 영상 하나의 상태·메타데이터
```markdown
---
from: codex
type: youtube-check
url: https://www.youtube.com/watch?v=R-iAk3UtERQ
status: pending
---

공개 상태, 업로드 일시, 길이, 조회수, 그리고 자막이 있는지(있으면 첫 200자)를 확인해 주세요.
출력: 항목 | 값 두 칸 표.
```

**web-read** — 표에서 숫자만 뽑기
```markdown
---
from: claude-code
type: web-read
url: https://www.airkorea.or.kr/web/sidoQuality
status: pending
---

오늘 서울 PM10·PM2.5 시간평균 수치와 측정 시각을 확인해 주세요.
출력: 수치와 측정 시각 한 줄. 발표 기준이 '시간평균'인지 '일평균'인지도 적어 주세요.
```

**browser-task** — 로그인이 필요한 화면
```markdown
---
from: claude-code
type: browser-task
url: https://studio.youtube.com/channel/UC.../videos
status: pending
---

이미 로그인된 계정으로 채널 스튜디오 콘텐츠 목록을 열어, 최근 업로드 5개의 제목·공개 상태·게시 시각을 표로 주세요.
```

**research** — 여러 페이지 모아 정리
```markdown
---
from: codex
type: research
status: pending
---

다음 세 곳에서 2026년 11월 미국 반도체 수출 규제 관련 보도를 찾아 주세요(URL 은 본문 아래).
사이트마다: 제목 | 발행일 | 핵심 문장 1개 | 링크. 같은 사안을 다룬 기사는 묶어서 표시해 주세요.
- https://www.reuters.com/...
- https://www.bloomberg.com/...
- https://www.ft.com/...
```
