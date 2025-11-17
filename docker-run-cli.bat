@echo off
REM Run Project Forge CLI
REM This script runs the CLI to generate a README/PRD from a project idea

echo ========================================
echo Project Forge CLI
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

REM Check if user provided a project idea
if "%~1"=="" (
    echo Usage: docker-run-cli.bat "Your project idea here"
    echo.
    echo Example:
    echo docker-run-cli.bat "Build a habit tracker app with daily reminders"
    echo.
    pause
    exit /b 1
)

echo Running Project Forge CLI...
echo Project Idea: %~1
echo.

docker-compose run --rm cli %*

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo CLI execution completed!
    echo ========================================
    echo.
    echo Check the 'output' folder for your generated README/PRD.
) else (
    echo.
    echo ========================================
    echo CLI execution failed!
    echo ========================================
    echo Please check the errors above.
)

pause
