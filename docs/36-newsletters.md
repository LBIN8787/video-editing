# 36. 뉴스레터 — 채널별 소재 목록 (2026-11-15)

> 사용자: "save 를 포함하여 소스탐색겸 참조용으로 무료 뉴스레터를 구독한 상황" → GPT 안 두 개 검토 → "진행해주세요".
> 코드 `ytflow/stages/newsletters.py` · 목록·분류 규칙 `config/newsletters.yaml` · 결과 `inbox/newsletters/<YYYYMMDD>.md|json`

## 0. 원칙
- 뉴스레터는 **단서**입니다. "어제 무엇이 화제였나"만 얻고, 영상에 넣을 숫자·발언은 링크를 따라 **1차 출처**(공시·당국·논문·회사 발표)로 확인합니다 (manual/09 §3, SAVE 와 같은 자리).
- 뉴스레터 문장을 대본·화면에 옮기지 않습니다. 저장소에는 **제목·링크·분류만** 커밋하고, 메일 본문은 `.cache/` 에만 둡니다.
- 메일을 그대로 쌓지 않고 소재마다 다섯 칸으로 나눕니다: **소재(원래 제목) · 원문·기사 · 원자료·통계 · 영상·이미지 · 재사용 조건** (+ 어느 뉴스레터, 여러 곳이 같이 다뤘는지).

## 1. 구독 목록 (2026-11-15 결정)
| 채널 | 뉴스레터 | 상태 |
|---|---|---|
| 시장 | Axios · The Daily Upside · 어피티 머니레터 · KDI 경제정보센터 | 구독 예정 |
| 시장 | Bloomberg 아침 판 · WSJ The 10-Point | 막힘 — 봇 차단·로그인. **우회하지 않음**, 사람이 휴대폰에서 가입 |
| AI | TLDR AI ✓ · TLDR Tech ✓ · The Batch · Simon Willison(블로그 RSS ✓) | |
| 호기심 | Quanta ✓ · Aeon ✓ · JSTOR Daily · The Public Domain Review | |
| 시사 | Our World in Data Brief · Pew Research (KDI 도 같이) · 뉴닉(막힘 — 본인인증) | |

빼거나 미룬 것: Finimize(Axios·Daily Upside 와 겹침), The Rundown AI(TLDR AI 와 겹침, 쇼츠 소재가 모자라면 다시), Nature Briefing(매일·연구 위주·Quanta 와 겹침, 받는다면 주간), NASA Earth Observatory(NASA 자료는 이미 `media.py`, 발행 여부 확인 필요), Smithsonian Magazine·World Bank·IEEE Spectrum(겹침).

**도착 시각:** 미국 아침 판은 한국 전날 밤에 옵니다 → 매일 브리핑의 원인 찾기가 아니라 심층·주간의 배경. 장 마감 판(06~07시 도착)만 아침 제작에 바로 씁니다. 구독 1주 뒤 실제 도착 시각을 `config/newsletters.yaml` 의 `arrives` 에 고쳐 적습니다.
**날짜 규칙:** 한국 06:00 이후 도착분은 다음 날 영상 몫 (`inbox/save` 와 같음).

## 2. 흐름
```
Gmail '뉴스레터' 라벨 ─(에이전트, Gmail 커넥터)→ .cache/newsletters/raw/*.json ─ newsletters ingest ─┐
블로그 RSS ──────────────────────────────────────────────────── newsletters rss ──────┤
                                                                                        ▼
                                              inbox/newsletters/<YYYYMMDD>.md|json (채널별 표, 2주 안 중복 제거)
                                                                                        ▼
                         daily (시장·시사) → daily_brief.md 끝 '⑦ 뉴스레터 화제'  ·  호기심·AI 는 show 로 주간 소재 고르기
```

