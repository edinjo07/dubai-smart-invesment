#!/usr/bin/env python3
"""
Quick status check for Le Blanc Dubai Real Estate Backend
"""

import requests
import sys
import os
import json

def check_backend_status():
    """Check if backend is running and responsive"""
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is running successfully!")
            print(f"   Status: {data['status']}")
            print(f"   Timestamp: {data['timestamp']}")
            print(f"   Version: {data['version']}")
            return True
        else:
            print(f"❌ Backend responded with error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running or not accessible on localhost:5000")
        print("   Try running: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return False

def check_website():
    """Check if website is accessible"""
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✅ Website is accessible at http://localhost:5000")
            return True
        else:
            print(f"❌ Website responded with error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing website: {e}")
        return False

def check_files():
    """Check if required files exist"""
    required_files = [
        'app.py',
        'index.html',
        'requirements.txt',
        '.env.example'
    ]
    
    optional_files = [
        '.env',
        'leads.json'
    ]
    
    print("\nFile Status:")
    all_required_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (REQUIRED)")
            all_required_exist = False
    
    for file in optional_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"⚠️  {file} (optional - will be created when needed)")
    
    return all_required_exist

def show_leads_summary():
    """Show summary of leads if available"""
    try:
        if os.path.exists('leads.json'):
            with open('leads.json', 'r') as f:
                leads = json.load(f)
                print(f"\n📊 Leads Summary: {len(leads)} total leads")
                if leads:
                    latest = leads[-1]
                    print(f"   Latest lead: {latest.get('firstName', 'N/A')} {latest.get('lastName', 'N/A')}")
                    print(f"   Email: {latest.get('email', 'N/A')}")
                    print(f"   Timestamp: {latest.get('timestamp', 'N/A')}")
        else:
            print("\n📊 No leads file found (will be created on first submission)")
    except Exception as e:
        print(f"\n❌ Error reading leads: {e}")

def main():
    print("=" * 60)
    print("Le Blanc Dubai Real Estate - Backend Status Check")
    print("=" * 60)
    
    # Check files first
    files_ok = check_files()
    
    if not files_ok:
        print("\n❌ Missing required files. Please ensure all files are in place.")
        sys.exit(1)
    
    print("\nService Status:")
    backend_ok = check_backend_status()
    
    if backend_ok:
        website_ok = check_website()
        show_leads_summary()
        
        print("\n" + "=" * 60)
        print("✅ All systems operational!")
        print("   Website: http://localhost:5000")
        print("   API Health: http://localhost:5000/api/health")
        print("   Admin Leads: http://localhost:5000/api/leads")
        print("=" * 60)
    else:
        print("\n❌ Backend is not running. Start it with:")
        print("   python app.py")
        print("   or")
        print("   start_server.bat")

if __name__ == "__main__":
    main()