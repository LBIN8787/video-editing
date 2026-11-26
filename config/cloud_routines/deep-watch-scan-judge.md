'이어 읽는 시장' 심층(분석) 영상의 **소재 감시 — 클라우드 차례 (훑기 Sonnet → 판단 Fable)**입니다. **4시간마다** 클라우드 루틴으로 돕니다.
영상은 만들지 않습니다. "만든다"로 정해지면 **일감 한 장**을 `inbox/deep-watch/queue/` 에 올리고 끝냅니다 — 제작·검수·예약 업로드는 사용자 PC 의 `market-deep-watch`(4시간마다, 클라우드 차례 1시간 반 뒤)가 그 일감을 집어 이어 갑니다.

> 2026-11-26 사용자: "4시간 간격으로 설정하고 클라우드에서 탐색해주세요 영상 제작만 로컬에서 진행하시구요"
> 2026-11-24 사용자: "소재 감시는 당연히 sonnet이 하시구요" · 판단·검수는 Fable.

## 0. 준비
- 저장소 LBIN8787/video-editing 이 없으면 add_repo(owner LBIN8787, repo video-editing, access push) → clone → register_repo_root. main 에서 `git pull`. `pip install -q -r requirements.txt`. `git config core.hooksPath .githooks`.
- 이 차례는 **매뉴얼·규칙 파일(`manual/OWNERS.yaml` protected)을 고치지 않습니다.** 렌더·목소리·그림·유튜브 업로드·ElevenLabs 등 크레딧 도구도 쓰지 않습니다. PR 은 만들지 않습니다.
- 판단 기록은 git 의 `inbox/deep-watch/log.md` 하나에 씁니다(아침 작업·PC 제작도 같은 파일). `$YTFLOW_DRIVE` 는 클라우드에 없으니 Drive 경로가 나오는 줄은 이 파일로 바꿔 읽습니다.

## 1. 훑기 (이 세션 = Sonnet, 30분 안)
`config/local_routines/deep-watch-scan.md` §1 을 그대로 따릅니다. 클라우드라서 다른 점만:
- 유튜브 검색·자막·사이트에서 봇 확인·429·403 이 나오면 **우회하지 않고** 그 소스만 건너뛰고, 후보에 '원문 미확인 (클라우드에서 막힘)'이라 적습니다. 원본 구간 확인은 PC 제작 단계가 합니다.
- 걸러 내기(§1-5)에는 `inbox/deep-watch/log.md` 끝 40줄과 `inbox/deep-watch/queue/`·`done/` 의 일감(같은 원본·같은 질문)을 더합니다.
- 결과는 `deep-watch-scan.md` §2 형식의 `DEEP_SCAN.md`(커밋하지 않음). 새 후보가 없으면 `inbox/deep-watch/log.md` 에 `<YYYY-MM-DD HH:MM> | 없음 | - | 훑기(클라우드 Sonnet)` 한 줄 → 3번으로.

## 2. 판단 (Fable 하위 에이전트 — 후보가 있을 때만)
Agent 도구로 **model `fable`** 하위 에이전트 하나를 띄워 맡깁니다. 프롬프트에 넣을 것: 저장소 경로, "`DEEP_SCAN.md` 와 `config/local_routines/deep-watch-judge.md` 를 읽고 §0·§1 기준으로 판단하라. 결과는 §2 형식대로 — 기록 줄은 `inbox/deep-watch/log.md` 에 `(클라우드 Fable)` 로, 만들면 `DEEP_WATCH.json` 을 저장소 맨 위에. `ROUTINE_STOP`·`LOCAL_RESULT.md` 는 쓰지 않는다. 원본을 클라우드에서 못 열었으면 그 사실을 sources·quote 에 표시하고, 그것만으로 '안 만듦'으로 하지 말 것(원문 확인은 PC 제작 단계가 함). 결론을 한 줄로 돌려줄 것."
- 하위 에이전트가 `DEEP_WATCH.json` 을 썼으면, 그 내용에 `"status": "pending"`, `"judged_at": "<YYYY-MM-DD HH:MM KST>"`, `"judged_by": "cloud"` 를 더해 **`inbox/deep-watch/queue/<YYYYMMDD-HHMM>-<project>.json`** 으로 옮깁니다(같은 project 의 일감이 queue·done 에 이미 있거나 `projects/<project>` 가 main 에 있으면 올리지 않고 log 에 '이미 있음').

## 3. 올리기
- 바뀐 것만 커밋: `inbox/deep-watch/`, 그리고 훑기가 바꾼 `inbox/radar/`·`inbox/insights/`·`inbox/research/deep-topics.md`. 메시지 `심층 감시(클라우드) <HH:MM>: <없음|안 만듦|지켜봄|일감 올림 — project>`. main 으로 push(거부되면 `git pull --rebase origin main` 후 다시, 네트워크 오류는 최대 4번 재시도). `DEEP_SCAN.md`·`DEEP_WATCH.json` 은 커밋하지 않습니다.

## 4. 끝 보고 (한 줄, 한국어)
- 일감을 올렸으면: `🛰️ 심층 일감: <질문> (<kind>, 마감 <deadline>) — PC 가 다음 차례에 제작`
- 아니면: `심층 감시(클라우드) <HH:MM>: <새 소재 없음 | 안 만듦 — 이유 | 지켜봄 — 무엇>`
