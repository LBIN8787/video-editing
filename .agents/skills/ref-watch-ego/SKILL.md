---
name: ref-watch-ego
description: 사용자 PC 의 ego lite 브라우저(로그인된 사용자 브라우저)로 레퍼런스 유튜브 영상을 직접 재생·정지하며 일정 간격으로 화면을 캡처하고, 캡처 묶음을 rea-video 로 장면별 분석해 움직임(애니메이션) 문법을 정리한다. "이 영상 애니메이션 분석해줘", "미주일기 최신 영상 움직임 봐줘"처럼 클라우드에서 영상을 받을 수 없을 때 PC 에서 쓴다.
---

# 레퍼런스 영상 보기 — ego lite + rea-video (사용자 PC 전용)

클라우드 세션은 YouTube 봇 확인에 막히고(우회하지 않음), ego lite 는 Windows·macOS 에서만 돕니다.
그래서 **이 스킬은 사용자 PC 의 Claude Code(또는 Codex) 가 저장소 폴더에서 실행**합니다.
영상 파일을 내려받지 않습니다. 사용자가 브라우저로 보는 것과 같이 **재생 화면을 보고 캡처**만 합니다.

## 0. 지킬 것
- **캡처·분석 결과는 Google Drive 에** (2026-11-15~, `docs/09-storage.md` §0): `%YTFLOW_DRIVE%\refs\<영상ID>\` (예: `G:\내 드라이브\ytflow\refs\EV8NmofeWPk\`). `YTFLOW_DRIVE` 가 없으면 만들지 말고 사용자에게 Drive 경로를 묻습니다.
- 가상환경·모델처럼 동기화하면 깨지는 것은 Drive 밖, 저장소 옆 기존 위치에 둡니다(D·C 에 새 폴더를 만들지 않음): 가상환경 `..\reavenv`, 모델 `REA_VIDEO_MODELS=..\rea-models`.
- **ego lite 는 사용자 로그인 상태를 씁니다.** youtube.com 영상 페이지만 엽니다. 다른 사이트, 댓글 작성·구독·좋아요·설정 변경은 하지 않습니다.
- 다운로드 도구(yt-dlp 등)에 브라우저 쿠키를 넘기지 않습니다. 광고는 끝날 때까지 기다리고 건너뛰기 버튼만 누릅니다.
- 큰 캡처·클립(이미지·mp4)은 Drive 에만 두고 커밋하지 않습니다. 작은 분석 문서(md/json)와 소스·검수·파일 목록(Drive 경로·장 수)은 Git 에 커밋할 수 있습니다 (`docs/09-storage.md` §0-0).
- 레퍼런스의 캐릭터·대사·로고는 복제하지 않습니다. 움직임의 **구조와 기법**만 기록합니다.

## 1. 준비 (처음 한 번)
1. ego lite 설치: 사용자가 https://lite.ego.app/ 에서 Windows 설치 파일을 받아 실행하고 첫 실행 안내를 마칩니다(크롬 데이터 가져오기는 사용자가 결정).
2. 새 터미널에서 확인: `ego-browser nodejs -e "console.log('ego-browser ready')"` → `ego-browser skill` 을 실행해 **출력된 사용법을 끝까지 읽습니다**(마지막 줄 `[ego-browser:skill] end of guide`). 아래 2단계의 함수 이름은 이 안내를 따릅니다.
3. rea-video (버전은 `tools/external.json`):
   ```powershell
   py -3.12 -m venv ..\reavenv
   ..\reavenv\Scripts\pip install "rea-video[ocr] @ git+https://github.com/JuneYaooo/rea-video@5b09832ab64c334045b99aaaeb8207e86da765e8"
   $env:REA_VIDEO_MODELS = (Resolve-Path ..).Path + "\rea-models"
   ```

## 2. 영상 보기 → 캡처 (ego-browser)
영상마다 에이전트 전용 Space 에서 다음을 한 번의 스크립트로 합니다(사용자 탭은 건드리지 않음).
1. `https://www.youtube.com/watch?v=<ID>` 를 열고 광고가 끝나 본편이 재생될 때까지 기다립니다.
2. 화질을 1080p(없으면 720p)로, 영상 영역만 보이게 합니다(극장 모드 또는 `video` 요소 크기·위치로 잘라 캡처).
3. **재생하면서 찍지 말고 '정지 → 이동 → 찍기'** 를 반복합니다. 시간이 정확합니다.
   - `video.pause()` → `video.currentTime = t` → `seeked` 이벤트를 기다림 → 한 프레임 더 그려질 때까지 대기 → `video` 영역 캡처 → `%YTFLOW_DRIVE%\refs\<ID>\frames\f_<t*1000 을 6자리>.png`
   - 기본 간격 **0.25초**(초당 4장). 5분 영상이면 약 1,200장.
   - 이해를 돕는 애니메이션 구간(정보 장면)은 사용자 지정 구간이나 1차 분석에서 고른 구간을 **0.1초** 간격으로 다시 찍습니다 → `frames_fine\`.
4. 같은 페이지에서 제목·채널·길이·공개일과, 있으면 자막(스크립트 표시) 문장·시각을 `meta.json`, `transcript.txt` 로 저장합니다.

## 3. 캡처 묶음 → 영상 → rea-video
```powershell
python scripts/frames_to_clip.py $env:YTFLOW_DRIVE\refs\<ID>\frames --fps 4 -o $env:YTFLOW_DRIVE\refs\<ID>\ref.mp4
..\reavenv\Scripts\rea-video decompose $env:YTFLOW_DRIVE\refs\<ID>\ref.mp4 -o $env:YTFLOW_DRIVE\refs\<ID>\rea --lang en --no-asr
..\reavenv\Scripts\rea-video review $env:YTFLOW_DRIVE\refs\<ID>\rea
```
- 소리가 없는 캡처라 효과음·목소리 분석은 건너뜁니다(소리는 `transcript.txt` 로 대신).
- `review_tasks.json` 의 장면 그림을 **직접 보고** `review_answers.json` 을 채운 뒤 `rea-video apply-review ... --by claude` 를 실행합니다.

## 4. 움직임 문법 정리 (이 스킬의 결과물)
`rea\VIDEO.md`, `rea\video\timeline.md`, 장면 그림, `frames_fine\` 을 보고 `docs/31-motion-grammar.md` 에 영상마다 표를 씁니다.

| 시각 | 대본(그 순간 말) | 화면에서 **무엇이** 움직이나 | 어떻게 (그려짐·변신·나뉨·이어짐·채워짐·이동·교체) | 걸린 시간 | 왜 이해를 돕나 |
|---|---|---|---|---|---|

- **카메라 움직임과 요소 움직임을 나눠 적습니다.** (우리 v7 은 카메라만 움직여 '흔든다'는 평을 받았습니다. 레퍼런스는 요소가 대본의 동사를 연기하는지 확인)
- 숫자로: 장면 수/분, 평균 장면 길이, 장면 안 요소 변화 횟수/10초, 정지 비율.
- 끝에 "우리 stage 엔진에 없는 움직임" 목록과 구현 제안을 씁니다.

## 5. 마무리
`docs/31-motion-grammar.md` 만 커밋·푸시합니다. Google Drive 의 캡처 폴더 경로와 장 수를 보고합니다(클라우드 세션은 Drive 커넥터로 장면 그림을 볼 수 있음). 클라우드 세션은 이 문서를 읽고 매뉴얼과 `ytflow/stages/stage.py` 를 고칩니다.
