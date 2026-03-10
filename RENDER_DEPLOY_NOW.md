# 🚀 RENDER DEPLOYMENT - 3 MINUTES!

## ✅ WHY RENDER IS BETTER:
- ✅ Persistent SQLite database
- ✅ Long-running server (not serverless)
- ✅ Free tier supports 50+ users
- ✅ Auto-deploys from GitHub

---

## 🎯 DO THIS NOW (3 STEPS):

### STEP 1: Sign Up (30 seconds)
**Go to**: https://dashboard.render.com/register

Click **"Sign up with GitHub"** → Authorize Render

---

### STEP 2: Create Web Service (1 minute)

1. Click **"New +"** → **"Web Service"**
2. Click **"Connect account"** if needed
3. Find **"Runtime-Rush"** repository → Click **"Connect"**
4. Fill in these EXACT values:

```
Name: runtime-rush-backend
Region: Singapore (or closest)
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```

5. Click **"Create Web Service"**

---

### STEP 3: Wait & Copy URL (2 minutes)

Watch the logs:
- Installing dependencies...
- Starting server...
- ✅ **Your service is live at https://runtime-rush-backend.onrender.com**

**COPY THIS URL!**

---

## 📋 COPY-PASTE VALUES:

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## ⚡ AFTER DEPLOYMENT:

**Tell me your Render URL** (like `https://runtime-rush-backend-xxxx.onrender.com`)

I'll update frontend in 10 seconds!

---

## 🆘 TROUBLESHOOTING:

**"Build failed"**
- Check Root Directory is set to "backend"
- Make sure latest code is pushed (I already did this)

**"Can't find requirements.txt"**
- Root Directory must be "backend" not "/"

---

## ⏱️ TIMELINE:
- **Now**: Sign up at Render
- **+1 min**: Create web service
- **+3 min**: Backend deployed
- **+4 min**: Frontend updated (I'll do this)
- **+5 min**: EVERYTHING WORKING!

---

## 🎯 START NOW!
https://dashboard.render.com/register
