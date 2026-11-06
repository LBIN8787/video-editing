# 04. 에이전트별 제작 절차 (Claude Code · Codex 공통)

목표: 사람이든 Claude Code 든 Codex 든 **같은 저장소, 같은 명령, 같은 산출물**로 영상을 만든다.
절차의 원본은 코드(`ytflow/`)와 문서(`AGENTS.md`, `skills/`, `styles/`)이고, 특정 에이전트 기능에 기대지 않습니다.

## 1. 구성 원리
```
AGENTS.md ─────────────── 모든 에이전트가 먼저 읽는 규칙·지도   (Codex: 자동으로 읽음 / Claude Code: CLAUDE.md 가 @AGENTS.md 로 불러옴)
skills/<이름>/SKILL.md ── 단계별 절차서 (Agent Skills 형식: name·description 머리말 + 본문)
   ├→ .claude/skills/   Claude Code 가 찾는 위치  ┐ scripts/sync_skills.py 가 복사
   └→ .agents/skills/   Codex 가 찾는 위치        ┘ (원본은 skills/ 하나)
styles/<id>/ ──────────── 편집 스타일 라이브러리 (STYLE.md · edit.yaml · script.md · rules.json · metrics.json)
schemas/*.schema.json ─── 에이전트가 직접 쓰는 파일의 형식 (scenes, shortlist, articles, upload, style_rules)
ytflow/ ──────────────── 실행 코드 (python -m ytflow ...)
```

## 2. LLM 을 누가 부르나: 백엔드 4가지
파이프라인에서 판단이 필요한 단계는 다섯 가지입니다: 주제 평가, 자료조사, 대본, 스타일 해석, 업로드 패키지.
이 단계들은 아래 넷 중 하나로 동작하고, 산출물 형식은 모두 같습니다.

| 백엔드 | 호출 방식 | 웹 검색 | 이미지 보기 | 확인 상태 |
|---|---|---|---|---|
| `claude-cli` | `claude -p --output-format json [--json-schema] [--tools WebSearch,WebFetch / Read]` | ✅ | ✅ (Read) | 이 저장소에서 실제 실행 확인 |
| `codex-cli` | `codex [--search] exec --skip-git-repo-check --ephemeral -s read-only [--output-schema f] [-i 이미지] -o out -` | ✅ (`--search`) | ✅ (`-i`) | 명령 형식은 codex-cli 0.167 도움말로 확인. **로그인한 실제 실행은 아직 안 함** |
| `api` | Anthropic SDK (구조화 출력, 서버 웹 검색 도구) | ✅ | ✅ | 코드 경로만 있음 (API 키로 시험 필요) |
| `manual` | 프로그램이 멈추고 `.llm/requests/<id>.md` 를 남김 → 에이전트가 `.llm/responses/<id>.json|md` 작성 → 같은 명령 재실행 | 에이전트 도구 | 에이전트 도구 | 이 저장소에서 왕복 확인 |

- **codex-cli 의 구조화 출력:** OpenAI strict 스키마 규칙(모든 객체 `additionalProperties:false`, 모든 속성 required)을 따르도록 `llm.strict_schema()` 가 바꿔서 넘깁니다.
- **모델 지정:** `config/pipeline.yaml` → `llm.cli_model`(Claude), `llm.codex_model`(Codex, 비우면 Codex 기본값)입니다.

## 3. 에이전트별 시작 방법

### Claude Code
1. 저장소를 엽니다. `CLAUDE.md` → `AGENTS.md` 가 자동으로 읽히고, `.claude/skills/` 의 스킬이 목록에 뜹니다.
2. "이번 주 영상 만들어줘 (미주일기 스타일)" 처럼 요청하면 `video-make` 스킬을 따라 `python -m ytflow make --style-ref mijudiary` 를 실행합니다.
3. 구독만 쓰려면 `llm.backend: claude-cli`, 대화 안에서 직접 판단하게 하려면 `YTFLOW_LLM_BACKEND=manual` 을 씁니다.

