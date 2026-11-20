유튜브 채널 '이어 읽는 시장'(주식, 1일 1영상)의 오늘 영상을 만들고 유튜브에 올리세요.

## 0. 준비 (이 PC — 클라우드 아님)
- 지금 폴더는 이 작업 전용 git worktree 이고, 최신 origin/main 에서 시작했습니다. 결과는 `git push origin HEAD:main` 으로 올립니다(거부되면 `git pull --rebase origin main` 후 다시, 최대 3번).
- 환경 준비가 안 됐을 때만 `pip install -q -r requirements.txt` · `python scripts/install_tools.py` 를 실행합니다(이미 있으면 건너뜀).
- 먼저 AGENTS.md, manual/README.md, **manual/09-market-daily.md**(매일 운영 매뉴얼), **docs/24-youtube-publish.md** 를 읽고 그 절차를 따릅니다.
- 사용량을 아낍니다: 같은 렌더를 여러 번 돌리지 않고, 실패하면 원인 한 가지를 고친 뒤 한 번만 다시 합니다.
- 오늘 프로젝트가 이미 main 에 있고 `05_edit/youtube_publish.json` 이 있으면(이미 올림) 아무것도 하지 않고 '이미 올림'으로 끝냅니다. 같은 프로젝트를 두 번 올리지 않습니다.

## 1. 오늘 무엇을 만들지 (한국 시간 오늘 = YYYYMMDD)
- 08:00 시작, 영상은 10:00 공개. 전날 장 마감 뒤 실적 발표·가이던스·어닝콜(녹취·경영진 발언)도 꼭 확인합니다. 큰 어닝콜이면 manual/03 §0-1 어닝콜 해부.
- **화~토 아침:** 전날 미국·한국 장의 아침 브리핑. 월요일은 금요일 미국 장 + 주말 소식. `python -m ytflow daily --project <YYYYMMDD>-market-daily` 로 시작.
- **브리핑이냐 심층이냐**는 manual/09 §2 신호가 둘 이상이면 심층. 요일로 고정하지 않습니다.
- **토요일:** 주간 분석 `<YYYYMMDD>-market-weekly` (한 주 흐름 3개 + 다음 주 일정).
- **일요일:** 분석글 한 편 `<YYYYMMDD>-market-analysis` (산업·테마 하나).
- **휴장:** 미국·한국 모두 휴장이면 만들지 않고 이유만 보고.
- 프로젝트 edit.yaml 에 `channel: ch-market-daily` 를 꼭 넣습니다(채널 목소리 Teo·유튜브 설정).

## 1-1. 소재 단서 (manual/09 §3-0)
- `inbox/newsletters/<오늘·어제>.md` 의 시장 소재와 `01_research/save_check.md`(daily 가 만듦)를 봅니다. 단서일 뿐 — 영상에 넣을 것은 1차 출처로 다시 확인해 factsheet 에 씁니다.
- SAVE 사이트를 직접 읽지 않습니다(봇 확인·AI 수집 거부). 알림이 없으면 `확인 못 함: 08:00 자동 실행, 알림 없음`.

## 2. 만들기 (manual/09 §3~§9)
1. **팩트시트**: 1차 출처(SEC 8-K·DART·실적 자료·공식 녹취록·연준 성명)로 원인을 확인해 `01_research/factsheet.md`, `## 해석` 절 포함.
2. **대본**: `scripts/daily_<YYYYMMDD>/make.py` → `02_script/hybrid.json`. 가장 최근 `scripts/daily_*` 를 본보기로, §4 장면표·고정 오프닝·마무리 문구를 지킵니다.
3. **검사·렌더**: `python -m ytflow check <프로젝트> --upto G5` (MUST 실패 0) → `python -m ytflow hybrid <프로젝트>`.
   - 렌더 로그에 "ElevenLabs 실패 → edge" 가 있으면 초안 목소리 → 유튜브에 올리지 말고 4단계까지만.
   - 오프닝 박자("이어 읽는, 이어 읽는 시장입니다")를 받아쓰기로 확인, 빠졌으면 그 박자 음성만 지우고 다시 렌더.
   - `04_assets/layout_qa.json` 이 `{}` 인지, 장면마다 프레임 한 장씩 뽑아 직접 봅니다.
   - 렌더 끝에 자동으로 도는 `05_edit/overlap_qa.json`(글자끼리·카드·선·화면 밖·자막 자리 겹침)이 0건인지 봅니다.
