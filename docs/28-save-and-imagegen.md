# 28. SAVE 를 메모 없이 · 그림 생성 여러 길 (2026-11-14)

> 사용자: "세이브의 경우 메모 없이 진행할 수 있도록 해 주세요. 플러그인이나 다른 여러 가지 방법도 조사해 주세요.
>  이미지의 경우 GPT 이미지 생성(gpt image 2.6) 같은 걸 응용하는 것은 어떠하죠? 모든 걸 일레븐랩스로 하는 게 아니라 다른 여러 방법도 있으니까요."

## 1. SAVE(오선) — 메모 없이 받는 법

### 조사 결과
| 길 | 됨? | 이유·조건 |
|---|---|---|
| 클라우드에서 saveticker.com 읽기 | ✗ | Cloudflare 봇 확인(403), robots.txt 가 AI 수집기(ClaudeBot·GPTBot·anthropic-ai…) 차단, `ai-train=no, use=reference`. **우회·앱 내부 API 호출 금지** |
| SAVE 공식 텔레그램·X·뉴스레터·RSS | ✗ (못 찾음) | 검색으로 공식 채널 없음. 사용자 Gmail 에도 SAVE 메일은 가입 인증 코드 1통뿐 (뉴스 메일 아님) |
| **휴대폰 알림 전달 → Gmail → 저장소 (추천)** | ✓ | 내 휴대폰에 온 **내 알림**만 씀 (사이트를 긁지 않음). Android 는 특정 앱 알림을 전달하는 앱이 있음: Notifly(이메일·텔레그램·HTTP), Message487(F-Droid, 오픈소스, HTTPS 웹훅), IFTTT 'Android 알림' 애플릿, Tasker·MacroDroid. iPhone 은 다른 앱 알림을 읽을 수 없어 이 길이 안 됨 |
| 사용자 PC 브라우저 + Claude in Chrome (로그인된 SAVE 웹을 사람 대신 열어 읽기) | △ | 사람이 시킨 브라우징이라 크롤러는 아니지만, 사이트가 AI 에이전트를 원치 않음을 밝힘 → 기본 경로로 쓰지 않음. 쓰려면 PC 가 06:00 에 켜져 있어야 함 |
| Fivelines 에 데이터 제공(API·제휴) 문의 | ✓ (장기) | 가장 깨끗한 길. 회사 연락처: 앱 '고객센터'(saveticker.com/CustomerService) |

### 지금 상태 (2026-11-14 완료) — Apps Script 없이 돎
| # | 무엇 | 어디서 |
|---|---|---|
| 1 | SAVE 앱 알림 켜기 (관심 기업·키워드·경제지표·리포트) | 휴대폰 SAVE 앱 설정 |
| 2 | **MacroDroid** 매크로 — 트리거 `알림을 받으면`(앱 `SAVE`, 조건 없음) → 동작 `이메일 보내기`(본인 Gmail 계정), 제목 `[save알림]`, 본문 `{notification}` | 휴대폰(Android) |
| 3 | **30분마다 Gmail 감시** — `[save알림]` 메일(**스팸함 포함**, `in:anywhere`)을 읽어 `LBIN8787/video-editing` `main` 의 `inbox/save/<YYYYMMDD>.md` 에 `- <내용> (알림 MM-dd HH:mm)` 로 덧붙임 (이미 적힌 알림은 건너뜀) | Pickle 정기 작업 `📈 SAVE 알림 메일 감시` |
| 4 | `daily` 가 `01_research/save_check.md` 표로 옮기고 상태 '확인함 (사용자 메모: …)' | 아침 06:05 자동 제작 |

