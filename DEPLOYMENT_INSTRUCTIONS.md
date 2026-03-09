# Runtime Rush - Deployment Instructions

## 🚀 Deployment Guide for Multi-Language Update

### Overview
This guide covers deploying the updated Runtime Rush platform with multi-language support, new challenges, and enhanced UI.

---

## 📋 Pre-Deployment Checklist

- [ ] All code changes committed to repository
- [ ] Database schema updated (new columns added)
- [ ] New challenges data prepared
- [ ] Frontend built and tested locally
- [ ] Backend tested locally
- [ ] Environment variables configured
- [ ] Backup of existing database created

---

## 🗄️ Database Migration

### Step 1: Backup Existing Database
```bash
# For SQLite
cp runtime_rush.db runtime_rush.db.backup

# For PostgreSQL
pg_dump -U username -d runtime_rush > backup.sql
```

### Step 2: Add New Columns
The new columns will be automatically added when the application starts (SQLAlchemy creates tables).

**New columns in `user_progress` table:**
- `level1_language` (VARCHAR(50), nullable)
- `level2_language` (VARCHAR(50), nullable)
- `level3_language` (VARCHAR(50), nullable)

**Manual migration (if needed):**
```sql
ALTER TABLE user_progress ADD COLUMN level1_language VARCHAR(50);
ALTER TABLE user_progress ADD COLUMN level2_language VARCHAR(50);
ALTER TABLE user_progress ADD COLUMN level3_language VARCHAR(50);
```

### Step 3: Initialize New Challenges
After deployment, call the initialize endpoint:
```bash
curl -X POST https://your-domain.com/initialize-db
```

This will:
- Create admin user (if not exists)
- Create 12 new challenges (3 levels × 4 languages)

---

## 🔧 Backend Deployment

### Option 1: Railway (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add multi-language support and new challenges"
   git push origin main
   ```

2. **Railway Auto-Deploy**
   - Railway will automatically detect changes
   - Build and deploy backend
   - Database migrations run automatically

3. **Verify Deployment**
   ```bash
   curl https://your-backend.railway.app/health
   ```

4. **Initialize Database**
   ```bash
   curl -X POST https://your-backend.railway.app/initialize-db
   ```

### Option 2: Manual Server Deployment

1. **SSH into Server**
   ```bash
   ssh user@your-server.com
   ```

2. **Pull Latest Code**
   ```bash
   cd /path/to/runtime-rush
   git pull origin main
   ```

3. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Restart Backend Service**
   ```bash
   # Using systemd
   sudo systemctl restart runtime-rush-backend

   # Or using PM2
   pm2 restart runtime-rush-backend

   # Or manually
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

5. **Initialize Database**
   ```bash
   curl -X POST http://localhost:8000/initialize-db
   ```

---

## 🎨 Frontend Deployment

### Option 1: Vercel (Recommended)

1. **Update Environment Variables**
   - Go to Vercel dashboard
   - Project Settings → Environment Variables
   - Update `REACT_APP_API_URL` if backend URL changed

2. **Deploy**
   ```bash
   git push origin main
   ```
   - Vercel auto-deploys from GitHub

3. **Verify Deployment**
   - Visit your Vercel URL
   - Check that language selector appears
   - Test challenge preview grid layout

### Option 2: Manual Build and Deploy

1. **Build Frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Deploy Build Folder**
   ```bash
   # Copy to web server
   scp -r build/* user@server:/var/www/runtime-rush/

   # Or use rsync
   rsync -avz build/ user@server:/var/www/runtime-rush/
   ```

3. **Configure Web Server**
   
   **Nginx Configuration:**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       root /var/www/runtime-rush;
       index index.html;

       location / {
           try_files $uri $uri/ /index.html;
       }

       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Restart Web Server**
   ```bash
   sudo systemctl restart nginx
   ```

---

## 🔐 Environment Variables

### Backend (.env)
```env
DATABASE_URL=sqlite:///./runtime_rush.db
# Or for PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/runtime_rush

CORS_ORIGINS=https://your-frontend-domain.com,http://localhost:3000
```

### Frontend (.env)
```env
REACT_APP_API_URL=https://your-backend-domain.com
```

---

## ✅ Post-Deployment Verification

### 1. Health Check
```bash
curl https://your-backend.com/health
# Expected: {"status": "healthy"}
```

### 2. Check Challenges
```bash
curl https://your-backend.com/api/challenges
# Expected: Array of 12 challenges
```

### 3. Test Language Selection
1. Register a new user
2. Navigate to Level 1
3. Verify language selector modal appears
4. Select a language
5. Verify only selected language challenges show

### 4. Test Preview UI
1. Start a challenge
2. Verify preview shows grid layout (not list)
3. Verify 3-second countdown works
4. Verify fragments displayed in cards

### 5. Test Admin Dashboard
1. Login as admin (mouniadmin / 1214@)
2. Verify enhanced header with animations
3. Check users table shows language selections
4. Verify stats are correct

### 6. Test Responsive Design
1. Open on mobile device
2. Verify language selector: 1 column
3. Verify preview grid: 1 column
4. Verify all features work

---

## 🐛 Troubleshooting

