# 🚀 QUICK RENDER DEPLOYMENT GUIDE

## Why Render?
- Free tier available
- Similar to Railway
- Auto-deploys from GitHub
- Fast setup (5 minutes)

## STEP 1: Create Render Account
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (easiest)

## STEP 2: Deploy Backend (FastAPI)
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `Runtime-Rush`
3. Configure:
   - **Name**: `runtime-rush-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

4. Click "Create Web Service"
5. Wait 2-3 minutes for deployment
6. Copy your backend URL (will be like: `https://runtime-rush-backend.onrender.com`)

## STEP 3: Update Frontend to Use Render Backend
After backend deploys, update the frontend API URL:

1. Open `frontend/src/services/api.ts`
2. Change line 3 to your Render URL:
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || "https://runtime-rush-backend.onrender.com";
```

3. Commit and push:
```bash
git add frontend/src/services/api.ts
git commit -m "Update API URL to Render backend"
git push
```

## STEP 4: Redeploy Frontend on Vercel
Vercel will auto-deploy when you push. Wait 1-2 minutes.

## STEP 5: Test
1. Go to your Vercel URL
2. Register a new user
3. Start Level 1 challenge
4. Test drag-drop
5. Login as admin: `mouniadmin` / `1214@`
6. Test terminate user

## Total Time: ~5-7 minutes

## Troubleshooting
If backend shows error, check Render logs:
- Go to your service on Render
- Click "Logs" tab
- Look for errors

## Need Help?
Just tell me which step you're on and I'll guide you!
