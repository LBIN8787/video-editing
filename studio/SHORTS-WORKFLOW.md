# AI 실전노트 제작 기준과 반복 워크플로우

사용자가 승인한 화면 기준은 **시각 안내형**이다. 날짜·상단 회차를 빼고, 무엇을 준비해 어디에 넣고 어떤 결과를 받는지 보여 준다. 1.1.1 / ShortsGuideTemplate은 승인한 1.1.0 디자인을 데이터 입력 방식으로 일반화한 패치다. 과거 버전은 재현용으로 보존한다.

## 한 편의 양식

| 항목 | 반드시 적을 것 | 화면 예시 |
|---|---|---|
| 질문 하나 | 이 영상으로 해결할 작업 | 정리 전 표·수정이 막힌 슬라이드 |
| 준비할 입력 | 파일·작업 환경·선행 설치 | 프로젝트 폴더와 선택할 파일 |
| 실행할 행동 | 어디에 어떤 요청을 넣는지 | 복사할 요청문·필요한 명령 |
| 결과 | 실제 파일 또는 명확히 표시한 설명용 예시 | 정리 후 표·텍스트 선택·결과 미리보기 |
| 검수 | 사용자가 직접 확인할 항목 | 원문·합계·수식·선택 개체·자막 시간 |
| 조건 | 설치·연결·비용·한계 | 실행 전 확인 흐름 |

자료가 없는 자리를 일반 글 목록으로 채우지 않는다. 기존 `flow/files/prompt/commands/browser/table/slides/image/check` 블록에 `visual_data`만 교체한다. 임의 CSS·폰트·좌표는 입력 양식에 넣지 않는다. 실제 실행 결과와 재구성 화면은 구분한다. 인기를 입증하지 않은 숫자·측정하지 않은 절감률을 만들지 않는다.

## 제작 순서

1. 실제 업무 하나를 고르고 공식 출처를 확인한다. 신규 AI 편은 작업 사례를 먼저 실행하고 증거를 남긴다. 예전 소개 샘플의 화면을 고쳤다고 실제 도구를 사용한 사례로 바꾸지 않는다.
2. `content_studio.py`로 작업과 편을 만들고 생성된 `production-brief.json`을 채운다. 출처·핵심 입력/행동/결과·장면별 내레이션·시각 자료를 적고 검수한 뒤 `editorial_reviewed`를 true로 한다.
3. 채널 설정에 있는 **ElevenLabs Han Aim / eleven_v4**를 사용한다. 이미 같은 대본의 음성이 있으면 재사용한다. 대본당 1회 생성하며 실패·혼잡이면 다른 보이스로 대체하거나 연속 재시도하지 않는다. 생성 ID·파일 해시·비용·실제 상태를 기록한다. 키·토큰은 Git에 넣지 않는다.
4. 고정 음성 파일의 로컬 Whisper 인식 결과로 자막 시간을 만든다. `transcribe_short.py`는 음성 인식만 하며 새 음성을 생성하지 않는다. 제품명·숫자를 원문 대조한다.
5. `prepare_visual_short.py`로 brief와 단어별 시간을 props로 변환한다. 자동 정렬이 불확실하면 해당 장면의 `start_ms`를 직접 검수해 입력한다. 음성 메타데이터는 provider/voice_id/model_id/fallback_used/sha256을 포함해야 한다.
6. `render_short.py --check-only`로 고정 폰트와 입력을 검사하고, 미리보기에서 제목·자료·자막이 겹치지 않는지 본다. MP4를 출력한다.
7. 최종 MP4의 모든 장면 중간과 끝 0.3초 전 프레임, 전체 디코딩, 음량, 자막 시간을 확인한다. 직접 청취 여부도 기록한다. 확인하지 못한 것을 완료로 표시하지 않는다.
8. 소스·대본·검수는 GitHub에, 미디어·복원 패키지는 기존 Drive 보관 폴더에 넣는다. 파일명에 버전을 명시하고 업로드 후 크기·부모 폴더를 읽어 확인한다. `active_revision_ref`로 최신 입력을 가리킨다.
9. 영상 제작·보관과 YouTube 게시를 분리한다. 무음 미리보기·음성 미검증·검수 미완료 파일은 게시하지 않는다. 정기 작업은 현재 비활성 상태이며 이 문서를 갱신했다고 하루 3편이 예약되는 것은 아니다.

```bash
python scripts/content_studio.py work-case --id my-real-task
python scripts/content_studio.py new --channel ai --topic my-tool --episode ai-007 --style shorts-ai-guide --work-case my-real-task

# production-brief.json을 완성·검수한 뒤 읽을 원고를 추출
python scripts/prepare_visual_short.py --brief channels/ai/episodes/ai-007/production-brief.json --export-narration --out channels/ai/episodes/ai-007/narration.txt

# 같은 원고의 고정 ElevenLabs 음성과 메타데이터를 준비한 뒤
python studio/renderer/tools/transcribe_short.py --audio studio/renderer/public/ai-007/voice.mp3 --prompt channels/ai/episodes/ai-007/narration.txt --out channels/ai/episodes/ai-007/words.json
python scripts/prepare_visual_short.py --brief channels/ai/episodes/ai-007/production-brief.json --words channels/ai/episodes/ai-007/words.json --out channels/ai/episodes/ai-007/props.json
python scripts/render_short.py --props channels/ai/episodes/ai-007/props.json --check-only
python scripts/render_short.py --props channels/ai/episodes/ai-007/props.json --out studio/renderer/out/ai-007.mp4
```

Windows에서는 `PYTHONUTF8=1`과 설치한 Chromium 경로 `--browser`를 사용한다. 로컬 인식에는 faster-whisper 모델과 실행 자원이 필요하다. Remotion 라이선스·AI 도구·음성 요금은 각 사용 조건을 따른다.

## 음성 생성이 막혔을 때

최종 영상은 음성이 없으면 준비·렌더 검증에서 중단된다. 화면 피드백이 필요한 경우에만 `--silent-preview`를 사용한다. 화면에 **무음 미리보기**가 표시되고, MP4 파일명에 `PREVIEW`가 있어야 한다. 시간은 추정치이므로 음성이 생기면 Whisper로 다시 맞추고 최종 QA를 반복한다. 이 파일을 완성된 고정 음성 영상으로 등록하지 않는다.

```bash
python scripts/prepare_visual_short.py --brief channels/ai/episodes/ai-007/production-brief.json --silent-preview --out channels/ai/episodes/ai-007/preview-props.json
python scripts/render_short.py --props channels/ai/episodes/ai-007/preview-props.json --silent-preview --out studio/renderer/out/ai-007-PREVIEW-MUTED.mp4
```

## 현재 이전 편 갱신 범위

001·002는 새 고정 음성 생성이 무료 서비스 혼잡으로 시작되지 않아 화면·자막 미리보기만 준비했다. 과금과 다른 TTS 대체는 없다. 003은 기존 검증된 ElevenLabs 음성을 재사용한다. 005·006은 이전에 승인받은 수정 MP4를 유지한다. 004는 실제 MP4가 없던 작업 초안이며, 퀴즈 채널은 보류 상태다.
