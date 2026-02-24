@echo off
echo ========================================
echo   Runtime Rush Platform - Starting...
echo ========================================
echo.

REM Check if PM2 is installed
where pm2 >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PM2 is not installed!
    echo Installing PM2 globally...
    call npm install -g pm2
    echo.
)

echo Starting servers with PM2...
call pm2 start ecosystem.config.js

echo.
echo ========================================
echo   Servers Started Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Useful PM2 Commands:
echo   pm2 status       - View server status
echo   pm2 logs         - View server logs
echo   pm2 stop all     - Stop all servers
echo   pm2 restart all  - Restart all servers
echo.
echo Press any key to view server status...
pause >nul

call pm2 status
echo.
echo Press any key to exit...
pause >nul
