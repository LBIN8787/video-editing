# 로컬 정기 작업 설치 — 한 번만 실행 (docs/56-local-routines.md)
# config/local_routines.yaml 의 작업마다 Windows 작업 스케줄러에 'ytflow-<작업>' 을 매일 그 시각으로 등록하고,
# 호기심 그림·렌더를 맡는 PC 일꾼(ytflow-pc-worker, 10분마다)도 함께 등록합니다.
# 실행기는 사용자 폴더(브랜치가 바뀜)가 아니라 E:\ytflow-local\runner (늘 최신 origin/main) 에서 돕니다.
# 실행:  PowerShell 에서 저장소 폴더로 가서
#   powershell -ExecutionPolicy Bypass -File scripts\install_local_routines.ps1
# 바로 한 번 돌리기: Start-ScheduledTask -TaskName ytflow-market-daily
# 끄기:  Unregister-ScheduledTask -TaskName ytflow-market-daily -Confirm:$false
# 로그·보고: %YTFLOW_DRIVE%\_local\logs, \_local\reports  (C 드라이브는 쓰지 않음)
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path "$PSScriptRoot\..").Path
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction Stop).Source }
$drive = [Environment]::GetEnvironmentVariable("YTFLOW_DRIVE", "User")
if (-not $drive) { throw "YTFLOW_DRIVE 가 없습니다: setx YTFLOW_DRIVE `"G:\내 드라이브\ytflow`" 후 새 PowerShell 에서 다시" }
New-Item -ItemType Directory -Force "$drive\_local\logs", "$drive\_local\reports" | Out-Null
$work = [Environment]::GetEnvironmentVariable("YTFLOW_WORK", "User")
if (-not $work) { $work = if (Test-Path "E:\") { "E:\ytflow-local" } else { (Split-Path $repo) + "\ytflow-local" } }
New-Item -ItemType Directory -Force $work | Out-Null
& $py -m pip install -q pyyaml

# 실행기 폴더: 최신 origin/main
$runner = "$work\runner"
git -C $repo fetch -q origin main
if (-not (Test-Path "$runner\.git")) { git -C $repo worktree add -f --detach $runner origin/main | Out-Null }
git -C $runner checkout -q -f -B local/runner origin/main

$jobs = & $py "$runner\scripts\local_routine.py" --list
foreach ($line in $jobs) {
  $name, $time = $line -split "\|", 2
  # 실행 직전에 실행기 폴더를 최신 main 으로 맞춘 뒤 실행
  $cmd = "git -C '$runner' fetch -q origin main; git -C '$runner' checkout -q -f -B local/runner origin/main; & '$py' '$runner\scripts\local_routine.py' $name"
  $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -Command `"$cmd`"" -WorkingDirectory $runner
  $trigger = New-ScheduledTaskTrigger -Daily -At $time
  # 꺼져 있다가 켜지면 놓친 차례를 바로 실행, 절전이면 깨워서 실행, 겹치면 새 것은 건너뜀
  $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries `
    -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 6)
  Register-ScheduledTask -TaskName "ytflow-$name" -Action $action -Trigger $trigger -Settings $settings `
    -Description "ytflow local routine $name (scripts/local_routine.py, docs/56)" -Force | Out-Null
  Write-Host "등록됨: ytflow-$name — 매일 $time"
}

# 호기심 그림·렌더를 맡는 PC 일꾼 (실행기 폴더 기준으로 등록)
& "$runner\scripts\install_pc_worker.ps1"

Write-Host ""
Write-Host "확인(실행 안 함):"
foreach ($line in $jobs) { & $py "$runner\scripts\local_routine.py" ($line -split "\|")[0] --dry-run }
