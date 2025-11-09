# 🔐 Le Blanc Dubai - Admin Authentication System

## ✅ **System Overview**

Your Dubai Real Estate admin dashboard now has a complete authentication system with secure login, session management, and protected API endpoints.

---

## 🎯 **Quick Access**

### **Login Page**
```
http://localhost:5000/login
```

### **Admin Dashboard (Protected)**
```
http://localhost:5000/admin
```

### **Default Credentials**
```
Username: admin
Password: admin123
```

⚠️ **Change these credentials before deploying to production!**

---

## 🚀 **How to Use**

### **1. Start the Server**
```bash
python app.py
```
or
```bash
start_server.bat
```

### **2. Access Login Page**
- Open browser: `http://localhost:5000/login`
- Enter username: `admin`
- Enter password: `admin123`
- Click "Login"

### **3. Automatic Redirect**
- Upon successful login, you'll be redirected to `/admin`
- Your session token is stored securely
- Token is valid for 24 hours

### **4. Logout**
- Click the "🚪 Logout" button in the top-right corner
- Session is cleared immediately
- Redirected back to login page

---

## 🔧 **Features Implemented**

### ✅ **Login Page**
- Beautiful, responsive design
- Username and password fields
- Password show/hide toggle
- Loading state during authentication
- Error and success messages
- Auto-redirect if already logged in

### ✅ **Session Management**
- Secure token generation (32-byte URL-safe tokens)
- 24-hour session expiration
- Server-side session storage
- Automatic session cleanup

### ✅ **Protected Dashboard**
- Auto-redirect to login if not authenticated
- Token verification on page load
- Session validation for all API calls
- Logout button in header

### ✅ **Secured API Endpoints**
All admin endpoints require authentication:
- `GET /api/leads` - View all leads
- `POST /api/leads/download/csv` - Export CSV
- `POST /api/leads/download/excel` - Export Excel

### ✅ **Security Features**
- Password hashing (SHA-256)
- Secure token generation
- Authorization header validation
- Automatic session expiration
- Unauthorized request handling

---

## 📱 **User Experience**

### **Login Flow**
1. User visits `/admin` without authentication
2. Automatically redirected to `/login`
3. Enter credentials
4. Server validates and generates token
5. Token stored in browser localStorage
6. Redirected to admin dashboard
7. Dashboard loads with full functionality

### **Protected Access**
1. Every admin page checks for valid token
2. Every API call includes authentication header
3. Expired or invalid tokens trigger re-login
4. Session remains active for 24 hours

### **Logout Flow**
1. User clicks logout button
2. Token sent to server for invalidation
3. localStorage cleared
4. Redirected to login page

---

## 🛡️ **Security Implementation**

### **Password Security**
```python
# Passwords are hashed, never stored in plain text
password_hash = hashlib.sha256(password.encode()).hexdigest()
```

### **Token Generation**
```python
# Cryptographically secure tokens
token = secrets.token_urlsafe(32)
```

### **Session Storage**
```python
active_sessions[token] = {
    'username': username,
    'created': datetime.now(),
    'expires': datetime.now() + timedelta(hours=24)
}
```

### **Authentication Decorator**
```python
@require_admin_auth
def protected_endpoint():
    # Only accessible with valid token
```

---

## 🔑 **Changing Credentials**

### **Option 1: Environment Variables (Recommended)**

Edit `.env` file:
```bash
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_password
```

### **Option 2: Direct Configuration**

Edit `app.py` line 24-26:
```python
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'your_username'
ADMIN_PASSWORD_HASH = hashlib.sha256((os.environ.get('ADMIN_PASSWORD') or 'your_password').encode()).hexdigest()
```

Then restart the server.

---

## 📊 **Session Information**

- **Token Storage**: localStorage (client-side)
- **Session Duration**: 24 hours
- **Token Format**: 32-byte URL-safe string
- **Storage Location**: Server memory (in-memory dictionary)
- **Expiration Check**: On every API request

---

## 🚨 **Important Notes**

### **For Development**
- Default credentials are fine for testing
- Session data stored in memory
- Lost on server restart

### **For Production**
1. **Change credentials immediately**
2. **Use environment variables**
3. **Enable HTTPS/SSL**
4. **Use Redis/database for sessions**
5. **Implement rate limiting**
6. **Add IP whitelisting**
7. **Enable audit logging**
8. **Add two-factor authentication**

---

## 📂 **Files Created/Modified**

### **New Files**
- `login.html` - Admin login page
- `README-AUTH.md` - Authentication documentation
- `ADMIN-LOGIN-GUIDE.md` - This file

### **Modified Files**
- `app.py` - Added authentication endpoints and session management
- `admin.html` - Added login check and logout button
- `.env.example` - Added admin credential examples

---

## 🔄 **API Endpoints**

### **Authentication Endpoints**
- `POST /api/admin/login` - Login and get token
- `POST /api/admin/logout` - Invalidate session
- `GET /api/admin/verify` - Check token validity

### **Protected Endpoints**
- `GET /api/leads` - Requires authentication
- `POST /api/leads/download/csv` - Requires authentication
- `POST /api/leads/download/excel` - Requires authentication

### **Public Endpoints**
- `GET /` - Main website
- `POST /api/contact` - Contact form
- `GET /api/health` - Health check
- `GET /login` - Login page

---

## 🎨 **Login Page Features**

- **Responsive Design**: Works on all devices
- **Password Toggle**: Show/hide password
- **Loading States**: Visual feedback during login
- **Error Handling**: Clear error messages
- **Auto-redirect**: Skip login if already authenticated
- **Modern UI**: Clean, professional appearance

---

## ✨ **What's Protected**

### **✅ Protected**
- Admin dashboard page
- Lead viewing
- Lead filtering
- CSV export
- Excel export
- Statistics

### **❌ Not Protected (Public)**
- Main website
- Contact form
- Health check endpoint

---

## 📞 **Quick Reference**

**Login URL**: http://localhost:5000/login  
**Dashboard URL**: http://localhost:5000/admin  
**Default Username**: admin  
**Default Password**: admin123  
**Session Duration**: 24 hours  
**Token Storage**: localStorage  

---

**Last Updated**: November 6, 2025  
**Status**: ✅ Fully Functional