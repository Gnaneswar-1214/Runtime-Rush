@echo off
echo ============================================
echo RUNTIME RUSH - LOCALHOST TESTING
echo ============================================
echo.
echo STEP 1: Starting Backend Server...
echo.
cd backend
start cmd /k "title Backend Server && python -m uvicorn app.main:app --reload"
timeout /t 3 /nobreak >nul
cd ..

echo.
echo STEP 2: Starting Frontend Server...
echo.
cd frontend
start cmd /k "title Frontend Server && npm start"
cd ..

echo.
echo ============================================
echo SERVERS STARTING...
echo ============================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause >nul
