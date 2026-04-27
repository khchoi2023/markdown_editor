@echo off
setlocal
cd /d "%~dp0"

set "QTWEBENGINE_CHROMIUM_FLAGS=--disable-gpu --disable-gpu-compositing --disable-accelerated-2d-canvas --use-angle=swiftshader"
set "QT_OPENGL=software"
set "QT_LOGGING_RULES=qt.webenginecontext=false"

if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" "%~dp0main.py"
    exit /b 0
)

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py
    goto check_error
)

where pythonw >nul 2>nul
if errorlevel 1 (
    python main.py
    goto check_error
)

start "" pythonw "%~dp0main.py"
exit /b 0

:check_error
if errorlevel 1 (
    echo.
    echo The app failed to start.
    echo Make sure dependencies are installed:
    echo   pip install -r requirements.txt
    echo.
    pause
)
