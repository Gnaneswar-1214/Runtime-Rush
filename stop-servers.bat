@echo off
echo ========================================
echo   Runtime Rush Platform - Stopping...
echo ========================================
echo.

call pm2 stop all

echo.
echo ========================================
echo   Servers Stopped Successfully!
echo ========================================
echo.
echo Press any key to exit...
pause >nul
