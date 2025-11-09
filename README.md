# 🏙️ Dubai Smart Invest - Real Estate Investment Platform

A premium real estate investment platform for Dubai properties, featuring lead management, multi-language support, and a comprehensive admin dashboard.

![Dubai Smart Invest](https://img.shields.io/badge/Status-Live-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.2-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 🎯 Public Website
- **Multi-Language Support**: English, Polish, German, Romanian, Turkish
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Contact Forms**: Lead capture with email notifications
- **WhatsApp Integration**: Direct messaging to sales team
- **Property Showcase**: Dynamic property listings
- **SEO Optimized**: Meta tags and structured data

### 👨‍💼 Admin Dashboard
- **Lead Management**: View, assign, and manage all leads
- **Bulk Operations**: Delete multiple leads at once
- **Manager Assignment**: Assign leads to specific managers
- **Export Data**: Download leads as CSV
- **Analytics**: Track lead sources and status
- **Website Editor**: Visual content management system

### 🔧 Website Editor
- **Content Editing**: Update text, images, and sections
- **Design Control**: Change colors, fonts, and styles
- **Section Builder**: Add new sections dynamically
- **Text/Image/Card Tools**: Insert content blocks easily
- **Live Preview**: See changes before publishing
- **Device Preview**: Test on desktop, tablet, mobile

### 👥 Manager Dashboard
- **Assigned Leads**: View only assigned leads
- **Lead Status**: Update lead status and notes
- **Offline Mode**: Cached data for offline access
- **Search & Filter**: Find leads quickly
- **Session Management**: Secure login with auto-refresh

### 🎨 Settings Management
- **Manager CRUD**: Add, edit, delete managers
- **View Assignments**: See all assigned leads per manager
- **Reset Passwords**: Change manager credentials
- **Statistics**: Total managers, active users, lead counts

## 🚀 Quick Start

### Local Development

1. **Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/dubai-smart-invest.git
   cd dubai-smart-invest
   ```

2. **Run Startup Script**:
   
   **Windows**:
   ```bash
   start.bat
   ```
   
   **Linux/Mac**:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

3. **Access Application**:
   - Website: http://localhost:5000
   - Admin: http://localhost:5000/admin
   - Login: `admin` / `admin123` (change in production!)

### Manual Setup

1. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create .env File**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run Application**:
   ```bash
   python app.py
   ```

## 📦 Deployment

### Deploy to Render.com (Recommended - FREE)

1. Push code to GitHub
2. Create account at [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Add environment variables (see `.env.example`)
7. Deploy! ✅

**Full deployment guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your configuration (see `.env.example` for template).

### Gmail Setup (for contact forms)

1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use App Password in `EMAIL_PASSWORD`

## 🛠️ Tech Stack

- **Backend**: Flask 2.3.2 (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: JSON files (easily migrate to PostgreSQL)
- **Server**: Gunicorn
- **Email**: SMTP (Gmail)
- **Authentication**: JWT tokens

## 📁 Key Files

- `app.py` - Main Flask application
- `start.bat` - Windows startup script
- `start.sh` - Linux/Mac startup script
- `DEPLOYMENT.md` - Complete deployment guide
- `index.html` - Landing page
- `admin.html` - Admin dashboard
- `editor.html` - Website editor
- `settings.html` - Manager settings

## 📊 Pages & Routes

- `/` - Landing page
- `/admin` - Admin dashboard
- `/login` - Admin login
- `/manager` - Manager dashboard
- `/manager-login` - Manager login
- `/settings` - Settings page
- `/editor` - Website editor
- `/api/*` - API endpoints

## 🆘 Support

Need help deploying?

1. Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides
2. Review application logs for errors
3. Test locally first: `python app.py`
4. Verify environment variables are set

## 📝 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

**Dubai Smart Invest Team**
- Email: info@dubaismart-invest.com
- Phone: +971 50 XXX XXXX

---

⭐ **Star this repo** if you find it useful!

For deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)