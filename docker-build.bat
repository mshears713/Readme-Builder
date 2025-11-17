@echo off
REM Build Docker image for Project Forge
REM This script builds the Docker image for Windows

echo ========================================
echo Building Project Forge Docker Image...
echo ========================================
echo.

docker-compose build

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Build completed successfully!
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Copy .env.example to .env and add your API keys
    echo 2. Run docker-start-ui.bat to start the Streamlit UI
    echo 3. Or run docker-run-cli.bat to use the CLI
) else (
    echo.
    echo ========================================
    echo Build failed! Please check the errors above.
    echo ========================================
)

pause
