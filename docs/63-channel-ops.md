# 63. 채널 운영·분석 — 에이전트가 맡아서 (2026-11-23)

> 2026-11-23 사용자: "앞으로 내 채널은 네가 운영하고 네가 분석하길 바래 이에 있어 도움이 되거나 필요한 요소는 조사하고 추가해줘"
> 운영 권한(같은 날 사용자 선택): 공개는 지금대로(시장 매일 브리핑만 자동 공개, 나머지는 D4 승인 뒤) · 제목·썸네일 교체, 재생목록, 사본 정리는 에이전트가 함 · 댓글 답글은 초안만.

## 1. 운영에 필요한 것 — 조사 결과와 지금 상태

| 필요한 것 | 어디서 | 지금 | 이번에 한 것 |
|---|---|---|---|
| 영상별 조회·좋아요·댓글, 공개 상태 | YouTube Data API (`youtube.force-ssl`, 업로드 토큰에 이미 있음) | 없었음 | `ops` 가 매일 수집·스냅숏 |
| 시청 지속 곡선·평균 시청 비율·구독 전환·유입 경로 | YouTube Analytics API (`yt-analytics.readonly`) | **권한 없음(403)** | 수집 코드 준비, 권한 받는 스크립트에 범위 추가 → **사용자가 채널마다 한 번 다시 승인** |
| 노출 수·노출 클릭률 | YouTube Reporting API 의 `channel_reach_basic_a1`(2025-09 추가, 같은 권한) — Analytics API 에는 없음 | 없음 | 권한이 생기면 작업을 만들고 매일 보고서를 받음(만든 다음 날부터) |
| 쇼츠 '본 비율(본 vs 넘김)' | 공개 API 에 없음. `engagedViews`(첫 프레임 넘어 본 수)로 가늠 | — | 쇼츠를 올리기 시작하면 `engagedViews ÷ views` 로 대신 봄 |
| 어디서 빠졌나 → 대본의 어느 말 | 시청 지속 곡선 + 우리가 올린 자막(captions.download, force-ssl) | 없었음 | 가장 크게 빠진 시각의 자막 문장을 보고서에 |
| 댓글 | commentThreads (force-ssl) | 없었음 | 새 댓글 수집(작성자 이름 저장 안 함), 질문 표시, 답글은 초안만 |
| 썸네일 A/B '테스트 및 비교' | Studio 에만 있음(API 없음) | 수동 | 그대로 수동(Chrome) — 대신 48시간 뒤 처진 편은 `ops-act rethumb` 로 B·C 교체 실험 |
| 고정 댓글 | API 가 '고정'을 지원하지 않음(올리기만) | — | 보고서 제안으로만 |
| 매일 돌리기 | 이 PC 정기 작업(docs/56) | 시장·호기심 제작만 | `channel-ops` 22:10 추가 |
| 분석 → 다음 편 | — | 없었음 | `channels/<폴더>/ops/next.md` 를 제작 작업이 S0 에서 읽음, 실험 장부 `data/analytics/experiments.md` |
| 비교 채널 | `last30days`·`claude-youtube` competitor (docs/62), vidIQ(크레딧 없음) | — | 매주 일요일 주간 요약에서 |

## 2. 매일 흐름 (22:10, `config/local_routines/channel-ops.md`)
```
python -m ytflow ops            수집(Data·Analytics·Reporting API) → 채널별 보고서 channels/<폴더>/ops/<날짜>.md
  ↓ 에이전트
해석: 앞섬▲·처짐▼ 영상의 차이를 주제·제목·썸네일·훅·결말·화면 중 하나로 (근거: 수치·빠진 지점의 말·유입 경로)
  ↓
실험 장부: 채널마다 한 번에 하나 — 가설 → 다음 편에 바꿀 것 하나 → 확인 지표·시점 → 판정
  ↓
next.md → 다음 날 제작 작업(시장 08:00·호기심 07:00)이 S0 에서 읽고 반영
  ↓ (허용된 것만)
ops-act: 사본 정리 · 재생목록 · 48시간 지난 처진 편의 제목/썸네일 한 번 교체(기록·되돌리기 가능)
```
매주 일요일: 주간 요약 + 비교 채널 점검. 같은 방향의 결과가 3편 이상이면 `manual-propose`(매뉴얼은 직접 고치지 않음).

## 3. 판정 원칙
- **같은 채널끼리, 같은 나이끼리.** 올린 지 24·48·168시간 때 조회를 서로 견줌(스냅숏이 쌓이기 전에는 '대략', 48시간 전은 '이른'). 고정 숫자 합격선은 두지 않음(manual README §5).
- **한두 편은 실험 기록.** 규칙으로 옮기지 않음(README §3-1).
- **한 번에 하나만 바꿈.** 여러 개를 바꾸면 무엇이 효과였는지 모름. 제목·썸네일 교체도 영상당 한 번.
- **수치가 없으면 '짐작'이라고 씀.**

## 4. 명령
```bash
python -m ytflow ops                         # 모든 채널 수집 + 보고서
python -m ytflow ops market --report-only    # 수집 없이 보고서만
python -m ytflow ops-act curiosity tidy --dry-run              # 공개본이 따로 있는 사본 삭제 (먼저 시험)
python -m ytflow ops-act market playlists                      # 재생목록에 빠진 공개 영상 넣기
python -m ytflow ops-act market retitle --video <id> --to 2    # youtube.md 제목 후보 2번으로 (48시간 뒤, 한 번)
python -m ytflow ops-act market rethumb --video <id> --to B    # 썸네일 B 로
python -m ytflow ops-act market revert --video <id>            # 마지막 교체 되돌리기
```
모든 행동은 `data/analytics/actions.jsonl` 에 전·후와 함께 기록.

## 5. 사용자가 할 일 (한 번)
분석 권한 추가 — 이 PC 에서 채널마다(브라우저가 열리면 해당 채널의 브랜드 계정을 고르고 허용):
```powershell
python scripts\youtube_auth.py E:\ytflow-local\.secrets\client_secret.json --to-github
python scripts\youtube_auth.py E:\ytflow-local\.secrets\client_secret.json --name knowledge --to-github
```
구글 클라우드 콘솔에서 이 OAuth 클라이언트의 프로젝트에 **YouTube Analytics API** 와 **YouTube Reporting API** 가 켜져 있어야 합니다(꺼져 있으면 403 이 계속 남 — 콘솔 'API 및 서비스 → 라이브러리'에서 사용 설정).

## 6. 첫 운영 기록 (2026-11-23)
- 시장 @이어읽는시장: 구독 11, 공개 9편. 앞섬 — 11-17 '칩을 팔지도 않았는데…'(2,080회), 드러켄밀러 편(0.8일 1,169회, 시간당 61.6). 처짐 — 11-18 실적 비교형 제목(107회). 실험 E1(제목: 사람·기관 + 의외의 행동 질문형), E2(11-18 편 제목 교체, 기준선 뒤).
- 호기심 @한겹더보면: 구독 2, 공개 5편 모두 100회 미만 — 표본 모으는 중. 중복 사본 4개 정리.
- 보고서: `channels/ch-market-daily/ops/20261123.md`, `channels/ch-knowledge/ops/20261123.md`.
