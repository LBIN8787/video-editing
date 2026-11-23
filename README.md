# 영상편집 — ytflow

조사해서 정리한 글을 **원고 → 대본 → 화면 → 영상**으로 바꾸는 유튜브 반복 제작 라인입니다.
기준은 특정 레퍼런스 채널이 아니라 **제작 매뉴얼(`manual/`)과 네 채널**입니다. 채널은 사람의 욕망으로 나눕니다 (`channels/brands.yaml`).

| 채널 | 욕망 | 매뉴얼 |
|---|---|---|
| ai | AI 를 더 잘 다루고 싶다 | `manual/02-ai.md` |
| market | 돈의 흐름을 알아 이기고 싶다 | `manual/03-market.md`, 매일 운영 `manual/09-market-daily.md` |
| curiosity | 궁금증을 풀고 싶다 | `manual/04-curiosity.md` |
| issues | 세상이 어떻게 돌아가는지 알고 싶다 | `manual/08-issues.md` |

레퍼런스 채널(식스시그마·머니크루·미주일기 등)은 **편집 스타일 하나하나의 출처**로만 씁니다 (`styles/<id>/STYLE.md`). 구조와 기법만 가져오고 대사·캐릭터·로고·썸네일은 복제하지 않습니다.

```
주제(욕망 → 트리거 → 질문, 지금의 고리) → 소스 → 자료조사 → 대본 ⏸사용자 → 편집점·연출 → 화면 → 자막·목소리 → check → 검토 ⏸사용자 → 업로드
```

> **에이전트(Claude Code · Codex)라면 [`AGENTS.md`](AGENTS.md) → [`manual/README.md`](manual/README.md) 순서로 읽으세요.**
> 단계별 절차는 [`skills/`](skills), 편집 스타일은 [`styles/`](styles), 업무 체계(단계·결정 지점)는 [`manual/11-workflow.md`](manual/11-workflow.md) 에 있습니다.

## 설치

```bash
pip install -r requirements.txt      # Python 3.10+, ffmpeg·node 는 따로 설치
python scripts/install_tools.py      # 외부 편집 도구 고정 버전 (tools/external.json)
git config core.hooksPath .githooks  # 매뉴얼 잠금 검사 (docs/35)
python -m ytflow --help
```

LLM 연결은 `config/pipeline.yaml` 의 `llm.backend` 로 고릅니다: `claude-cli`(Claude 구독) · `codex-cli`(ChatGPT 구독) · `api`(API 키, 사용량 과금) · `manual`(에이전트가 대화 안에서 직접 판단). 자세한 표는 `AGENTS.md` '환경'.

## 한 편 만드는 흐름 (요약)

```bash
python -m ytflow daily --brand market --project 20261120-market-daily   # 매일 브리핑 주제 찾기 (시장·시사)
python -m ytflow edit-plan <프로젝트>      # 박자마다 상황 → 장면·연출 (편집 전에 EDIT_CONTEXT.md 먼저 읽기)
python -m ytflow hybrid <프로젝트>         # 02_script/hybrid.json → final.mp4 (끝에 sync-qa 자동)
python -m ytflow check <프로젝트>          # 매뉴얼 체크리스트 (MUST 실패 시 종료 코드 1)
python -m ytflow review <프로젝트> --pass | --reject "이유"
python -m ytflow yt-pack <프로젝트>        # 설명란·제목 후보·태그
python -m ytflow yt-publish <프로젝트>     # 업로드·예약 공개·썸네일·자막 (공식 API, docs/24)
```

명령 전체와 '하려는 일 → 읽을 파일' 표는 `AGENTS.md` 에 있습니다.

## 어디에 무엇을 두나

- **Git:** 코드·매뉴얼·설정·기획 문서(md/json/csv/yaml). `projects/<영상>/` 의 기획 문서도 커밋합니다.
- **Google Drive:** 완성 영상·음성·원자료처럼 큰 파일. Git 에는 위치·판본만 남깁니다 (`docs/09-storage.md` §0).
- 미디어(mp4/wav/png/jpg)와 `.llm/` 은 커밋하지 않습니다 (`.gitignore`).

## 클라우드에서 안 되는 일

YouTube 는 클라우드 서버의 영상 받기·재생을 막습니다. 우회하지 않습니다.
- 원본 발언 구간은 클라우드가 주문서를 쓰고(`clip-order`) 사용자 PC 가 받습니다(`clip-fetch`, `docs/50-clip-lane.md`). PC 할 일은 `inbox/pc-tasks/` 에 쌓입니다.
- 그 밖에 막히는 일(재생·자막·로그인 페이지)은 `inbox/requests/` 로 피클에게 요청합니다.
- 클립이 아직 없는 장면은 노란 '임시' 표시 화면이 들어갑니다. 업로드 전에 실제 자료로 바꿔야 합니다.

## 처음 설계 (기록)

처음(2026-11 초)에는 식스시그마를 기준 채널, AI비즈PT를 보조로 삼아 `benchmark` 로 대본 규칙(`data/style_profile.json`)을 뽑는 구조였습니다.
지금은 매뉴얼과 채널별 기준이 그 역할을 하고, 벤치마킹 기록은 `docs/01-benchmark.md`·`docs/03-benchmark-result.md` 에 남아 있습니다. 로제타는 채널을 특정하지 못해 제외했습니다.
