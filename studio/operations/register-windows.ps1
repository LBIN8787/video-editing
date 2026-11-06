# Run on the chosen persistent Windows worker after its integrations are tested.
param([Parameter(Mandatory=$true)][string]$PythonExe)
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$WorkerPath = Join-Path $ProjectRoot 'studio/operations/daily_worker.py'
$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument ('"' + $WorkerPath + '"') -WorkingDirectory $ProjectRoot
$Trigger = New-ScheduledTaskTrigger -Daily -At '07:30'
$Settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable
Register-ScheduledTask -TaskName 'AI-Practice-Notes-Daily' -Action $Action -Trigger $Trigger -Settings $Settings -Description 'Prepare three AI Shorts and schedule verified uploads; uses local PC timezone.'