- **확인한 것 (2026-11-14 13:17 KST):** MacroDroid 시험 알림이 본인 Gmail 받은편지함(INBOX)에 `[save알림]` 제목으로 도착. 스팸함을 거치지 않았다.
- 날짜 규칙: **한국 06:00 이후 알림은 다음 날 파일**(`tools/save-forward/Code.gs` 의 `kstDay_` 와 같음).
- **`tools/save-forward/Code.gs`(Google Apps Script) 는 참고·백업용으로만 두고 켜지 않는다.** 30분 감시와 Apps Script 를 같이 켜면 같은 알림이 두 줄로 쌓인다. `script.google.com` 설치나 `GH_TOKEN` 발급을 사용자에게 다시 요청하지 않는다.
- **다른 에이전트(Claude Code·Codex)가 할 일은 없다** — 따로 설치·수집을 붙이지 말고 `inbox/save/<YYYYMMDD>.md` 를 지금처럼 읽는다 (`daily` 가 자동으로 표에 옮김, manual/09 §3-0).
- 알림은 **단서** — 영상에 넣을 것은 1차 출처로 재확인 (manual/09 §3-0). SAVE 문장을 대본에 그대로 쓰지 않음.

### (지금은 안 쓰는 길) Apps Script 로 직접 — 30분 감시를 멈출 때만
1. **SAVE 앱 알림 켜기:** 관심 기업·키워드·경제지표·리포트 알림 (앱 설정).
2. **알림 전달 앱** (MacroDroid·Notifly 등): 'SAVE' 앱만 선택 → **내 Gmail 주소**로 보내기, 제목 머리에 `[SAVE알림]`.
3. **Gmail 필터:** 제목 `[SAVE알림]` → 라벨 `SAVE알림` 붙이기 (받은편지함 건너뛰기 선택 가능).
4. **Apps Script** (`tools/save-forward/Code.gs`): script.google.com 새 프로젝트에 붙여넣기 → 매니페스트 `appsscript.json` → 스크립트 속성 `GH_TOKEN`(GitHub 세분화 토큰, 이 저장소 Contents 읽기·쓰기만) → `setup` 실행.
   10분마다 새 알림을 `inbox/save/<영상 날짜>.md` 에 한 줄씩 커밋 (한국 06:00 이후 알림은 다음 날 영상 몫).
5. 끝. 아침 06:05 자동 제작이 `daily` 로 `save_check.md` 표에 옮기고 상태 '확인함 (사용자 메모: …)'. 메모를 손으로 쓸 일이 없음.

## 2. 그림 생성 — 여러 길 (`python -m ytflow art-gen`, `ytflow/stages/imagegen.py`)
같은 '모델 시트'(한 장에 같은 인물의 자세 여러 개) 프롬프트를 어느 길로든 보내고, `art-cut` 이 배경(흰색·크림·투명)을 지워 조각으로 자른다.

| 길 | 모델 | 한 장 값(대략) | 장점 | 조건 |
|---|---|---|---|---|
| ElevenLabs 커넥터 (지금) | bytedance-seedream-5.5 | 98크레딧 ≈ $0.018 | 가장 쌈, 이번 시험 품질 좋음 | 목소리와 같은 크레딧을 나눠 씀, 에이전트가 커넥터로만 |
| ElevenLabs 커넥터 | **gpt-image-2.6** (sunburst·flare) | 190크레딧 ≈ $0.035 | GPT 이미지 2.6 그대로, 글자·구도 지시를 잘 따름 | 〃 |
| ElevenLabs 커넥터 | gemini-nano-banana-2.1 | 204크레딧 ≈ $0.037 | 참조 그림으로 같은 인물 유지 | 〃 |
| **OpenAI API 직접** (`--backend openai`) | gpt-image-2 계열 | 약 $0.006(저)~$0.21(고), 중간 품질 $0.03~0.1 | **투명 배경을 바로**(자르기 쉬움), 크레딧 분리 | `OPENAI_API_KEY` (네트워크 비밀값), 사용량 과금 |
| **Gemini API 직접** (`--backend gemini`) | Nano Banana 계열 | 약 $0.03~0.04 (Pro 는 $0.13) | 참조 그림 여러 장으로 인물 유지 | `GEMINI_API_KEY`, 무료 한도는 모델마다 다르고 줄어드는 중 |
| **Codex CLI + ChatGPT 구독** (`--backend codex`) | gpt-image-2 ($imagegen) | 추가 요금 없음 (구독 한도) | ChatGPT Plus/Pro 가 있으면 공짜 | Codex 로그인된 **사용자 PC** 에서만 (클라우드 자동 실행 불가) |
| Canva·Figma 커넥터 | 각 서비스 AI | 각 요금제 | Figma 는 벡터(층 나뉜 그림) 가능 → 관절 움직임에 유리 | 커넥터 권한·요금제 |
| 직접 그림 (`manual`) | — | 0 | 그림체 완전 통제 | 사람 손 |

