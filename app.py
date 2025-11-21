from flask import Flask, render_template, request, jsonify, send_from_directory, Response, redirect, session
from flask_cors import CORS
import smtplib
import os
import re
import json
import csv
import io
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import logging
import requests
import secrets
import hashlib
from database import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dubai-real-estate-secret-key-2024'
    
    # Email configuration
    SMTP_SERVER = os.environ.get('SMTP_SERVER') or 'smtp.gmail.com'
    SMTP_PORT = int(os.environ.get('SMTP_PORT') or 587)
    EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME') or 'your-email@gmail.com'
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD') or 'your-app-password'
    TO_EMAIL = os.environ.get('TO_EMAIL') or 'marketingspecials9@gmail.com,info@dubaismartinvestments.com'
    
    # Admin credentials (in production, store these securely in database with hashed passwords)
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'dubaiadmin'
    ADMIN_PASSWORD_HASH = hashlib.sha256((os.environ.get('ADMIN_PASSWORD') or 'dubai1234').encode()).hexdigest()

app.config.from_object(Config)

# Store active sessions (in production, use Redis or database)
active_sessions = {}

def verify_admin_token(token):
    """Verify admin authentication token and auto-refresh if expiring soon"""
    if not token:
        return False
    
    # Check if token exists and is not expired
    if token in active_sessions:
        session_data = active_sessions[token]
        if datetime.now() < session_data['expires']:
            # Auto-refresh token if it expires in less than 1 hour
            time_until_expiry = session_data['expires'] - datetime.now()
            if time_until_expiry.total_seconds() < 3600:  # Less than 1 hour
                # Extend expiration by 24 hours
                active_sessions[token]['expires'] = datetime.now() + timedelta(hours=24)
                logger.info(f"Token auto-refreshed for user: {session_data.get('username', 'unknown')}")
            return True
        else:
            # Remove expired token
            del active_sessions[token]
    
    return False

