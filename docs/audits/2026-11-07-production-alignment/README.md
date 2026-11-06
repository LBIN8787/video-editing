# Claude·Codex 영상 운영/보관 체계 비교

점검일: 2026-11-07 KST. 사용자가 Claude 쪽에서 올린 자료와 이 대화의 자료가 서로 다른 운영 규칙·폴더에 흩어져 있는지 확인해 달라고 요청했다.

## 결론

같은 저장소를 사용하지만 현재 하나의 운영 체계로 통합된 상태는 아니다. GitHub의 main(ytflow)과 organize/channel-content-studio(실제 작업·Remotion)가 분리되어 있고, Drive도 ytflow 영상과 AI 실전노트 쇼츠 자동화 보관이 서로 다른 최상위 폴더다. 공통 목표는 같지만 설정·실행기·산출물 구조·보관 정책은 다르다.

이 점검에서는 파일을 삭제·이동하거나 실행 중인 작업을 변경하지 않았다. 기존 자료를 유지하고 공통 위치 안내와 차이 목록을 남겼다. 작성 주체는 파일/커밋만으로 단정하지 않고 사용자가 지칭한 Claude 쪽은 최신 main 자료로 비교했다.

## 비교 기준과 증거

- main 스냅샷: d497f36 (config/storage.yaml, channels/ch-ai-shorts/channel.yaml, docs/06-operations.md, docs/08-voice.md, docs/09-storage.md, ytflow/stages/upload.py)
- 이 대화의 코드 스냅샷: 4f01520 (channels/ai/channel.json, styles/shorts-ai-guide/style-lock.json, studio/automation, studio/youtube)
- 고정 스타일 릴리스: shorts-ai-guide-v1.0.0 → 4f01520
- Drive: 아래 폴더 목록과 워크플로우 기준 문서를 커넥터로 실제 읽어 확인했다. 영상 내용 전체의 청취·시청 검사는 이번 범위가 아니다.

## 운영 규칙 차이