**추천:** 매일 자동(클라우드)은 **OpenAI API(gpt-image-2 계열, 투명 배경)** 또는 지금처럼 **ElevenLabs Seedream 5.5**(가장 쌈). 사용자 PC 에서 만들 때는 **Codex $imagegen**(구독 안, 추가 비용 0).
한 편 8~12장 기준: Seedream ≈ $0.2, GPT Image 2.6(ElevenLabs) ≈ $0.4, OpenAI 직접 중간 품질 ≈ $0.3~1.

### 시험 결과 (2026-11-14)
- **Codex `$imagegen` (ChatGPT Pro 구독, 클라우드 세션에서 `codex login --device-auth` 로 로그인):** 아기 모델 시트 1장 41초, 추가 비용 0, 1752×897.
  같은 프롬프트의 Seedream 5.5 와 비교해 품질 비슷(표정이 더 살아 있음, 반팔 우주복으로 해석), `art-cut` 으로 3조각 정상.
- 로그인은 **그 세션의 컨테이너에만** 남음 → 사람과 함께하는 세션에서는 Codex(무료)로, 사람 없는 아침 자동 실행은 ElevenLabs·OpenAI API 로 (또는 매번 로그인 승인).

### 주문서 예 (`02_script/art_plan.json`)
```json
{"sheets": [
  {"id": "baby", "prompt": "the same chubby toddler (about one year old, short dark hair, cream onesie with a muted red stripe), three poses: (1) sitting, looking around curiously; (2) reaching out, grabbing a wooden toy block; (3) standing, taking a wobbly first step",
   "pieces": ["baby_look", "baby_grab", "baby_walk"]}]}
```
`python -m ytflow art-gen <프로젝트> --backend openai` → `04_assets/story/gen/baby_sheet.png` + `baby_look.png`… → 대본에서 `{"do": "cut", "src": "gen/baby_look.png"}`, `{"do": "pose", ...}`.
`--backend manual` 은 `02_script/art_orders.md`(그대로 붙여 넣을 프롬프트)만 만듦 → ElevenLabs·ChatGPT 웹·Canva 어디서든 생성 → 시트를 `gen/<id>_sheet.png` 로 넣고 다시 실행하면 자름.

### 출처
- OpenAI gpt-image-2 가격(토큰 과금, 이미지 출력 $30/1M 토큰 등): [aipricing.guru](https://www.aipricing.guru/models/gpt-image-2/), [llmreference](https://www.llmreference.com/model/gpt-image-2/openai-api), 공식 [OpenAI pricing](https://developers.openai.com/api/docs/pricing)
- Gemini 이미지 가격: [activepieces](https://www.activepieces.com/blog/nano-banana-api-pricing-cost-per-image-in-2026.md), [eesel](https://www.eesel.ai/blog/nano-banana-2-lite-pricing)
- Codex $imagegen (ChatGPT 구독): [codex.danielvaughan.com](https://codex.danielvaughan.com/2026/04/27/codex-cli-image-generation-gpt-image-2-visual-development-workflows/), [IT Brief](https://itbrief.com.au/story/openai-launches-chatgpt-images-2-0-with-api-access)
- Android 알림 전달: [Message487 (F-Droid)](https://f-droid.org/en/packages/life.andre.message487/), [Notifly](https://apkcombo.com/notifly/app.idealiz.notifly/), [IFTTT 애플릿](https://ifttt.com/applets/RQyRZa3Y-forward-android-app-notifications-to-multiple-channels)
- ElevenLabs 값은 커넥터의 견적(estimate_only, 2026-11-14) 기준.
