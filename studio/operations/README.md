# 정기 실행 호스트

이 파일들은 등록 가능한 실행안이며 이 대화에서 PC 예약을 설치한 것은 아니다. ChatGPT 예약은 15/15 한도로 실제 생성이 실패했다.

PC 운영을 선택하면 저장소·미디어·Codex 로그인·외부 탐색·ElevenLabs 연결·YouTube OAuth가 **같은 PC**에 있어야 한다. 앱의 연결이 CLI에도 자동 제공되는 것은 아니다. 이 계정의 브라우저 세션을 다른 호스트로 복사하지 않는다.

1. 작업 PC에서 `python studio/operations/daily_worker.py`로 한 번 실행하고 보고서와 실제 새 MP4를 확인한다. 이 명령은 Codex를 호출하며 실제 작업을 시작한다.
2. 고정 보이스·렌더·OAuth 연결을 시험한 뒤 예약한다.
3. Windows는 PC 시간대를 한국으로 맞춘 뒤 `register-windows.ps1 -PythonExe <가상환경 Python 경로>`를 실행한다. 매일 07:30, 같은 사용자 로그인 환경에서 실행된다.
4. Linux는 상시 호스트의 cron에서 `30 7 * * * /ABS/PYTHON /ABS/REPO/studio/operations/daily_worker.py`를 등록한다. cron 시간대는 Asia/Seoul로 설정한다. 이번 클라우드에는 cron이 없어 설치하지 않았다.

하루 한 번의 에이전트 작업에서 3편을 준비해 YouTube API의 미래 공개 시간으로 각각 예약한다. PC가 꺼져 있거나 인증·모델·네트워크가 끊기면 제작은 완료되지 않는다. 실패 보고서의 차단 사유를 해소하고, 불확실한 업로드를 임의로 반복하지 않는다.

로컬 로그·작업 원장·잠금 파일은 .local/ 아래에 보관하고 Git에서 제외한다. 첫 전체 시험 전 '완전 자동 운영 중'이라고 표시하지 않는다.
