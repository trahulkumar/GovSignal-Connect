@echo off
echo [INFO] Starting GovSignal Scout (Prototype Mode)...

if not exist .venv (
    echo [ERROR] Virtual environment not found. Please run setup_env.bat first.
    pause
    exit /b 1
)

REM Activate venv and run
call .venv\Scripts\activate
python -m govsignal.scout examples/config.yaml

echo.
echo [INFO] Scout run completed.
pause
