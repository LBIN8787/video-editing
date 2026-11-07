# 반복 콘텐츠 제작 스튜디오

최신 제작 기준과 실행 순서는 [SHORTS-WORKFLOW.md](SHORTS-WORKFLOW.md)다. 승인된 시각 안내형 1.1.0 디자인을 데이터 입력으로 재사용하는 1.1.1 / ShortsGuideTemplate이 기본이다.

```text
실제 업무 → AI 적용과 증거 → 출처·조사 글 → production-brief
                                           ↓
                         고정 음성 → 단어별 시간 → props → MP4
                                           ↓
                       장면·자막·음량 검수 → Git/Drive 보관
                                           ↓
                               별도 게시 검수 → YouTube
```

| 경로 | 책임 |
|---|---|
| channels/ai/channel.json | 채널 ID·고정 음성·현재 스타일 |
| styles/shorts-ai-guide/profile.json | 활성 버전·공통 렌더 구성 |
| studio/templates/shorts | 새 편 제작 양식 |
| schemas/shorts-production-brief.schema.json | 입력 데이터 규격 |
| channels/ai/episodes/<편>/revisions/<버전> | 수정본 입력·음성 상태·검수·보관 위치 |
| content/topics | 공식 출처·조사 글·안내문 |
| work-cases | 실제 업무와 실행 증거·미완료 범위 |
| scripts/prepare_visual_short.py | 원고 추출·음성/타이밍 검증·props 준비 |
| scripts/render_short.py | 버전별 고정 입력 검사·MP4 출력 |
| .github/workflows/content-studio.yml | 구성 일치·코드·정책 검사. 유료 음성 생성/게시 아님 |

신규 AI 편은 실제 작업 사례가 필요하다. 예전 소개 샘플 재편집은 실행 사례로 소급하지 않는다. AI Shorts 목표는 하루 3편이지만 무인 정기 작업은 아직 비활성이다. 퀴즈는 보류했고 롱폼 렌더러와 빈도는 미완성이다.

Windows 작업 PC의 Google OAuth와 실제 ai실전노트 채널 ID 조회는 확인했다. 인증 정보는 PC의 무시된 로컬 폴더에만 있다. 실제 업로드·예약 공개·주기적 제작은 별도 검증 대상이다. 예약 작업 생성은 이전에 15/15 한도로 실패했으며 이번 문서 갱신으로 등록되지 않는다.

001·002 최신 화면은 고정 ElevenLabs 음성 생성 혼잡으로 무음 검토본이다. 과금·TTS 대체는 없었다. 003은 기존 고정 음성, 005·006은 승인된 수정본을 유지한다. 이전 영상·작업 초안은 덮어쓰지 않는다.

소스·글·입력·검수는 Git에, 미디어·DB·로그·인증은 로컬/외부에 둔다. 기존 Drive 보관 폴더를 사용하며 업로드 후 메타데이터로 확인한다. 기존 ytflow의 다른 채널·전역 TTS 설정과 현재 스튜디오를 혼동하지 않는다.
