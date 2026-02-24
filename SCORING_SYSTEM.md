# Time-Based Scoring System

## Overview
The Runtime Rush platform uses a time-based scoring system where faster submissions earn higher scores.

## Scoring Rules

### Base Points & Time
- **Each Level**: 100 marks, 3 minutes (180 seconds)
- **Total Possible**: 300 marks (100 + 100 + 100)

### Score Calculation
- **Score decreases** by 0.5556 marks per second
- **Formula**: Score = 100 - (time_taken × 0.5556)
- **Minimum score**: 0 marks

### Examples
**If you submit with:**
- **0 seconds taken** (instant): 100.00 marks
- **1 second taken**: 99.44 marks
- **30 seconds taken**: 83.33 marks
- **60 seconds taken**: 66.67 marks
- **90 seconds taken**: 50.00 marks
- **120 seconds taken**: 33.33 marks
- **150 seconds taken**: 16.67 marks
- **179 seconds taken**: 0.56 marks
- **180 seconds taken**: 0.00 marks

## Timer System
- Each level has **exactly 3 minutes** (180 seconds)
- Timer starts after 3-second code preview
- Time taken is recorded for scoring

## One Attempt Only
- **Cannot retry** after submitting a level
- Completed levels show "Already Completed"
- Button is disabled for completed levels

## Score Display
After completing each level:
1. **Success animation** appears
2. **Score earned** is displayed (e.g., "You earned: 95.67 marks")
3. **Auto-advance** to next level after 3 seconds
4. **Cannot go back** to retry

## Admin Dashboard Features

### Leaderboard View
The admin dashboard shows:
1. **Rank**: Position based on total score
2. **Username & Email**
3. **Current Level**
4. **Level Scores**: Individual scores out of 100
5. **Total Score**: Sum out of 300

### Example Display
```
Rank | Username | Level | L1 Score  | L2 Score  | L3 Score  | Total
-----|----------|-------|-----------|-----------|-----------|----------
#1   | user1    | 3     | 95.67/100 | 98.33/100 | 92.22/100 | 286.22/300
#2   | user2    | 3     | 88.89/100 | 85.56/100 | 90.00/100 | 264.45/300
#3   | user3    | 2     | 75.00/100 | 80.00/100 | -         | 155.00/300
```

## Database Schema

### UserProgress Table
New fields added:
- `level1_score`: Points earned for level 1
- `level2_score`: Points earned for level 2
- `level3_score`: Points earned for level 3
- `level1_time_taken`: Seconds taken to complete level 1
- `level2_time_taken`: Seconds taken to complete level 2
- `level3_time_taken`: Seconds taken to complete level 3
- `level1_submission_order`: 1st, 2nd, 3rd, etc.
- `level2_submission_order`: 1st, 2nd, 3rd, etc.
- `level3_submission_order`: 1st, 2nd, 3rd, etc.
- `total_score`: Sum of all level scores

## API Endpoints

### Complete Level
```
POST /api/auth/users/{user_id}/complete-level/{level}?time_taken={seconds}
```

**Response:**
```json
{
  "message": "Level 1 completed!",
  "current_level": 2,
  "score": 30,
  "submission_order": 1,
  "total_score": 30
}
```

### Get All Users (Admin)
```
GET /api/admin/users?admin_id={admin_id}
```

**Response includes:**
- All user details
- Individual level scores
- Submission orders
- Total scores

## Testing

### Test Users
- **Admin**: username=`admin`, password=`admin123`
- **Test User**: username=`testuser`, password=`password123`

### Test Scenario
1. Login as testuser
2. Complete Level 1 (should get 30 points as 1st)
3. Create another user and complete Level 1 (should get 29 points as 2nd)
4. Login as admin to view leaderboard

## Implementation Details

### Frontend Changes
1. Timer fixed to exactly 5 minutes
2. Time taken calculated and sent to backend
3. Success message shows score earned

### Backend Changes
1. Score calculation based on submission order
2. Minimum score enforcement (50% of base)
3. Admin API returns detailed score data

### Database Changes
1. New columns for scores and submission orders
2. Automatic total score calculation
3. Time tracking for each level