def require_admin_auth(f):
    """Decorator to require admin authentication"""
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header or query parameter
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            token = request.args.get('token', '')
        
        if not verify_admin_token(token):
            return jsonify({
                'success': False,
                'message': 'Unauthorized access. Please login.'
            }), 401
        
        return f(*args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function

def get_country_from_ip(ip_address):
    """Get country information from IP address"""
    try:
        # Skip for localhost/private IPs
        if ip_address in ['127.0.0.1', 'localhost'] or ip_address.startswith('192.168.') or ip_address.startswith('10.'):
            return 'AE', 'United Arab Emirates'  # Default to UAE
        
        # Use ipapi.co service (free tier)
        response = requests.get(f'https://ipapi.co/{ip_address}/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            country_code = data.get('country_code', 'Unknown')
            country_name = data.get('country_name', 'Unknown')
            return country_code, country_name
        else:
            return 'Unknown', 'Unknown'
    except Exception as e:
        logger.error(f"Error getting country from IP {ip_address}: {str(e)}")
        return 'Unknown', 'Unknown'

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    # Remove spaces, dashes, and parentheses
    cleaned_phone = re.sub(r'[\s\-\(\)]+', '', phone)
    # Check if it contains only digits and + (for country code)
    pattern = r'^\+?[0-9]{8,15}$'
    return re.match(pattern, cleaned_phone) is not None

def send_email(form_data):
    """Send email notification for new contact form submission"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = app.config['EMAIL_USERNAME']
        # Support multiple recipients (comma-separated)
        to_emails = [email.strip() for email in app.config['TO_EMAIL'].split(',')]
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = f"New Contact Form Submission - Le Blanc Dubai"
        
        # Create email body
        body = f"""
        New Contact Form Submission - Le Blanc Dubai Real Estate
        
        Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        CONTACT INFORMATION:
        =====================
        Name: {form_data.get('firstName', 'N/A')} {form_data.get('lastName', 'N/A')}
        Email: {form_data.get('email', 'N/A')}
        WhatsApp: {form_data.get('whatsapp', 'N/A')}
        Country: {form_data.get('country', 'N/A')}
        
        INQUIRY DETAILS:
        ================
        Preferred Contact: {form_data.get('contactMethod', 'N/A')}
        Buying Timeframe: {form_data.get('timeframe', 'N/A')}
        Property Interest: {form_data.get('propertyType', 'Not specified')}
        
        ADDITIONAL INFO:
        ================
        Source: Le Blanc Dubai Website
        IP Address: {request.environ.get('REMOTE_ADDR', 'Unknown')}
        User Agent: {request.environ.get('HTTP_USER_AGENT', 'Unknown')}
        
        Please follow up with this lead within 24 hours.
        
        Best regards,
        Le Blanc Dubai Website System
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(app.config['SMTP_SERVER'], app.config['SMTP_PORT'])
        server.starttls()
        server.login(app.config['EMAIL_USERNAME'], app.config['EMAIL_PASSWORD'])
        text = msg.as_string()
        # Support multiple recipients
        to_emails = [email.strip() for email in app.config['TO_EMAIL'].split(',')]
        server.sendmail(app.config['EMAIL_USERNAME'], to_emails, text)
        server.quit()
        
        logger.info(f"Email sent successfully for {form_data.get('email')} to {', '.join(to_emails)}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

def send_confirmation_email(form_data):
    """Send confirmation email to the user"""
    try:
        # Create confirmation message
        msg = MIMEMultipart()
        msg['From'] = app.config['EMAIL_USERNAME']
        msg['To'] = form_data.get('email')
        msg['Subject'] = "Thank you for your interest in Le Blanc Dubai"
        
        # Create confirmation email body
        body = f"""
        Dear {form_data.get('firstName', 'Valued Customer')},
        
        Thank you for your interest in Le Blanc by Imtiaz in Dubailand!
        
        We have received your inquiry and one of our real estate specialists will contact you within 24 hours to discuss:
        
        • Le Blanc apartment options and pricing
        • Payment plans (60/40 and 70/30 available)
        • Handover timeline (Q1 2027)
        • Investment benefits and Golden Visa eligibility
        • Site visit arrangements
        
        YOUR INQUIRY DETAILS:
        =====================
        Name: {form_data.get('firstName')} {form_data.get('lastName')}
        Email: {form_data.get('email')}
        WhatsApp: {form_data.get('whatsapp')}
        Country: {form_data.get('country')}
        Preferred Contact: {form_data.get('contactMethod')}
        Buying Timeframe: {form_data.get('timeframe')}
        Property Interest: {form_data.get('propertyType', 'To be discussed')}
        
        WHY CHOOSE LE BLANC DUBAI?
        ===========================
        ✓ Fully furnished luxury apartments
        ✓ Prime Dubailand location (20 mins from Sheikh Zayed Road)
        ✓ Resort-style amenities
        ✓ Flexible payment plans
        ✓ Freehold ownership with 0% tax
        ✓ Golden Visa eligibility
        
        For immediate assistance, please call us at +971 4 XXX XXXX or WhatsApp +971 50 XXX XXXX
        
        Best regards,
        Le Blanc Dubai Sales Team
        Imtiaz Developments
        
        ---
        This is an automated confirmation. Please do not reply to this email.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send confirmation email
        server = smtplib.SMTP(app.config['SMTP_SERVER'], app.config['SMTP_PORT'])
        server.starttls()
        server.login(app.config['EMAIL_USERNAME'], app.config['EMAIL_PASSWORD'])
        text = msg.as_string()
        server.sendmail(app.config['EMAIL_USERNAME'], form_data.get('email'), text)
        server.quit()
        
        logger.info(f"Confirmation email sent to {form_data.get('email')}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send confirmation email: {str(e)}")
        return False

def save_lead_data(form_data):
    """Save lead data to MongoDB database"""
    try:
        # Get country information from IP
        ip_address = request.environ.get('REMOTE_ADDR', '127.0.0.1')
        country_code, country_name = get_country_from_ip(ip_address)
        
        lead_data = {
            'firstName': form_data.get('firstName'),
            'lastName': form_data.get('lastName'),
            'email': form_data.get('email'),
            'whatsapp': form_data.get('whatsapp'),
            'country': form_data.get('country'),
            'contactMethod': form_data.get('contactMethod'),
            'timeframe': form_data.get('timeframe'),
            'propertyType': form_data.get('propertyType', 'Not specified'),
            'source': form_data.get('source', 'Website Contact Form'),
            'campaign_id': form_data.get('campaign_id', ''),
            'lead_id': form_data.get('lead_id', ''),
            'ip_address': ip_address,
            'user_agent': request.environ.get('HTTP_USER_AGENT'),
            'detected_country_code': country_code,
            'detected_country': country_name,
            'status': 'new'
        }
        
        # Save to MongoDB
        lead_id = db.save_lead(lead_data)
        
        logger.info(f"Lead data saved to MongoDB for {form_data.get('email')}")
        return lead_id
        
    except Exception as e:
        logger.error(f"Failed to save lead data: {str(e)}")
        return False

@app.route('/')
def index():
    """Serve the main website"""
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (images, css, js)"""
    return send_from_directory('static', filename)

@app.route('/favicon.ico')
def favicon():
    """Serve favicon explicitly"""
    return send_from_directory('.', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Clean URL routes for legal pages (without .html extension)
@app.route('/terms')
def terms_clean():
    """Serve terms page without .html extension"""
    return send_from_directory('.', 'terms.html')

@app.route('/privacy')
def privacy_clean():
    """Serve privacy page without .html extension"""
    return send_from_directory('.', 'privacy.html')

@app.route('/disclaimer')
def disclaimer_clean():
    """Serve disclaimer page without .html extension"""
    return send_from_directory('.', 'disclaimer.html')

@app.route('/cookies')
def cookies_clean():
    """Serve cookies page without .html extension"""
    return send_from_directory('.', 'cookies.html')

@app.route('/thank-you')
def thank_you_page():
    """Thank you page for form submissions and conversion tracking"""
    return send_from_directory('.', 'thank-you.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/api/contact', methods=['POST'])
def handle_contact_form():
    """Handle contact form submissions"""
    try:
        # Get form data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data received'
            }), 400
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'whatsapp', 'country', 'contactMethod', 'timeframe']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Validate email format
        if not validate_email(data.get('email')):
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400
        
        # Validate WhatsApp number format
        if not validate_phone(data.get('whatsapp')):
            return jsonify({
                'success': False,
                'message': 'Invalid WhatsApp number format'
            }), 400
        
        # Save lead data
        save_lead_data(data)
        
        # Send notification email
        email_sent = send_email(data)
        
        # Send confirmation email to user
        confirmation_sent = send_confirmation_email(data)
        
        # Return success response
        return jsonify({
            'success': True,
            'message': 'Thank you for your inquiry! We will contact you within 24 hours.',
            'email_sent': email_sent,
            'confirmation_sent': confirmation_sent
        })
        
    except Exception as e:
        logger.error(f"Error handling contact form: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your request. Please try again.'
        }), 500

