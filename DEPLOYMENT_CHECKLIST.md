# ✅ Deployment Checklist

## Before You Start

- [ ] Backend code is pushed to Railway
- [ ] Frontend code is pushed to Vercel
- [ ] You have your Railway URL (e.g., `https://your-app.railway.app`)
- [ ] You have your Vercel URL (e.g., `https://your-app.vercel.app`)

## Step 1: Initialize Railway Database

Choose ONE method:

### Method A: Browser/Postman (Easiest)
- [ ] Open browser or Postman
- [ ] Make POST request to: `https://your-railway-url.railway.app/initialize-db`
- [ ] Verify response shows `"success": true`

### Method B: Test Script
- [ ] Run: `python test_deployment.py https://your-railway-url.railway.app`
- [ ] Verify all 5 tests pass

### Method C: Curl Commands
- [ ] Edit `test_api_commands.bat` (Windows) or `test_api_commands.sh` (Mac/Linux)
- [ ] Replace `your-app.railway.app` with your actual Railway URL
- [ ] Run the script
- [ ] Verify all commands succeed

## Step 2: Verify Backend

Test these URLs in your browser:

- [ ] `https://your-railway-url.railway.app/health`
  - Should return: `{"status":"healthy"}`

- [ ] `https://your-railway-url.railway.app/api/challenges`
  - Should return: Array with 3 challenges

## Step 3: Verify Admin Login

- [ ] Go to your Vercel site
- [ ] Click Login
- [ ] Enter username: `admin`
- [ ] Enter password: `admin123`
- [ ] Verify you can access admin dashboard

## Step 4: Test User Flow

- [ ] Register a new user account
- [ ] Verify you see 3 levels (Binary Search, Quick Sort, Merge Sort)
- [ ] Try Level 1 challenge
- [ ] Verify drag-and-drop works
- [ ] Verify timer works
- [ ] Complete the challenge
- [ ] Verify score is recorded

## Step 5: Test Admin Features

Login as admin and verify:

- [ ] Statistics tab shows correct counts
- [ ] Users tab shows registered users
- [ ] Challenges tab shows 3 challenges
- [ ] Can view challenges by level

## Common Issues & Fixes

### Issue: "No challenges found"
**Fix:** Run the initialization endpoint again
```bash
curl -X POST https://your-railway-url.railway.app/initialize-db
```

### Issue: "Admin login failed"
**Fix:** Check if admin was created
```bash
curl -X POST https://your-railway-url.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Issue: CORS errors in browser console
**Fix:** 
1. Verify Railway URL is correct in frontend
2. Check `frontend/src/services/api.ts` has correct URL
3. Redeploy frontend to Vercel

### Issue: "Failed to fetch" errors
**Fix:**
1. Check Railway is actually running (visit health endpoint)
2. Check Railway logs for errors
3. Verify Railway URL is accessible

## Final Verification

- [ ] Frontend loads without errors
- [ ] Backend responds to API calls
- [ ] Admin can login
- [ ] Users can register
- [ ] Challenges load correctly
- [ ] Drag-and-drop works
- [ ] Timer counts down
- [ ] Scores are saved
- [ ] Leaderboard displays after completing all levels

## 🎉 Success Criteria

If all items are checked, your deployment is successful!

**Admin Credentials:**
- Username: `admin`
- Password: `admin123`

**Test User (if you created one):**
- Username: `testuser`
- Password: `test123`

## 📞 Still Having Issues?

1. Check Railway logs
2. Check Vercel logs  
3. Check browser console (F12)
4. Run test script: `python test_deployment.py https://your-railway-url.railway.app`
5. Share error messages for help

## 🔄 If You Need to Reset

To reset the database and start fresh:

1. Delete the database file on Railway (if using SQLite)
2. Or drop all tables (if using PostgreSQL)
3. Redeploy backend
4. Run initialization endpoint again

## 📚 Documentation Files

- `RAILWAY_VERCEL_DEPLOYMENT.md` - Detailed deployment guide
- `DEPLOYMENT_FIX_SUMMARY.md` - Quick summary of fixes
- `test_deployment.py` - Automated test script
- `test_api_commands.bat` - Windows curl commands
- `test_api_commands.sh` - Mac/Linux curl commands
- `backend/init_db.py` - Database initialization script
