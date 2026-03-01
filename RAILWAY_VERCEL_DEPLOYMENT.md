# 🚀 Railway + Vercel Deployment Guide

## Issues You're Facing

1. ❌ No challenges loading → Database is empty on Railway
2. ❌ Admin not logging in → Admin user doesn't exist in Railway database
3. ❌ CORS errors → Frontend can't communicate with backend

## ✅ Solution: Step-by-Step Fix

### Step 1: Initialize Railway Database

After deploying your backend to Railway, you need to initialize the database with admin user and challenges.

**Option A: Use the API endpoint (Recommended)**

1. Open your browser or Postman
2. Make a POST request to: `https://your-railway-url.railway.app/initialize-db`
3. You should see a success response with:
   ```json
   {
     "success": true,
     "message": "Database initialized successfully",
     "details": {
       "admin_created": true,
       "challenges_created": 3
     }
   }
   ```

**Option B: Use the Python script**

1. SSH into Railway or run locally pointing to Railway:
   ```bash
   cd backend
   python init_db.py
   ```

### Step 2: Verify Backend is Working

Test these endpoints on your Railway URL:

1. **Health Check**: `GET https://your-railway-url.railway.app/health`
   - Should return: `{"status": "healthy"}`

2. **Get Challenges**: `GET https://your-railway-url.railway.app/api/challenges`
   - Should return array of 3 challenges

3. **Admin Login**: `POST https://your-railway-url.railway.app/api/auth/login`
   - Body: `{"username": "admin", "password": "admin123"}`
   - Should return user object with role "admin"

### Step 3: Update Frontend API URL

Make sure your frontend is pointing to the correct Railway URL.

In `frontend/src/services/api.ts`, the API_BASE_URL should be:
```typescript
const API_BASE_URL =
  process.env.REACT_APP_API_URL ||
  "https://your-actual-railway-url.railway.app";
```

### Step 4: Set Environment Variable in Vercel

1. Go to your Vercel project settings
2. Navigate to "Environment Variables"
3. Add: `REACT_APP_API_URL` = `https://your-railway-url.railway.app`
4. Redeploy your frontend

### Step 5: Verify CORS is Working

The backend now allows all origins (`allow_origins=["*"]`). This should fix CORS issues.

If you still have CORS problems:
1. Check browser console for exact error
2. Verify Railway URL is correct
3. Make sure Railway backend is actually running

## 🔧 Railway Configuration

### Required Files

**Procfile** (if not auto-detected):
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**runtime.txt** (specify Python version):
```
python-3.11.0
```

**requirements.txt** (make sure it includes):
```
fastapi
uvicorn[standard]
sqlalchemy
pydantic
pydantic[email]
```

### Railway Environment Variables

You don't need any environment variables for basic setup, but you can add:
- `DATABASE_URL` - if you want to use PostgreSQL instead of SQLite
- `CORS_ORIGINS` - if you want to restrict CORS to specific domains

## 🌐 Vercel Configuration

### Build Settings

- **Framework Preset**: Create React App
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Install Command**: `npm install`

### Environment Variables

Add in Vercel dashboard:
```
REACT_APP_API_URL=https://your-railway-url.railway.app
```

## 🐛 Troubleshooting

### Problem: Challenges not loading

**Check:**
1. Did you call `/initialize-db` endpoint?
2. Is Railway backend actually running? Check Railway logs
3. Open browser DevTools → Network tab → Check API calls

**Fix:**
```bash
# Call the initialization endpoint
curl -X POST https://your-railway-url.railway.app/initialize-db
```

### Problem: Admin can't login

**Check:**
1. Was admin user created? Check `/initialize-db` response
2. Are you using correct credentials? (admin / admin123)
3. Check Railway logs for errors

**Fix:**
```bash
# Reinitialize database
curl -X POST https://your-railway-url.railway.app/initialize-db
```

### Problem: CORS errors

**Check:**
1. Browser console shows exact CORS error
2. Railway backend URL is correct in frontend
3. Backend is actually running

**Fix:**
- Backend now allows all origins
- Make sure you're using HTTPS for Railway URL
- Redeploy both frontend and backend

### Problem: Database resets on Railway restart

**Issue:** SQLite file is lost when Railway restarts

**Solution:** Use Railway's volume mounting:
1. Go to Railway project settings
2. Add a volume mount: `/app/backend` → `/data`
3. Update `database.py`:
   ```python
   DATABASE_URL = "sqlite:////data/runtime_rush.db"
   ```

**Better Solution:** Use PostgreSQL on Railway:
1. Add PostgreSQL plugin in Railway
2. Update `database.py` to use `DATABASE_URL` environment variable
3. Install `psycopg2-binary` in requirements.txt

## 📝 Quick Checklist

- [ ] Backend deployed to Railway
- [ ] Called `/initialize-db` endpoint
- [ ] Verified `/health` endpoint works
- [ ] Verified `/api/challenges` returns 3 challenges
- [ ] Updated frontend API URL to Railway URL
- [ ] Set `REACT_APP_API_URL` in Vercel
- [ ] Redeployed frontend to Vercel
- [ ] Tested admin login (admin / admin123)
- [ ] Tested user registration
- [ ] Tested challenge loading

## 🎯 Expected Results

After following all steps:

1. ✅ Frontend loads on Vercel
2. ✅ Backend responds on Railway
3. ✅ Admin can login
4. ✅ 3 challenges appear (Binary Search, Quick Sort, Merge Sort)
5. ✅ Users can register and complete challenges
6. ✅ Leaderboard works

## 🆘 Still Having Issues?

1. Check Railway logs: Railway Dashboard → Your Project → Deployments → Logs
2. Check Vercel logs: Vercel Dashboard → Your Project → Deployments → Function Logs
3. Check browser console: F12 → Console tab
4. Check network requests: F12 → Network tab

Share the error messages and I can help debug further!