@app.route('/api/google-ads/webhook', methods=['POST'])
def google_ads_webhook():
    """Handle Google Ads Lead Form webhook submissions"""
    try:
        # Verify webhook key for security
        webhook_key = request.headers.get('X-Goog-Signature') or request.args.get('key')
        expected_key = 'GSI2025Dubai'  # Your webhook secret key
        
        if webhook_key != expected_key:
            logger.warning(f"Invalid webhook key attempt: {webhook_key}")
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
        # Get lead data from Google Ads
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data received'}), 400
        
        # Map Google Ads fields to your format
        lead_data = {
            'firstName': data.get('user_column_data', {}).get('FIRST_NAME', ''),
            'lastName': data.get('user_column_data', {}).get('LAST_NAME', ''),
            'email': data.get('user_column_data', {}).get('EMAIL', ''),
            'whatsapp': data.get('user_column_data', {}).get('PHONE_NUMBER', ''),
            'country': data.get('user_column_data', {}).get('COUNTRY', 'Not specified'),
            'contactMethod': 'WhatsApp',
            'timeframe': 'As soon as possible',
            'propertyType': data.get('user_column_data', {}).get('PROPERTY_TYPE', ''),
            'source': 'Google Ads Lead Form',
            'campaign_id': data.get('google_key', ''),
            'lead_id': data.get('lead_id', '')
        }
        
        # Validate essential fields
        if not lead_data['email'] or not lead_data['firstName']:
            logger.warning(f"Incomplete Google Ads lead data: {data}")
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Save lead data
        save_lead_data(lead_data)
        
        # Send notification email
        email_sent = send_email(lead_data)
        
        # Send confirmation email to user
        confirmation_sent = send_confirmation_email(lead_data)
        
        logger.info(f"Google Ads lead processed successfully: {lead_data['email']}")
        
        return jsonify({
            'success': True,
            'message': 'Lead received successfully',
            'lead_id': lead_data.get('lead_id')
        })
        
    except Exception as e:
        logger.error(f"Error processing Google Ads webhook: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    mongo_connected = db.client is not None and db.db is not None
    mongo_uri_set = bool(os.environ.get('MONGODB_URI'))
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'mongodb_connected': mongo_connected,
        'mongodb_uri_configured': mongo_uri_set,
        'database_name': db.db.name if mongo_connected else 'not_connected'
    })

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        
        # Hash the provided password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Verify credentials
        if username == app.config['ADMIN_USERNAME'] and password_hash == app.config['ADMIN_PASSWORD_HASH']:
            # Generate secure token
            token = secrets.token_urlsafe(32)
            
            # Store session (expires in 24 hours)
            active_sessions[token] = {
                'username': username,
                'created': datetime.now(),
                'expires': datetime.now() + timedelta(hours=24)
            }
            
            logger.info(f"Admin login successful for user: {username}")
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'token': token
            })
        else:
            logger.warning(f"Failed login attempt for user: {username}")
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
            
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during login'
        }), 500

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    """Admin logout endpoint"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if token in active_sessions:
            del active_sessions[token]
            logger.info("Admin logout successful")
        
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        })
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during logout'
        }), 500

@app.route('/api/admin/verify')
def verify_token():
    """Verify admin token is valid"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if verify_admin_token(token):
        return jsonify({
            'success': True,
            'message': 'Token is valid'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid or expired token'
        }), 401

