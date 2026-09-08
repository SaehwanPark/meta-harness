@echo off
setlocal

where py -3 >nul 2>&1
if %ERRORLEVEL% equ 0 (
  py -3 "%~dp0scripts\install_harness.py" %*
  exit /b %ERRORLEVEL%
)

where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
  python "%~dp0scripts\install_harness.py" %*
  exit /b %ERRORLEVEL%
)

where python3 >nul 2>&1
if %ERRORLEVEL% equ 0 (
  python3 "%~dp0scripts\install_harness.py" %*
  exit /b %ERRORLEVEL%
)

echo Error: Python 3.8 or newer was not found on your PATH. 1>&2
echo Please install Python 3 and ensure it is added to your PATH. 1>&2
exit /b 1
