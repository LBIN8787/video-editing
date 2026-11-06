# AI 채널 운영 연결

계정 개설·운영 요청에 따라 AI만 활성 운영 대상으로 설정했습니다. 큐 worker는 아직 비활성이고 채널 OAuth 연결 전 업로드를 차단합니다. studio/youtube/에 업로더를 추가했습니다. channels/ai/launch/README.md가 최신 안내입니다. 기존 점검 문서는 당시 상태의 이력입니다.

# 반복 작업 큐와 검수

원본 shorts-automation 코드를 저장소 상대 경로로 옮겼다. 채널 보이스의 원본은 ../../channels/<id>/channel.json이다. settings.json은 실행 단계와 목표만 관리한다.

```bash
cd studio/automation
python -m unittest -v test_workflow.py test_content_policy.py
python runner.py
```

runner는 automation_enabled=false이므로 중지된다. 새 정기 실행은 만들지 않았다. plan은 채널별 하루 3개 슬롯, bind/build/approve/export는 고정 음성·활용형 필수 항목과 미디어를 검사한다. DB·로그·health와 업로드 묶음은 Git 제외다.

manifests/ai-003-fixed-voice.json은 현재 보이스에 맞는 과거 샘플 명세다. 먼저 미디어를 복원해야 bind가 가능하다. 같은 명세를 반복 게시하는 용도가 아니다. 새 대본·음성·장면을 자동 생성하는 연결은 아직 없다.

원본 점검 보고서 automation-audit.md는 이전 로컬 환경에서 수행한 시험 기록이다. 현재 저장소의 새 제작 명령은 scripts/content_studio.py이며 작업 문서만 생성한다. 새 환경의 전체 생성·정기 실행 검증과 업로드 인증은 별도로 남아 있다.
