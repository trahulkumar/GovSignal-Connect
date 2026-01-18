@echo off
REM Requires Python 3.10+
echo [INFO] Setting up GovSignal-Connect Environment...

REM Check if uv is installed
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] uv is not installed. Please install uv (e.g., pip install uv).
    exit /b 1
)

echo [INFO] Creating virtual environment...
uv venv .venv

echo [INFO] Installing dependencies...
uv pip install -r requirements.txt

echo [INFO] Setup complete.
pause
