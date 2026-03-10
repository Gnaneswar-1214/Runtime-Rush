# 🧪 Localhost Testing Guide

## Quick Start

**Double-click:** `START_LOCALHOST_TEST.bat`

This will open 2 command windows:
- Backend Server (port 8000)
- Frontend Server (port 3000)

## Manual Start (if batch file doesn't work)

### Terminal 1 - Backend:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm start
```

## Testing Checklist

### 1. Basic Functionality ✓
- [ ] Open http://localhost:3000
- [ ] Register a new test user
- [ ] Login with test user
- [ ] Select a language for Level 1

### 2. Drag-Drop Testing ✓
- [ ] Start Level 1 challenge
- [ ] Drag fragments UP - items below should shift up
- [ ] Drag fragments DOWN - items above should shift down
- [ ] Verify both directions work correctly

### 3. Tab Switch Detection (3-Strike System) ✓
- [ ] Challenge should enter FULLSCREEN automatically
- [ ] Press Alt+Tab to switch away - **Warning 1** should appear
- [ ] Click OK, press Alt+Tab again - **Warning 2** should appear
- [ ] Click OK, press Alt+Tab 3rd time - **Auto-fail with 0 marks**
- [ ] Should move to next level automatically

### 4. Fullscreen Exit Detection ✓
- [ ] Start a challenge
- [ ] Press ESC to exit fullscreen - should count as violation
- [ ] Same 3-strike system applies

### 5. Admin Dashboard - Violations Display ✓
- [ ] Login as admin: `mouniadmin` / `1214@`
- [ ] Go to Users tab
- [ ] Check "VIOLATIONS" column shows red badges 🚫
- [ ] Users with 0 violations show green checkmark ✓

### 6. Leaderboard - Violations Display ✓
- [ ] Complete all 3 levels with a user
- [ ] View leaderboard
- [ ] Check "Violations" column shows correctly

### 7. Delete User Feature (Already Working) ✓
- [ ] Admin dashboard → Users tab
- [ ] Click "🗑️ Terminate" button
- [ ] Confirm deletion works

## Expected Behavior

### Tab Switch Warnings:
- **1st violation:** "Warning 1 of 3 - First warning"
- **2nd violation:** "Warning 2 of 3 - Second warning - one more will fail!"
- **3rd violation:** Auto-fail, 0 marks, move to next level

### Fullscreen:
- Automatically enters fullscreen when challenge starts
- Exiting fullscreen counts as violation
- Must stay in fullscreen during challenge

### Admin View:
- Red badge 🚫 with count for users with violations
- Green ✓ for users with no violations

## After Testing

If everything works:

1. **Revert API URL** in `frontend/src/services/api.ts`:
   ```typescript
   const API_BASE_URL = "https://runtime-rush-backend2.onrender.com";
   ```

2. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add tab switch detection, fullscreen enforcement, and violation tracking"
   git push origin main
   ```

3. **Wait for auto-deploy:**
   - Vercel: ~2 minutes
   - Render: ~3-5 minutes

## Troubleshooting

### Backend won't start:
- Make sure Python is installed
- Install dependencies: `cd backend && pip install -r requirements.txt`

### Frontend won't start:
- Make sure Node.js is installed
- Install dependencies: `cd frontend && npm install`

### Database errors:
- Delete `backend/runtime_rush.db` and restart backend

### Port already in use:
- Kill processes on ports 8000 and 3000
- Or change ports in the commands
