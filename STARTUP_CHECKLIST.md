# ✅ Runtime Rush - Startup Checklist

## Before You Start:

- [ ] Close all previous terminal windows
- [ ] Make sure ports 8000 and 3000 are free
- [ ] Have two terminal windows ready

---

## Step-by-Step Startup:

### 1️⃣ Start Backend (Terminal 1)

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Wait for this message:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

✅ Backend is running!

---

### 2️⃣ Start Frontend (Terminal 2)

```bash
cd frontend
npm start
```

**Wait for:**
```
Compiled successfully!
```

Browser should open automatically to http://localhost:3000

✅ Frontend is running!

---

### 3️⃣ Initialize Database (Browser)

Visit: http://localhost:8000/initialize-db

**Expected response:**
```json
{
  "success": true,
  "message": "Database initialized successfully",
  "details": {
    "admin_created": true,
    "challenges_created": 12,
    "errors": []
  }
}
```

✅ Database initialized!

---

### 4️⃣ Test Admin Login

1. Go to: http://localhost:3000
2. Enter credentials:
   - Username: `mouniadmin`
   - Password: `1214@`
3. Click "Login"

**You should see:**
- ✅ Admin Dashboard
- ✅ Beautiful animated header with logos
- ✅ Statistics showing 12 challenges
- ✅ Tabs: Statistics, Users, Challenges, Create Challenge

✅ Admin login works!

---

### 5️⃣ Test User Registration

1. Click "Logout" (top right)
2. Click "Register here"
3. Fill in:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `test123`
4. Click "Register"

**You should see:**
- ✅ Redirected to challenge list
- ✅ Level selector showing Level 1, 2, 3
- ✅ Level 1 is active
- ✅ 4 challenges visible

✅ User registration works!

---

### 6️⃣ Test Language Selection

1. Click "Start Challenge" on any Level 1 challenge
2. **Language selector modal should appear**
3. Select a language (Python, C, Java, or C++)
4. Modal closes
5. Badge shows "Selected Language: PYTHON" (or your choice)

**You should see:**
- ✅ Language selector modal with 4 options
- ✅ Beautiful cards with icons
- ✅ Selected language badge appears
- ✅ Only challenges in selected language show

✅ Language selection works!

---

### 7️⃣ Test Challenge Preview

1. Click "Start Challenge" again (after selecting language)
2. **Preview modal should appear for 3 seconds**
3. Preview shows fragments in **GRID layout** (side-by-side)
4. After 3 seconds, challenge starts

**You should see:**
- ✅ Preview shows fragments in grid (2-3 columns)
- ✅ NOT scrolling vertically
- ✅ Easy to see all fragments at once
- ✅ Countdown timer

✅ Preview works!

---

### 8️⃣ Test Challenge Completion

1. Drag and drop fragments in correct order
2. Click "Submit Solution"
3. If correct, see success message
4. Level 1 marked as completed
5. Progress to Level 2

**You should see:**
- ✅ Drag and drop works smoothly
- ✅ Submit button enabled when all fragments placed
- ✅ Success message with score
- ✅ Level 2 unlocked
- ✅ Level 1 shows "Completed ✓"

✅ Challenge completion works!

---

### 9️⃣ Test Level Progression

1. Click "Level 2" button
2. **Language selector appears again**
3. Select a language for Level 2
4. See 4 new challenges (Merge Sort)

**You should see:**
- ✅ Level 2 challenges are different (Merge Sort)
- ✅ Can select different language than Level 1
- ✅ Language is locked after selection
- ✅ 4 challenges in selected language

✅ Level progression works!

---

### 🔟 Test Leaderboard (After Completing All Levels)

1. Complete Level 1, 2, and 3
2. "View Leaderboard" button appears
3. Click it
4. See rankings with scores and times

**You should see:**
- ✅ Leaderboard button appears after completing all levels
- ✅ Rankings sorted by total score
- ✅ Shows individual level scores
- ✅ Shows time taken for each level
- ✅ Top 3 have medals (🥇🥈🥉)

✅ Leaderboard works!

---

## 🎯 Final Verification:

### Admin Dashboard:
- [ ] Can see all users
- [ ] Can see all challenges (12 total)
- [ ] Can filter by level (1, 2, 3)
- [ ] Can create new challenges
- [ ] Can delete challenges
- [ ] Header has animated gradients
- [ ] Logos are visible and floating

### User Experience:
- [ ] Registration works
- [ ] Login works
- [ ] Language selection works
- [ ] Language is locked after selection
- [ ] Preview shows grid layout
- [ ] Drag and drop works
- [ ] Challenge completion works
- [ ] Level progression works
- [ ] Leaderboard appears after completing all levels
- [ ] Thank you banner shows after completion

---

## 🐛 If Something Doesn't Work:

### Backend Issues:
```bash
# Check if backend is running
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

### Frontend Issues:
```bash
# Check browser console (F12)
# Look for red errors
```

### Database Issues:
```bash
# Re-initialize database
# Visit: http://localhost:8000/initialize-db
```

### Port Issues:
```bash
# Check what's using port 8000
netstat -ano | findstr :8000

# Check what's using port 3000
netstat -ano | findstr :3000

# Kill process if needed
taskkill /PID <process_id> /F
```

---

## 🚀 Ready to Deploy?

Once everything works locally:

```bash
git add .
git commit -m "Add multi-language support and UI improvements"
git push origin main
```

Then:
1. Wait 2-3 minutes for Railway/Vercel deployment
2. Visit: https://runtime-rush-production.up.railway.app/initialize-db
3. Test deployed app at your Vercel URL

---

## 📊 Expected Numbers:

- **Total Challenges:** 12
- **Level 1:** 4 (Armstrong Number in Python, C, Java, C++)
- **Level 2:** 4 (Merge Sort in Python, C, Java, C++)
- **Level 3:** 4 (Valid Parenthesis in Python, C, Java, C++)
- **Languages:** 4 (Python, C, Java, C++)
- **Fragments per challenge:** 4-5
- **Max score per level:** 100
- **Total max score:** 300

---

## ✅ All Done!

If you checked all boxes above, your Runtime Rush platform is working perfectly! 🎉

**Admin credentials:** mouniadmin / 1214@

**Test user:** testuser / test123 (or create your own)

Enjoy! 🚀
