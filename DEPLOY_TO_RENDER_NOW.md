# ⚡ DEPLOY TO RENDER NOW - 5 MINUTE GUIDE

## 🎯 FASTEST PATH - DO THIS NOW:

### 1️⃣ Go to Render (1 minute)
**Open this link**: https://dashboard.render.com/register

- Click "Sign up with GitHub"
- Authorize Render to access your repositories

### 2️⃣ Create Backend Service (2 minutes)
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Find and select your **"Runtime-Rush"** repository
4. Fill in these EXACT values:

```
Name: runtime-rush-backend
Region: Singapore (or closest to you)
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```

5. Click **"Create Web Service"**
6. **WAIT 2-3 MINUTES** - Render will build and deploy
7. **COPY YOUR URL** - It will look like: `https://runtime-rush-backend.onrender.com`

### 3️⃣ Update Frontend (1 minute)
I'll do this for you right now! Just tell me your Render backend URL when it's ready.

### 4️⃣ Done! (1 minute)
Vercel will auto-deploy your frontend. Wait 1 minute, then test!

---

## 📋 COPY-PASTE VALUES FOR RENDER:

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## ✅ WHAT TO EXPECT:

1. **Render Build Logs** - You'll see:
   - Installing dependencies...
   - Starting server...
   - ✅ "Your service is live"

2. **Backend URL** - Copy this URL from Render dashboard

3. **Tell me the URL** - I'll update your frontend immediately

---

## 🆘 IF YOU GET STUCK:

Just tell me:
- "I'm on step 1" - I'll guide you through Render signup
- "I'm on step 2" - I'll help with service creation
- "Backend is deployed" - Give me the URL and I'll update frontend
- "I see an error" - Tell me what it says

---

## ⏱️ TIMELINE:
- **Now**: Start Render signup
- **+1 min**: Create web service
- **+3 min**: Backend deployed
- **+4 min**: Frontend updated
- **+5 min**: EVERYTHING WORKING!

**START NOW! Go to: https://dashboard.render.com/register**
