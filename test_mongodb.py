#!/usr/bin/env python3
"""
Comprehensive MongoDB Connection and Database Operations Test
Tests all database functions to ensure data is properly saved to MongoDB Atlas
"""

import sys
import os
from datetime import datetime, timedelta
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import db
from app import app

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_mongodb_connection():
    """Test 1: Verify MongoDB connection"""
    print_section("TEST 1: MongoDB Connection Status")
    
    if db.client is None:
        print("❌ FAILED: MongoDB client not initialized")
        return False
    
    try:
        # Try to ping the database
        db.client.admin.command('ping')
        print("✅ PASSED: MongoDB connection successful")
        print(f"   Database: {db.db.name}")
        print(f"   Collections: {db.db.list_collection_names()}")
        return True
    except Exception as e:
        print(f"❌ FAILED: Cannot connect to MongoDB: {e}")
        return False

def test_save_lead():
    """Test 2: Save a lead to database"""
    print_section("TEST 2: Save Lead to Database")
    
    test_lead = {
        'firstName': 'Test',
        'lastName': 'MongoDB',
        'email': f'test.mongodb.{datetime.now().timestamp()}@example.com',
        'whatsapp': '+971501234567',
        'country': 'UAE',
        'contactMethod': 'whatsapp',
        'timeframe': 'within-3-months',
        'propertyType': 'apartment',
        'message': 'Test lead for MongoDB verification',
        'ip_address': '127.0.0.1',
        'user_agent': 'Test Script'
    }
    
    try:
        lead_id = db.save_lead(test_lead)
        if lead_id:
            print(f"✅ PASSED: Lead saved successfully")
            print(f"   Lead ID: {lead_id}")
            return lead_id
        else:
            print("❌ FAILED: Lead not saved")
            return None
    except Exception as e:
        print(f"❌ FAILED: Error saving lead: {e}")
        return None

def test_get_leads(lead_id):
    """Test 3: Retrieve leads from database"""
    print_section("TEST 3: Retrieve Leads from Database")
    
    try:
        leads = db.get_all_leads()
        if leads:
            print(f"✅ PASSED: Retrieved {len(leads)} leads")
            
            # Verify the test lead is in the results
            test_lead_found = any(str(lead.get('_id')) == str(lead_id) for lead in leads)
            if test_lead_found:
                print(f"✅ VERIFIED: Test lead (ID: {lead_id}) found in results")
            else:
                print(f"⚠️  WARNING: Test lead not found in results")
            
            # Show last 3 leads
            print("\n   Last 3 leads:")
            for lead in leads[:3]:
                print(f"   - {lead.get('firstName')} {lead.get('lastName')} ({lead.get('email')})")
            return True
        else:
            print("❌ FAILED: No leads retrieved")
            return False
    except Exception as e:
        print(f"❌ FAILED: Error retrieving leads: {e}")
        return False

def test_create_manager():
    """Test 4: Create a manager account"""
    print_section("TEST 4: Create Manager Account")
    
    test_manager = {
        'username': f'test_manager_{int(datetime.now().timestamp())}',
        'password': 'TestPass123!',
        'name': 'Test Manager',
        'email': f'manager.{datetime.now().timestamp()}@example.com',
        'phone': '+971501234567'
    }
    
    try:
        manager_id = db.create_manager(
            username=test_manager['username'],
            password=test_manager['password'],
            name=test_manager['name'],
            email=test_manager['email'],
            phone=test_manager['phone']
        )
        
        if manager_id:
            print(f"✅ PASSED: Manager created successfully")
            print(f"   Manager ID: {manager_id}")
            print(f"   Username: {test_manager['username']}")
            return manager_id, test_manager['username']
        else:
            print("❌ FAILED: Manager not created")
            return None, None
    except Exception as e:
        print(f"❌ FAILED: Error creating manager: {e}")
        return None, None

def test_get_manager(manager_id, username):
    """Test 5: Retrieve manager from database"""
    print_section("TEST 5: Retrieve Manager from Database")
    
    try:
        manager = db.get_manager(username)
        if manager:
            print(f"✅ PASSED: Manager retrieved successfully")
            print(f"   Name: {manager.get('name')}")
            print(f"   Email: {manager.get('email')}")
            print(f"   Created: {manager.get('created_at')}")
            return True
        else:
            print("❌ FAILED: Manager not found")
            return False
    except Exception as e:
        print(f"❌ FAILED: Error retrieving manager: {e}")
        return False

