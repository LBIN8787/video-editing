# AI 실전노트 쇼츠 자동화 보관본 v1.0.0

여러 번 제작해도 같은 편집 스타일을 유지하기 위한 기준 소스·설정·입력 예시·폰트·기준 영상의 보관본이다. 기존 AI 실전노트의 종이색·짙은 녹색·라임 강조와 상하 배치를 재사용 템플릿으로 정리했다. 엑셀 설명 영상의 기존 ElevenLabs 음성을 사용해 기준 MP4를 만들며 새 유료 음성 생성은 하지 않았다.

## 고정되는 것

| 항목 | 고정 값 |
|---|---|
| 스타일 / 렌더러 | shorts-ai-guide 1.0.0 / ShortsGuideV1 |
| 화면 | 1080×1920, 30fps |
| 색 | 종이색 #f3f1e8 / 짙은 녹색 #19231e / 라임 #d4f85a |
| 서체 | 보관한 Noto Sans CJK KR Regular/Bold, 파일 해시 검사 |
| 제목 | 84px, 최대 두 줄, 줄당 10자 제한 |
| 본문 | 40px, 고정 카드, 최대 3개 항목 |
| 자막 | 54px, 왼쪽 80px·상단 1380px, 짙은 녹색 배경 |
| 배치 | 공통 헤더·제목·본문 카드·자막·출처·진행 표시 위치 |
| 움직임 | 5프레임 등장, 12프레임 상승, 공통 spring 값 |
| 음성 | ElevenLabs Han Aim / eleven_v4 |
| 소리 | 전환 효과음·배경음악 없음, -16 LUFS 목표 |
| 출력 | H.264 / AAC / yuv420p / 48kHz / faststart |

숫자는 style-lock.json과 공통 컴포넌트에 보관한다. 편별 입력에서 임의 색·글자 크기·CSS를 넘기지 못하도록 검사한다. 디자인 변경은 새 버전과 새 기준 프레임으로 남긴다.

## 편마다 바꾸는 것

회차, 자료 확인일, 출처, 제목·설명, 실제 작업 화면, 내레이션 파일, 자막, 장면별 길이. 날짜를 하드코딩한 옛 샘플과 달리 새 템플릿은 checkedAt 입력을 사용한다.

현재 공통 템플릿은 카드와 선택적인 실제 자료 이미지에 대응한다. 복잡한 차트·다른 편집 스타일은 별도 버전으로 추가한다. 실제 업무 사례가 기본이며 설명용 예시를 직접 실행한 결과처럼 표시하지 않는다.

## 다음 제작 순서

1. 실제 작업의 목적·실행·결과를 work-cases/에 남긴다.
2. 조사 글을 정리하고 쇼츠 대본과 장면을 작성한다.
3. 채널 고정 보이스로 생성한 음성을 public/에 놓고 타이밍을 맞춘다.
4. reference-props.json을 복사해 내용만 바꾼다. 색상·크기·좌표는 바꾸지 않는다.
5. 아래 입력 검사를 통과시킨 다음 같은 렌더러로 MP4를 출력한다.
6. 주요 프레임과 자막·음성·전체 파일을 확인한 후 별도 업로드 큐로 넘긴다.

```bash
# 저장소 루트. 보관 ZIP은 이 상대 경로 구조로 압축 해제한다.
cd studio/renderer
npm ci
cd ../..
python scripts/render_short.py --props studio/renderer/src/template/reference-props.json --check-only
python scripts/render_short.py --props studio/renderer/src/template/reference-props.json --out studio/renderer/out/shorts-guide-v1-reference.mp4 --browser /usr/bin/chromium
```

Windows에서는 설치된 Chrome/Chromium 실행 파일 경로를 --browser에 지정한다. Node 24, Python 3.11 이상, FFmpeg/FFprobe가 필요하다. 기준 환경의 상세 버전과 파일 해시는 보관 ZIP 안 ARCHIVE-MANIFEST.json에 있다. Windows에서 전체 실행을 검증한 것은 아니다.

## 파일 구성과 복원

- styles/shorts-ai-guide/style-lock.json: 스타일 버전과 고정 규칙.
- studio/renderer/src/template/: 공통 React 템플릿, 기준 내용 입력.
- scripts/render_short.py: 내용·폰트 검사, 렌더, 음량 정리, 전체 디코딩 검사.
- studio/renderer/package-lock.json: npm ci에 사용할 의존성 잠금.
- studio/renderer/public/fonts/: 동일 글꼴. Git에는 바이너리 대신 해시·라이선스를 두고 보관 ZIP에 실제 파일을 포함한다.
- studio/renderer/public/episode-003/voice.mp3: 기준 영상 재현용 기존 음성.
- studio/renderer/out/shorts-guide-v1-reference.mp4: 편집 스타일의 기준 영상.
- ARCHIVE-MANIFEST.json: 소스 커밋, 환경, 파일별 SHA-256.

GitHub에는 버전 관리용 원본, Drive에는 복원에 필요한 폰트·음성·기준 MP4를 포함한 ZIP과 별도 안내서·기준 영상을 보관한다. OAuth JSON·토큰·비공개 작업 원문·실행 DB·로그는 넣지 않는다.

## 동일 스타일과 동일 파일의 차이

이 보관본은 디자인과 고정 보이스를 유지하는 기준이다. 내레이션을 새로 합성하면 같은 보이스라도 억양·길이는 달라질 수 있다. 같은 입력·같은 폰트·같은 코드·같은 렌더 환경을 재사용해야 출력 차이를 줄일 수 있으며, 다른 브라우저/OS의 모든 픽셀이나 새 음성 파형까지 동일하다고 보장하지 않는다.

현재 예약 실행과 YouTube OAuth 연결은 별도 미완료 상태다. 이 보관 작업이 새 정기 예약이나 업로드를 활성화하지 않는다. 퀴즈와 롱폼은 별도 규칙·초안이며 이번에 기준 영상을 확정한 대상은 AI 활용 쇼츠다.
