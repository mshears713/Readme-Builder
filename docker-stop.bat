@echo off
REM Stop all Project Forge Docker containers
REM This script stops and removes all running containers

echo ========================================
echo Stopping Project Forge containers...
echo ========================================
echo.

docker-compose down

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo All containers stopped successfully!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Failed to stop containers!
    echo ========================================
    echo Please check the errors above.
)

pause