@app.route('/api/admin/refresh', methods=['POST'])
def refresh_token():
    """Refresh admin token to extend session"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token or token not in active_sessions:
            return jsonify({
                'success': False,
                'message': 'Invalid token'
            }), 401
        
        session_data = active_sessions[token]
        
        # Check if token is not expired
        if datetime.now() < session_data['expires']:
            # Extend expiration by 24 hours
            active_sessions[token]['expires'] = datetime.now() + timedelta(hours=24)
            
            logger.info(f"Token refreshed for user: {session_data.get('username', 'unknown')}")
            
            return jsonify({
                'success': True,
                'message': 'Token refreshed successfully',
                'expiresIn': 86400  # 24 hours in seconds
            })
        else:
            # Token already expired
            del active_sessions[token]
            return jsonify({
                'success': False,
                'message': 'Token has expired. Please login again.'
            }), 401
            
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error refreshing token'
        }), 500

@app.route('/api/leads')
@require_admin_auth
def get_leads():
    """Get all leads (admin endpoint)"""
    try:
        leads = db.get_all_leads()
        return jsonify(leads)
    except Exception as e:
        logger.error(f"Error retrieving leads: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error retrieving leads'
        }), 500

@app.route('/api/leads/delete', methods=['POST'])
@require_admin_auth
def delete_lead():
    """Delete a lead (admin endpoint)"""
    try:
        data = request.get_json()
        lead_id = data.get('leadId')
        
        if not lead_id:
            return jsonify({
                'success': False,
                'message': 'Lead ID is required'
            }), 400
        
        # Delete from MongoDB using MongoDB _id
        success = db.delete_lead(lead_id)
        
        if success:
            logger.info(f"Lead deleted: {lead_id}")
            return jsonify({
                'success': True,
                'message': 'Lead deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Lead not found'
            }), 404
        
    except Exception as e:
        logger.error(f"Error deleting lead: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error deleting lead'
        }), 500

@app.route('/api/leads/delete/bulk', methods=['POST'])
@require_admin_auth
def delete_leads_bulk():
    """Delete multiple leads (admin endpoint)"""
    try:
        data = request.get_json()
        lead_ids = data.get('leadIds', [])
        
        if not lead_ids or not isinstance(lead_ids, list):
            return jsonify({
                'success': False,
                'message': 'Lead IDs array is required'
            }), 400
        
        # Delete from MongoDB using MongoDB _id
        deleted_count = db.delete_leads_bulk(lead_ids)
        
        logger.info(f"Bulk delete: {deleted_count} leads deleted")
        
        return jsonify({
            'success': True,
            'message': f'{deleted_count} lead(s) deleted successfully',
            'deletedCount': deleted_count
        })
        
    except Exception as e:
        logger.error(f"Error deleting leads: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error deleting leads'
        }), 500

@app.route('/api/leads/download/csv', methods=['POST'])
@require_admin_auth
def download_leads_csv():
    """Download leads as CSV"""
    try:
        data = request.get_json()
        leads = data.get('leads', [])
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Date', 'Time', 'First Name', 'Last Name', 'Email', 'WhatsApp',
            'Country', 'Contact Method', 'Buying Timeframe', 'Property Type', 'IP Address', 'User Agent'
        ])
        
        # Write data
        for lead in leads:
            timestamp = datetime.fromisoformat(lead['timestamp'].replace('Z', '+00:00'))
            date_str = timestamp.strftime('%Y-%m-%d')
            time_str = timestamp.strftime('%H:%M:%S')
            
            writer.writerow([
                date_str,
                time_str,
                lead.get('firstName', ''),
                lead.get('lastName', ''),
                lead.get('email', ''),
                lead.get('whatsapp', lead.get('phone', '')),
                lead.get('country', 'Unknown'),
                lead.get('contactMethod', ''),
                lead.get('timeframe', ''),
                lead.get('propertyType', lead.get('interest', '')),
                lead.get('ip_address', ''),
                lead.get('user_agent', '')
            ])
        
        # Create response
        csv_data = output.getvalue()
        output.close()
        
        response = Response(
            csv_data,
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename=leblanc_leads_{datetime.now().strftime("%Y%m%d")}.csv'
            }
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating CSV: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error generating CSV file'
        }), 500

@app.route('/api/leads/download/excel', methods=['POST'])
@require_admin_auth
def download_leads_excel():
    """Download leads as Excel (using CSV format for simplicity)"""
    try:
        data = request.get_json()
        leads = data.get('leads', [])
        
        # For basic Excel functionality, we'll use CSV with .xlsx extension
        # In a production environment, you'd want to use openpyxl or xlsxwriter
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Date', 'Time', 'First Name', 'Last Name', 'Email', 'WhatsApp',
            'Country', 'Contact Method', 'Buying Timeframe', 'Property Type', 'IP Address', 'User Agent'
        ])
        
        # Write data
        for lead in leads:
            timestamp = datetime.fromisoformat(lead['timestamp'].replace('Z', '+00:00'))
            date_str = timestamp.strftime('%Y-%m-%d')
            time_str = timestamp.strftime('%H:%M:%S')
            
            writer.writerow([
                date_str,
                time_str,
                lead.get('firstName', ''),
                lead.get('lastName', ''),
                lead.get('email', ''),
                lead.get('whatsapp', lead.get('phone', '')),
                lead.get('country', 'Unknown'),
                lead.get('contactMethod', ''),
                lead.get('timeframe', ''),
                lead.get('propertyType', lead.get('interest', '')),
                lead.get('ip_address', ''),
                lead.get('user_agent', '')
            ])
        
        # Create response
        csv_data = output.getvalue()
        output.close()
        
        response = Response(
            csv_data,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                'Content-Disposition': f'attachment; filename=leblanc_leads_{datetime.now().strftime("%Y%m%d")}.xlsx'
            }
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating Excel file: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error generating Excel file'
        }), 500

@app.route('/admin')
def admin_dashboard():
    """Serve admin dashboard"""
    return send_from_directory('.', 'admin.html')

# DEPRECATED: settings.html uses localStorage - needs rewrite to use MongoDB API
# @app.route('/settings')
# def settings_page():
#     """Serve settings page"""
#     return send_from_directory('.', 'settings.html')

@app.route('/editor')
def editor_page():
    """Serve website editor page"""
    return send_from_directory('.', 'editor.html')

# Manager Management Endpoints
@app.route('/api/managers/create', methods=['POST'])
@require_admin_auth
def create_manager():
    """Create a new manager user (admin only)"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        # Check if username already exists
        if db.get_manager(username):
            return jsonify({
                'success': False,
                'message': 'Username already exists'
            }), 400
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Create manager
        success = db.create_manager(username, password_hash, email)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Manager {username} created successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create manager'
            }), 500
            
    except Exception as e:
        logger.error(f"Error creating manager: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error creating manager'
        }), 500

