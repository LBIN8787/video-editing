# AGENTS.md — ytflow (영상편집 자동화)

이 저장소는 **유튜브 영상 제작 워크플로우**를 코드와 문서로 담은 것입니다.
조사해서 글로 정리하던 일(대화형 LLM 의 답을 다듬던 일)을 이어서, 그 글을 **원고 → 대본 → 화면 → 영상**으로 바꾸는 반복 제작 라인입니다.
롱폼은 장편 칼럼·보고서 분석, 쇼츠는 짧은 주제 안내입니다. 편집 스타일 하나가 유튜브 채널 하나입니다(`channels/`).
**순서: 소스 먼저 → 소스가 강한 주제·형식 결정 → 글(원고) → 소스에 맞춘 편집 → 편집 스타일은 그 위에.**
서술할 내용이 많고 자세한 분석이면 롱폼, 한 가지를 알려 주는 정보형이면 쇼츠로 나눕니다(다른 형식 소재는 그 채널 대기열로).
주제 선정 → 소스 탐색 → 자료조사 → 대본 → 편집점 → 편집 스타일 → 자막 → 업로드 준비 순서로 진행합니다.
Claude Code, Codex 등 어떤 코딩 에이전트든 이 파일과 `skills/` 를 따라 **같은 절차로** 작업합니다.

## 가장 먼저: 제작 매뉴얼 (`manual/`)
**새 세션·새 모델은 `manual/README.md` 부터 읽습니다.** 세 채널은 사람의 욕망으로 나뉩니다 (`channels/brands.yaml`):
**ai**(AI 를 더 잘 다루고 싶다) · **market**(돈의 흐름을 알아 이기고 싶다) · **curiosity**(궁금증을 풀고 싶다).
한 편마다 `01_research/topic_brief.json`(욕망 → 트리거 → 질문 → 주제)을 먼저 쓰고, 단계마다 `python -m ytflow check <프로젝트>` 를 통과해야 다음으로 갑니다.
사용자 검토 결과는 `python -m ytflow review <프로젝트> --pass | --reject "이유"` 로 기록하고, 기각 사유는 매뉴얼 기준으로 바꿔 `manual-bump` 로 버전을 올립니다 (`manual/CHANGELOG.md`, 스냅샷 브랜치 `manual/vN`).

## 먼저 읽을 것
| 하려는 일 | 읽을 파일 |
|---|---|
| **제작 매뉴얼 (욕망 → 주제 → 조사 → 대본 → 연출 → 검사)** | `manual/README.md` → `manual/01~06` |
| **편집 스타일 등록부·자동 추천** (상황에 맞는 스타일, 파일 하나로 늘림) | `styles/recipes/`, `python -m ytflow style-pick <프로젝트>`, `manual/07-extend.md` |
| **반드시 지킬 것·검사** | `manual/06-checklist.md`, `python -m ytflow check <프로젝트>` |
| 채널 회차 만들기 (반복 운영) | `skills/channel-run/SKILL.md`, `channels/README.md`, `docs/06-operations.md` |
| 영상 1편 만들기 | `skills/video-make/SKILL.md` |
| 형식: 롱폼 칼럼·보고서 / 쇼츠 안내 | `formats/README.md` |
| 자료조사 / 대본 / 소스 / 편집만 | `skills/video-research`, `video-script`, `video-sources`, `video-edit` |
| **교양·상식·역사·심리 채널** (수요 분석 → 주제 → 깊은 조사 → 이야기 대본) | `docs/10-knowledge-demand.md`, `channels/ch-knowledge/`, `prompts/script_knowledge.md` |
| 하이브리드 (식스시그마 영상 + 머니크루 논리 + 미주일기 손그림) | `styles/hybrid/STYLE.md`, `prompts/script_hybrid.md`, `skills/edit-style-hybrid` |
| 편집 스타일 고르기·적용 | `styles/README.md`(계열 구분), `styles/<id>/STYLE.md`, `skills/edit-style-<id>` |
| 새 편집 스타일 추가 (레퍼런스 영상 분석) | `skills/edit-style-new/SKILL.md` |
| 전체 설계·에이전트별 차이 | `docs/04-agents.md`, `docs/02-workflow-sop.md` |
| 영상편집 skill 도입 검토 | `docs/05-skills-review.md` |
| **소스 찾기 (벤치마킹 채널 방식, 소스 먼저)** | `docs/07-sourcing.md`, `channels/<id>/channel.yaml` 의 `sourcing` |
| 목소리(ElevenLabs, 영상 확정 후 적용) | `docs/08-voice.md` |
| **어디에 무엇을 두나** (GitHub / Google Drive / 다시 만들기) | `docs/09-storage.md` |
| **제작 플레이북: 다음에도 똑같이 만들기** (명령 순서·자동 점검·보관) | `docs/11-playbook.md` |
| **연출과 그래픽 분리** (편집점·편집 포인트는 대본, 색·글꼴·배경은 갈아 끼우는 스킨) | `docs/13-direction-vs-graphics.md`, `skins/` |
| 그래픽 팩에 쓸 스킬·도구 (라이선스 확인·도입 순서) | `docs/14-graphic-pack-tools.md` |
| **연출 조사** (시청 유지 원칙·벤치마크 대비 측정·개선안·연출 도구) | `docs/15-direction-research.md` |
| **새 연출·그래픽 시험작** (아카이브 다큐·지도 여정·키네틱 타이포, 새 팩 newsprint·blueprint·kinetic-poster) | `docs/16-new-styles.md`, `ytflow/stages/directions.py`, `styles/demos/` |
| 키 없이 Google Drive 로 자동 복사 (Apps Script, 한 번 설치) | `docs/12-drive-sync.md`, `tools/drive-sync/` |