| 항목 | main / ytflow 쪽 | 이 대화 / AI 실전노트 쪽 |
|---|---|---|
| 채널 식별 | ch-ai-shorts, 가칭 AI 꿀팁 1분, 실제 YouTube ID 없음 | ai, 실제 대상 UCb6tSnNY6X3BtH-ujxMIf3g |
| 운영 편수 | 주 3~5편 | 하루 3편 목표 |
| AI 콘텐츠 | 저장소/도구 안내 중심 | 사용자 실제 작업 적용 → 결과·검사 → 공개용 사례 중심 |
| 쇼츠 길이 | 30~45초, 채널 목표 40초 | 기본 45~60초, 파일 QA 허용 범위는 10~60초 |
| 편집 | shorts-aitips, 검정/흰색/노랑, NanumGothic, 70px 자막 | shorts-ai-guide 1.0.0, 종이색/녹색/라임, 고정 Noto, 54px 자막 |
| 음성 | 기본 초안 Edge, 최종 ElevenLabs이지만 voice_id 미정; 예시 모델 multilingual_v2 | Han Aim / eleven_v4 고정, 임의 대체 금지 |
| 음량 | -14 LUFS 기본 | -16 LUFS 목표 |
| 채널·스타일 관계 | 스타일 하나 = 채널 하나 | AI 한 채널에서 안내 쇼츠·칼럼 롱폼 및 여러 업무 분야 |
| 작업 기록 | projects/<날짜-프로젝트>/00_source~06_package, channels/*/episodes.md | work-cases/, content/topics/, channels/ai/episodes/, SQLite 큐 |
| 렌더러 | Python/FFmpeg, HyperFrames·rough.js 등 | Remotion / ShortsGuideV1 |
| upload 명령 | Google Drive 보관 | studio/youtube/publish.py는 YouTube API 전송 |
| 음성·복원 | 음성을 재생성 가능한 것으로 분류해 일반 보관에서 제외 | 동일 스타일 복원을 위해 고정 폰트·기존 음성·기준 MP4·해시를 ZIP에 포함 |

ch-ai-shorts와 ai를 이름이 비슷하다는 이유만으로 동일 실제 YouTube 채널로 확정하지 않는다. 현재 실제 채널 ID가 확인된 것은 이 대화의 ai 설정이다. 기존 ytflow의 주기·스타일·보이스를 이 채널에 그대로 적용하면 사용자 요청과 달라진다. 다른 경제·롱폼 채널은 별도 기획으로 보존한다.

## Drive에 실제 있는 것

| 위치 | 역할 | 확인한 상태 |
|---|---|---|
| [ytflow 영상](https://drive.google.com/drive/folders/16Y2oMXY7Ze_4yQP3Omlqll9rUwWPJvnu) | 여러 채널의 영상·원고·자료 진입점 | 채널별·실험 폴더 직접 포함 MP4 합계 9개 확인 |
| [워크플로우 문서](https://drive.google.com/drive/folders/1YeHhwSfReqx1XOqGnH_PxSehDx2ItKg8) | GitHub main의 읽기용 사본 | Google Docs 9개 확인 |
| [AI 꿀팁 폴더](https://drive.google.com/drive/folders/1f0SYDO5VMUdpfll-FgnbjSbxevGSMP2i) | ch-ai-shorts 결과물 위치 | 원고·업로드 문구 Doc 1개, 직접 포함 MP4는 이번 조회에서 없음 |
| [보관 자료](https://drive.google.com/drive/folders/1E8H46Mgh2kcniwrIgdyoU8Ftfbb_TT4E) | 재료·자료의 프로젝트별 보관 | 프로젝트별 하위 폴더 존재 |
| [AI 실전노트 쇼츠 보관](https://drive.google.com/drive/folders/1hwqNs_zIaOkP8KZp3g95htzkW7tlW0qs) | 고정 스타일 v1 복원본 | 안내서·31,562,605바이트 ZIP·기준 MP4·해시 JSON 4개 확인 |

main 쪽 docs/09-storage.md는 '영상 16개를 아직 못 올렸다'고 적고 있으나, 현재 목록에서는 일부 영상이 실제 올라와 있다. 상태 문서가 후속 업로드를 따라가지 못한 것으로 보이며 '모두 미업로드'로 판단하면 안 된다. Drive의 upload는 YouTube 게시 증거가 아니다.

## 이름·파일 검사의 문제

1. 실험 폴더에는 같은 제목의 MP4가 3개 있다. 크기는 각각 3,278,134 / 12,082,242 / 6,881,143바이트로 다르다. 같은 이름이지만 같은 파일이라고 단정할 수 없다.
2. main 업로더의 파일명은 프로젝트 전체 ID가 아니라 앞 8자리 날짜와 제목을 사용한다. 같은 날짜·제목의 서로 다른 프로젝트가 같은 폴더에서 같은 이름이 될 수 있다.
3. main 업로더는 기존 기록과 파일 크기만 비교해 재업로드를 건너뛴다. 네트워크 없는 임시 폴더 시험에서 AAAA → BBBB(동일 4바이트)로 바꿔도 두 번째 전송 함수가 호출되지 않는 것을 재현했다. archive 경로도 크기 비교다. 이 점검에서 실제 Drive 전송은 하지 않았다.
4. final.mp4가 없으면 draft.mp4를 같은 최종 파일명 형태로 보관한다. 보관 자체와 게시 승인은 구분해야 한다.
5. 원래 음성과 가격 자료를 재생성하면 동일한 스타일은 유지할 수 있어도 이전 영상과 동일한 출력이 보장되지 않는다. 고정 버전과 당시 입력을 함께 보관해야 한다.

## GitHub 통합 상태

PR #1은 아직 main과 병합되지 않았다. `git merge-tree --write-tree --name-only origin/main HEAD`로 작업 트리를 건드리지 않고 병합 가능성을 확인했으며 .gitignore와 channels/README.md 두 파일에서 충돌을 확인했다. 자동 병합 가능한 파일도 내용상 '스타일 하나=채널 하나'와 AI 실전노트의 다중 형식 규칙을 별도로 조율해야 한다. 이 점검에서 main에 강제 병합하지 않았다.

## 공통 보관 형식

향후 작성자와 도구가 달라도 아래 식별자를 남긴다.

- channel_id: 내부 채널 ID와 실제 YouTube ID를 구분.
- work_case_id / episode_id: 실제 작업과 영상 회차의 고유 ID.
- format / style_id / style_version: 쇼츠·롱폼과 편집 스타일을 분리.
- artifact_role: source, narration, captions, preview, final, upload_metadata, restore_bundle 중 역할.
- stage: draft, qa_passed, drive_archived, youtube_uploaded, scheduled, published를 구분.
- source_commit / sha256: 당시 소스와 실제 파일을 식별.
- storage_url: 실제 업로드가 확인된 파일 주소만 기록.

이것은 통합 운영 제안/색인 기준이며 두 실행기가 이미 같은 설정을 자동으로 읽는다는 뜻은 아니다. v1.0.0 릴리스와 원본 파일은 변경하지 않고 보존한다.

## 우선순위

1. 개설된 AI 실전노트의 고정 설정을 기준으로 상대 체계의 AI 초안 채널과 대응 여부를 정리한다. 확인 전 임의로 별도 계정을 만들거나 같은 채널에 서로 다른 스타일로 게시하지 않는다.
2. GitHub의 main/PR 충돌을 검토해 병합하고 공통 채널·보이스·편수 규칙을 한곳에서 읽도록 연결한다.
3. Drive에 이 통합 위치 안내를 두 보관 진입점에 같은 내용으로 두어 서로를 찾을 수 있게 한다. 원본 폴더와 공유 권한은 유지한다.
4. 파일명에 프로젝트/회차 ID·역할·스타일 버전을 넣고, 중복 판단은 이름이나 크기가 아닌 SHA-256을 사용하도록 업로더를 고친다.
5. 오래된 상태 문서와 목록을 실물 파일 목록·영수증에 맞춰 갱신한다. YouTube 실제 게시 완료로 표시하는 것은 OAuth/API 확인 뒤다.

이번 결과는 운영/보관의 실제 차이를 확인한 점검이다. 실행기 전체 통합이나 폴더 이동을 완료한 결과로 표시하지 않는다.
