# Railway Deployment Guide - Le Blanc Dubai

## Quick Deploy to Railway

### Step 1: Prepare GitHub Repository
1. Create a GitHub account (if you don't have one): https://github.com
2. Create a new repository called "leblanc-dubai"
3. Upload these files to GitHub

### Step 2: Deploy on Railway
1. Go to: https://railway.app
2. Click "Start a New Project"
3. Choose "Deploy from GitHub repo"
4. Select your "leblanc-dubai" repository
5. Railway will automatically detect Flask and deploy!

### Step 3: Configure Environment Variables
In Railway dashboard, add these environment variables:
- `PORT` = 5000
- `EMAIL_USERNAME` = your-email@gmail.com (optional)
- `EMAIL_PASSWORD` = your-app-password (optional)
- `TO_EMAIL` = sales@leblanc-dubai.com (optional)

### Step 4: Get Your Live URL
Railway will provide a URL like:
`https://leblanc-dubai-production.up.railway.app`

---

## Alternative: Quick Git Commands

If you have Git installed:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial Le Blanc Dubai website"

# Add GitHub remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/leblanc-dubai.git

# Push to GitHub
git push -u origin main
```

Then connect to Railway!

---

## Files Created for Railway:
✅ Procfile - Tells Railway how to run the app
✅ runtime.txt - Specifies Python version
✅ requirements.txt - Updated with gunicorn

Your project is ready for Railway deployment! 🚂
