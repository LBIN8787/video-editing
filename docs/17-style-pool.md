# 17. 스타일 풀 늘리기 — 조사와 추가 (2026-11-09)

목표: 영상마다 원하는 스타일을 골라 쓰거나 섞을 수 있게 **등록부(`styles/recipes/`)를 늘린다.** 늘리는 법은 `manual/07-extend.md`, 섞는 규칙은 `manual/05-style-matching.md` §0-1.

## 1. 이번에 추가한 스타일 (등록부 10 → 17종)
| id | 무엇 | 아이디어 출처 | 상태 |
|---|---|---|---|
| `ai-chat` | AI 대화 화면 (질문 타자 + 답 흘러나옴) | HyperFrames 레지스트리 `chat-thread`·`claude-exchange` (Apache-2.0, 설치됨) | demo |
| `terminal-typing` | 터미널 명령 타자 + 결과 | `code-terminal-run` | demo |
| `screen-zoom` | 화면 자동 줌 + 얇은 테두리 | `cursor-zoom-follow` | demo |
| `hand-annotate` | 손그림 동그라미·밑줄·화살표 (겹치기 `mark`) | `cursor-annotate`, `hw-callout-circle` | demo |
| `data-choropleth` | 나라 색칠 지도 | `world-map` (+ world-atlas ISC) | demo |
| `shorts-claude` | 세로 쇼츠, 실제 녹화 화면 중심 (`ytflow/stages/shorts_hf.py`) | Codex 쇼츠와 비교하며 새로 만듦 | demo |
| `shorts-guide-codex` | 세로 쇼츠 설명 카드형 (Codex 'AI 실전노트') | Codex 보관본 (Drive) | approved (사용자 선호) |

구현은 우리 렌더러(HTML + GSAP)로 직접 했다 — 레지스트리 블록을 그대로 붙이지 않은 이유: 블록마다 고정 크기·토큰 체계가 달라 장면 길이·자막·그래픽 팩과 맞추기 어렵다. 아이디어와 움직임 값만 참고.

## 2. 아직 추가하지 않은 후보 (레지스트리에 이미 있음, 448개 중)
| 후보 | 블록 | 쓸 곳 | 주의 |
|---|---|---|---|
| 코드 변경 보여 주기 | `code-diff`, `code-highlight`, `code-scroll` | AI 코딩 사용법 | 실제 코드만 |
| 순위가 바뀌는 막대 | `bar-chart-race` | 시장: 시가총액·순위 변화 | 시세 출처 필수 |
| 한 숫자에서 물러나며 전체 보기 | `pull-back-reveal` | 시장·호기심 훅 | 강조 예산 |
| 화면을 찍은 듯한 원근 | `filmed-screen` | 화면 녹화가 단조로울 때 | 과하면 어지러움 |
| 알림이 쌓이는 휴대폰 | `notification-cascade` | 'AI 소식이 쏟아진다' 훅 | 실제 알림처럼 보이게 금지 |
| 손그림 액자·말풍선 | `hw-frame`, `hw-text-cloud` | 호기심 채널 자료 사진 | — |
| 차분한 장 표지 | `titlecard-calm` | 모든 채널 | — |
| 단어별 하이라이트 자막 | `caption-highlight`, `caption-pill-karaoke` | 쇼츠 | **강조 남용 판정** — 쓰려면 사용자 확인 후 |

## 3. 외부 스킬 조사 (라이선스 원문 확인한 것만 '가능')
| 스킬 | 라이선스 | 내용 | 판단 |
|---|---|---|---|
| charlie947/motion-graphics-skills | MIT (확인) | 15개 스킬: vox-explainer, animated-chart, model-showdown, title-sequence-3d, loop-cover, reel-export 등. API 키 불필요, HyperFrames 내보내기 선택 | **아이디어 참고** — 렌더러가 겹쳐 그대로 설치는 안 함. vox-explainer·model-showdown 구성을 다음 후보로 |
| haidrrrry/claude-remotion-skill | MIT (확인) | Remotion 으로 모션그래픽·자막·켄 번스, "렌더 → 프레임 확인 → 고치기" 고리 | 보류 — Remotion 은 렌더러 교체 비용 (docs/14) |
| JakeB-5/motion-graphic-skill | MIT (LICENSE 확인, 본문은 접속 실패) | 브리프 → 박자 맞춘 HTML 모션그래픽 | 본문 확인 후 재검토 |
| mattypark/Motion-graphics-skill | 확인 못 함 (LICENSE 404) | 계획·애니메이션·자막·사운드 | 라이선스 확인 전 사용 안 함 |
| heygen-com/hyperframes 스킬 (설치됨) | Apache-2.0 | general-video, pr-to-video 등 | 사용 중 |

## 4. 2026 편집 경향 (업체·크리에이터 글 — 참고만)
- 종이·점토 같은 '손으로 만든 느낌'과 혼합 매체가 다시 늘어남 → paper-sketch·hand-annotate 방향과 맞음.
- 화면·손을 가까이 보여 주는 줌, 단계 표시, 장(챕터) → screen-zoom·chapter.
- 단어 하이라이트 자막이 흔함 → **우리 채널은 사용자 판정(강조 남용 금지)이 우선.**

## 출처
- HyperFrames 레지스트리 카탈로그: `hyperframes catalog --json` (v0.8.190, 로컬)
- [charlie947/motion-graphics-skills](https://github.com/charlie947/motion-graphics-skills), [haidrrrry/claude-remotion-skill](https://github.com/haidrrrry/claude-remotion-skill), [JakeB-5/motion-graphic-skill LICENSE](https://raw.githubusercontent.com/JakeB-5/motion-graphic-skill/main/LICENSE), [mattypark/Motion-graphics-skill](https://github.com/mattypark/Motion-graphics-skill)
- 경향: [Hatch Studios](https://hatchstudios.com/top-video-and-animation-trends-to-know-in-2026/), [AdWave](https://adwave.com/resources/explainer-video-styles), [Async](https://async.com/blog/youtube-trends/), [Offshore Clipping](https://offshoreclipping.com/blog/video-editing-trends/), [Visionedge](https://visionedgeofficial.com/best-video-editing-styles-for-youtube/)
- Codex 쇼츠: Drive 'AI 실전노트 — 쇼츠 자동화 보관' / '00-쇼츠자동화-재사용안내-v1.0.0.md'
