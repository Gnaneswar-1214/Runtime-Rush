# Runtime Rush - Testing Guide

## 🧪 Complete Testing Checklist

### Prerequisites
1. Backend running on port 8000
2. Frontend running on port 3000
3. Database initialized with `/initialize-db` endpoint

---

## 1. Database Initialization

### Test: Initialize Database
```bash
# Method 1: Browser
http://localhost:8000/initialize-db

# Method 2: cURL
curl -X POST http://localhost:8000/initialize-db
```

**Expected Result:**
- Admin user created: `mouniadmin` / `1214@`
- 12 challenges created (3 levels × 4 languages)
- Success message returned

---

## 2. User Registration & Login

### Test: Register New User
1. Navigate to registration page
2. Enter username, email, password
3. Click Register

**Expected Result:**
- User created successfully
- Redirected to login or home page
- User starts at Level 1

### Test: Login
1. Navigate to login page
2. Enter credentials
3. Click Login

**Expected Result:**
- Successful login
- Redirected to challenge list
- User info displayed in header

---

## 3. Language Selection

### Test: Level 1 Language Selection
1. Login as a new user
2. Navigate to Level 1
3. Click on any challenge

**Expected Result:**
- Language selector modal appears
- 4 options shown: Python, C, Java, C++
- Each option has icon and name

### Test: Select Python
1. Click on Python option

**Expected Result:**
- Modal closes
- "Selected Language: PYTHON" badge appears
- Only Python challenges visible
- Challenge button changes to "Start Challenge →"

### Test: Language Lock
1. Try to select language again

**Expected Result:**
- No modal appears
- Language remains locked
- Cannot change selection

### Test: Different Languages Per Level
1. Complete Level 1 with Python
2. Move to Level 2
3. Select C language
4. Complete Level 2
5. Move to Level 3
6. Select Java language

**Expected Result:**
- Each level can have different language
- Language selection independent per level
- Previous selections preserved

---

## 4. Challenge Preview UI

### Test: Preview Display
1. Select a language
2. Click "Start Challenge"
3. Wait for "PREVIEW" text (1.5 seconds)
4. Observe preview screen

**Expected Result:**
- "PREVIEW" text appears with animation
- Preview screen shows fragments in grid layout
- 3-second countdown timer visible
- Fragments displayed in cards (2-3 columns on desktop)
- Each fragment numbered (1, 2, 3, 4...)
- Easy to see all fragments at once

### Test: Preview Timer
1. Watch the countdown

**Expected Result:**
- Timer counts down from 3 to 0
- Circular progress indicator
- After 0, "START!" animation appears
- Then challenge workspace loads

### Test: Grid Layout Responsiveness
1. Resize browser window
2. Test on mobile device

**Expected Result:**
- Desktop: 2-3 columns
- Tablet: 2 columns
- Mobile: 1 column
- All fragments visible without excessive scrolling

---

## 5. Challenge Completion

### Test: Complete Level 1
1. Start Armstrong Number challenge
2. Drag fragments to correct order
3. Submit solution

**Expected Result:**
- Success animation if correct
- Score calculated based on time
- Level 2 unlocked
- Progress saved

### Test: Complete All Levels
1. Complete Level 1 (any language)
2. Complete Level 2 (any language)
3. Complete Level 3 (any language)

**Expected Result:**
- Thank you banner appears
- "View Leaderboard" button visible
- All levels marked as completed
- Total score calculated

---

## 6. Admin Dashboard

### Test: Admin Login
1. Login with `mouniadmin` / `1214@`

**Expected Result:**
- Admin dashboard loads
- Enhanced header with animations
- Logos visible on both sides
- Gradient title with glow effect

### Test: Admin Header Animations
1. Hover over logos
2. Observe title animations

**Expected Result:**
- Logos scale and rotate on hover
- Title has gradient animation
- Shimmer effect in background
- Logout button has ripple effect

### Test: View Users
1. Click "Users" tab

**Expected Result:**
- Table shows all users
- Language selections visible (if any)
- Scores and times displayed
- Top 3 users highlighted

