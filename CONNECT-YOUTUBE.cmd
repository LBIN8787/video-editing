@echo off
setlocal
powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File "%~dp0studio\youtube\connect-windows.ps1"
set "connect_exit=%errorlevel%"
echo.
if not "%connect_exit%"=="0" echo Connection did not complete. Read the message above and run this file again after fixing it.
pause
exit /b %connect_exit%