@app.route('/api/managers')
@require_admin_auth
def get_managers():
    """Get all managers (admin only)"""
    try:
        managers = db.get_all_managers()
        # Remove sensitive data
        for manager in managers:
            manager.pop('password_hash', None)
        return jsonify(managers)
    except Exception as e:
        logger.error(f"Error fetching managers: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error fetching managers'
        }), 500

@app.route('/api/managers/update', methods=['POST'])
@require_admin_auth
def update_manager():
    """Update a manager (admin only)"""
    try:
        data = request.get_json()
        username = data.get('username')
        update_data = data.get('update_data', {})
        
        if not username:
            return jsonify({
                'success': False,
                'message': 'Username is required'
            }), 400
        
        # If updating password, hash it
        if 'password' in update_data:
            update_data['password_hash'] = hashlib.sha256(update_data['password'].encode()).hexdigest()
            del update_data['password']
        
        success = db.update_manager(username, update_data)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Manager {username} updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Manager not found or no changes made'
            }), 404
            
    except Exception as e:
        logger.error(f"Error updating manager: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error updating manager'
        }), 500

@app.route('/api/managers/delete', methods=['POST'])
@require_admin_auth
def delete_manager():
    """Delete a manager (admin only)"""
    try:
        data = request.get_json()
        username = data.get('username')
        
        if not username:
            return jsonify({
                'success': False,
                'message': 'Username is required'
            }), 400
        
        success = db.delete_manager(username)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Manager {username} deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Manager not found'
            }), 404
            
    except Exception as e:
        logger.error(f"Error deleting manager: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error deleting manager'
        }), 500

