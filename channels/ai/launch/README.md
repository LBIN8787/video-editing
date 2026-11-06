# Windows 연결

사용 환경은 Windows로 확인했다. 저장소 루트의 WINDOWS-START.md와 CONNECT-YOUTUBE.cmd를 사용한다. 대상 채널 ID가 고정되어 있으며, 이 PC에서 OAuth 연결을 마쳐야 업로드 권한을 사용할 수 있다. 예약 운영 방식은 아직 미선택이다.

# AI 실전노트 개설·운영

현재: 사용자가 채널 생성과 URL을 전달했다. 대상은 https://www.youtube.com/channel/UCb6tSnNY6X3BtH-ujxMIf3g 이다. 공개 페이지 조회는 throttled로 실패하여 이름·화면은 별도 확인하지 못했다. 업로드 OAuth 권한은 아직 미연결이며 실제 게시한 영상은 없다. 채널 생성 절차는 완료한 사용자 단계로 처리한다.

## 개설에 사용할 값

- 채널명: **AI 실전노트**
- 한 줄 소개: **새로운 AI 소식부터 내 일에 쓰는 방법까지**
- 핸들 후보: `@ai-siljeonnote`, `@ai-practice-note`, `@ai-work-notes`. 사용 가능 여부는 개설 화면에서 확인해야 한다.
- 설명: `AI 도구·스킬·업데이트를 쉽게 소개하고, 내 일에 적용하는 방법을 안내합니다. 쇼츠에서는 한 가지 활용법을 짧게, 긴 영상에서는 근거와 사례를 바탕으로 분석합니다. 기능·사용 조건·실제 결과와 설명용 예시를 구분합니다.`
- 기본 언어: 한국어. 대상: AI를 실무·일상에 활용하려는 일반 사용자.
- 고정 음성: ElevenLabs Han Aim / eleven_v4. 전환 효과음 없음.

계정 이름과 채널 표시 이름은 다를 수 있다. 개인정보를 채널 설명에 넣지 않는다.

## 사용자가 직접 할 첫 단계

1. https://accounts.google.com/signup 에서 새 Google 계정을 만든다.
2. 그 계정으로 https://www.youtube.com/channel_switcher 에 로그인해 새 채널을 만들고 위 이름과 소개를 입력한다.
3. YouTube 고급 계정 설정 https://www.youtube.com/account_advanced 에서 `UC...` 형식의 채널 ID를 확인한다.

비밀번호·인증 코드·복구 코드는 채팅에 보내지 않는다. 채널 URL 또는 공개 채널 ID가 준비되면 다음 연결을 진행한다.

## 무인 업로드: 최초 한 번의 API 연결

현재 이 대화에는 YouTube 채널 생성/업로드용 커넥터와 브라우저 조작 도구가 없다. vidIQ 인증은 이 업로더의 OAuth를 대신하지 않는다. 계정 생성·로그인·Google 동의는 사용자가 직접 진행한다.

업로드를 실행할 동일한 상시 PC/호스트에서 아래를 준비한다. 이 대화의 클라우드 파일과 사용자 PC 파일이 자동으로 공유된다고 가정하지 않는다.

1. Google Cloud Console https://console.cloud.google.com/ 에 프로젝트를 만들고 YouTube Data API v3를 활성화한다.
2. Google Auth Platform에서 개인용 앱의 동의 화면을 설정하고 사용할 계정을 테스트 사용자로 추가한다. 테스트 상태의 refresh token은 7일 만료가 발생할 수 있으므로 2주 무인 운영 전 앱 상태·토큰 유지 조건을 확인한다.
3. OAuth 클라이언트 유형을 **Desktop app**으로 만들고 JSON을 다운로드한다. 비밀 파일은 Git이나 채팅에 올리지 않는다.
4. 저장소를 같은 PC에 체크아웃한 뒤 Python 환경을 준비하고 다음을 실행한다.

```bash
python -m pip install -r studio/youtube/requirements.txt
python studio/youtube/auth.py --client /PRIVATE/client_secret.json --token studio/youtube/.local/youtube-token.json --channel-id UCb6tSnNY6X3BtH-ujxMIf3g --activate-publishing
```

이 명령은 그 PC 브라우저에서 Google 로그인을 열고 선택한 실제 채널 ID가 일치하는지 검사한다. 일치한 경우에만 토큰을 저장하고 로컬 채널 프로필에 업로드를 활성화한다. callback은 PC localhost이므로 클라우드 터미널에서 실행한 URL을 다른 PC로 열어 연결하려 하지 않는다.

이후 같은 호스트의 업로더가 refresh token으로 권한을 갱신한다. 취소·만료·자격 부족이면 중지하며 다른 Google 계정으로 바꾸지 않는다. 토큰을 다른 호스트에 옮겨야 하는 경우 비밀 저장소를 사용하고 대화·Git에 남기지 않는다.

## 편성·제작·게시

- 2주 시험: AI 쇼츠 하루 3편 목표. 기본 후보는 소식 1, 활용법 1, 적용 사례 1이다. 검증한 소재가 없으면 낡은 소식을 새 출시로 꾸미거나 중복 영상을 올리지 않는다.
- 게시 슬롯 제안: KST 09:00, 14:00, 20:00. 최적 시간이라는 근거는 없으며 실제 성과로 조정한다.
- 롱폼은 칼럼형 제작 후보로 관리하며 별도 빈도는 아직 정하지 않았다.
- 퀴즈 채널 생성과 정기 운영은 보류한다.
- 예약 업로드는 명시적으로 private + 미래 publishAt을 사용한다. 실제 API ID와 응답이 있어야 업로드 성공으로 기록한다. 공개 완료는 별도 상태 확인 전 단정하지 않는다.
- 최초 후보는 엑셀 스킬 003편이다. 고정 보이스와 일치한다. 다른 샘플은 재녹음 전 게시하지 않는다. 첫 후보가 오래 대기하면 출처·내용을 재확인하고 현재 게시일의 새 미래 슬롯에 연결한다.

```bash
# 제작과 QA를 거쳐 큐에서 approved가 된 작업만 업로드한다.
python studio/youtube/publish.py --job-id JOB_ID --token studio/youtube/.local/youtube-token.json --channel-id UCb6tSnNY6X3BtH-ujxMIf3g
```

예외 발생 후 결과 불확실 상태에서는 Studio와 업로드 원장을 확인할 때까지 자동 재전송하지 않는다.

## 정기 실행 상태

2026-11-06: 이곳의 예약 작업 등록을 실제 시도했으나 `too_many_active_automations` (15/15)로 거절됐다. 예약 ID는 없고 새 작업이 실행 중이라는 뜻이 아니다. 다른 작업은 중지하지 않았다.

사용자는 기존 예약 한 자리 확보 또는 상시 PC 운영 중 선택할 수 있다. PC 운영 파일은 studio/operations/를 참고한다. 정기 실행 호스트에서 Codex 로그인, 외부 탐색, 고정 ElevenLabs 보이스 연결, 렌더 의존성, OAuth를 먼저 시험해야 한다. 앱의 커넥터가 별도 CLI에도 자동 제공된다고 가정하지 않는다. 제공 크레딧과 한도 내에서만 제작하고 추가 충전·구독·유료 재시도는 하지 않는다.

## 참고

- 채널 만들기: https://support.google.com/youtube/answer/1646861?hl=ko
- 업로드 API: https://developers.google.com/youtube/data/guides/uploading_a_video
- 예약 공개: https://developers.google.com/youtube/data/reference/rest/v3/videos#status.publishAt
- OAuth와 만료: https://developers.google.com/identity/protocols/oauth2#expiration
