# Le Blanc Dubai - Admin Authentication Guide

## 🔐 **Admin Login System**

The admin dashboard is now protected with username and password authentication.

### **Default Credentials**
```
Username: admin
Password: admin123
```

⚠️ **IMPORTANT:** Change these credentials in production!

---

## 🚀 **How to Access Admin Dashboard**

### **Step 1: Start the Server**
```bash
python app.py
```

### **Step 2: Navigate to Login Page**
Open your browser and go to:
```
http://localhost:5000/login
```

### **Step 3: Enter Credentials**
- Username: `admin`
- Password: `admin123`

### **Step 4: Access Dashboard**
After successful login, you'll be redirected to:
```
http://localhost:5000/admin
```

---

## 🔧 **Changing Admin Credentials**

### **Method 1: Using Environment Variables (Recommended)**

1. Create or edit the `.env` file:
```bash
ADMIN_USERNAME=your_custom_username
ADMIN_PASSWORD=your_secure_password
```

2. Restart the server

### **Method 2: Edit app.py Directly**

In `app.py`, find this section:
```python
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
ADMIN_PASSWORD_HASH = hashlib.sha256((os.environ.get('ADMIN_PASSWORD') or 'admin123').encode()).hexdigest()
```

Change the default values from `'admin'` and `'admin123'` to your desired credentials.

---

## 🛡️ **Security Features**

### **Password Hashing**
- Passwords are hashed using SHA-256
- Never stored in plain text
- Secure comparison during login

### **Session Management**
- Secure token generation using `secrets` module
- 24-hour session expiration
- Token stored in browser's localStorage
- Server-side session validation

### **Authentication Protection**
All admin endpoints are protected:
- `/api/leads` - Get all leads
- `/api/leads/download/csv` - Download CSV
- `/api/leads/download/excel` - Download Excel

### **Auto-logout**
- Expired sessions automatically cleared
- Invalid tokens redirect to login page
- Manual logout clears session immediately

---

## 📱 **Access Points**

### **Public Pages (No Authentication)**
- `/` - Main website
- `/api/health` - Health check
- `/api/contact` - Contact form submission

### **Protected Pages (Require Login)**
- `/admin` - Admin dashboard
- `/api/leads` - Lead management API
- `/api/leads/download/csv` - CSV export
- `/api/leads/download/excel` - Excel export

### **Authentication Pages**
- `/login` - Admin login page
- `/api/admin/login` - Login endpoint
- `/api/admin/logout` - Logout endpoint
- `/api/admin/verify` - Token verification

---

## 🔑 **Session Management**

### **How It Works**
1. User enters username/password on login page
2. Server validates credentials and generates secure token
3. Token sent to client and stored in localStorage
4. Client includes token in Authorization header for all API requests
5. Server validates token before processing requests
6. Token expires after 24 hours

### **Token Format**
```
Authorization: Bearer <token>
```

### **Session Duration**
- Default: 24 hours
- Configurable in `app.py`
- Can be changed by modifying this line:
  ```python
  'expires': datetime.now() + timedelta(hours=24)
  ```

---

## 🚨 **Production Recommendations**

### **1. Change Default Credentials**
Never use default `admin/admin123` in production!

### **2. Use Strong Passwords**
- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- Use a password manager

### **3. Enable HTTPS**
- Use SSL/TLS certificates
- Redirect HTTP to HTTPS
- Secure cookie transmission

### **4. Implement Rate Limiting**
- Prevent brute force attacks
- Limit login attempts
- Add CAPTCHA after failed attempts

### **5. Use Database Sessions**
- Replace in-memory sessions with Redis or database
- Persist sessions across server restarts
- Enable session revocation

### **6. Add Multi-Factor Authentication (MFA)**
- SMS verification
- Email verification
- Authenticator apps (Google Authenticator, Authy)

### **7. Monitor Login Attempts**
- Log all login attempts
- Alert on suspicious activity
- IP-based blocking

### **8. Regular Security Updates**
- Keep dependencies updated
- Apply security patches
- Regular security audits

---

## 🐛 **Troubleshooting**

### **Can't Login**
1. Check credentials are correct
2. Verify server is running: `http://localhost:5000/api/health`
3. Clear browser localStorage and try again
4. Check server logs for errors

### **Session Expired**
- Sessions expire after 24 hours
- Simply login again
- Token is automatically cleared

### **Unauthorized After Login**
1. Clear browser cache and localStorage
2. Try logging out and back in
3. Check browser console for errors
4. Verify token in localStorage

### **Password Not Working**
1. Check for typos (case-sensitive)
2. Verify .env file is loaded
3. Check app.py for hardcoded credentials
4. Restart server after changing credentials

---

## 📊 **API Authentication Examples**

### **Login Request**
```javascript
const response = await fetch('/api/admin/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'admin',
        password: 'admin123'
    })
});

const data = await response.json();
// Store token
localStorage.setItem('adminToken', data.token);
```

### **Authenticated Request**
```javascript
const token = localStorage.getItem('adminToken');

const response = await fetch('/api/leads', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
});
```

### **Logout Request**
```javascript
const token = localStorage.getItem('adminToken');

await fetch('/api/admin/logout', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`
    }
});

localStorage.removeItem('adminToken');
```

---

## 📞 **Support**

For authentication issues or security concerns, contact the development team.

**Login Page:** http://localhost:5000/login  
**Last Updated:** November 6, 2025