@app.route('/api/leads/assign', methods=['POST'])
@require_admin_auth
def assign_lead():
    """Assign or unassign a lead to/from a manager (admin only)"""
    try:
        data = request.get_json()
        lead_id = data.get('leadId')
        manager_username = data.get('managerUsername')
        
        logger.info(f"Assign lead request: leadId={lead_id}, manager={manager_username}")
        
        if not lead_id:
            logger.warning("Assign lead: No lead ID provided")
            return jsonify({
                'success': False,
                'message': 'Lead ID is required'
            }), 400
        
        # If manager_username is None/null, unassign the lead
        if manager_username is None:
            logger.info(f"Unassigning lead {lead_id}")
            success = db.update_lead(lead_id, {'assigned_to': None, 'assigned_at': None})
            message = 'Lead unassigned successfully'
        else:
            # Verify manager exists
            manager = db.get_manager(manager_username)
            if not manager:
                logger.warning(f"Manager not found: {manager_username}")
                return jsonify({
                    'success': False,
                    'message': f'Manager "{manager_username}" not found'
                }), 404
            
            logger.info(f"Assigning lead {lead_id} to manager {manager_username}")
            success = db.assign_lead_to_manager(lead_id, manager_username)
            message = 'Lead assigned successfully'
        
        if success:
            logger.info(f"Lead assignment successful: {message}")
            return jsonify({
                'success': True,
                'message': message
            })
        else:
            logger.error(f"Lead assignment failed for lead {lead_id}")
            return jsonify({
                'success': False,
                'message': 'Failed to update lead assignment. Lead may not exist.'
            }), 404
            
    except Exception as e:
        logger.error(f"Error updating lead assignment: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error updating lead assignment: {str(e)}'
        }), 500

