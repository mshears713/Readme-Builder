@echo off
REM View Project Forge Docker logs
REM This script displays logs from the Streamlit container

echo ========================================
echo Project Forge Logs
echo ========================================
echo.
echo Press Ctrl+C to stop viewing logs
echo.

docker logs -f project-forge-streamlit
