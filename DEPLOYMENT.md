# Dubai Smart Invest - Deployment Guide

## 🚀 Hosting Options

### Option 1: Deploy to Render.com (Recommended - FREE)

1. **Create Account**: Go to [render.com](https://render.com) and sign up

2. **New Web Service**: Click "New +" → "Web Service"

3. **Connect Repository**: 
   - Connect your GitHub account
   - Select your repository

4. **Configure Service**:
   - **Name**: dubai-smart-invest
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type**: Free

5. **Environment Variables** (Add these in Render dashboard):
   ```
   SECRET_KEY=your-random-secret-key
   FLASK_ENV=production
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_USERNAME=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   TO_EMAIL=sales@dubaismart-invest.com
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=your-secure-password
   ```

6. **Deploy**: Click "Create Web Service" - Your site will be live in 5-10 minutes!

**Your URL**: `https://dubai-smart-invest.onrender.com`

---

### Option 2: Deploy to Railway.app (Easy - FREE)

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Flask and deploys automatically
5. Add environment variables in Settings
6. Get your live URL from the dashboard

---

### Option 3: Deploy to Vercel (Fast - FREE)

1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Vercel will auto-detect and deploy
4. Add environment variables
5. Live in 30 seconds!

---

### Option 4: Deploy to Heroku (Paid - $5/month)

1. Install Heroku CLI: `npm install -g heroku`

2. Login to Heroku:
   ```bash
   heroku login
   ```

3. Create new app:
   ```bash
   heroku create dubai-smart-invest
   ```

4. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set FLASK_ENV=production
   heroku config:set EMAIL_USERNAME=your-email@gmail.com
   # ... add all other variables
   ```

5. Deploy:
   ```bash
   git push heroku main
   ```

6. Open your app:
   ```bash
   heroku open
   ```

---

### Option 5: VPS Deployment (DigitalOcean, Linode, AWS)

#### Prerequisites:
- Ubuntu/Debian server
- Domain name (optional)
- SSH access

#### Setup Steps:

1. **Connect to Server**:
   ```bash
   ssh root@your-server-ip
   ```

2. **Update System**:
   ```bash
   apt update && apt upgrade -y
   ```

3. **Install Dependencies**:
   ```bash
   apt install python3-pip python3-venv nginx supervisor -y
   ```

4. **Upload Your Code**:
   ```bash
   cd /var/www
   git clone https://github.com/yourusername/dubai-real-estate.git
   cd dubai-real-estate
   ```

5. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Create .env File**:
   ```bash
   nano .env
   # Copy contents from .env.example and fill in real values
   ```

7. **Configure Supervisor** (keeps app running):
   ```bash
   nano /etc/supervisor/conf.d/dubai-smart-invest.conf
   ```
   
   Add:
   ```ini
   [program:dubai-smart-invest]
   command=/var/www/dubai-real-estate/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
   directory=/var/www/dubai-real-estate
   user=www-data
   autostart=true
   autorestart=true
   stderr_logfile=/var/log/dubai-smart-invest.err.log
   stdout_logfile=/var/log/dubai-smart-invest.out.log
   ```

8. **Start Supervisor**:
   ```bash
   supervisorctl reread
   supervisorctl update
   supervisorctl start dubai-smart-invest
   ```

9. **Configure Nginx**:
   ```bash
   nano /etc/nginx/sites-available/dubai-smart-invest
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static {
           alias /var/www/dubai-real-estate/static;
           expires 30d;
       }
   }
   ```

10. **Enable Site**:
    ```bash
    ln -s /etc/nginx/sites-available/dubai-smart-invest /etc/nginx/sites-enabled/
    nginx -t
    systemctl reload nginx
    ```

11. **Setup SSL (HTTPS)**:
    ```bash
    apt install certbot python3-certbot-nginx -y
    certbot --nginx -d your-domain.com -d www.your-domain.com
    ```

---

## 📊 Recommended: Render.com (FREE)

**Why Render?**
- ✅ FREE forever for web services
- ✅ Automatic HTTPS/SSL
- ✅ Auto-deploys from GitHub
- ✅ Easy environment variables
- ✅ Built-in monitoring
- ✅ Custom domain support
- ✅ No credit card required

**Quick Start (5 minutes)**:
1. Push code to GitHub
2. Connect GitHub to Render
3. Click "Deploy"
4. Add environment variables
5. ✅ LIVE!

---

## 🔧 Pre-Deployment Checklist

- [ ] Push code to GitHub repository
- [ ] Update `SECRET_KEY` to random string
- [ ] Configure Gmail App Password for SMTP
- [ ] Change admin password from default
- [ ] Test all forms locally
- [ ] Verify all pages load correctly
- [ ] Test lead management system
- [ ] Test manager login/dashboard
- [ ] Test website editor
- [ ] Check mobile responsiveness

---

## 🌐 Custom Domain Setup

After deployment, to use your own domain (e.g., www.dubaismart-invest.com):

1. **Get Domain**: Purchase from Namecheap, GoDaddy, or Google Domains

2. **DNS Configuration**:
   - Add A record: `@` → `your-server-ip`
   - Add CNAME: `www` → `your-domain.com`
   
   For Render/Vercel:
   - Add CNAME: `www` → `your-app.onrender.com`

3. **Wait for DNS**: Propagation takes 1-24 hours

4. **Enable SSL**: Most platforms auto-enable HTTPS

---

## 📧 Email Configuration (Gmail)

1. Enable 2-Factor Authentication on Gmail
2. Go to: https://myaccount.google.com/apppasswords
3. Create "App Password" for "Mail"
4. Use this password in `EMAIL_PASSWORD` environment variable

---

## 🎯 Next Steps After Deployment

1. **Test Everything**: Go through all pages and features
2. **Monitor Logs**: Check for any errors
3. **Setup Analytics**: Add Google Analytics
4. **SEO Optimization**: Submit sitemap to Google
5. **Backup Database**: Setup automated backups for leads.json
6. **Setup Monitoring**: Use UptimeRobot for uptime monitoring

---

## 🆘 Need Help?

**Common Issues**:

1. **500 Error**: Check environment variables are set correctly
2. **Email Not Sending**: Verify Gmail App Password
3. **Static Files 404**: Ensure `/static` folder is included
4. **Database Lost**: Leads.json needs persistent storage

**Support**:
- Check platform documentation
- Review application logs
- Test locally first with `python app.py`

---

## 💡 Cost Comparison

| Platform | Cost | SSL | Custom Domain | Auto-Deploy |
|----------|------|-----|---------------|-------------|
| **Render** | FREE | ✅ | ✅ | ✅ |
| **Railway** | FREE (500hrs) | ✅ | ✅ | ✅ |
| **Vercel** | FREE | ✅ | ✅ | ✅ |
| **Heroku** | $5/month | ✅ | ✅ | ✅ |
| **DigitalOcean** | $5-12/month | ✅ | ✅ | ❌ |

---

🚀 **Recommendation**: Start with Render.com (FREE), then upgrade to VPS if you need more control.
