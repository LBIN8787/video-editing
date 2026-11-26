# 심층 감시 — 클라우드가 고르고 PC 가 만든다 (2026-11-26)

> 사용자: "4시간 간격으로 설정하고 클라우드에서 탐색해주세요 영상 제작만 로컬에서 진행하시구요"

| 차례 | 어디서 | 언제 (한국) | 하는 일 |
|---|---|---|---|
| 훑기(Sonnet) → 판단(Fable) | 클라우드 루틴 | 02:40 · 06:40 · 10:40 · 14:40 · 18:40 · 22:40 | `config/cloud_routines/deep-watch-scan-judge.md` — 만들 소재면 `queue/` 에 일감 한 장 |
| 제작 → 검수·예약 업로드(Fable) | 이 PC `market-deep-watch` | 00:10 · 04:10 · 08:10 · 12:10 · 16:10 · 20:10 | `queue/` 의 가장 오래된 일감 → `DEEP_WATCH.json` → `deep-watch-make.md` → `deep-watch-review.md`. 일감이 없으면 에이전트를 띄우지 않고 끝 |

- `queue/<YYYYMMDD-HHMM>-<project>.json` — 판단 단계의 `DEEP_WATCH.json` + `status: pending`. PC 제작이 시작하면 `done/` 으로 옮김(`status: taken`).
- `log.md` — 판단·제작·검수 기록 한 줄씩 (예전 Drive `_local/deep-watch-log.md` 대신).
- PC 가 꺼져 있으면 일감은 쌓여 있다가 켜진 뒤 첫 차례에 오래된 것부터 하나씩 만듭니다. 마감(`deadline`)이 한참 지난 일감은 제작 단계가 판단해 '지남'으로 닫습니다.
