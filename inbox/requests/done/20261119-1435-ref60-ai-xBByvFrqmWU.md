---
from: codex
type: youtube-check
url: https://www.youtube.com/watch?v=xBByvFrqmWU
status: done
title: Fireship — 공개 영상 표본과 타임코드
---

공개 페이지에서 영상 ID와 채널 일치, 길이·공개일·조회수 관찰시각, 공개 스크립트 트랙 종류를 확인. 다른 요청에 같은 영상이 진행 중이거나 이미 확보됐다면 재수집하지 말고 기존 위치만 반환.

도입·핵심 설명·본편 결론 각 20초의 처음·중간·끝에서 실제 플레이어 타임코드와 함께 3장씩(최대 9장)을 확보합니다. 광고·로딩·이전 화면 잔류는 제외하고 결론은 엔드카드 말고 내용상 마무리로 선택. 음향은 실제 들었을 때만 확인 범위 기재. 자료는 비공개 Drive ytflow/refs/channel-study-20261118/ai/xBByvFrqmWU/에만 보관, 공개 저장소에는 상태·범위·개수·사용권 확인 여부·상대 위치만 기록합니다.

출력: 관찰 시각 | 대상·상태 | 대본 종류 | 프레임 시각·수 | 실제 청취 범위 | 누락·차단 | 비공개 Drive 상대 위치. 다운로드·스트림 추출·차단 우회·새 로그인·설치·결제·공개·권한 변경 금지. 수집만, 스타일 분석·매뉴얼 변경 금지.

## 결과

- **관찰 시각**: 2026-11-20 04:19~04:24 KST (원격 브라우저, 로그인 없이 공개 재생, KR 출구)
- **대상·상태**: `xBByvFrqmWU` — 요청 URL과 `videoDetails.videoId` 일치, 채널 **Fireship**(`UCsBjURrPoezykLs9EqgamOA`) 일치. 제목 "DeepSeek is back... and Silicon Valley is terrified". 길이 **332초(5:31)** / 플레이어 331.521초, 공개일 **2026-08-20T10:53:37-07:00**(페이지 표기 2026. 8. 21.), 조회수 **1,249,144회**(관찰 시점), 좋아요 32,074·댓글 1,341, Science & Technology. 공개 상태 `isUnlisted=false`, `isFamilySafe=true`, playabilityStatus **OK**(연령·지역 제한·재생 오류 배너 없음). 사용권: microformat `license` 필드 없음 → **표준 YouTube 라이선스(CC 아님)**, 설명란에 재사용 허락 문구 없음 → **사용권 확인 안 됨**(다운로드·재사용 권한으로 해석하지 않음).
- **대본 종류**: 수동(제작자) 자막 **없음**. 공개 자막 트랙은 영어 자동 생성(ASR) **1개뿐**(`kind=asr`, `vssId=a.en`), 번역 트랙 없음. 공개 스크립트 패널에서 **44개 구간(0:00~5:24) 전문** 확보(자동 챕터 6개 머리말 삽입: AI safety theater 0:00 / DeepSeek enters the fray 1:03 / Understanding AI harnesses 1:38 / Spatiotemporal architecture 2:50 / Building with DeepSeek 3:13 / BlueDot Impact resources 4:36). 플레이어 CC 버튼은 "자막 사용 불가"여서 캡처 프레임에 자막이 그려지지 않는다.
- **프레임 시각·수**: **9장**(1280x720 PNG), 구간당 20초의 시작·중간·끝.

  | 구간 | 실제 플레이어 타임코드 | 화면 내용 |
  |---|---|---|
  | A 도입 (0:00~0:20) | 0:00.000 / 0:10.000 / 0:19.750 | "YESTERDAY..." 타이틀 카드 / AI 리더 신뢰 여론조사 카드(Trust 31% vs Don't trust 69%) / 샘 올트먼 PAUSE 밈 |
  | B 핵심 설명 (2:16~2:36) | 2:16.000 / 2:26.000 / 2:35.750 | DeepSeek Harness 설정>Models(모델 어댑터=플러그인) / YAML 한 줄 커스텀 프로바이더 설정 / Anthropic "Cloud sandbox reference" 문서 |
  | C 본편 결론 (4:16~4:36) | 4:16.000 / 4:26.000 / 4:35.750 | API 사용량 대시보드(Cost $0.30, 2,821,257 토큰) / 완성된 Horse Tinder 앱 / "if I were Sam or Dario…" 펀치라인(올트먼·아모데이 사진) |

  - 결론은 엔드카드가 아니라 내용상 마무리로 잡았다(스폰서 BlueDot 구간 4:36 시작 직전까지, 펀치라인 화면 포함). B 구간 중간값 2:23은 검은 전환 프레임이어서 밝기 스캔으로 식별한 뒤 2:26으로 옮겼다.
  - 각 캡처 직전 `video.currentTime`이 요청값과 일치하고 `seeking=false`·`readyState=4`임을 확인했다. 광고(`ad-showing=false`)·검은 버퍼링·이전 시크 잔여 프레임 없음. 플레이어 컨트롤바는 자동 숨김 상태에서 캡처했다(페이지 CSS 조작 없음). 프레임 우하단 불꽃 아이콘은 YouTube가 영상 위에 그리는 Fireship 채널 워터마크다.
- **실제 청취 범위**: **미확인** — 원격 브라우저에서 오디오 청취 불가. 음성·BGM·효과음은 확인하지 않았고, 자막 텍스트와 무음 캡처를 음향 증거로 쓰지 않았다.
- **누락·차단**: 없음(요청 항목 전부 확보). 참고 사항만 기록: ① 이 영상은 플레이어 CC가 "자막 사용 불가"다. ② 대본은 ASR 원문 그대로라 고유명사 오인식(Sam Alman, Cenamed Astra, codeex, T-Mu, Daario 등)이 있고 교정하지 않았다. ③ 설명란에 타임스탬프 목록이 없어 챕터는 스크립트 패널 헤더 기준이다. ④ 설명란에는 스폰서(BlueDot) 링크·뉴스레터/코스 링크만 있고 라이선스 문구는 없다.
- **비공개 Drive 상대 위치**: `ytflow/refs/channel-study-20261118/ai/xBByvFrqmWU/` — 기존 `ai/` 폴더를 재사용하고 그 아래에 영상 폴더만 새로 만들었다(중복 폴더 없음).
  - `meta.json`, `transcript.txt`(7,802 B), `frame-index.json`, `frames/` PNG **9장** = 파일 12개(하위 폴더 1).
  - 업로드 후 Drive 목록·바이트를 로컬과 대조해 9장 전부 일치 확인, `transcript.txt`는 Drive에서 재다운로드해 **md5 일치**까지 검증했다. 폴더 공유 권한은 소유자 1건뿐으로 비공개 유지.
- **미수행**: 영상 다운로드·스트림 추출·차단 우회·새 로그인·설치·결제·공개·권한 변경·스타일 분석·매뉴얼 변경은 하지 않았다. 공개 저장소에는 대본 전문·캡처 파일·Drive 링크를 넣지 않았다.
