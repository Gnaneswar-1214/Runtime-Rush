@echo off
REM Quick API test commands for Railway deployment
REM Replace YOUR_RAILWAY_URL with your actual Railway URL

set RAILWAY_URL=https://your-app.railway.app

echo Testing Runtime Rush API on Railway
echo ========================================
echo.

REM Test 1: Health Check
echo 1. Health Check
curl -X GET "%RAILWAY_URL%/health"
echo.
echo.

REM Test 2: Initialize Database
echo 2. Initialize Database (creates admin + challenges)
curl -X POST "%RAILWAY_URL%/initialize-db"
echo.
echo.

REM Test 3: Get All Challenges
echo 3. Get All Challenges
curl -X GET "%RAILWAY_URL%/api/challenges"
echo.
echo.

REM Test 4: Admin Login
echo 4. Admin Login
curl -X POST "%RAILWAY_URL%/api/auth/login" -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
echo.
echo.

REM Test 5: Register Test User
echo 5. Register Test User
curl -X POST "%RAILWAY_URL%/api/auth/register" -H "Content-Type: application/json" -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"test123\"}"
echo.
echo.

echo ========================================
echo Tests complete!
echo.
echo If all tests passed, your deployment is working!
echo Admin credentials: admin / admin123
pause
