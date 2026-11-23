# 61. last30days 스킬 — 우리 채널에 쓸 곳 (2026-11-23)

설치·보안 검토는 `docs/05-skills-review.md` 의 2026-11-23 항목. 이 문서는 **쓸모**와 **쓰는 법**입니다.

## 1. 무엇을 더해 주나

우리가 이미 가진 소재 찾기: Google News·HN·YouTube 아웃라이어(`trends`), 뉴스레터(`newsletters`), SAVE 소식, X(유료 키라 안 씀), Reddit(클라우드에서는 막혀 안 씀).

last30days 가 더하는 것 — **사람들이 지금 무엇에 반응하고 어떤 말로 이야기하나**:
- 주제 하나로 Reddit·HN·YouTube·GitHub·dev.to·Stocktwits 를 한 번에 찾고, 추천·댓글·조회로 순위를 매김.
- YouTube 는 **자막 하이라이트**까지 뽑아 줌 → 방송사·전문가가 실제로 한 말의 위치를 바로 찾음.
- 높은 추천을 받은 댓글을 모아 줌 → 시청자가 쓰는 말·걱정·오해.
- **PC 에서는 Reddit 이 열림**(클라우드는 403). 키·쿠키 없이 됨.

## 2. 시험 결과 (2026-11-23, 키 없이, PC)

| 채널 | 주제 | 모인 것 | 쓸모 |
|---|---|---|---|
| ai | Claude Code 스킬 | Reddit 19·HN 22·YouTube 3(85만 회, 자막 3/3)·GitHub 4·dev.to 4 | **높음** — 잘 된 영상(조회 63만 "13분이면 Claude 를 잘 쓰게")의 각도, 디자인 스킬 워크플로 영상, 보안 사건(설정 파일 비밀값 노출 · 확장 프로그램 변조)과 Anthropic 직원 답글, 구독·약관을 둘러싼 불만 → AI 채널 소재·훅 후보 |
| market | 엔비디아 실적 | YouTube 11(94만 회: Bloomberg·CNBC·Schwab·USA TODAY 공식 채널, 어닝콜 원본 포함)·Reddit 6·HN 13·Stocktwits 5 | **높음** — 실적 발표 직후 방송사 공식 반응 영상과 자막 위치(v36 `## 영상 소스`·`bite`), 경영진 인터뷰(CEO 소식 ⑥), 개인 투자자의 걱정(고객 신용·경쟁 칩·경영진 공백)과 낙관(낮은 PER) — `## 인사이트` 의 반대 시각 후보 |
| (참고) | 얼굴 없는 쇼츠 | Reddit 17·HN 14·GitHub 12, 반응 적음 | 낮음 — 넓은 주제는 반응 적은 글·GitHub 잡음이 섞임 |

- 주의: 엔비디아 결과에는 "CEO 사임" 같은 큰 주장이 영상 제목·자막으로 들어 있음. **이 도구의 결과는 단서이지 사실 확인이 아님** — 1차 출처(회사 발표·공시)로 다시 확인하기 전에는 대본에 쓰지 않음(AGENTS '사실' 규칙).
- Polymarket 은 이 PC 에서 연결이 끊김 → 시장 확률은 아직 못 씀.

## 3. 채널별로 쓰는 곳

| 채널 | 단계 | 쓰는 법 | 매뉴얼에서 이어지는 곳 |
|---|---|---|---|
| **ai** | 주제 선정(S1)·훅 | 도구·모델 이름으로 돌려 "가장 반응 큰 각도"와 "자주 나오는 불만·질문"을 뽑음 → 제목·훅 후보 | 02-ai, `shorts-ai` 소재 고르기 |
| **market** | 매일 브리핑·실적(어닝콜) | 종목·사건으로 `--days=3` 정도로 돌려 방송사 공식 반응 영상(+자막 위치)과 개인 투자자 걱정을 모음 | 09 §3-4 인사이트·§3-5 영상 소스, 03 §0-1 어닝콜, CEO 소식 |
| **issues** | 반응 지도 | 사건 이름으로 돌려 해외 커뮤니티 반응을 모음 — 한쪽에 기울기 쉬우니 **양쪽 다 있는지** 확인용으로만 | 08-issues, `## 매체 프레임` 보조 |
| **curiosity** | 시청자 조사 | 오래된 주제가 많아 30일 창과 잘 안 맞음. 소재 후보가 요즘 다시 이야기되는지(재점화) 확인할 때만 | 04 §0-6 `audience.md` 보조 |

## 4. 지키는 선
- 커뮤니티 글·댓글은 **사실 출처도, 이름 있는 인사이트도 아님**(인사이트는 원문 확인된 사람·매체만). SAVE·뉴스레터와 같은 '단서' 자리.
- 댓글 문장을 대본에 옮기지 않음 — 시청자의 말투·걱정을 읽는 데만.
- 영어권 위주(국내 커뮤니티 없음). 국내 반응은 별도로.
- 결과 파일은 저장하지 않음(`LAST30DAYS_MEMORY_DIR=`). 남길 것은 프로젝트의 `01_research/` 에 요약해 적음.

## 5. 실행 (Git Bash, 이 PC)
```bash
export SKILL_DIR="$PWD/.claude/skills/last30days" LAST30DAYS_PYTHON="$(command -v python)" PYTHONIOENCODING=utf-8 LAST30DAYS_NATIVE_SEARCH=1
export PATH="$PATH:$(cygpath -u "$LOCALAPPDATA/Packages/PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0/LocalCache/local-packages/Python313/Scripts")"   # yt-dlp
"$LAST30DAYS_PYTHON" "$SKILL_DIR/scripts/last30days.py" "Nvidia earnings" --emit=compact --save-dir="" --days=7 \
  --subreddits=stocks,investing,StockMarket --plan - <<'PLAN_EOF'
{ "intent": "opinion", "freshness_mode": "strict_recent", "cluster_mode": "debate",
  "subqueries": [ {"label": "primary", "search_query": "nvidia earnings", "ranking_query": "How did investors react to Nvidia's latest earnings?",
                   "sources": ["reddit", "youtube", "hackernews"], "weight": 1.0} ] }
PLAN_EOF
```
Claude Code 에서는 `/last30days <주제>` 로 불러도 됨(스킬이 위 절차를 따름). 처음 쓰는 PC 는 `python scripts/install_tools.py` 후 `~/.config/last30days/.env` 를 docs/05 대로 직접 만들고, **설정 마법사는 돌리지 않음**.