### Test: View Challenges
1. Click "Challenges" tab
2. Select Level 1

**Expected Result:**
- Shows 4 challenges (Python, C, Java, C++)
- Each challenge shows fragment count
- Delete button available

### Test: Create Challenge
1. Click "Create Challenge" tab
2. Fill in form:
   - Title: "Test Challenge"
   - Language: Python
   - Level: 1
   - Description: "Test description"
   - Add 3 fragments
   - Add 1 test case
3. Click "Create Challenge"

**Expected Result:**
- Challenge created successfully
- Alert shows success message
- Form resets
- New challenge appears in challenges list

**Note**: If only one challenge appears instead of expected behavior, this is the bug mentioned in requirements. Investigation needed.

---

## 7. Challenge Display

### Test: Challenge Cards
1. View challenge list as user
2. Observe card styling

**Expected Result:**
- Cards have gradient borders
- Hover effects work smoothly
- Language badge visible
- Fragment count shown
- Status badge (Active/Completed)

### Test: Language Badge
1. Select a language
2. Observe badge display

**Expected Result:**
- Badge shows selected language
- Gradient background
- Glow animation
- Positioned prominently

---

## 8. Responsive Design

### Test: Mobile View
1. Open on mobile device or resize browser
2. Test all features

**Expected Result:**
- Language selector: 1 column layout
- Preview grid: 1 column
- Challenge cards: 1 column
- Headers: Logos stack vertically
- All buttons accessible
- Text readable

### Test: Tablet View
1. Test on tablet or medium screen

**Expected Result:**
- Language selector: 2 columns
- Preview grid: 2 columns
- Challenge cards: 2 columns
- Headers: Horizontal layout maintained

---

## 9. Edge Cases

### Test: No Language Selected
1. Try to start challenge without selecting language

**Expected Result:**
- Modal appears automatically
- Cannot proceed without selection
- Button text: "Select Language First"

### Test: Already Completed Level
1. Complete a level
2. Try to start same level again

**Expected Result:**
- Challenge marked as "Completed ✓"
- Button disabled
- Cannot restart

### Test: Time Runs Out
1. Start a challenge
2. Wait for timer to reach 0:00

**Expected Result:**
- Auto-submit with 0 score
- Level marked as completed
- Can proceed to next level

### Test: Tab Switch During Challenge
1. Start a challenge
2. Switch to another browser tab
3. Return to challenge

**Expected Result:**
- Warning overlay appears
- Timer paused
- Must click "OK - Resume Challenge"
- Timer resumes

---

## 10. Performance Tests

### Test: Load Time
1. Measure page load times

**Expected Result:**
- Initial load < 3 seconds
- Challenge list < 1 second
- Preview transition smooth
- No lag in animations

### Test: Multiple Users
1. Open multiple browser windows
2. Login as different users
3. Complete challenges simultaneously

**Expected Result:**
- No conflicts
- Each user's progress independent
- Leaderboard updates correctly

---

## 11. Data Persistence

### Test: Refresh During Challenge
1. Start a challenge
2. Arrange some fragments
3. Refresh browser

**Expected Result:**
- Challenge state preserved
- Fragments remain in place
- Timer continues from saved time
- No preview shown again

### Test: Logout and Login
1. Select language for Level 1
2. Logout
3. Login again

**Expected Result:**
- Language selection preserved
- Progress maintained
- Can continue where left off

---

## 12. API Endpoint Tests

### Test: Language Selection API
```bash
# Select Python for Level 1
curl -X POST "http://localhost:8000/api/auth/users/{user_id}/select-language/1?language=python"
```

**Expected Result:**
```json
{
  "message": "Language python selected for Level 1",
  "level": 1,
  "language": "python"
}
```

### Test: Get User Progress
```bash
curl "http://localhost:8000/api/auth/users/{user_id}/progress"
```

**Expected Result:**
```json
{
  "user_id": "...",
  "current_level": 1,
  "level1_completed": false,
  "level2_completed": false,
  "level3_completed": false,
  "level1_language": "python",
  "level2_language": null,
  "level3_language": null,
  "total_score": 0
}
```