### 메일 가져오기 (에이전트가 할 일)
클라우드의 Python 은 Gmail 에 직접 들어가지 못합니다(프록시 키는 Gmail 범위가 아님). Gmail 커넥터를 가진 에이전트가 합니다.
1. Gmail 검색: `label:뉴스레터 newer_than:2d` (라벨이 없으면 `config/newsletters.yaml` 의 `match` 주소로 `from:(…)`)
2. 메일마다 `get_message`(PLAIN_TEXT) → `{"id","sender","subject","date","body"}` 를 `.cache/newsletters/raw/<id>.json` 으로 저장
3. `python -m ytflow newsletters ingest .cache/newsletters/raw/*.json` (짧은 추적 주소는 따라가서 진짜 주소로, 끄려면 `--no-resolve`)
4. `python -m ytflow newsletters rss`
5. `inbox/newsletters/` 커밋 (이미 들어간 메일·주소는 다시 넣지 않으므로 여러 번 돌려도 됨)

구독 확인·환영 메일은 자동으로 건너뜁니다. 모르는 보낸 사람도 건너뜁니다 → 새로 구독하면 `config/newsletters.yaml` 에 한 줄 더합니다.

### 보기
```bash
python -m ytflow newsletters sources                         # 목록·상태·도착 시각
python -m ytflow newsletters show --brand curiosity --days 7 # 호기심 채널 이번 주 소재
python -m ytflow daily --project <YYYYMMDD>-market-daily     # 시장 브리핑 끝에 ⑦ 뉴스레터 화제
```

## 3. 분류 규칙 (`config/newsletters.yaml`)
- **채널:** 뉴스레터마다 기본 채널(`brands`). 여러 개면 소재 제목의 낱말(`route`)로 나눔 — 예: TLDR Tech 의 실적 기사 → 시장.
- **링크 종류:** 도메인으로 원문(1차: sec.gov·DART·연준·arXiv·GitHub·회사 IR…) / 원자료(OWID·FRED·KOSIS·Pew…) / 영상·이미지(LoC·NASA·Commons·스미스소니언…) / 보도·글. 'See the data' 같은 짧은 링크는 바로 앞 소재에 붙음.
- **재사용 조건:** 도메인마다 한 줄 (`reuse`). 없으면 "보도·글: 단서만". OWID 는 CC BY 지만 원자료로 다시 그리기를 권장, Pew 는 차트 이미지를 그대로 쓰지 않음.
- **중복:** 최근 14일 안에 나온 주소는 새로 넣지 않고 '같이 다룸'에 뉴스레터를 더함 → 여러 곳이 다룬 소재가 위로.

## 4. 자료실 — 스미스소니언 추가
GPT 가 권한 자료실 셋 중 미국 의회도서관(`archive search`)·NASA(`media.py`)·위키미디어 공용(`archive commons`)은 이미 있었고, **스미스소니언 Open Access** 를 더했습니다.
```bash
python -m ytflow archive si "steam locomotive"     # CC0 이미지만, 소장처·크기·주소
```
키: 환경변수 `SI_API_KEY`(api.data.gov 무료 키). 없으면 `DEMO_KEY`(시간당 약 30회).

## 5. 남은 일
- Gmail 필터 (사람, 한 번): `from:(tldrnewsletter.com OR simonsfoundation.org OR aeon.co OR axios.com OR thedailyupside.com OR uppity.co.kr OR kdi.re.kr OR deeplearning.ai OR jstor.org OR publicdomainreview.org OR ourworldindata OR pewresearch.org)` → 받은편지함 건너뛰기 + `뉴스레터` 라벨. 첫 메일이 오면 실제 보낸 주소로 맞추기.
- 매일 자동 수집 (2026-11-15 만듦): 정기 작업 `📰 뉴스레터 소재 수집 (매일 05:40)` (`trig_01FofZNNb2FYStBdN4L9MZv7`, 한국 05:40, 매번 새 세션) 이 §2 의 1~5 를 돌림.
  main 에 이 코드가 합쳐지기 전에는 `ccr-28400ba3-s13cmo` 브랜치에, 합쳐진 뒤에는 main 에 커밋.
  **⚠️ 만들 때 Gmail 커넥터를 붙이지 못함** — 사용자가 claude.ai 의 정기 작업(루틴) 설정에서 이 작업에 Gmail 커넥터를 더해야 메일을 읽음. 그 전에는 RSS 만 수집.
- 매뉴얼 반영(manual/09 §3-0 옆에 '뉴스레터 화제'): 매뉴얼 담당에게 제안함으로 남김 (`proposals/manual/`).
