# AGENTS.md — ytflow (영상편집 자동화)

이 저장소는 **유튜브 영상 제작 워크플로우**를 코드와 문서로 담은 것입니다.
주제 선정 → 소스 탐색 → 자료조사 → 대본 → 편집점 → 편집 스타일 → 자막 → 업로드 준비 순서로 진행합니다.
Claude Code, Codex 등 어떤 코딩 에이전트든 이 파일과 `skills/` 를 따라 **같은 절차로** 작업합니다.

## 먼저 읽을 것
| 하려는 일 | 읽을 파일 |
|---|---|
| 영상 1편 만들기 | `skills/video-make/SKILL.md` |
| 자료조사 / 대본 / 소스 / 편집만 | `skills/video-research`, `video-script`, `video-sources`, `video-edit` |
| 편집 스타일 고르기·적용 | `styles/README.md`(계열 구분), `styles/<id>/STYLE.md`, `skills/edit-style-<id>` |
| 새 편집 스타일 추가 (레퍼런스 영상 분석) | `skills/edit-style-new/SKILL.md` |
| 전체 설계·에이전트별 차이 | `docs/04-agents.md`, `docs/02-workflow-sop.md` |
| 영상편집 skill 도입 검토 | `docs/05-skills-review.md` |

스킬은 `skills/` 가 원본입니다. `.claude/skills/`(Claude Code)와 `.agents/skills/`(Codex)는 `python scripts/sync_skills.py` 로 만든 복사본입니다. **원본만 고치고 동기화하세요.**

## 환경
```bash
pip install -r requirements.txt      # Python 3.10+, 그리고 ffmpeg·node(Playwright 캡처용)가 필요
python scripts/install_tools.py      # 외부 편집 도구·skill (HyperFrames, ffmpeg-skill) 고정 버전 설치
python -m ytflow --help
```

### LLM 백엔드 (`config/pipeline.yaml` → `llm.backend`, 또는 환경변수 `YTFLOW_LLM_BACKEND`)
| 값 | 언제 | 비용 |
|---|---|---|
| `claude-cli` | Claude Code 를 쓰는 사람 (`claude` 로그인) | Claude 구독 |
| `codex-cli` | Codex 를 쓰는 사람 (`codex login`) | ChatGPT 구독 |
| `api` | 서버·자동 실행 (`ANTHROPIC_API_KEY`) | 사용량 과금 |
| `manual` | **에이전트가 대화 안에서 직접 판단**. 요청이 `.llm/requests/` 에 쌓이면 답을 `.llm/responses/` 에 쓰고 다시 실행 | 에이전트 세션 안 |

## 주요 명령
```bash
python -m ytflow make --style-ref <스타일id> [--topic "주제"]   # 전체 자동
python -m ytflow stage <프로젝트> <단계>                          # 단계 하나
python -m ytflow rebuild <프로젝트>                               # 소스 넣은 뒤 재생성
python -m ytflow validate <프로젝트>                              # 대본 점검 (직접 쓴 뒤 필수)
python -m ytflow style <id> ref.mp4 --title <이름>               # 새 편집 스타일 분석
python -m ytflow styles | schemas | status <프로젝트>
```

## 트렌드 소스
| 소스 | 방식 | 필요한 것 |
|---|---|---|
| Google News (국문·영문) | 공개 RSS | 없음 |
| Hacker News | 공개 Algolia API | 없음 |
| YouTube 이번 주 아웃라이어 | 검색 결과 페이지 | 없음 |
| X 최근 게시물·공식 계정 | X API v2 최근 검색 | `X_BEARER_TOKEN` (선택, 유료 요금제) |
| X 게시물 캡처 | 공식 임베드(oEmbed) | 없음 (게시물 URL 만) |
| Reddit | 공개 JSON | 클라우드 IP 는 403 으로 막힘 → 쓰지 않음 |

## 편집 스타일 계열
| 계열 | 뼈대 | 스타일 | 대본 화면 문법 |
|---|---|---|---|
| `source` 원본 소스형 | CEO·CFO 인터뷰·실적발표 원본 영상 + 자막 + 핵심요약 애니메이션 | sixsigma | `prompts/script_source.md` |
| `infographic` 자체 제작 인포그래픽형 | 직접 그린 도식·차트·비유 그림 | **mijudiary(기본)**, moneycrew | `prompts/script_infographic.md` |
| `shorts` 쇼츠 | 9:16 고정 훅 + 큰 자막 | shorts-aitips | `prompts/shorts_script.md` |

## 규칙 (모든 에이전트 공통)
- **쉬운 대본:** 시청자는 일반인입니다. 핵심 한 문장(`core_message`), 논리 구조(`logic`), 숫자마다 비교 기준(`compare_to`), 비유 2개 이상, 과거 사례 1개 이상, 어려운 말 풀이(`glossary`)를 넣습니다. `prompts/script.md`, `validate` 가 점검합니다.
- **사실:** 숫자와 발언은 출처로 확인된 것만 씁니다. '재확인 필요'는 단정하지 않습니다. 투자 권유 표현은 금지합니다.
- **소스:** YouTube 봇 확인이나 사이트 접근 차단을 **우회하지 않습니다.** 막히면 임시 화면을 두고 사용자 PC 에서 `rebuild` 하게 안내합니다.
- **스타일:** 레퍼런스 채널의 대사, 고유 캐릭터, 로고, 썸네일을 복제하지 않습니다. 구조와 기법만 가져옵니다.
- **커밋 대상:** 기획 문서(md/json/csv/yaml)는 커밋합니다. 미디어(mp4/wav/png/jpg), 타 채널 자막, `styles/**/work/`, `.llm/` 은 커밋하지 않습니다(.gitignore).
- **결과 확인:** 영상을 만든 뒤에는 프레임을 뽑아 직접 확인하고(`skills/video-edit`), `REPORT.md` 의 남은 일을 사용자에게 알립니다.
- **스키마:** 에이전트가 직접 쓰는 JSON 은 `schemas/*.schema.json` 을 따릅니다(`python -m ytflow schemas` 로 갱신).

## 폴더
| 경로 | 내용 |
|---|---|
| `ytflow/` | 파이프라인 코드 |
| `ytflow/stages/` | 단계별 코드. 렌더러는 `cards.py`(sixsigma), `paper.py`(paper), `flat.py`(flat) |
| `prompts/` | 단계별 LLM 지시문 |
| `config/` | 채널·파이프라인 설정 |
| `styles/` | 편집 스타일 라이브러리 |
| `skills/` | 에이전트용 절차서 |
| `schemas/` | JSON Schema |
| `projects/` | 영상별 작업 폴더. 기획 문서만 버전 관리 |
| `data/style_profile.json` | 채널 대본 규칙 (benchmark) |
