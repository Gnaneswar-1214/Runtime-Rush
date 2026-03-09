@echo off
echo ========================================
echo Deploying Runtime Rush to Production
echo ========================================
echo.

echo Step 1: Adding all changes...
git add .
echo ✅ Changes added
echo.

echo Step 2: Committing changes...
git commit -m "Add multi-language support with 12 new challenges"
echo ✅ Changes committed
echo.

echo Step 3: Pushing to GitHub...
git push origin main
echo ✅ Pushed to GitHub
echo.

echo ========================================
echo Deployment Started!
echo ========================================
echo.
echo Railway (Backend): Deploying... (2-3 minutes)
echo Vercel (Frontend): Deploying... (2-3 minutes)
echo.
echo After deployment completes:
echo 1. Visit: https://runtime-rush-production.up.railway.app/initialize-db
echo 2. Then test your Vercel URL
echo.
echo Press any key to exit...
pause