### Codex (CLI · IDE · 클라우드)
1. 저장소를 엽니다. Codex 는 루트 `AGENTS.md` 를 자동으로 읽고, `.agents/skills/` 의 스킬을 찾습니다.
2. 같은 요청을 하면 같은 스킬과 명령을 씁니다.
3. 판단 단계를 ChatGPT 구독으로 돌리려면 `llm.backend: codex-cli` 를 씁니다. Codex 세션이 직접 판단하게 하려면 `YTFLOW_LLM_BACKEND=manual` 을 씁니다.
4. 샌드박스에서 네트워크가 막혀 있으면 웹 검색·YouTube 검색·TTS 단계가 실패합니다. 이때는 네트워크를 허용하거나 manual 로 진행합니다.

### 사람이 직접 (에이전트 없이)
`docs/02-workflow-sop.md` 의 명령 표대로 실행하고, 게이트(주제·대본·가편집)에서 결과 파일을 확인합니다.

## 4. 제작 절차 (어떤 에이전트든 이 순서)
| # | 단계 | 명령 | 산출물 | 에이전트가 확인할 것 |
|---|---|---|---|---|
| 0 | 스타일 선택 | `python -m ytflow styles` | — | 먼저 계열(원본 소스형 / 자체 제작 인포그래픽형)을 정하고 스타일을 고름 (`styles/README.md`) |
| 1 | 주제 선정 (트렌드 우선) | `stage discover` → `stage select` | `00_source/trends.json`, `shortlist.md` | 48시간 내 여러 매체 보도, 아웃라이어 근거, 리스크 |
| 2 | 자료조사 | `stage research` | `01_research/factsheet.md`, `articles.json` | 모든 팩트에 URL·날짜, 교차확인 |
| 3 | 대본 | `stage script` → `validate` | `02_script/scenes.json`, `script.md` | validate 통과, 분량, 원본 발언 근거 |
| 4 | 소스 탐색 | `stage sources` | `04_assets/sources.csv` | 영상이 장면 내용과 맞는가 |
| 5 | 소스 확보 | `stage clips` | `scene_XXX.mp4 / _shot.png / _temp.jpg`, `clips.csv` | 실패·임시 장면 목록 |
| 6 | 음성 | `stage voice` | `03_voice/clean/*.wav`, `durations.json` | 발음, 길이 |
| 7 | 편집점·화면 | `stage assets` | 카드·애니메이션, `shotlist.csv` | 스타일 렌더러 적용 |
| 8 | 자막 | `stage subtitles` | `subs.ass`, `subs.srt`, `chapters.json` | 줄 길이, 강조 |
| 9 | 가편집 | `stage assemble` | `05_edit/draft.mp4`, `timeline.csv` | **프레임을 뽑아 직접 확인** |
| 10 | 업로드 준비 | `stage package` → `stage report` | `06_package/upload.json`, `REPORT.md` | 남은 일을 사용자에게 보고 |

`make` 는 1~10 을 연속 실행합니다(게이트 자동 통과). 사람의 승인을 받으려면 `run` 을 쓰고 `approve` 로 게이트를 넘깁니다.

## 5. 새 편집 스타일 늘리기
`skills/edit-style-new/SKILL.md` 를 따릅니다. 요약하면 다음 순서입니다.
1. 레퍼런스 영상 파일을 받습니다.
2. `python -m ytflow style <id> <파일들> --title <이름>` 을 실행합니다.
3. `styles/<id>/` 의 초안을 직접 보고 다듬습니다.
4. 기존 렌더러로 되는지 판단하고, 필요하면 새 렌더러를 만듭니다.
5. 시험 렌더링으로 레퍼런스와 비교합니다.
6. `styles/README.md` 와 `skills/edit-style-<id>` 를 추가하고 `sync_skills.py` 를 실행합니다.

## 6. 커밋 전 점검
```bash
python scripts/sync_skills.py --check     # 스킬 복사본 동기화
python -m ytflow schemas                  # 스키마 갱신 (모델을 바꿨다면)
python -m ytflow validate <프로젝트>       # 대본을 고쳤다면
```
