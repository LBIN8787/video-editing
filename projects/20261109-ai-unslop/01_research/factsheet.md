# 팩트시트 — unslop (AI 채널 첫 영상, 2026-11-09)

상태: ✅ 1차 출처(저장소 원문·공식 문서·직접 실행)로 확인 / ⚠️ 2차 출처만 / ❌ 확인 안 됨(쓰지 않음)

## 1. 무엇인가
| # | 사실 | 상태 | 출처 |
|---|---|---|---|
| F1 | unslop = Claude Code·Codex·Google Antigravity 용 스킬, AI 가 만든 티 나는 화면(UI)을 디자인된 화면으로 바꿈 | ✅ | README https://github.com/heydamir/unslop |
| F2 | 만든 사람: 디자이너 다미르 소콜롭스키(Damir Sokolovsky, @heydamir), X 의 'Unslopping series' 를 시작 | ✅ | README, SKILL.md |
| F3 | 저장소 생성 2026-10-29, 2026-11-09 기준 별 12,004 · 포크 667 (화면 캡처 시점 668) | ✅ | GitHub 검색 API `repo:heydamir/unslop` (2026-11-09), 저장소 화면 캡처 |
| F4 | 2026-10-20 이후 생긴 저장소 별 순위(11-09): craft-anything 22,638 / dsh-superagent-prototype 21,201 / dsh-Go 16,093 / unslop 12,004 (4위) | ✅ | GitHub 검색 API `created:>2026-10-20 stars:>800` 정렬 |
| F5 | 라이선스 CC BY 4.0 — 상업 사용 가능, 만든 사람 표시·저장소 링크 필요 | ✅ | LICENSE, README |
| F6 | 공개 전 X 게시물: "1M views on a design post is wild 🤯 I'll share the unslop skill for Claude in a few days!" | ✅ | https://x.com/heydamir/status/2115431530407301345 |

## 2. 어떻게 일하나 (SKILL.md 원문)
| # | 사실 | 상태 | 출처 |
|---|---|---|---|
| F7 | 순서: 화면 보기 → 진단(signs.md 목록) → 고칠 양 판단 → 방향 5줄(제품·성격·세계·강조·서명) 쓰고 **사용자에게 먼저 물음** → 9단계 수정 → 점검 → 보고 | ✅ | SKILL.md "Run it" |
| F8 | 9단계 순서: 간격 → 색 → 아이콘 → 문구 → 글꼴 → 배치 → 마감 → 그림 → 움직임. 간격이 먼저인 이유: 리듬이 맞아야 나머지가 다르게 보임 | ✅ | SKILL.md "Fix in nine passes" |
| F9 | 방향은 제품에서 찾는다, 유행에서 찾지 않는다 ("Never from what is trending") | ✅ | SKILL.md "Direction" |
| F10 | "Vibecoded UI fails in the same predictable ways." (바이브 코딩한 화면은 늘 같은 방식으로 실패한다) | ✅ | SKILL.md 첫머리 |
| F11 | 링크만 있으면 페이지를 저장해 사본을 고침 → 결과는 '고친 코드', 실제 사이트 주인에게 넘겨야 함 | ✅ | SKILL.md Run it 1 |
| F12 | 그림 생성은 fal·Replicate·OpenAI images 등 이미지 서비스, 유료 생성 전에 매번 묻는다 | ✅ | README "Visuals" |
| F13 | 스토리 영상(화면이 스스로 고쳐지는 10초 영상)은 Playwright·ffmpeg 필요, 영상마다 'unslop by @heydamir' 표시 | ✅ | SKILL.md "Story video" |

## 3. 스킬이란 (Claude Code 공식 문서)
| # | 사실 | 상태 | 출처 |
|---|---|---|---|
| F14 | 스킬 = SKILL.md(이름·설명 + 지시문)가 든 폴더. 개인 `~/.claude/skills/<이름>/`, 프로젝트 `.claude/skills/<이름>/` | ✅ | https://code.claude.com/docs/en/skills |
| F15 | "Claude uses skills when relevant, or you can invoke one directly with /skill-name" | ✅ | 같은 문서 |
| F16 | "a skill's body loads only when it's used, so long reference material costs almost nothing until you need it" — 평소엔 이름·설명만, 쓸 때 본문, 참고 파일은 필요할 때 | ✅ | 같은 문서 |

## 4. 직접 해 본 것 (이 영상 제작 세션, 2026-11-09)
| # | 사실 | 상태 | 근거 |
|---|---|---|---|
| F17 | 설치: `git clone` → `cp -r unslop/skills/unslop ~/.claude/skills/` → 폴더에 SKILL.md·agents·references·scripts | ✅ | 실제 실행 기록 `04_assets/demo/term_log.txt` |
| F18 | 예제 대시보드(examples/dashboard.html, 일부러 AI 처럼 만든 화면)의 이모지 30개, 빛나는 그림자 5곳, 대문자 라벨 6곳, '!!' 3번, 메뉴 줄 높이 46·30·40·32·44·31px | ✅ | 원본 파일 계산 (`04_assets/demo/original.html`) |
| F19 | unslop 절차(진단 → 방향 5줄 → 단계별 수정)를 이 세션의 Claude Code 가 그대로 적용: 이모지 0개(선 아이콘), 메뉴 줄 높이 모두 32px, 인사말 → 기간 'November 2026', '+12%!!' → '+12% vs last month', '$124,860.40' → '$124,860' | ✅ | `04_assets/demo/build_story.py`, `after.html` |
| F20 | 방향 5줄(이번 적용): 제품=구독 결제 관리 대시보드 / 성격=정확·차분·조금 따뜻 / 세계=이름 그대로 '잉걸불(ember)' / 강조=매출 막대 하나 / 서명=연체 옆 작은 주황 점 | ✅ | 같은 파일 |
| F21 | 모핑 영상은 unslop 의 story.mjs 대신 이 채널의 녹화 스크립트(`record_morph.js`)로 같은 방식(단계별 CSS)을 녹화 — 외부 스크립트 실행 안 함 | ✅ | 제작 기록 |

## 5. 배경
| # | 사실 | 상태 | 출처 |
|---|---|---|---|
| F22 | '바이브 코딩' = 안드레이 카르파시가 2025년 2월 2일 X 에 쓴 말, AI 에 말로 시켜 코드를 만드는 방식 | ✅ | https://glossary.openssf.org/vibe-coding/ , https://knowyourmeme.com/memes/vibe-coding |
| F23 | 부트스트랩(Bootstrap)은 2011년 트위터 개발자들이 공개한 웹 화면 틀 — 많은 사이트가 비슷해 보인다는 말이 나옴 | ⚠️ | 널리 알려진 사실 (공개 연도 ✅ getbootstrap.com/docs/about, '비슷해 보인다'는 평은 의견 → "말이 나왔다"로만) |

## 쓰지 않는 것
- unslop 이 "디자이너를 대체한다" 같은 주장 (근거 없음, 스킬 스스로도 디자이너 의뢰를 함께 안내)
- 별 수의 '세계 몇 위' 류 순위 (우리가 확인한 건 특정 기간 새 저장소 중 4위뿐)
- Claude Code·Codex 정확한 요금 숫자 (자주 바뀜 → "이용료는 따로"로만)
