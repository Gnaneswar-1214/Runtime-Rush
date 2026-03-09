@echo off
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║           FIX EVERYTHING - Runtime Rush                     ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo This will:
echo 1. Deploy your code to Railway
echo 2. Wait for deployment
echo 3. Initialize database with 12 challenges
echo.
pause
echo.

echo ========================================
echo Step 1: Deploying Code to Railway...
echo ========================================
echo.

git add .
if errorlevel 1 (
    echo ❌ Error adding files
    pause
    exit /b 1
)
echo ✅ Files added

git commit -m "Add 12 challenges with multi-language support"
if errorlevel 1 (
    echo ⚠️  Nothing to commit or error occurred
)
echo ✅ Changes committed

git push origin main
if errorlevel 1 (
    echo ❌ Error pushing to GitHub
    pause
    exit /b 1
)
echo ✅ Pushed to GitHub
echo.

echo ========================================
echo Step 2: Waiting for Railway Deployment...
echo ========================================
echo.
echo Please wait 2-3 minutes for Railway to deploy...
echo.
echo You can check status at: https://railway.app
echo.
timeout /t 120 /nobreak
echo.

echo ========================================
echo Step 3: Initializing Database...
echo ========================================
echo.
echo Opening browser to initialize database...
echo.
start https://runtime-rush-production.up.railway.app/initialize-db
echo.
echo ✅ Database initialization page opened in browser
echo.
echo You should see a success message with:
echo   - admin_created: true
echo   - challenges_created: 12
echo.

echo ========================================
echo Step 4: Opening Localhost...
echo ========================================
echo.
timeout /t 5 /nobreak
start http://localhost:3000
echo.
echo ✅ Localhost opened in browser
echo.

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║                    ALL DONE! ✅                              ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Next steps:
echo 1. Check the browser tab for /initialize-db
echo 2. Verify you see "success": true
echo 3. Go to localhost:3000 tab
echo 4. Login: mouniadmin / 1214@
echo 5. You should see 12 challenges!
echo.
echo If challenges don't show:
echo - Refresh the page (Ctrl + R)
echo - Clear cache (Ctrl + Shift + Delete)
echo - Try a different browser
echo.
pause
