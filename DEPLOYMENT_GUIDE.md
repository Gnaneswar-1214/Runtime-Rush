# Runtime Rush Platform - Deployment Guide

## Why Servers Stop When You Close the Terminal

When you run `npm run dev` or `uvicorn`, these processes are attached to your terminal session. When you close the terminal or press Ctrl+C, the processes are terminated. This is normal behavior for development servers.

To keep servers running permanently, you need to:
1. Run them as background services
2. Use process managers
3. Deploy to a hosting platform

---

## Option 1: Local Deployment (Keep Running on Your PC)

### Method A: Using PM2 (Recommended for Local)

PM2 is a process manager that keeps your apps running even after closing the terminal.

#### 1. Install PM2 globally
```bash
npm install -g pm2
```

#### 2. Create PM2 ecosystem file
Create `ecosystem.config.js` in the root directory:

```javascript
module.exports = {
  apps: [
    {
      name: 'runtime-rush-backend',
      cwd: './backend',
      script: 'uvicorn',
      args: 'app.main:app --host 0.0.0.0 --port 8000',
      interpreter: 'python',
      env: {
        PYTHONPATH: '.'
      }
    },
    {
      name: 'runtime-rush-frontend',
      cwd: './frontend',
      script: 'npm',
      args: 'start',
      env: {
        PORT: 3000
      }
    }
  ]
};
```

#### 3. Start both servers with PM2
```bash
# Start all apps
pm2 start ecosystem.config.js

# View status
pm2 status

# View logs
pm2 logs

# Stop all apps
pm2 stop all

# Restart all apps
pm2 restart all

# Delete all apps
pm2 delete all
```

#### 4. Make PM2 start on system boot (optional)
```bash
pm2 startup
pm2 save
```

### Method B: Using Windows Services (Windows Only)

#### 1. Install NSSM (Non-Sucking Service Manager)
Download from: https://nssm.cc/download

#### 2. Create Backend Service
```cmd
nssm install RuntimeRushBackend "C:\path\to\python.exe" "C:\path\to\uvicorn" "app.main:app --host 0.0.0.0 --port 8000"
nssm set RuntimeRushBackend AppDirectory "C:\path\to\backend"
nssm start RuntimeRushBackend
```

#### 3. Create Frontend Service
```cmd
nssm install RuntimeRushFrontend "C:\path\to\npm.cmd" "start"
nssm set RuntimeRushFrontend AppDirectory "C:\path\to\frontend"
nssm start RuntimeRushFrontend
```

---

## Option 2: Production Deployment (Recommended for Events)

### A. Deploy to Cloud Platform

#### 1. **Vercel (Frontend) + Railway (Backend)** - Easiest

**Frontend on Vercel:**
```bash
cd frontend
npm run build
# Install Vercel CLI
npm install -g vercel
# Deploy
vercel
```

**Backend on Railway:**
1. Go to https://railway.app
2. Create new project
3. Connect your GitHub repo
4. Railway will auto-detect FastAPI
5. Add environment variables if needed
6. Deploy!

#### 2. **Heroku (Full Stack)**

**Backend:**
Create `Procfile` in backend folder:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Create `runtime.txt`:
```
python-3.11
```

Deploy:
```bash
cd backend
heroku create runtime-rush-backend
git push heroku main
```

**Frontend:**
```bash
cd frontend
npm run build
# Deploy build folder to Heroku or Netlify
```

#### 3. **DigitalOcean / AWS / Azure**

Use Docker for easy deployment (see Docker section below).

---

## Option 3: Docker Deployment (Professional)

### 1. Create Dockerfile for Backend

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create Dockerfile for Frontend

Create `frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
```

### 3. Create docker-compose.yml

Create `docker-compose.yml` in root:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - ./backend/runtime_rush.db:/app/runtime_rush.db
    environment:
      - PYTHONPATH=/app
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped
```

### 4. Run with Docker
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build
```

---

## Option 4: Simple Background Running (Quick Fix)

### Windows (PowerShell)

**Backend:**
```powershell
cd backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

**Frontend:**
```powershell
cd frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm start"
```

### Linux/Mac

**Backend:**
```bash
cd backend
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
```

**Frontend:**
```bash
cd frontend
nohup npm start > frontend.log 2>&1 &
```

To stop:
```bash
# Find process IDs
ps aux | grep uvicorn
ps aux | grep node

# Kill processes
kill <PID>
```

---

## Production Build (For Events)

### 1. Build Frontend for Production
```bash
cd frontend
npm run build
```

This creates an optimized `build` folder.

### 2. Serve Frontend with Backend

Update `backend/app/main.py` to serve static files:

```python
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Add after creating app
if os.path.exists("../frontend/build"):
    app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")
    
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        if full_path.startswith("api/"):
            return {"error": "Not found"}
        file_path = f"../frontend/build/{full_path}"
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse("../frontend/build/index.html")
```

Now you only need to run the backend:
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Access at: http://localhost:8000

---

## Network Access (For Event Participants)

### 1. Find Your Local IP Address

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

**Linux/Mac:**
```bash
ifconfig
# or
ip addr show
```

### 2. Update Frontend API URL

Edit `frontend/src/services/api.ts`:
```typescript
const API_BASE_URL = 'http://YOUR_IP_ADDRESS:8000/api';
// Example: 'http://192.168.1.100:8000/api'
```

### 3. Allow Firewall Access

**Windows:**
```cmd
netsh advfirewall firewall add rule name="Runtime Rush Backend" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="Runtime Rush Frontend" dir=in action=allow protocol=TCP localport=3000
```

### 4. Share URLs with Participants
- Frontend: `http://YOUR_IP:3000`
- Backend API: `http://YOUR_IP:8000`

---

## Recommended Setup for Your Event

### For Development/Testing:
Use **PM2** (Option 1A) - Easy to start/stop, view logs

### For Production Event:
1. **Build frontend** for production
2. **Serve from backend** (single server)
3. Use **PM2** or **Docker** to keep running
4. Share your local IP with participants

### Quick Start Script

Create `start.bat` (Windows) or `start.sh` (Linux/Mac):

**Windows (start.bat):**
```batch
@echo off
echo Starting Runtime Rush Platform...

cd backend
start "Backend Server" cmd /k "uvicorn app.main:app --host 0.0.0.0 --port 8000"

cd ../frontend
start "Frontend Server" cmd /k "npm start"

echo Servers started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
pause
```

**Linux/Mac (start.sh):**
```bash
#!/bin/bash
echo "Starting Runtime Rush Platform..."

cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ../frontend
npm start &
FRONTEND_PID=$!

echo "Servers started!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Press Ctrl+C to stop"

wait
```

---

## Troubleshooting

### Servers stop when closing terminal
- Use PM2, Docker, or nohup (see above)
- Don't close the terminal window
- Use Windows Services (NSSM)

### Can't access from other computers
- Check firewall settings
- Use correct IP address (not localhost)
- Ensure both computers are on same network

### Database not persisting
- Make sure `runtime_rush.db` file exists in backend folder
- Don't delete the database file
- Backup regularly

### Port already in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

---

## Summary

**Quick Answer:** Servers stop because they're attached to your terminal. Use **PM2** to keep them running in the background.

**Best for your event:**
1. Install PM2: `npm install -g pm2`
2. Create `ecosystem.config.js` (see above)
3. Run: `pm2 start ecosystem.config.js`
4. Servers will keep running even after closing terminal!

Need help? Check the logs with `pm2 logs`
