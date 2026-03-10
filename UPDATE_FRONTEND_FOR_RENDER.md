# 🔄 Frontend Update for Render Backend

## When Your Render Backend is Ready:

### Tell me your Render URL
It will look like: `https://runtime-rush-backend-XXXX.onrender.com`

### I will update these files:
1. `frontend/src/services/api.ts` - Change API_BASE_URL
2. `frontend/src/components/AdminDashboard.tsx` - Update admin API calls

### Then I'll commit and push:
```bash
git add frontend/
git commit -m "Switch to Render backend"
git push
```

### Vercel will auto-deploy in 1 minute!

---

## OR Do It Yourself (30 seconds):

1. Open `frontend/src/services/api.ts`
2. Change line 3 to:
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || "https://YOUR-RENDER-URL.onrender.com";
```

3. Open `frontend/src/components/AdminDashboard.tsx`
4. Find line 104 (in handleTerminateUser function)
5. Change to:
```typescript
const response = await fetch(
  `https://YOUR-RENDER-URL.onrender.com/api/admin/users/${userId}?admin_id=${user.id}`,
  { method: "DELETE" }
);
```

6. Save, commit, push:
```bash
git add frontend/
git commit -m "Switch to Render backend"
git push
```

---

## Just Give Me Your Render URL!
I'll do everything for you in 10 seconds!
