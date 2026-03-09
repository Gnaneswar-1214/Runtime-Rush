@echo off
echo Testing Challenges API...
echo.

echo 1. Testing /api/challenges endpoint:
curl https://runtime-rush-production.up.railway.app/api/challenges
echo.
echo.

echo 2. Testing health check:
curl https://runtime-rush-production.up.railway.app/health
echo.
echo.

echo 3. Testing if challenges exist in database:
curl https://runtime-rush-production.up.railway.app/initialize-db
echo.

pause
