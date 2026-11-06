# One-time Windows OAuth setup. No administrator permission or scheduled task required.
param([string]$ClientSecretPath)
$ErrorActionPreference = 'Stop'
try {
    $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
    $ProfilePath = Join-Path $ProjectRoot 'channels/ai/channel.json'
    $Profile = Get-Content -LiteralPath $ProfilePath -Raw -Encoding UTF8 | ConvertFrom-Json
    $ChannelId = [string]$Profile.youtube_channel_id
    if ($ChannelId -notmatch '^UC[A-Za-z0-9_-]{22}$') { throw 'The configured YouTube channel ID is missing or invalid.' }
    Write-Host 'AI Practice Notes - YouTube upload connection'
    Write-Host ('Expected channel: ' + $ChannelId)
    Write-Host 'This connects upload access only. It does not upload a video or register a recurring task.'

    $PythonCommand = Get-Command py -ErrorAction SilentlyContinue
    $PythonArgs = @()
    if ($PythonCommand) { $PythonArgs = @('-3') }
    else {
        $PythonCommand = Get-Command python -ErrorAction SilentlyContinue
        if ($PythonCommand -and $PythonCommand.Source -match 'WindowsApps') { $PythonCommand = $null }
    }
    if (-not $PythonCommand) {
        Start-Process 'https://www.python.org/downloads/windows/'
        throw 'Install Python 3.11 or newer, enable Add Python to PATH, and run CONNECT-YOUTUBE.cmd again.'
    }
    $VersionCheck = & $PythonCommand.Source @PythonArgs -c 'import sys; print(sys.version_info.major >= 3 and sys.version_info[:2] >= (3, 11))'
    if ($LASTEXITCODE -ne 0 -or $VersionCheck -ne 'True') { throw 'Python 3.11 or newer is required.' }

    if (-not $ClientSecretPath) {
        Add-Type -AssemblyName System.Windows.Forms
        $Dialog = New-Object System.Windows.Forms.OpenFileDialog
        $Dialog.Title = 'Choose the Desktop app OAuth JSON downloaded from Google Cloud'
        $Dialog.Filter = 'Google OAuth JSON (*.json)|*.json'
        $Dialog.InitialDirectory = Join-Path ([Environment]::GetFolderPath('UserProfile')) 'Downloads'
        if ($Dialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { throw 'No OAuth JSON selected. See WINDOWS-START.md for Google Cloud setup.' }
        $ClientSecretPath = $Dialog.FileName
    }
    $Client = Get-Content -LiteralPath $ClientSecretPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if (-not $Client.installed -or -not $Client.installed.client_id -or -not $Client.installed.client_secret) {
        throw 'Choose a Google OAuth Desktop app JSON, not a Web app or service-account key.'
    }
    if ($Client.installed.token_uri -ne 'https://oauth2.googleapis.com/token') { throw 'Unexpected OAuth token endpoint.' }
    if ($Client.installed.auth_uri -notin @('https://accounts.google.com/o/oauth2/auth', 'https://accounts.google.com/o/oauth2/v2/auth')) { throw 'Unexpected OAuth authorization endpoint.' }

    $LocalDir = Join-Path $PSScriptRoot '.local'
    New-Item -ItemType Directory -Path $LocalDir -Force | Out-Null
    $Venv = Join-Path $LocalDir 'venv'
    $VenvPython = Join-Path $Venv 'Scripts/python.exe'
    if (-not (Test-Path -LiteralPath $VenvPython)) {
        & $PythonCommand.Source @PythonArgs -m venv $Venv
        if ($LASTEXITCODE -ne 0) { throw 'Could not create the local Python environment.' }
    }
    & $VenvPython -m pip install --disable-pip-version-check -r (Join-Path $PSScriptRoot 'requirements.txt')
    if ($LASTEXITCODE -ne 0) { throw 'Could not install the Google upload libraries. Check network access.' }
    $PrivateClient = Join-Path $LocalDir 'client_secret.json'
    if ([IO.Path]::GetFullPath($ClientSecretPath) -ne [IO.Path]::GetFullPath($PrivateClient)) {
        Copy-Item -LiteralPath $ClientSecretPath -Destination $PrivateClient -Force
    }
    $Token = Join-Path $LocalDir 'youtube-token.json'
    $env:PYTHONUTF8 = '1'
    & $VenvPython (Join-Path $PSScriptRoot 'auth.py') --client $PrivateClient --token $Token --channel-id $ChannelId --activate-publishing
    if ($LASTEXITCODE -ne 0) { throw 'Google authorization or channel verification did not finish.' }
    Write-Host 'SUCCESS: The expected channel is connected on THIS Windows PC.' -ForegroundColor Green
    Write-Host 'Tell the assistant that connection succeeded. Do not share the token or OAuth JSON.'
    exit 0
} catch {
    Write-Host ('SETUP STOPPED: ' + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
