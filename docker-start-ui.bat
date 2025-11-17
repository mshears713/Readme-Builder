@echo off
REM Start Project Forge Streamlit UI
REM This script starts the Streamlit web interface on http://localhost:8501

echo ========================================
echo Starting Project Forge Streamlit UI...
echo ========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found!
    echo.
    echo Please create a .env file with your API keys:
    echo 1. Copy .env.example to .env
    echo 2. Add your OPENAI_API_KEY or ANTHROPIC_API_KEY
    echo.
    pause
    exit /b 1
)

REM Create output directory if it doesn't exist
if not exist output mkdir output

echo Starting Streamlit UI container...
docker-compose up -d streamlit

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Streamlit UI started successfully!
    echo ========================================
    echo.
    echo Open your browser and navigate to:
    echo http://localhost:8501
    echo.
    echo To stop the UI, run: docker-stop.bat
    echo To view logs, run: docker logs -f project-forge-streamlit
    echo.
) else (
    echo.
    echo ========================================
    echo Failed to start Streamlit UI!
    echo ========================================
    echo Please check the errors above.
)

pause