### Test: Get Challenges
```bash
curl "http://localhost:8000/api/challenges"
```

**Expected Result:**
- Returns array of 12 challenges
- Each has level, language, fragments
- Correct structure

---

## 13. Browser Compatibility

### Test: Chrome
- All features work
- Animations smooth
- No console errors

### Test: Firefox
- All features work
- Animations smooth
- No console errors

### Test: Safari
- All features work
- Animations smooth
- No console errors

### Test: Edge
- All features work
- Animations smooth
- No console errors

---

## 14. Accessibility

### Test: Keyboard Navigation
1. Use Tab key to navigate
2. Use Enter to select

**Expected Result:**
- All buttons accessible
- Focus indicators visible
- Can complete challenge with keyboard

### Test: Screen Reader
1. Use screen reader software

**Expected Result:**
- All text readable
- Buttons labeled correctly
- Navigation clear

---

## 🐛 Known Issues to Test

### Issue: Admin Challenge Creation
**Description**: "Currently only one challenge gets added when admin creates a challenge"

**Test Steps**:
1. Login as admin
2. Go to "Create Challenge" tab
3. Create a new challenge
4. Check if challenge appears in list
5. Check database to see if fragments and test cases saved

**Expected Behavior**:
- Challenge created with all fragments
- All test cases saved
- Challenge appears in correct level

**Actual Behavior** (if bug exists):
- Only challenge created, fragments missing?
- Test cases not saved?
- Need to investigate

**Debugging Steps**:
1. Check browser console for errors
2. Check network tab for API calls
3. Check backend logs
4. Verify database entries
5. Check if commit() called after all inserts

---

## 📊 Test Results Template

```
Test Date: ___________
Tester: ___________

| Test Category | Test Name | Status | Notes |
|---------------|-----------|--------|-------|
| Database Init | Initialize DB | ☐ Pass ☐ Fail | |
| User Auth | Register | ☐ Pass ☐ Fail | |
| User Auth | Login | ☐ Pass ☐ Fail | |
| Language Selection | Select Python | ☐ Pass ☐ Fail | |
| Language Selection | Language Lock | ☐ Pass ☐ Fail | |
| Preview UI | Grid Layout | ☐ Pass ☐ Fail | |
| Preview UI | Timer Countdown | ☐ Pass ☐ Fail | |
| Challenge | Complete Level 1 | ☐ Pass ☐ Fail | |
| Challenge | Complete All Levels | ☐ Pass ☐ Fail | |
| Admin | Login | ☐ Pass ☐ Fail | |
| Admin | View Users | ☐ Pass ☐ Fail | |
| Admin | Create Challenge | ☐ Pass ☐ Fail | |
| Responsive | Mobile View | ☐ Pass ☐ Fail | |
| Responsive | Tablet View | ☐ Pass ☐ Fail | |
| Edge Cases | No Language Selected | ☐ Pass ☐ Fail | |
| Edge Cases | Time Runs Out | ☐ Pass ☐ Fail | |
| Edge Cases | Tab Switch | ☐ Pass ☐ Fail | |
```

---

## 🚀 Quick Smoke Test (5 minutes)

1. ✅ Initialize database
2. ✅ Register new user
3. ✅ Select language (Python)
4. ✅ Start challenge
5. ✅ View preview (grid layout)
6. ✅ Complete challenge
7. ✅ Check score
8. ✅ Login as admin
9. ✅ View users table
10. ✅ Check enhanced headers

If all pass, major features working!

---

## 📝 Bug Report Template

```
**Bug Title**: 
**Severity**: Critical / High / Medium / Low
**Steps to Reproduce**:
1. 
2. 
3. 

**Expected Result**:

**Actual Result**:

**Screenshots**: (if applicable)

**Browser**: 
**OS**: 
**Date Found**: 
```

---

## ✅ Success Criteria

All tests should pass with:
- ✅ No console errors
- ✅ Smooth animations
- ✅ Correct data persistence
- ✅ Responsive on all devices
- ✅ All features functional
- ✅ Good user experience

---

**Happy Testing! 🎉**
