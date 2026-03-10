# 📸 RENDER STEP-BY-STEP GUIDE

## STEP 1: Open Render
**URL**: https://dashboard.render.com/register

Click **"Sign up with GitHub"**

---

## STEP 2: New Web Service
After login, you'll see the dashboard.

Click the blue **"New +"** button (top right)

Select **"Web Service"**

---

## STEP 3: Connect Repository
You'll see "Connect a repository"

If you don't see your repos:
- Click **"Connect account"** 
- Authorize Render to access GitHub

Find **"Runtime-Rush"** in the list

Click **"Connect"** button next to it

---

## STEP 4: Configure Service (MOST IMPORTANT!)

Fill in these EXACT values:

**Name:**
```
runtime-rush-backend
```

**Region:**
```
Singapore
```
(or choose closest to your location)

**Branch:**
```
main
```

**Root Directory:**
```
backend
```
⚠️ **CRITICAL**: Type "backend" here!

**Runtime:**
```
Python 3
```

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:**
```
Free
```

---

## STEP 5: Deploy!
Scroll down and click **"Create Web Service"**

---

## STEP 6: Watch Logs (2-3 minutes)
You'll see:
```
==> Cloning from https://github.com/...
==> Installing dependencies...
==> Collecting fastapi...
==> Starting server...
==> Your service is live 🎉
```

---

## STEP 7: Copy URL
After "Your service is live", you'll see:
```
https://runtime-rush-backend-xxxx.onrender.com
```

**COPY THIS ENTIRE URL!**

---

## STEP 8: Tell Me!
Paste the URL here and I'll update your frontend immediately!

---

## 🎯 QUICK CHECKLIST:
- [ ] Signed up at Render with GitHub
- [ ] Clicked "New +" → "Web Service"
- [ ] Connected Runtime-Rush repository
- [ ] Set Root Directory to "backend"
- [ ] Set Build Command correctly
- [ ] Set Start Command correctly
- [ ] Clicked "Create Web Service"
- [ ] Waited for deployment (2-3 min)
- [ ] Copied the URL
- [ ] Told me the URL

---

## ⏱️ EXPECTED TIME:
- Sign up: 30 seconds
- Configure: 1 minute
- Deploy: 2-3 minutes
- **Total: ~4 minutes**

---

## 🚀 START NOW!
https://dashboard.render.com/register