스킬은 `skills/` 가 원본입니다. `.claude/skills/`(Claude Code)와 `.agents/skills/`(Codex)는 `python scripts/sync_skills.py` 로 만든 복사본입니다. **원본만 고치고 동기화하세요.**

## 환경
```bash
pip install -r requirements.txt      # Python 3.10+, 그리고 ffmpeg·node(Playwright 캡처용)가 필요 (faster-whisper 포함)
python scripts/install_tools.py      # 외부 편집 도구·skill 고정 버전: HyperFrames·GSAP·rough.js, ffmpeg-skill, hand-drawn-diagrams
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
python -m ytflow make --channel <채널id> [--topic "주제" | --from-text 조사글.md]   # 채널 규칙으로 한 편
python -m ytflow make --style-ref <스타일id> [--topic "주제"]   # 스타일만 지정해 한 편
python -m ytflow make --channel <채널id> --plan                  # 트렌드 → 소스 찾기 → 주제·형식 결정까지만 (검토용)
python -m ytflow channels                                       # 채널 목록
python -m ytflow demand [--channel ch-knowledge]                 # 분야별 수요 분석 (검색 → 채널 → 아웃라이어 배수)
python -m ytflow archive search "influenza 1918" [--films]       # 공공 기록 사진·영상 (미국 의회도서관, 퍼블릭 도메인)
python -m ytflow hybrid <프로젝트>                                # 하이브리드 영상 (02_script/hybrid.json → final.mp4, 끝에 sync-qa 자동)
python -m ytflow skin-preview <프로젝트> [--skins a,b,c]          # 같은 연출을 그래픽 스킨별로 렌더해 비교 (YTFLOW_SKIN=<id> 로 한 번만 바꾸기)
python -m ytflow thumbnail <프로젝트>                             # 제목·썸네일 A/B/C (hybrid.json 의 package, 규칙 prompts/thumbnail.md)
python -m ytflow recipes | style-pick <프로젝트>                    # 편집 스타일 등록부 / 이 영상에 맞는 스타일 추천
python -m ytflow check <프로젝트> [--upto G4]                     # 체크리스트 자동 검사 (MUST 실패 시 종료 코드 1)
python -m ytflow review <프로젝트> --pass | --reject "이유"        # 사용자 검토 기록 → 기각은 매뉴얼 '반영 대기'로
python -m ytflow manual-bump "바꾼 기준 요약"                      # 기각 사유 반영 후 매뉴얼 버전 올리기
python -m ytflow sync-qa <프로젝트>                               # 완성본 자막·목소리·화면 싱크를 받아쓰기로 측정 → 05_edit/sync_qa.json
python -m ytflow voice-import <프로젝트> part1.mp3 [...]          # ElevenLabs 긴 음성을 대본 박자별로 자르기 (키 없이)
python -m ytflow upload <프로젝트> [--archive]                    # 완성 영상 → GitHub Release (키 불필요), --to drive 는 Drive (docs/09-storage.md)
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
| `source` 원본 소스형 | CEO·CFO 인터뷰·실적발표 원본 영상 + 자막 + 핵심요약 애니메이션 | sixsigma, **hybrid**(원본 영상 + 인과 지도 + 손그림, `python -m ytflow hybrid <프로젝트>`) | `prompts/script_source.md`, hybrid 는 `prompts/script_hybrid.md` |
| `infographic` 자체 제작 인포그래픽형 | 직접 그린 도식·차트·비유 그림 | **mijudiary(기본)**, moneycrew | `prompts/script_infographic.md` |
| `shorts` 쇼츠 | 9:16 고정 훅 + 큰 자막 | shorts-aitips | `prompts/shorts_script.md` |

## 규칙 (모든 에이전트 공통)
- **쉬운 대본:** 시청자는 일반인입니다. 핵심 한 문장(`core_message`), 논리 구조(`logic`), 숫자마다 비교 기준(`compare_to`), 비유 2개 이상, 과거 사례 1개 이상, 어려운 말 풀이(`glossary`)를 넣습니다. `prompts/script.md`, `validate` 가 점검합니다.
- **사실:** 숫자와 발언은 출처로 확인된 것만 씁니다. '재확인 필요'는 단정하지 않습니다. 투자 권유 표현은 금지합니다.
- **소스:** YouTube 봇 확인이나 사이트 접근 차단을 **우회하지 않습니다.** 막히면 임시 화면을 두고 사용자 PC 에서 `rebuild` 하게 안내합니다.
- **스타일:** 레퍼런스 채널의 대사, 고유 캐릭터, 로고, 썸네일을 복제하지 않습니다. 구조와 기법만 가져옵니다.
- **커밋 대상:** 기획 문서(md/json/csv/yaml)는 커밋합니다. 미디어(mp4/wav/png/jpg), 타 채널 자막, `styles/**/work/`, `.llm/` 은 커밋하지 않습니다(.gitignore). 완성 영상과 다시 만들 수 없는 자료 화면은 **GitHub Release** 에 보관합니다(`upload <프로젝트> --archive`, 키 불필요, `docs/09-storage.md`·`docs/11-playbook.md`).
- **제목·썸네일:** 모든 영상은 제목(후보 3개)과 썸네일 3장(A/B/C)을 함께 만듭니다(`prompts/thumbnail.md`). 사진 장소·숫자는 영상과 같은 사실 규칙.
- **결과 확인:** `layout_qa.json` 이 비어 있는지(화살표·글자 겹침, 대비) 보고, 영상을 만든 뒤에는 프레임을 뽑아 직접 확인하고(`skills/video-edit`), `REPORT.md` 의 남은 일을 사용자에게 알립니다.
- **목소리:** 초안은 edge-tts, **업로드 최종본은 ElevenLabs**(영상 확정 후 채널별 voice_id 지정). API 키는 채팅에 쓰지 않고 환경변수·네트워크 비밀값으로.
- **외부 도구:** 버전은 `tools/external.json` 에 고정합니다. 올릴 때는 그 도구의 SKILL.md·스크립트를 다시 읽고(네트워크 호출·자동 설치 확인) `docs/05-skills-review.md` 에 기록합니다.
- **스키마:** 에이전트가 직접 쓰는 JSON 은 `schemas/*.schema.json` 을 따릅니다(`python -m ytflow schemas` 로 갱신).

## 폴더
| 경로 | 내용 |
|---|---|
| `channels/` | 운영 채널: `channel.yaml`(형식·스타일·키워드·분량), `README.md`, `episodes.md`(회차 기록) |
| `formats/` | 영상 형식: 롱폼(칼럼·보고서) / 쇼츠(짧은 안내) 원고 구조 |
| `tools/external.json` | 외부 편집 도구 고정 버전 (HyperFrames, ffmpeg-skill). 본체는 설치 후 `tools/` 에 (커밋 안 함) |
| `ytflow/` | 파이프라인 코드 |
| `ytflow/stages/` | 단계별 코드. 렌더러는 `cards.py`(sixsigma), `paper.py`(paper), `flat.py`(flat), `hyper.py`(미주일기 카드 HTML + rough.js 손그림), `hybrid.py`(하이브리드: 원본 영상·인과 지도·손그림 장면), 마스터링 `finish.py`, 발언 단어 정렬 `align.py`, 소스 먼저 `scout.py`, 보관 `upload.py`, 공공 기록 자료 `archive.py`, 수요 분석 `demand.py` |
| `prompts/` | 단계별 LLM 지시문 |
| `config/` | 채널·파이프라인 설정 |
| `styles/` | 편집 스타일 라이브러리 (연출 문법 + 그래픽 스킨의 묶음, docs/13) |
| `skins/` | **그래픽 스킨**: 색 토큰·글꼴·배경·선 질감·사진 톤·자막 상자 (`skin.yaml`) |
| `skills/` | 에이전트용 절차서 |
| `schemas/` | JSON Schema |
| `projects/` | 영상별 작업 폴더. 기획 문서만 버전 관리 |
| `data/style_profile.json` | 채널 대본 규칙 (benchmark) |
