# New Features Implementation Plan

## 1. Fix Drag-Drop Bidirectional Shifting ✅
**Issue:** When dragging items down, items above don't shift properly
**Solution:** The current code already handles this correctly with insert logic. Need to verify it's working.

## 2. Tab Switch Detection & Penalties 🔴
**Requirements:**
- Detect when user switches tabs/windows or exits fullscreen
- Warning 1: Show warning, resume challenge
- Warning 2: Show warning, resume challenge  
- Warning 3: Auto-fail challenge, give 0 marks, move to next level
- Track violations in database
- Force fullscreen mode during challenge

**Implementation:**
- Add `tab_switch_count` field to User model
- Track violations per challenge attempt
- Show warnings with count
- Auto-fail on 3rd violation
- Use Fullscreen API to enforce fullscreen

## 3. Admin Dashboard - Show Violations 🔴
**Requirements:**
- Display tab switch violations as red marks/badges
- Show violation count for each user
- Visible in both Users tab and Leaderboard

**Implementation:**
- Add red badge/indicator showing violation count
- Update admin stats to include violations
- Update leaderboard to show violations

## Files to Modify:
1. `backend/app/models_sqlite.py` - Add tab_switch_count field
2. `backend/app/routers/auth.py` - Add endpoint to track violations
3. `frontend/src/components/DragDropChallenge.tsx` - Implement detection & fullscreen
4. `frontend/src/components/AdminDashboard.tsx` - Show violations
5. `frontend/src/components/Leaderboard.tsx` - Show violations
6. `frontend/src/services/api.ts` - Add API methods

## Estimated Time: 15-20 minutes
