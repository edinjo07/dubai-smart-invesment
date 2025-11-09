# Le Blanc Dubai Real Estate - Backend Documentation

## Backend Architecture

This project now includes a complete Python Flask backend that handles:
- Contact form submissions
- Email notifications
- Lead data storage
- API endpoints for frontend integration

## Quick Start

### Windows Setup
```cmd
setup.bat
```

### Unix/Linux/Mac Setup
```bash
bash setup.sh
```

### Manual Setup
1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and configure email settings
5. Run server: `python app.py`

## Email Configuration

### Gmail Setup (Recommended)
1. Enable 2-factor authentication on Gmail
2. Generate App Password: Google Account > Security > App passwords
3. Update `.env` file:
```
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-16-character-app-password
TO_EMAIL=sales@leblanc-dubai.com
```

### Other Email Providers
- **Outlook/Hotmail**: Use `smtp.outlook.com:587`
- **Yahoo**: Use `smtp.mail.yahoo.com:587`
- **Custom SMTP**: Configure your server details

## API Endpoints

### POST /api/contact
Submit contact form data
- **Body**: JSON with firstName, lastName, email, phone, interest, message
- **Response**: Success/error status with message

### GET /api/health
Check backend status
- **Response**: Health status and timestamp

### GET /api/leads
View all leads (admin endpoint)
- **Response**: Array of all submitted leads

## Features

### Email Notifications
- Sends notification to sales team
- Sends confirmation to customer
- Professional email templates
- HTML and plain text support

### Data Storage
- Leads saved to JSON file
- Backup system for reliability
- Timestamped entries
- IP address tracking

### Validation
- Server-side form validation
- Email format checking
- Phone number validation
- Required field enforcement

### Security
- CORS support for cross-origin requests
- Input sanitization
- Error handling and logging
- Environment variable configuration

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Environment Variables for Production
```bash
export SECRET_KEY="your-production-secret-key"
export EMAIL_USERNAME="sales@yourdomain.com"
export EMAIL_PASSWORD="your-email-password"
export TO_EMAIL="leads@yourdomain.com"
export FLASK_ENV="production"
```

## Monitoring and Logging

### Log Files
- Application logs printed to console
- Email sending status tracked
- Form submission logging
- Error tracking and debugging

### Lead Management
- All leads stored in `leads.json`
- Accessible via `/api/leads` endpoint
- Export functionality available
- Timestamp and metadata included

## Integration Notes

### Frontend Integration
- JavaScript automatically detects backend
- Fallback mode if backend unavailable
- Loading states and error handling
- Success/error message display

### Analytics Integration
- Google Analytics event tracking
- Facebook Pixel conversion tracking
- Custom event logging
- Form submission metrics

## Troubleshooting

### Common Issues
1. **Email not sending**: Check SMTP credentials and App Password
2. **Port already in use**: Change port in app.py or stop other services
3. **CORS errors**: Ensure backend URL is correct in frontend
4. **Form validation errors**: Check field requirements and formats

### Debug Commands
```bash
# Check Python version
python --version

# Test email configuration
python -c "import smtplib; print('SMTP available')"

# Verify dependencies
pip list

# Check port availability
netstat -an | findstr :5000
```

## File Structure
```
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env.example       # Environment template
├── .env               # Environment configuration (do not commit)
├── setup.bat          # Windows setup script
├── setup.sh           # Unix setup script
├── leads.json         # Lead data storage
├── venv/              # Virtual environment (created by setup)
└── README-BACKEND.md  # This documentation
```

## Support and Maintenance

### Regular Tasks
- Monitor `leads.json` for new submissions
- Check email delivery status
- Update dependencies regularly
- Backup lead data periodically

### Performance Optimization
- Use production WSGI server (Gunicorn)
- Configure reverse proxy (Nginx)
- Enable gzip compression
- Use CDN for static assets

### Security Updates
- Regularly update Python packages
- Monitor for security vulnerabilities
- Use HTTPS in production
- Implement rate limiting

## License
This backend implementation is proprietary and confidential.