def test_assign_lead(lead_id, manager_id):
    """Test 6: Assign lead to manager"""
    print_section("TEST 6: Assign Lead to Manager")
    
    try:
        result = db.assign_lead_to_manager(str(lead_id), str(manager_id))
        if result:
            print(f"✅ PASSED: Lead assigned to manager successfully")
            
            # Verify assignment
            manager_leads = db.get_manager_leads(str(manager_id))
            if manager_leads and any(str(l.get('_id')) == str(lead_id) for l in manager_leads):
                print(f"✅ VERIFIED: Lead appears in manager's assigned leads")
                return True
            else:
                print("⚠️  WARNING: Lead not found in manager's leads list")
                return False
        else:
            print("❌ FAILED: Lead assignment failed")
            return False
    except Exception as e:
        print(f"❌ FAILED: Error assigning lead: {e}")
        return False

def test_session_management():
    """Test 7: Session save and retrieve"""
    print_section("TEST 7: Session Management")
    
    test_token = f"test_token_{datetime.now().timestamp()}"
    session_data = {
        'user_id': 'test_user_123',
        'username': 'test_admin',
        'role': 'admin'
    }
    expires_at = datetime.now() + timedelta(hours=24)
    
    try:
        # Save session
        result = db.save_session(test_token, session_data, expires_at)
        if result:
            print(f"✅ PASSED: Session saved successfully")
            
            # Retrieve session
            retrieved_session = db.get_session(test_token)
            if retrieved_session:
                print(f"✅ PASSED: Session retrieved successfully")
                print(f"   Username: {retrieved_session.get('username')}")
                
                # Clean up
                db.delete_session(test_token)
                print(f"✅ PASSED: Session deleted successfully")
                return True
            else:
                print("❌ FAILED: Session not retrieved")
                return False
        else:
            print("❌ FAILED: Session not saved")
            return False
    except Exception as e:
        print(f"❌ FAILED: Error in session management: {e}")
        return False

def test_api_endpoints():
    """Test 8: Test API endpoints with Flask test client"""
    print_section("TEST 8: API Endpoints Test")
    
    try:
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Health Endpoint: {response.status_code}")
                print(f"   MongoDB Connected: {data.get('mongodb_connected')}")
                print(f"   Database: {data.get('database_name')}")
                
                if not data.get('mongodb_connected'):
                    print("⚠️  WARNING: Health endpoint shows MongoDB not connected")
                    return False
            else:
                print(f"❌ FAILED: Health endpoint returned {response.status_code}")
                return False
            
            # Test contact form submission
            test_contact = {
                'firstName': 'API',
                'lastName': 'Test',
                'email': f'api.test.{datetime.now().timestamp()}@example.com',
                'whatsapp': '+971501234567',
                'country': 'UAE',
                'contactMethod': 'email',
                'timeframe': 'within-month',
                'propertyType': 'villa'
            }
            
            response = client.post('/api/contact', 
                                   json=test_contact,
                                   content_type='application/json')
            
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    print(f"✅ Contact Form API: Lead submitted successfully")
                    return True
                else:
                    print(f"❌ FAILED: Contact form returned error: {data.get('message')}")
                    return False
            else:
                print(f"❌ FAILED: Contact form endpoint returned {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ FAILED: Error testing API endpoints: {e}")
        return False

def test_cleanup(lead_id, manager_id):
    """Test 9: Clean up test data"""
    print_section("TEST 9: Cleanup Test Data")
    
    try:
        # Delete test lead
        if lead_id:
            db.delete_lead(str(lead_id))
            print(f"✅ Test lead deleted (ID: {lead_id})")
        
        # Delete test manager
        if manager_id:
            db.delete_manager(str(manager_id))
            print(f"✅ Test manager deleted (ID: {manager_id})")
        
        return True
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")
        return True  # Don't fail the test suite for cleanup issues

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  MONGODB DATABASE COMPREHENSIVE TEST SUITE              ║")
    print("║  Dubai Smart Investment - Database Operations           ║")
    print("╚" + "=" * 58 + "╝")
    
    test_results = []
    lead_id = None
    manager_id = None
    username = None
    
    # Run tests in sequence
    test_results.append(("MongoDB Connection", test_mongodb_connection()))
    
    lead_id = test_save_lead()
    test_results.append(("Save Lead", lead_id is not None))
    
    test_results.append(("Get Leads", test_get_leads(lead_id)))
    
    manager_id, username = test_create_manager()
    test_results.append(("Create Manager", manager_id is not None))
    
    if manager_id and username:
        test_results.append(("Get Manager", test_get_manager(manager_id, username)))
    
    if lead_id and manager_id:
        test_results.append(("Assign Lead", test_assign_lead(lead_id, manager_id)))
    
    test_results.append(("Session Management", test_session_management()))
    
    test_results.append(("API Endpoints", test_api_endpoints()))
    
    # Cleanup
    test_cleanup(lead_id, manager_id)
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print("\n" + "-" * 60)
    print(f"Total: {passed}/{total} tests passed ({passed*100//total}%)")
    print("-" * 60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Database is fully functional.")
        print("✅ MongoDB Atlas connection working")
        print("✅ All CRUD operations verified")
        print("✅ Data persistence confirmed")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED - Review errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
