# Windows에서 AI 실전노트 업로드 연결

연결할 채널: https://www.youtube.com/channel/UCb6tSnNY6X3BtH-ujxMIf3g

채널은 생성된 상태다. 아래는 이 PC가 그 채널에 영상을 업로드할 수 있게 허용하는 최초 1회 설정이다. 실행 파일은 아직 실제 업로드나 예약 작업을 시작하지 않는다.

## 1. Google에서 인증 설정 파일 받기

새 채널을 만든 Google 계정으로 아래 작업을 한다.

1. [Google Cloud 프로젝트 만들기](https://console.cloud.google.com/projectcreate): 프로젝트 이름은 `AI 실전노트 운영`으로 입력한다. 만든 프로젝트가 선택돼 있는지 확인한다.
2. [YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com): **사용**을 누른다.
3. [Google Auth Platform](https://console.cloud.google.com/auth/overview): 시작하기에서 앱 이름 `AI 실전노트 업로드`, 지원 이메일과 연락 이메일은 본인 이메일로 입력한다. 개인 Google 계정의 대상은 **외부**를 선택한다.
4. [대상(Audience)](https://console.cloud.google.com/auth/audience): 테스트 사용자에 새 채널의 Google 계정을 추가한다.
5. [클라이언트](https://console.cloud.google.com/auth/clients): **클라이언트 만들기 → 데스크톱 앱**으로 생성하고 JSON을 다운로드한다. 웹 앱이나 서비스 계정 키는 사용하지 않는다.

Google 동의 화면과 새 OAuth 클라이언트는 사용자의 Google Cloud 프로젝트에서 만들어야 한다. 현재 이 대화에 해당 프로젝트 접근 권한이 없어 대신 생성하지 못했다. JSON은 비밀 파일이므로 채팅·GitHub에 올리지 않는다.

## 2. 연결 실행

1. 받은 ZIP을 `C:\AI-Notes` 같은 폴더에 **압축 해제**한다. ZIP 안에서 바로 실행하지 않는다.
2. 폴더 안의 **CONNECT-YOUTUBE.cmd**를 더블클릭한다.
3. Python이 없으면 설치 페이지가 열린다. Python 3.11 이상을 설치하면서 Add Python to PATH를 체크한 뒤 다시 실행한다.
4. 파일 선택 창에서 1단계의 JSON을 선택한다. Google 라이브러리가 해당 폴더의 전용 Python 환경에 설치된다.
5. 브라우저가 열리면 새 채널 계정으로 로그인하고 요청한 YouTube 업로드·조회 권한을 허용한다.
6. 콘솔에 **SUCCESS**가 나오면 연결 완료다. 다른 채널을 선택했다면 일치 검사에서 중지한다.

연결 결과는 이 PC에만 저장된다. 비밀번호·인증 코드·JSON·토큰 대신 **연결 성공 여부**만 알려주면 된다. `studio/youtube/.local/`은 Git에서 제외된다.

## 3. 연결 다음에 할 일

- 이 PC와 현재 클라우드 작업 공간은 자동으로 파일·인증을 공유하지 않는다.
- 최초 후보 MP4와 음성이 들어 있는 전달 ZIP에는 복사본을 동봉했다. GitHub 소스 ZIP만 받은 경우 미디어는 별도 복원이 필요하다.
- 연결 후 첫 업로드와 실제 YouTube ID·예약 시간을 확인한다. 현재 실행 파일은 업로드 명령을 호출하지 않는다.
- 이후 하루 3편 제작·업로드를 위한 실행 호스트를 확정한다. Windows라고 답한 것이 상시 PC 운영 방식까지 선택했다는 뜻은 아니다.
- ChatGPT 예약은 15/15 한도로 등록 실패 상태다. 기존 예약 한 자리 확보 또는 이 PC의 예약 운영 중 선택이 남아 있다.
- PC 운영 시 Codex 로그인·ElevenLabs 고정 보이스 연결·렌더 환경을 같은 PC에서 별도로 시험한다. 인증만으로 새 영상 자동 제작까지 완료되는 것은 아니다.

Google OAuth 앱이 테스트 모드인 경우 refresh token의 7일 만료 조건이 있으므로, 2주 무인 운영 전 앱 상태와 토큰 유지 조건을 확인한다.
