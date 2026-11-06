# 실제 작업에서 콘텐츠로

우선 사용자의 실제 일을 해결하고, 그 작업의 입력·적용·산출물·검사를 기록한다. 작업 결과에서 공개할 수 있는 부분을 추려 조사 글·안내문·대본·영상으로 전환한다.

```text
내 실제 할 일 → 적용할 AI 후보 → 실행 → 산출물·검사·수정 → 업무에 사용
                                                       ↓
                         공개용 사례 → 쇼츠 안내 / 롱폼 분석 → 피드백 → 작업 개선
```

## 원본과 공개 자료

- `.local/work-cases/<id>/`: 작업 원문·내부 자료·원본 기록. Git 제외.
- `work-cases/<id>/task.md`: 작업 목적과 완료 기준.
- `execution.md`: 실제 실행과 수정 기록.
- `case.json`: 결과, 미완료 항목, 공개 범위, 증거 파일과 해시.
- `public-case.md`: 영상으로 풀어낼 공개용 설명.
- `channels/ai/episodes/`: 같은 사례를 짧은 안내 또는 칼럼으로 구성한 대본·장면·검수.

```bash
python scripts/content_studio.py work-case --id my-real-task
python scripts/content_studio.py new --channel ai --topic useful-tool --episode ai-005 --style shorts-ai-guide --work-case my-real-task
python scripts/content_studio.py new --channel ai --topic useful-tool --episode ai-long-002 --style longform-ai-column --work-case my-real-task
```

신규 AI 편은 실제 작업 사례에 연결해야 한다. 새로 만든 사례는 planned 상태이며 실행 증거를 남기기 전 직접 사용한 사례로 검수할 수 없다. 실제 적용 영상으로 명시한 제작 명세는 case 기록과 증거 해시를 검사한다. planned는 실패나 미완료를 감추기 위한 성공 상태가 아니다.

기능 확인과 실제 업무 효과를 구분한다. 모의 API 테스트를 실제 YouTube 업로드로 말하지 않는다. 측정하지 않은 시간·비용 절감률을 만들지 않는다. 실패·수정·적용하지 않은 이유도 콘텐츠가 될 수 있다.

쇼츠는 작업 하나의 문제·방법·확인한 결과를 짧게 설명한다. 롱폼은 배경·도구 선택 이유·시행착오·비교·한계·판단을 연결한다. 하나의 작업에서 여러 편을 만들 수 있지만 중복된 내용을 반복 게시하거나 하루 3편 때문에 필요 없는 작업을 만들지 않는다.

기존 AI 001~003편은 도구 소개·설명용 샘플이다. 실제 업무 적용을 증명한 편으로 소급 변경하지 않는다. 첫 실제 사례는 ai-channel-operations이며 코드와 로컬 검사를 확인했지만 Windows 실행·Google 인증·실제 업로드·전체 무인 운영은 아직 미완료다.

## 분야별 확장

현재 실행 분야는 video-channel이다. 게임·앱·Agent 분야는 향후 확장 범위이며 이 요청으로 새 개발 작업을 시작한 것은 아니다. 분야가 늘어도 AI 실전노트의 실제 적용 사례로 묶고 채널을 임의로 추가하지 않는다.

| domain | 실제 작업 | 업무에 남길 재사용 산출물 | 영상 소재 |
|---|---|---|---|
| video-channel | 제작·자막·렌더·업로드 | 편집 템플릿, 코드, 운영 규칙 | 만든 과정·검사·막힌 부분·개선 |
| game-development | 게임 기능·플레이테스트 | 프로젝트 코드, 에셋 제작 흐름, 검사 기록 | 구현 전후·실패·수정 과정 |
| app-development | 앱 기능·테스트·배포 준비 | 앱 코드, UI, 테스트, 작업 흐름 | 실제 기능 구현과 검증 |
| agent-setup | Agent 역할·도구·메모리·연결 | 설정, 프롬프트, 워크플로우, 실행 검사 | 세팅 이유·실행 결과·유지보수 |

```bash
python scripts/content_studio.py work-case --id my-game-feature --domain game-development
python scripts/content_studio.py work-case --id my-app-feature --domain app-development
python scripts/content_studio.py work-case --id my-agent-setup --domain agent-setup
```

명령은 작업 기록만 만들며 게임·앱·Agent를 자동으로 완성하지 않는다. 각 작업은 목적·완료 기준·실제 산출물과 증거를 별도로 확보한다. 비밀 값이 없는 재사용 설정과 민감한 실행 설정을 분리한다.