3-1. **제목·썸네일 — 유명 인물 (manual/09 §7-1 ⑥, docs/55, 2026-11-20 사용자)**: 오늘 중심 사건에 **당사자인 이름 있는 사람**(CEO·창업자·투자 대가·중앙은행 수장 — 그 사람의 결정·발언·퇴진·상장이 사건의 중심)이 있으면
   - 제목 후보 1번 앞 20자 안에 그 이름 + 그 사람의 결정·말 + 숨은 계산(또는 내 계좌로 번역). 정치인 이름을 배경으로 붙이지 않습니다(트럼프를 얹은 시황 제목은 같은 채널 기준 0.82배).
   - 썸네일 A 는 `layout: person`(얼굴 크게 + 이름표 + 큰 두 줄 숫자, 따옴표 한 마디는 영상 속 원본 발언과 같은 말). 사진은 `python -m ytflow archive commons "영문 이름"` 의 PD·CC0·CC BY 만 받아 `04_assets/footage/raw/` 에 두고, `credit` 에 출처를 적습니다. 자유 사진이 없으면 인물 썸네일을 만들지 않고 숫자 대비(versus)로.
   - 사생활·소문은 쓰지 않습니다. `thumbnail_qa.json` 의 `face_area` ≥ 0.06·`ok` 를 확인합니다.
   - **올릴 썸네일은 자동으로 고릅니다** (manual/09 §7-1 ⑦, 2026-11-20 사용자): `thumbnail` 단계가 A/B/C 에 근거 점수를 매겨 `05_edit/thumbnail_pick.json` 을 남기고, `yt-publish` 가 기본으로 그것을 올립니다. `thumbnail_pick.json` 도 기획 문서와 함께 커밋해야 Actions 가 읽습니다. 보고에 고른 썸네일과 점수 이유 한 줄, Studio '테스트 및 비교'에 넣을 나머지 둘을 적습니다.
4. **묶음·보관**: `yt-pack` → `upload` → `channels/ch-market-daily/episodes.md` 한 줄 → `check <프로젝트>` → 기획 문서만 커밋해 main 에 푸시.
   큰 파일(영상·음성·그림)은 git 에 넣지 않습니다. 실행기가 끝난 뒤 Google Drive `영상/<프로젝트>/` 로 옮깁니다.
5. **유튜브 올리기** (docs/24): `yt-publish <프로젝트> --dry-run` 으로 제목·예약 시각·재생목록 확인 → `yt-publish <프로젝트>`. 몇 분 뒤 `git pull` 해서 `05_edit/youtube_publish.json`(영상 주소·경고) 확인. Actions 실패·비밀값 없음이면 보고만.

## 지킬 것
- 확인된 숫자와 발언만. 장중 값을 마감처럼 쓰지 않음. 투자 권유 표현 금지. 개인(사인)의 이름 금지.
- 사이트 차단·봇 확인을 우회하지 않습니다. 막히면 다른 1차 출처를 쓰거나 그 이야기를 뺍니다 — 막힌 사실은 보고에 한 줄만.
- ElevenLabs 이외의 유료 크레딧 도구는 쓰지 않습니다.

## 보고 (LOCAL_RESULT.md)
첫 줄: `시장 <날짜>: <올림|초안만|안 만듦> — <제목>` 한 줄.
그 아래 짧게: 유튜브 주소(또는 못 올린 이유), 길이, 목소리(Teo/초안), 브리핑/심층 판단 이유, SAVE·뉴스레터 단서 반영 몇 건, 확인 못 해 뺀 것, Studio 에서 사람이 할 것(썸네일 B·C 테스트, 정정 댓글 고정).
