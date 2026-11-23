# 56. 로컬 정기 작업 — 시장·호기심 자동화를 이 PC 에서

> 2026-11-21 사용자: "시장 관련 자동화처럼 호기심 채널도 자동화 세팅해줘" · "시장 자동화도 로컬에서 돌 수 있도록 세팅해주고 매번 클라우드라서 막혔니 뭐니 말이 너무 많아서" · "단 작업파일은 c드라이브에 두지 말고 구글드라이브에 보관해줘"

클라우드 루틴은 유튜브·사이트 봇 확인, 저장소 푸시 권한, 컨테이너마다 다시 설치하는 일에 자주 막혔습니다. 이제 매일 하는 작업은 **사용자 PC** 에서 Claude Code(구독)가 직접 실행합니다. 시장·호기심은 Claude 데스크톱 앱의 **예약된 작업**(사이드바 Scheduled, 앱이 켜져 있을 때 · 꺼져 있었으면 켤 때 실행)에 따로 보이고, 그 작업이 `scripts/local_routine.py <작업>` 을 실행합니다(2026-11-21 사용자: "예약된 작업에 안보이는데 호기심 따로 시장 따로 나눠줘"). (PC 일꾼 `ytflow-pc-worker` 는 뺐습니다 — 2026-11-21 사용자: "자동일꾼 그냥 빼 나 그냥 로컬에서 전부 영상작업 할테니까". 호기심 그림·렌더는 호기심 예약 작업이 직접 합니다.)

| 작업 | 시각 (한국) | 하는 일 | 지시문 |
|---|---|---|---|
| 📈 시장 (앱 예약 `ytflow-market-daily`) | 매일 08:00 | 이어 읽는 시장 오늘 영상: 조사 → 대본 → 렌더 → 유튜브 예약 공개(10:00) | `config/local_routines/market-daily.md` |
| 🔍 호기심 (앱 예약 `ytflow-curiosity`) | 매일 07:00 | 호기심 채널 진행 중인 편을 다음 사용자 결정(D1~D4)까지 진행하고, 진행 중인 편이 없고 7일이 지났으면 새 주제 카드 | `config/local_routines/curiosity.md` |
| 🛰️ 시장 심층 감시 (앱 예약 `ytflow-market-deep-watch`) | 2시간마다 (:40) | 심층(분석) 영상은 정해진 시각이 아니라 소재가 생길 때: ⓪ 훑기(Sonnet — 원본 레이더·72시간 안 거물 인터뷰·큰 날·CEO 소식·심층 후보) → 후보가 있으면 ① 판단(Fable — docs/63 기준: 사람의 말·사건형/원본형 시점·한국 종목 고리) → ② 제작 → ③ 검수(Fable) → 통과하면 바로 공개. '새 소재 없음'·'안 만듦'이면 알림 없이 Drive `_local/deep-watch-log.md` 에 한 줄. 아침 브리핑이 도는 동안은 건너뜀 (2026-11-24 사용자, manual/09 §2-00) | `config/local_routines/deep-watch-{scan,judge,make,review}.md` |

**단계 작업 (`steps`)**: 한 작업을 여러 단계로 나누고 단계마다 지시문·모델(`model`, 예 `claude-fable-5-2`)·시간을 따로 줄 수 있습니다. 단계는 같은 작업 폴더를 이어 쓰고, 어느 단계든 폴더 맨 위에 `ROUTINE_STOP` 을 만들면 거기서 멈춥니다(단계 사이 쪽지는 `DEEP_WATCH.json` 처럼 git 에 넣지 않는 파일로). `wait_for` 는 다른 작업이 도는 중이면 차례를 건너뛰고, `quiet_skip` 은 첫 단계에서 멈췄을 때 알림·보고 파일을 만들지 않습니다.

시각·목록은 `config/local_routines.yaml`. 지시문은 실행할 때마다 origin/main 에서 새로 읽으므로 지시문만 바꿀 때는 다시 설치하지 않아도 됩니다.
뉴스레터 수집(05:40)은 Gmail 커넥터가 필요해서 클라우드 루틴으로 둡니다.

## 1. 한 번만 설치
```powershell
# 1) Claude Code 로그인 (헤드리스 실행용, 한 번) — 데스크톱 앱의 로그인과 따로입니다
& (Get-ChildItem "$env:LOCALAPPDATA\Claude-Data\*\claude-code\*\*\claude.exe" | Sort LastWriteTime -Desc | Select -First 1).FullName
#    → 창에서 /login, 끝나면 /exit
# 2) 실행기 설치 (저장소 폴더에서). 앱을 안 켜 두는 PC 면 끝에 -Windows (그때는 앱 예약은 끔)
powershell -ExecutionPolicy Bypass -File scripts\install_local_routines.ps1
```
Claude 로그인이 안 되어 있으면 실행기가 **Codex(ChatGPT 구독)** 로 대신 돌리고 보고에 적습니다.
PC 가 꺼져 있던 시각은 켜지자마자 실행하고(StartWhenAvailable), 절전 중이면 깨웁니다(WakeToRun). 로그인한 상태에서만 돕니다(Drive `G:` 가 보여야 해서).

## 2. 파일은 어디에 — C 드라이브는 쓰지 않음
| 무엇 | 위치 |
|---|---|
| 실행기·작업 폴더 (git worktree) | `E:\ytflow-local\runner`(실행기, 실행 직전 최신 main) · `routine-<작업>`(작업마다) — git 저장소는 Drive 동기화에서 깨지므로 Drive 대신 E:(`docs/09` §0). 바꾸려면 환경변수 `YTFLOW_WORK` |
| 임시 파일 (TEMP) | `E:\ytflow-local\tmp\<작업>` — 매 실행 시작 때 비움 |
| 완성 영상·음성·그림 | 끝날 때 Drive `영상\<프로젝트>\` 로 복사·크기 확인. 7일 지난 것은 작업 폴더에서 지우고 Drive 사본만 |
| 보고 | Drive `_local\reports\<YYYYMMDD-HHMM>-<작업>.md` (첫 줄 = 한 줄 요약, Windows 알림으로도 뜸) |
| 로그 | Drive `_local\logs\` (작업 로그·에이전트 전체 출력) |
| 기획 문서 | git (main 에 푸시) |

## 3. 사용자가 할 일 (호기심)
결정이 필요하면 `inbox/decisions/<날짜>-<프로젝트>-D<n>.md` 가 main 에 올라오고 알림이 뜹니다. Claude 세션에서 답하면 기록됩니다 — 주제(D1)·대본(D2)은 `topic_brief.decision`·`script_review.md`, 최종(D4)은 `python -m ytflow review <프로젝트> --pass | --reject "이유"`. 다음 날 07:00 실행이 이어서 진행합니다.

## 4. 관리
```powershell
Start-ScheduledTask -TaskName ytflow-market-daily                 # 지금 한 번
python scripts\local_routine.py market-daily --dry-run            # 준비·에이전트만 확인
Get-ScheduledTask ytflow-* | Get-ScheduledTaskInfo | ft TaskName,LastRunTime,LastTaskResult,NextRunTime
Unregister-ScheduledTask -TaskName ytflow-curiosity -Confirm:$false   # 끄기
```
클라우드의 '이어 읽는 시장 — 매일 아침 영상 준비' 루틴은 같은 영상을 두 번 올리지 않도록 꺼 두었습니다(claude.ai/code/routines 에서 다시 켤 수 있음).
