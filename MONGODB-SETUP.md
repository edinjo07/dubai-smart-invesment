# MongoDB Setup Guide for Dubai Smart Investment

## ✅ What I've Done:

1. **Added MongoDB Support** to `requirements.txt`
2. **Created `database.py`** - MongoDB database module with fallback to local files
3. **Updated `app.py`** - Imports MongoDB database module
4. **Updated `save_lead_data()`** function - Now saves to MongoDB

## 🎯 What You Need to Do:

### Step 1: Create Free MongoDB Atlas Account

1. Go to **https://www.mongodb.com/cloud/atlas/register**
2. Sign up for FREE (no credit card required)
3. Create a **FREE M0 Cluster** (512 MB storage)
4. Choose cloud provider: **AWS** or **Google Cloud**
5. Choose region closest to your users (e.g., Dubai/Mumbai/Europe)

### Step 2: Get Your MongoDB Connection String

1. In MongoDB Atlas, click **"Connect"** on your cluster
2. Choose **"Connect your application"**
3. Copy the connection string (looks like):
   ```
   mongodb+srv://username:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
4. Replace `<password>` with your actual database password

### Step 3: Add Environment Variable on Render

1. Go to your **Render Dashboard** (https://dashboard.render.com/)
2. Click on your `dubai-smart-invest` web service
3. Go to **"Environment"** tab
4. Add new environment variable:
   - **Key**: `MONGODB_URI`
   - **Value**: `mongodb+srv://your-connection-string`
5. Click **"Save Changes"**
6. Render will automatically redeploy

### Step 4: Configure Email Notifications

In Render Environment variables, also add:

```
EMAIL_USERNAME=your-gmail@gmail.com
EMAIL_PASSWORD=your-16-digit-app-password
TO_EMAIL=your-notification-email@gmail.com
```

**To get Gmail App Password:**
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to **App Passwords**
4. Generate password for "Mail"
5. Copy the 16-digit password

### Step 5: Deploy

The changes are ready in your code. Just:

```powershell
git add .
git commit -m "Add MongoDB database support for persistent storage"
git push origin main
```

Render will auto-deploy with MongoDB!

## 🎉 Benefits:

✅ **Persistent Storage** - Leads never disappear  
✅ **Multi-Browser Access** - Same data everywhere  
✅ **Real-Time Sync** - All admins see same leads  
✅ **Auto-Backup** - MongoDB handles backups  
✅ **Scalable** - Handles unlimited leads  
✅ **Fast Queries** - Indexed for performance  

## 📊 After Setup:

- All new leads → Saved to MongoDB
- Old leads from `leads.json` → Will still work (fallback)
- Deleted leads → Stay deleted (persistent)
- Sessions → Synced across browsers

## 🔧 Troubleshooting:

If MongoDB connection fails:
- App automatically falls back to local `leads.json` files
- Check Render logs for connection errors
- Verify `MONGODB_URI` environment variable is set correctly
- Make sure MongoDB Atlas allows connections from all IPs (0.0.0.0/0)

Need help? Let me know your MongoDB Atlas username and I'll guide you through the setup!
