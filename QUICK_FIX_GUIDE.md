# 🚨 QUICK FIX GUIDE - Runtime Rush

## Problem Summary
- ❌ Backend is NOT running
- ❌ Users cannot login
- ❌ Admin cannot login
- ❌ No challenges are showing
- ✅ Database exists and has data

## Root Cause
**The backend server is not running!** The frontend cannot connect to the API.

---

## ✅ SOLUTION - Follow These Steps:

### Option 1: Use the Batch File (EASIEST)
```bash
START_EVERYTHING.bat
```

This will:
1. Start the backend server on port 8000
2. Start the frontend server on port 3000
3. Open both in separate command windows

---

### Option 2: Manual Start (If batch file doesn't work)

#### Step 1: Start Backend
Open a NEW command prompt and run:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Keep this window open!** You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

#### Step 2: Start Frontend
Open ANOTHER command prompt and run:
```bash
cd frontend
npm start
```

**Keep this window open too!** Browser will open automatically.

---

### Step 3: Initialize Database (IMPORTANT!)
Once both servers are running, visit this URL in your browser:
```
http://localhost:8000/initialize-db
```

You should see:
```json
{
  "success": true,
  "message": "Database initialized successfully",
  "details": {
    "admin_created": true,
    "challenges_created": 12
  }
}
```

---

### Step 4: Test Login

#### Admin Login:
- Username: `mouniadmin`
- Password: `1214@`
- URL: http://localhost:3000

#### Create a Test User:
1. Click "Register here"
2. Fill in details
3. Login with your credentials

---

## 🎯 What You Should See Now:

### For Admin:
✅ Admin dashboard with statistics
✅ 12 challenges (3 levels × 4 languages)
✅ User list (empty initially)
✅ Challenge management

### For Users:
✅ Login/Register works
✅ Level 1 shows 4 challenges (Python, C, Java, C++)
✅ Language selector appears before starting
✅ Preview shows fragments in grid layout
✅ Can complete challenges and progress

---

## 🔍 Troubleshooting:

### If backend won't start:
```bash
# Check if port 8000 is already in use
netstat -ano | findstr :8000

# If something is using it, kill the process:
taskkill /PID <process_id> /F
```

### If frontend won't start:
```bash
# Check if port 3000 is already in use
netstat -ano | findstr :3000

# If something is using it, kill the process:
taskkill /PID <process_id> /F
```

### If you see "Failed to fetch challenges":
1. Make sure backend is running (check http://localhost:8000/health)
2. Check browser console for errors (F12)
3. Make sure you ran `/initialize-db`

---

## 📝 Deployment to Railway/Vercel:

Once everything works locally, deploy with:

```bash
# Commit changes
git add .
git commit -m "Fix: Add multi-language support and improved UI"
git push origin main
```

Then:
1. Railway auto-deploys backend (2-3 minutes)
2. Vercel auto-deploys frontend (2-3 minutes)
3. Visit: `https://runtime-rush-production.up.railway.app/initialize-db`

---

## ✅ Success Checklist:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Visited /initialize-db endpoint
- [ ] Admin can login
- [ ] Users can register and login
- [ ] Challenges are showing
- [ ] Language selector works
- [ ] Preview shows grid layout

---

## 🆘 Still Having Issues?

Check these files for errors:
1. Backend console output
2. Frontend console output (F12 in browser)
3. Network tab in browser (F12 → Network)

Common issues:
- **CORS errors**: Backend not running or wrong URL
- **404 errors**: Database not initialized
- **Login fails**: Wrong credentials or backend down
- **No challenges**: Database not initialized or backend down
