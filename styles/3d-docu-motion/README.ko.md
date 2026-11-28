# 3D 다큐 모션 · 광학 예제 재현

> **다른 영상에 쓰려면 이 문서가 아니라 `cutaway3d` 장면을 쓴다 (2026-11-29).** 이 폴더의 `scene.html` 은 마벨 광학 편 한 구간(152.6–184.9초)을 그대로 재현하는 시간 고정 판이다. 같은 무대를 대본으로 움직이는 판이 `sets/dc-rack.html` 이고, 샷 목록·맞는 이야기는 `sets.yaml`, 쓰는 법은 `styles/hybrid/scenes/cutaway3d.md`, 기준은 `manual/05-style-matching.md` §0-10 이다. 아래는 원래 광학 편 재현 절차.

공간 배치, 내부 구조, 신호 경로를 설명하는 보조 영상이다. 광학 예제의 3D 플레이트(V2), 작은 패널 합성(V4), 설명 구간 확대(V5)를 재현한다. 이 폴더는 수동으로 실행하는 별도 도구이며 기존 제작·게시 경로에 연결되지 않는다.

## 입력과 실행

- Windows PowerShell, Node.js 22+, FFmpeg 및 FFprobe(libx264 포함), WebGL2/SwiftShader를 지원하는 Chrome 또는 Chromium이 필요하다. 브라우저는 플레이트를 만들 때만 필요하다. npm 패키지나 외부 장면 자산은 사용하지 않는다.
- 이 레시피는 정확히 일치하는 원본 광학 본편 MP4를 입력으로 요구한다. 작업자가 가진 파일을 직접 지정한다. 실행기는 레시피에 기록된 SHA-256과 영상 규격을 확인한다. 원본과 생성 영상은 이 저장소에 포함하지 않는다.
- 기존 파일을 덮어쓰지 않는다. 각 명령의 출력은 아직 존재하지 않는 별도 폴더로 정한다. 결과에는 작업용 브라우저 프로필, 영상, 검사 프레임과 로그가 생길 수 있으므로 저장소 밖에 보관한다.

이 폴더에서 실행한다. 입력 질문에는 작업자가 가진 파일의 경로를 입력한다.

~~~powershell
$orig = Read-Host '원본 광학 본편 MP4 경로'
$chrome = Read-Host 'Chrome 또는 Chromium 실행 파일 경로'
$out = Join-Path ([IO.Path]::GetTempPath()) ('docu-motion-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $out | Out-Null
$plateDir = Join-Path $out 'plate'
$reviewDir = Join-Path $out 'review'
$verifyDir = Join-Path $out 'verify'
node .\render-plate.cjs --browser $chrome --out-dir $plateDir
$plate = Join-Path $plateDir 'v2-B-regenerated.mp4'
node .\compose.cjs --mode review --source $orig --plate $plate --out-dir $reviewDir
node .\verify-review.cjs --source $orig --plate $plate --v4 (Join-Path $reviewDir 'review-V4.mp4') --v5 (Join-Path $reviewDir 'review-V5.mp4') --out-dir $verifyDir
~~~

이미 생성한 플레이트가 있으면 해당 파일을 직접 --plate 인자로 줘 합성부터 확인할 수 있다. 검수기에는 이전 결과를 각각 --reference-plate, --reference-v4, --reference-v5로 선택 입력할 수 있다. 비교용 V4/V5는 검수 발췌본이 아닌 동일한 원본 시간축의 전체 영상이어야 한다. FFmpeg 도구가 PATH에 없으면 각 명령에 --ffmpeg와 --ffprobe 실행 파일 경로를 넘길 수 있다.

## 범위와 한계

- 검수본은 본편 152.600–184.900초를 1080p로 유지한다. V4 패널은 152.600–177.600초, V5 확대는 163.333333–171.700초에 합성한다. 레시피는 시작 포함, 종료 제외 기준이다. 검수본에서 FFmpeg 합성은 보관본과 같이 마지막 경계 직전인 171.666667초 프레임에서 이미 작은 패널로 복귀한다. 위치와 크롭은 레시피에 있다.
- 원본 카드와 자막을 다시 그리지 않는다. 검수기는 대표 프레임의 보호 영역 유사도, 확대 구간 안팎과 경계 프레임, 연속 AAC 패킷, 플레이트 디코딩을 확인한다. 합성기는 결과의 영상과 음성을 디코딩 검사한다.
- 본편 파일을 별도로 재현하려면 합성기에 --mode full을 주고 새 출력 폴더를 지정한다. 이 모드는 결과의 전체 AAC 페이로드 해시도 확인한다.
- V4 테두리는 기존 영상에 대조해 추정한 값이다. 브라우저, 운영체제 글꼴, 인코더에 따라 픽셀이 달라질 수 있으며 기존 MP4와 해시가 같은 복제는 목표가 아니다. 이 레시피의 좌표와 시각은 다른 영상용 기본값이 아니다.n