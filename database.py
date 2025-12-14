"""
MongoDB Database Module for Dubai Smart Investment
Handles all database operations for lead management
"""

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Database:
    """MongoDB database handler"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.leads_collection = None
        self.connected = False
        self._connect()
    
    def _connect(self):
        """Connect to MongoDB"""
        try:
            # Get MongoDB URI from environment variable
            mongodb_uri = os.environ.get('MONGODB_URI')
            
            if not mongodb_uri:
                logger.warning("MONGODB_URI not set. Database features will be disabled.")
                return
            
            # Create MongoDB client
            self.client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
            
            # Test connection
            self.client.admin.command('ping')
            
            # Get database (extract DB name from URI or use default)
            db_name = os.environ.get('MONGODB_DB_NAME', 'dubai_real_estate')
            self.db = self.client[db_name]
            
            # Get collections
            self.leads_collection = self.db['leads']
            
            self.connected = True
            logger.info(f"Successfully connected to MongoDB database: {db_name}")
            
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            self.connected = False
        except Exception as e:
            logger.error(f"MongoDB connection error: {str(e)}")
            self.connected = False
    
    def is_connected(self):
        """Check if database is connected"""
        return self.connected
    
    def save_lead(self, lead_data):
        """
        Save lead data to MongoDB
        
        Args:
            lead_data (dict): Lead information
            
        Returns:
            str: Lead ID if successful, None otherwise
        """
        if not self.connected:
            logger.warning("Cannot save lead: Database not connected")
            return None
        
        try:
            # Add timestamp
            lead_data['created_at'] = datetime.utcnow()
            lead_data['updated_at'] = datetime.utcnow()
            
            # Insert lead
            result = self.leads_collection.insert_one(lead_data)
            
            logger.info(f"Lead saved successfully: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error saving lead: {str(e)}")
            return None
    
    def get_all_leads(self, limit=100, skip=0):
        """
        Get all leads from database
        
        Args:
            limit (int): Maximum number of leads to return
            skip (int): Number of leads to skip (for pagination)
            
        Returns:
            list: List of lead documents
        """
        if not self.connected:
            return []
        
        try:
            leads = list(self.leads_collection.find()
                        .sort('created_at', -1)
                        .skip(skip)
                        .limit(limit))
            
            # Convert ObjectId to string for JSON serialization
            for lead in leads:
                lead['_id'] = str(lead['_id'])
                if 'created_at' in lead:
                    lead['created_at'] = lead['created_at'].isoformat()
                if 'updated_at' in lead:
                    lead['updated_at'] = lead['updated_at'].isoformat()
            
            return leads
            
        except Exception as e:
            logger.error(f"Error getting leads: {str(e)}")
            return []
    
    def get_lead_by_id(self, lead_id):
        """Get a single lead by ID"""
        if not self.connected:
            return None
        
        try:
            from bson.objectid import ObjectId
            lead = self.leads_collection.find_one({'_id': ObjectId(lead_id)})
            
            if lead:
                lead['_id'] = str(lead['_id'])
                if 'created_at' in lead:
                    lead['created_at'] = lead['created_at'].isoformat()
                if 'updated_at' in lead:
                    lead['updated_at'] = lead['updated_at'].isoformat()
            
            return lead
            
        except Exception as e:
            logger.error(f"Error getting lead by ID: {str(e)}")
            return None
    
    def update_lead_status(self, lead_id, status):
        """Update lead status"""
        if not self.connected:
            return False
        
        try:
            from bson.objectid import ObjectId
            result = self.leads_collection.update_one(
                {'_id': ObjectId(lead_id)},
                {
                    '$set': {
                        'status': status,
                        'updated_at': datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating lead status: {str(e)}")
            return False
    
    def delete_lead(self, lead_id):
        """Delete a lead by ID"""
        if not self.connected:
            return False
        
        try:
            from bson.objectid import ObjectId
            result = self.leads_collection.delete_one({'_id': ObjectId(lead_id)})
            
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error deleting lead: {str(e)}")
            return False
    
    def get_leads_count(self):
        """Get total number of leads"""
        if not self.connected:
            return 0
        
        try:
            return self.leads_collection.count_documents({})
        except Exception as e:
            logger.error(f"Error counting leads: {str(e)}")
            return 0
    
    def search_leads(self, query, limit=50):
        """Search leads by email, name, or phone"""
        if not self.connected:
            return []
        
        try:
            # Create search query
            search_filter = {
                '$or': [
                    {'email': {'$regex': query, '$options': 'i'}},
                    {'firstName': {'$regex': query, '$options': 'i'}},
                    {'lastName': {'$regex': query, '$options': 'i'}},
                    {'whatsapp': {'$regex': query, '$options': 'i'}}
                ]
            }
            
            leads = list(self.leads_collection.find(search_filter)
                        .sort('created_at', -1)
                        .limit(limit))
            
            # Convert ObjectId to string
            for lead in leads:
                lead['_id'] = str(lead['_id'])
                if 'created_at' in lead:
                    lead['created_at'] = lead['created_at'].isoformat()
                if 'updated_at' in lead:
                    lead['updated_at'] = lead['updated_at'].isoformat()
            
            return leads
            
        except Exception as e:
            logger.error(f"Error searching leads: {str(e)}")
            return []

# Create global database instance
db = Database()
