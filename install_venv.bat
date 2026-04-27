@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found.
    echo Install Python 3.11 or newer, then run this file again.
    pause
    exit /b 1
)

python --version
python -m venv .venv
if errorlevel 1 goto error

".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto error

".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error

echo.
echo Virtual environment setup complete.
echo Double-click run.bat to start the app.
pause
exit /b 0

:error
echo.
echo Virtual environment setup failed.
pause
exit /b 1