@app.route('/api/manager/login', methods=['POST'])
def manager_login():
    """Manager login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        
        # Get manager from database
        manager = db.get_manager(username)
        
        if not manager:
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
        
        # Verify password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if manager['password_hash'] == password_hash and manager.get('active', True):
            # Generate token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=24)
            
            # Save session to database with role
            db.save_session(token, username, expires_at, role='manager')
            
            # Also keep in memory for compatibility
            active_sessions[token] = {
                'username': username,
                'role': 'manager',
                'expires': expires_at,
                'created': datetime.now()
            }
            
            logger.info(f"Manager login successful: {username}")
            
            return jsonify({
                'success': True,
                'token': token,
                'username': username,
                'expiresIn': 86400
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
            
    except Exception as e:
        logger.error(f"Manager login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during login'
        }), 500

@app.route('/api/manager/leads')
def get_manager_leads():
    """Get leads assigned to logged-in manager"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        logger.info(f"Manager leads request with token: {token[:20] if token else 'none'}...")
        
        if not token:
            logger.warning(f"Manager unauthorized - no token provided")
            return jsonify({
                'success': False,
                'message': 'Unauthorized - no token'
            }), 401
        
        # Check in-memory sessions first
        session_data = active_sessions.get(token)
        
        # If not in memory, check database
        if not session_data:
            logger.info(f"Token not in memory, checking database...")
            db_session = db.get_session(token)
            if db_session:
                logger.info(f"Found session in database for user: {db_session.get('username')}")
                # Restore to memory
                session_data = {
                    'username': db_session['username'],
                    'role': 'manager',
                    'expires': db_session['expires_at'],
                    'created': db_session['created_at']
                }
                active_sessions[token] = session_data
            else:
                logger.warning(f"Manager unauthorized - token not found in memory or database")
                return jsonify({
                    'success': False,
                    'message': 'Unauthorized - invalid or expired token. Please log in again.'
                }), 401
        
        # Verify it's a manager session
        if session_data.get('role') != 'manager':
            logger.warning(f"Non-manager role attempting to access manager leads: {session_data.get('role')}")
            return jsonify({
                'success': False,
                'message': 'Unauthorized'
            }), 401
        
        username = session_data.get('username')
        logger.info(f"Fetching leads for manager: {username}")
        leads = db.get_manager_leads(username)
        logger.info(f"Found {len(leads)} leads for manager {username}")
        
        return jsonify({
            'success': True,
            'leads': leads,
            'count': len(leads)
        })
        
    except Exception as e:
        logger.error(f"Error fetching manager leads: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': 'Error fetching leads'
        }), 500

@app.route('/api/website/update', methods=['POST'])
@require_admin_auth
def update_website():
    """Update website content (admin only)"""
    try:
        data = request.get_json()
        
        # Save website changes to a JSON file
        website_config_file = 'website_config.json'
        
        # Load existing config or create new
        if os.path.exists(website_config_file):
            with open(website_config_file, 'r') as f:
                config = json.load(f)
        else:
            config = {}
        
        # Update config with new changes
        if 'content' in data:
            config['content'] = {**config.get('content', {}), **data['content']}
        if 'design' in data:
            config['design'] = {**config.get('design', {}), **data['design']}
        if 'images' in data:
            config['images'] = {**config.get('images', {}), **data['images']}
        
        config['lastUpdated'] = datetime.now().isoformat()
        
        # Save updated config
        with open(website_config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info("Website configuration updated")
        
        return jsonify({
            'success': True,
            'message': 'Website updated successfully'
        })
        
    except Exception as e:
        logger.error(f"Error updating website: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error updating website'
        }), 500

@app.route('/api/website/config')
def get_website_config():
    """Get current website configuration"""
    try:
        website_config_file = 'website_config.json'
        
        if os.path.exists(website_config_file):
            with open(website_config_file, 'r') as f:
                config = json.load(f)
            return jsonify(config)
        else:
            return jsonify({})
    except Exception as e:
        logger.error(f"Error retrieving website config: {str(e)}")
        return jsonify({}), 500

@app.route('/login')
def admin_login_page():
    """Serve admin login page"""
    return send_from_directory('.', 'login.html')

@app.route('/manager-login')
def manager_login_page():
    """Serve manager login page"""
    return send_from_directory('.', 'manager-login.html')

@app.route('/manager')
def manager_dashboard():
    """Serve manager dashboard"""
    return send_from_directory('.', 'manager-dashboard.html')

if __name__ == '__main__':
    # Create leads file if it doesn't exist
    if not os.path.exists('leads.json'):
        with open('leads.json', 'w') as f:
            json.dump([], f)
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)