# PC 자동 일꾼 설치 — 한 번만 실행 (2026-11-20 사용자: "손수 명령 안해도 되도록 자동화 세팅")
# Windows 작업 스케줄러에 'ytflow-pc-worker' 를 등록: 로그인해 있는 동안 10분마다 scripts/pc_worker.py 실행.
# 실행:  PowerShell 에서 저장소 폴더로 가서
#   powershell -ExecutionPolicy Bypass -File scripts\install_pc_worker.ps1
# 끄기:  Unregister-ScheduledTask -TaskName ytflow-pc-worker -Confirm:$false
# 로그:  %YTFLOW_DRIVE%\_local\pc-worker\pc_worker.log
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path "$PSScriptRoot\..").Path
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction Stop).Source }
if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
  Write-Warning "codex 명령을 찾지 못했습니다. 그림(GPT 이미지)은 Codex 로그인이 필요합니다: npm i -g @openai/codex 후 codex login"
}
if (-not $env:YTFLOW_DRIVE) {
  Write-Warning "환경변수 YTFLOW_DRIVE 가 없습니다 (예: G:\내 드라이브\ytflow). 그림·영상 저장 위치로 씁니다."
}
& $py -m pip install -q pypdfium2 pyyaml pillow   # 자동 빌드에 필요한 것 (논문 PDF 쪽 → 그림)
$action = New-ScheduledTaskAction -Execute $py -Argument "`"$repo\scripts\pc_worker.py`" --once" -WorkingDirectory $repo
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 10)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries `
  -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 3)
Register-ScheduledTask -TaskName "ytflow-pc-worker" -Action $action -Trigger $trigger -Settings $settings `
  -Description "ytflow: inbox/pc-tasks 의 pending 할 일을 Codex(GPT 이미지)·Claude 로 자동 처리 (scripts/pc_worker.py)" -Force | Out-Null
Write-Host "등록됨: ytflow-pc-worker (10분마다). 첫 실행은 1분 뒤. 로그: $env:YTFLOW_DRIVE\_local\pc-worker\pc_worker.log"
& $py "$repo\scripts\pc_worker.py" --dry-run
