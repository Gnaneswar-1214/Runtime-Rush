# 🔄 Admin Credentials and Challenges Update

## Changes Made

### 1. Admin Credentials Updated
**Old:**
- Username: `admin`
- Password: `admin123`

**New:**
- Username: `mouni`
- Password: `1214@`

### 2. Challenge Fragments Reduced

Each challenge now has **4-5 fragments** instead of 8-10 for easier gameplay.

**Level 1: Binary Search (5 fragments)**
1. `def binary_search(arr, target):\n    left, right = 0, len(arr) - 1`
2. `    while left <= right:\n        mid = (left + right) // 2`
3. `        if arr[mid] == target:\n            return mid`
4. `        elif arr[mid] < target:\n            left = mid + 1`
5. `        else:\n            right = mid - 1\n    return -1`

**Level 2: Quick Sort (5 fragments)**
1. `def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr`
2. `    pivot = arr[len(arr) // 2]`
3. `    left = [x for x in arr if x < pivot]`
4. `    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]`
5. `    return quick_sort(left) + middle + quick_sort(right)`

**Level 3: Merge Sort (5 fragments)**
1. `def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr`
2. `    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])`
3. `    return merge(left, right)\n\ndef merge(left, right):\n    result = []`
4. `    i = j = 0\n    while i < len(left) and j < len(right):`
5. `    if left[i] <= right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result`

## Files Updated

1. `backend/app/main.py` - Updated `/initialize-db` endpoint
2. `backend/init_db.py` - Updated standalone initialization script

## Next Steps

### 1. Push to Git
```powershell
git add .
git commit -m "Update admin credentials and reduce challenge fragments to 4-5"
git push origin main
```

### 2. Wait for Railway to Redeploy
- Go to https://railway.app
- Wait for deployment to complete (2-3 minutes)

### 3. Initialize Database with New Data
```powershell
Invoke-WebRequest -Uri "https://runtime-rush-production.up.railway.app/initialize-db" -Method POST
```

### 4. Test New Admin Login
- Go to your Vercel website
- Login with:
  - Username: `mouni`
  - Password: `1214@`

## Important Notes

⚠️ **If you already initialized the database with old admin credentials:**

The new initialization will NOT overwrite the existing admin user. You have two options:

**Option A: Keep both admins**
- Old admin (admin/admin123) will still work
- New admin (mouni/1214@) will be created alongside

**Option B: Reset database (deletes all data)**
1. Go to Railway dashboard
2. Delete the database file or reset the service
3. Redeploy
4. Run initialization again

## Testing Checklist

After deployment:
- [ ] Railway deployment successful
- [ ] `/initialize-db` endpoint called
- [ ] Can login with username: `mouni` and password: `1214@`
- [ ] Level 1 shows 5 fragments
- [ ] Level 2 shows 5 fragments
- [ ] Level 3 shows 5 fragments
- [ ] Challenges are easier to complete

## Summary

✅ Admin username changed to `mouni`
✅ Admin password changed to `1214@`
✅ All challenges now have 4-5 fragments (easier gameplay)
✅ Ready to push and deploy!
