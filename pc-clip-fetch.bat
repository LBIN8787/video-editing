@echo off
REM ============================================================================
REM  원본 발언 구간 받기 + 다시 렌더 — PC 에서 더블클릭 (2026-11-21 사용자: "터미널 실행버튼 만들어주세요")
REM  하는 일: git pull → clip-fetch(주문서의 구간만, 본인 브라우저) → hybrid 렌더 → clip_manifest 커밋·푸시
REM  다른 영상: 이 파일을 터미널에서  pc-clip-fetch.bat <프로젝트이름>
REM  클라우드는 유튜브 봇 확인 때문에 못 받으므로 PC 가 대신 받습니다 (docs/50-clip-lane.md, 우회하지 않음)
REM ============================================================================
chcp 65001 >nul
setlocal
cd /d "%~dp0"

set "PROJ=%~1"
if "%PROJ%"=="" set "PROJ=20261120-market-deep-druckenmiller"
echo.
echo  [1/5] 저장소 최신으로 받기 ...
git pull --ff-only || goto :fail

echo.
echo  [2/5] 원본 구간 받기 — %PROJ%
python -m ytflow clip-fetch %PROJ%
python -c "import json,sys;m=json.load(open(r'projects/%PROJ%/04_assets/clip_manifest.json',encoding='utf-8'));bad=[k for k,v in m['clips'].items() if v.get('status')!='ok'];print('  받지 못한 구간:',bad) if bad else None;sys.exit(1 if bad else 0)" 2>nul
if errorlevel 1 (
  echo.
  echo  일부 구간을 받지 못했습니다. 유튜브가 로그인 확인을 요구했을 수 있습니다.
  echo  이 PC 의 브라우저 로그인으로 다시 받으려면 브라우저 이름을 입력하세요 (chrome / edge / firefox, 그냥 Enter 면 건너뜀^)
  set /p "BROWSER=브라우저: "
  if not "!BROWSER!"=="" (
    echo  ※ 브라우저를 모두 닫은 뒤 계속하세요 (열려 있으면 로그인 정보를 읽지 못합니다^)
    pause
    set "YTFLOW_CLIP_COOKIES=!BROWSER!"
    python -m ytflow clip-fetch %PROJ%
  )
)

echo.
echo  [3/5] 영상 다시 만들기 (임시 목소리 edge) ...
set "YTFLOW_TTS=edge"
python -m ytflow hybrid %PROJ% || goto :fail

echo.
echo  [4/5] 받은 구간 기록 올리기 (영상 파일은 올리지 않음) ...
git add "projects/%PROJ%/04_assets/clip_manifest.json" "projects/%PROJ%/05_edit/*.json" "inbox/pc-tasks" 2>nul
git commit -m "clip-fetch %PROJ% (PC)" && git push

echo.
echo  [5/5] 끝 — 완성본: projects\%PROJ%\05_edit\final.mp4
start "" "projects\%PROJ%\05_edit"
pause
exit /b 0

:fail
echo.
echo  실패했습니다. 위 메시지를 그대로 복사해서 클로드에게 보내 주세요.
pause
exit /b 1