### Issue: Language Selector Not Appearing
**Solution:**
1. Check browser console for errors
2. Verify API endpoint `/api/auth/users/{id}/progress` returns language fields
3. Clear browser cache
4. Check frontend build includes latest changes

### Issue: Preview Still Shows List Layout
**Solution:**
1. Verify CSS changes deployed
2. Clear browser cache (Ctrl+Shift+R)
3. Check `.preview-code-grid` class exists in CSS
4. Verify DragDropChallenge.tsx uses `preview-code-grid`

### Issue: Challenges Not Showing
**Solution:**
1. Check `/initialize-db` was called
2. Verify database has 12 challenges
3. Check challenge level and language filters
4. Verify API returns challenges correctly

### Issue: Database Migration Failed
**Solution:**
1. Check database permissions
2. Manually add columns (see SQL above)
3. Restart backend service
4. Check logs for errors

### Issue: Admin Header Not Enhanced
**Solution:**
1. Verify AdminDashboard.css changes deployed
2. Clear browser cache
3. Check CSS animations supported in browser
4. Verify no CSS conflicts

---

## 📊 Monitoring

### Key Metrics to Monitor

1. **User Registrations**
   - Track new user signups
   - Monitor registration errors

2. **Language Selection Distribution**
   ```sql
   SELECT 
     level1_language, COUNT(*) as count
   FROM user_progress
   WHERE level1_language IS NOT NULL
   GROUP BY level1_language;
   ```

3. **Challenge Completion Rates**
   ```sql
   SELECT 
     COUNT(*) as total_users,
     SUM(CASE WHEN level1_completed THEN 1 ELSE 0 END) as level1_completed,
     SUM(CASE WHEN level2_completed THEN 1 ELSE 0 END) as level2_completed,
     SUM(CASE WHEN level3_completed THEN 1 ELSE 0 END) as level3_completed
   FROM user_progress;
   ```

4. **Average Scores by Language**
   ```sql
   SELECT 
     level1_language,
     AVG(level1_score) as avg_score
   FROM user_progress
   WHERE level1_completed = TRUE
   GROUP BY level1_language;
   ```

5. **Error Rates**
   - Monitor backend logs for errors
   - Check frontend console errors
   - Track API failure rates

---

## 🔄 Rollback Plan

If issues occur, rollback procedure:

### 1. Rollback Backend
```bash
# Railway
railway rollback

# Manual
git checkout <previous-commit>
git push origin main --force

# Or restore from backup
cp runtime_rush.db.backup runtime_rush.db
```

### 2. Rollback Frontend
```bash
# Vercel
vercel rollback

# Manual
git checkout <previous-commit>
npm run build
# Deploy build folder
```

### 3. Restore Database
```bash
# SQLite
cp runtime_rush.db.backup runtime_rush.db

# PostgreSQL
psql -U username -d runtime_rush < backup.sql
```

---

## 📝 Deployment Checklist

### Pre-Deployment
- [ ] Code reviewed and tested locally
- [ ] Database backup created
- [ ] Environment variables configured
- [ ] Dependencies updated
- [ ] Build tested locally

### Deployment
- [ ] Backend deployed
- [ ] Frontend deployed
- [ ] Database migrated
- [ ] Initialize endpoint called
- [ ] Environment variables set

### Post-Deployment
- [ ] Health check passed
- [ ] Challenges loaded (12 total)
- [ ] Language selector works
- [ ] Preview grid layout works
- [ ] Admin dashboard enhanced
- [ ] Responsive design works
- [ ] No console errors
- [ ] Performance acceptable

### Monitoring
- [ ] Error monitoring enabled
- [ ] Analytics tracking
- [ ] User feedback collected
- [ ] Performance metrics tracked

---

## 🎯 Success Criteria

Deployment is successful when:
- ✅ All 12 challenges visible
- ✅ Language selection works for all levels
- ✅ Preview shows grid layout
- ✅ Admin dashboard has enhanced header
- ✅ No critical errors in logs
- ✅ Users can complete challenges
- ✅ Leaderboard updates correctly
- ✅ Responsive on all devices

---

## 📞 Support Contacts

**Technical Issues:**
- Backend: Check Railway logs
- Frontend: Check Vercel logs
- Database: Check database logs

**Emergency Rollback:**
1. Notify team
2. Execute rollback plan
3. Investigate issue
4. Fix and redeploy

---

## 📚 Additional Resources

- [MULTI_LANGUAGE_UPDATE_SUMMARY.md](./MULTI_LANGUAGE_UPDATE_SUMMARY.md) - Feature overview
- [TESTING_GUIDE.md](./TESTING_GUIDE.md) - Complete testing checklist
- [README.md](./README.md) - General project documentation

---

## 🎉 Post-Deployment Tasks

1. **Announce Update**
   - Notify users of new features
   - Highlight multi-language support
   - Explain new challenge types

2. **Monitor Initial Usage**
   - Watch for errors
   - Track language selection distribution
   - Monitor completion rates

3. **Gather Feedback**
   - User surveys
   - Bug reports
   - Feature requests

4. **Optimize**
   - Performance tuning
   - UI/UX improvements
   - Bug fixes

---

**Deployment Date**: ___________
**Deployed By**: ___________
**Version**: 2.0.0
**Status**: ☐ Pending ☐ In Progress ☐ Complete

---

**Good luck with the deployment! 🚀**
