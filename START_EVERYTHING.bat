@echo off
echo ========================================
echo Starting Runtime Rush Platform
echo ========================================
echo.

echo Step 1: Starting Backend Server...
cd backend
start cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
cd ..
echo Backend starting on http://localhost:8000
echo.

timeout /t 5 /nobreak

echo Step 2: Starting Frontend Server...
cd frontend
start cmd /k "npm start"
cd ..
echo Frontend starting on http://localhost:3000
echo.

echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Initialize DB: http://localhost:8000/initialize-db
echo.
echo Press any key to exit this window...
pause
