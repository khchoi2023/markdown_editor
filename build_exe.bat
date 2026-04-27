@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else (
    set "PYTHON=python"
)

%PYTHON% -m pip install -r requirements.txt
if errorlevel 1 goto error

%PYTHON% -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --hidden-import pymdownx.tasklist ^
  --hidden-import pymdownx.tilde ^
  --collect-submodules pymdownx ^
  --name "Markdown Live Editor" ^
  main.py
if errorlevel 1 goto error

echo.
echo Build complete: dist\Markdown Live Editor\Markdown Live Editor.exe
pause
exit /b 0

:error
echo.
echo exe build failed.
pause
exit /b 1
