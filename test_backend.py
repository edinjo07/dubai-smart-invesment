#!/usr/bin/env python3
"""
Test script for Le Blanc Dubai Real Estate Backend
This script tests the backend functionality without requiring the server to be running
"""

import json
import sys
import os

# Add current directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_email_validation():
    """Test email validation function"""
    from app import validate_email
    
    print("Testing email validation...")
    
    # Valid emails
    valid_emails = [
        "test@example.com",
        "user.name@domain.co.uk",
        "firstname+lastname@company.org"
    ]
    
    # Invalid emails
    invalid_emails = [
        "invalid-email",
        "@domain.com",
        "user@",
        "user space@domain.com"
    ]
    
    for email in valid_emails:
        if validate_email(email):
            print(f"✅ {email} - Valid")
        else:
            print(f"❌ {email} - Should be valid but failed")
    
    for email in invalid_emails:
        if not validate_email(email):
            print(f"✅ {email} - Invalid (correctly identified)")
        else:
            print(f"❌ {email} - Should be invalid but passed")

def test_phone_validation():
    """Test phone validation function"""
    from app import validate_phone
    
    print("\nTesting phone validation...")
    
    # Valid phones
    valid_phones = [
        "+971501234567",
        "971501234567",
        "+1 (555) 123-4567",
        "0501234567"
    ]
    
    # Invalid phones
    invalid_phones = [
        "123",
        "abc123def",
        "+971-abc-def",
        ""
    ]
    
    for phone in valid_phones:
        if validate_phone(phone):
            print(f"✅ {phone} - Valid")
        else:
            print(f"❌ {phone} - Should be valid but failed")
    
    for phone in invalid_phones:
        if not validate_phone(phone):
            print(f"✅ {phone} - Invalid (correctly identified)")
        else:
            print(f"❌ {phone} - Should be invalid but passed")

def test_lead_storage():
    """Test lead storage functionality"""
    from app import save_lead_data
    
    print("\nTesting lead storage...")
    
    # Mock request object
    class MockRequest:
        environ = {
            'REMOTE_ADDR': '127.0.0.1',
            'HTTP_USER_AGENT': 'Test Agent'
        }
    
    # Temporarily replace the request object
    import app
    original_request = getattr(app, 'request', None)
    app.request = MockRequest()
    
    test_data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '+971501234567',
        'interest': 'Investment Opportunity',
        'message': 'I am interested in Le Blanc apartments'
    }
    
    try:
        result = save_lead_data(test_data)
        if result:
            print("✅ Lead data saved successfully")
            
            # Check if data was actually saved
            if os.path.exists('leads.json'):
                with open('leads.json', 'r') as f:
                    leads = json.load(f)
                    if leads and leads[-1]['email'] == test_data['email']:
                        print("✅ Lead data verified in leads.json")
                    else:
                        print("❌ Lead data not found in leads.json")
            else:
                print("❌ leads.json file not created")
        else:
            print("❌ Failed to save lead data")
    except Exception as e:
        print(f"❌ Error saving lead data: {e}")
    finally:
        # Restore original request
        app.request = original_request

def test_api_endpoints():
    """Test API endpoints using Flask test client"""
    print("\nTesting API endpoints...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            if response.status_code == 200:
                data = json.loads(response.data)
                print(f"✅ Health endpoint: {data['status']}")
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
            
            # Test leads endpoint
            response = client.get('/api/leads')
            if response.status_code == 200:
                data = json.loads(response.data)
                print(f"✅ Leads endpoint: Found {data['count']} leads")
            else:
                print(f"❌ Leads endpoint failed: {response.status_code}")
            
            # Test contact form endpoint
            test_form_data = {
                'firstName': 'Jane',
                'lastName': 'Smith',
                'email': 'jane.smith@example.com',
                'phone': '+971501234567',
                'interest': 'General Inquiry',
                'message': 'Test message from automated test'
            }
            
            response = client.post('/api/contact', 
                                   json=test_form_data,
                                   content_type='application/json')
            
            if response.status_code == 200:
                data = json.loads(response.data)
                if data['success']:
                    print("✅ Contact form endpoint: Success")
                else:
                    print(f"❌ Contact form endpoint: {data['message']}")
            else:
                print(f"❌ Contact form endpoint failed: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")

def main():
    """Run all tests"""
    print("=" * 50)
    print("Le Blanc Dubai Real Estate Backend Tests")
    print("=" * 50)
    
    test_email_validation()
    test_phone_validation()
    test_lead_storage()
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    print("Tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()