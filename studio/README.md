# 반복 제작 스튜디오

한 번 만들고 끝내는 영상이 아니라, 조사·글·대본·시각화를 반복하는 프로젝트다. 글로 답하던 정보 탐색을 검증된 콘텐츠로 정리하고 채널과 길이에 맞춰 영상화한다.

```text
공식 소스·커뮤니티 탐색 → 조사 원장 → 안내문/분석 글
                                    ├─ 쇼츠: 질문 하나 → 짧은 안내 → 적용 예시
                                    └─ 롱폼: 주장 → 근거 → 사례 → 반론 → 판단
                                              ↓
                              대본 → 장면 → 고정 음성 → 자막 → MP4 → 검수
```

| 경로 | 역할 |
|---|---|
| channels/ai, channels/quiz (저장소 루트) | 채널 정체성·고정 보이스·편별 기록 |
| content/topics (저장소 루트) | 재사용할 출처·조사·글 |
| styles (저장소 루트) | 채널과 독립된 편집 규칙 |
| studio/prompts | 조사 글을 대본과 화면으로 바꾸는 지시문 |
| studio/renderer | 기존 Remotion 영상 소스와 자막 |
| studio/automation | 큐·고정 음성 검사·렌더·파일 QA |
| scripts/content_studio.py | 채널·주제·스타일로 다음 제작 폴더 생성 |

## 새 영상 시작

```bash
python scripts/content_studio.py new --channel ai --topic example-tool --episode ai-004 --style shorts-ai-guide
python scripts/content_studio.py new --channel ai --topic example-tool --episode ai-long-001 --style longform-ai-column
python scripts/content_studio.py inventory
```

두 번째 명령은 같은 조사 글을 재사용한다. 이미 있는 글이나 영상 기록을 덮어쓰지 않는다. 생성 명령은 작업 문서만 만들며 대본 작성·유료 음성·렌더·예약·업로드를 자동 실행하지 않는다.

## 권한과 현재 상태

계정·업로드·자동 정기 실행은 샘플 피드백 전 보류. 목표는 채널별 하루 3편이며 롱폼 3편/일이라는 뜻은 아니다. 롱폼은 제작 형식으로 추가했고 빈도는 미정이다. 퀴즈 대상과 학습/오락 방향은 미확정이다.

소스 탐색부터 새 영상까지 무인 제작하는 연결은 미완성이다. 독립적으로 실행 가능한 기존 큐/QA와 Remotion 코드를 정리했으며, 전체 운영 상태는 automation/README.md와 docs/06-ai-production-audit.md를 본다.

기존 ytflow는 별도 제작 경로다. 기존 전역 TTS 설정을 이 두 채널에 그대로 적용하지 않는다. 새 채널은 channels/<id>/channel.json의 고정 보이스를 따르고, 자동 생성 연결 전까지 다른 경로로 우회 실행하지 않는다.

## 복구와 미디어

소스·대본·기획·검수 기록은 Git에, MP4·음성·자료 이미지는 로컬/외부 아티팩트 저장소에 둔다. 각 편 episode.json과 renderer/assets-index.json에 파일명·체크섬을 기록했다. 이번 정리는 MP4를 GitHub에 업로드하거나 외부 저장소를 새로 연결한 것이 아니다.

기존 작업 원본은 /workspace/ai-radar-short와 /workspace/shorts-automation에 남아 있다. 새 체크아웃에서 미디어를 복구한 뒤 npm ci로 의존성을 설치한다. 의존성·미디어가 없는 fresh clone에서 바로 렌더된다고 주장하지 않는다.
