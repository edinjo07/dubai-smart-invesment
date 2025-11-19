# Test MongoDB Connection
# Run this to verify your MongoDB setup

import os
from pymongo import MongoClient

# Your MongoDB connection string
MONGODB_URI = "mongodb+srv://dubai_admin:h8lnVDWOJTsxBpus@dubaismart1.y1dbyro.mongodb.net/dubai_smart_invest?retryWrites=true&w=majority&appName=DubaiSmart1"

print("Testing MongoDB connection...")
print(f"URI: {MONGODB_URI[:50]}...")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    
    # Test connection
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
    
    # Test database access
    db = client['dubai_smart_invest']
    print(f"✅ Database 'dubai_smart_invest' accessible")
    
    # Test collections
    collections = db.list_collection_names()
    print(f"✅ Collections: {collections if collections else 'None yet (will be created on first insert)'}")
    
    # Test insert
    test_data = {
        'test': True,
        'message': 'MongoDB connection test'
    }
    result = db['test_collection'].insert_one(test_data)
    print(f"✅ Test insert successful! ID: {result.inserted_id}")
    
    # Clean up test
    db['test_collection'].delete_one({'_id': result.inserted_id})
    print(f"✅ Test cleanup successful")
    
    print("\n🎉 MongoDB is working perfectly!")
    print("\nNext step: Make sure this same URI is added to Render:")
    print("1. Go to https://dashboard.render.com/")
    print("2. Click your service")
    print("3. Environment tab")
    print("4. Add MONGODB_URI with the value above")
    
except Exception as e:
    print(f"❌ MongoDB connection failed: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Check if your IP is whitelisted in MongoDB Atlas (Network Access)")
    print("2. Verify username and password are correct")
    print("3. Make sure the cluster is running")
