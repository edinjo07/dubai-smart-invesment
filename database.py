"""
MongoDB Database Configuration for Dubai Smart Investment
Handles leads, users, and website configuration storage
MongoDB connection is REQUIRED - no local fallback
"""
import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        # MongoDB connection string from environment variable (REQUIRED)
        mongo_uri = os.environ.get('MONGODB_URI')
        
        if not mongo_uri:
            raise RuntimeError("MONGODB_URI environment variable is required")
        
        try:
            self.client = MongoClient(mongo_uri)
            self.db = self.client['dubai_smart_invest']
            
            # Collections
            self.leads = self.db['leads']
            self.users = self.db['users']
            self.sessions = self.db['sessions']
            self.config = self.db['website_config']
            
            # Create indexes for better performance
            self.leads.create_index([('email', ASCENDING)])
            self.leads.create_index([('created_at', DESCENDING)])
            self.sessions.create_index([('token', ASCENDING)])
            self.sessions.create_index([('expires_at', ASCENDING)])
            self.users.create_index([('username', ASCENDING)], unique=True)
            
            # Test connection
            self.client.admin.command('ping')
            logger.info("MongoDB connected successfully")
            
        except Exception as e:
            logger.error(f"MongoDB connection failed: {str(e)}")
            raise RuntimeError(f"Failed to connect to MongoDB: {str(e)}")
    
    def save_lead(self, lead_data):
        """Save a new lead to database"""
        try:
            lead_data['created_at'] = datetime.now()
            lead_data['updated_at'] = datetime.now()
            lead_data['status'] = lead_data.get('status', 'new')
            
            result = self.leads.insert_one(lead_data)
            logger.info(f"Lead saved to MongoDB: {lead_data.get('email')}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error saving lead to MongoDB: {str(e)}")
            raise
    
    def get_all_leads(self):
        """Get all leads sorted by newest first"""
        try:
            leads = list(self.leads.find().sort('created_at', DESCENDING))
            
            # Convert ObjectId to string for JSON serialization
            for lead in leads:
                lead['_id'] = str(lead['_id'])
                if 'created_at' in lead:
                    lead['timestamp'] = lead['created_at'].isoformat()
            
            return leads
            
        except Exception as e:
            logger.error(f"Error fetching leads from MongoDB: {str(e)}")
            return []
    
    def delete_lead(self, lead_id):
        """Delete a lead by ID"""
        try:
            result = self.leads.delete_one({'_id': ObjectId(lead_id)})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error deleting lead from MongoDB: {str(e)}")
            return False
    
    def delete_leads_bulk(self, lead_ids):
        """Delete multiple leads"""
        try:
            object_ids = [ObjectId(lid) for lid in lead_ids]
            result = self.leads.delete_many({'_id': {'$in': object_ids}})
            return result.deleted_count
            
        except Exception as e:
            logger.error(f"Error bulk deleting leads from MongoDB: {str(e)}")
            return 0
    
    def update_lead(self, lead_id, update_data):
        """Update a lead"""
        try:
            update_data['updated_at'] = datetime.now()
            
            result = self.leads.update_one(
                {'_id': ObjectId(lead_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating lead in MongoDB: {str(e)}")
            return False
    
    def save_session(self, token, username, expires_at):
        """Save user session"""
        try:
            self.sessions.insert_one({
                'token': token,
                'username': username,
                'created_at': datetime.now(),
                'expires_at': expires_at
            })
            return True
            
        except Exception as e:
            logger.error(f"Error saving session: {str(e)}")
            return False
    
    def get_session(self, token):
        """Get session by token"""
        try:
            session = self.sessions.find_one({'token': token})
            if session and session['expires_at'] > datetime.now():
                return session
            return None
            
        except Exception as e:
            logger.error(f"Error fetching session: {str(e)}")
            return None
    
    def delete_session(self, token):
        """Delete session"""
        try:
            result = self.sessions.delete_one({'token': token})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error deleting session: {str(e)}")
            return False
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        try:
            self.sessions.delete_many({'expires_at': {'$lt': datetime.now()}})
            
        except Exception as e:
            logger.error(f"Error cleaning up sessions: {str(e)}")
    
    def get_website_config(self):
        """Get website configuration"""
        try:
            config = self.config.find_one({'type': 'website'})
            if config:
                config.pop('_id', None)
                return config
            return {}
            
        except Exception as e:
            logger.error(f"Error fetching config: {str(e)}")
            return {}
    
    def save_website_config(self, config_data):
        """Save website configuration"""
        try:
            config_data['updated_at'] = datetime.now()
            
            self.config.update_one(
                {'type': 'website'},
                {'$set': config_data},
                upsert=True
            )
            return True
            
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")
            return False
    
    # Manager user management methods
    def create_manager(self, username, password_hash, email=''):
        """Create a new manager user"""
        try:
            manager_data = {
                'username': username,
                'password_hash': password_hash,
                'email': email,
                'role': 'manager',
                'created_at': datetime.now(),
                'active': True
            }
            
            self.users.insert_one(manager_data)
            logger.info(f"Manager created: {username}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating manager: {str(e)}")
            return False
    
    def get_manager(self, username):
        """Get manager by username"""
        try:
            manager = self.users.find_one({'username': username, 'role': 'manager'})
            if manager:
                manager['_id'] = str(manager['_id'])
            return manager
            
        except Exception as e:
            logger.error(f"Error fetching manager: {str(e)}")
            return None
    
    def get_all_managers(self):
        """Get all manager users"""
        try:
            managers = list(self.users.find({'role': 'manager'}))
            for manager in managers:
                manager['_id'] = str(manager['_id'])
            return managers
            
        except Exception as e:
            logger.error(f"Error fetching managers: {str(e)}")
            return []
    
    def update_manager(self, username, update_data):
        """Update manager information"""
        try:
            update_data['updated_at'] = datetime.now()
            
            result = self.users.update_one(
                {'username': username, 'role': 'manager'},
                {'$set': update_data}
            )
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating manager: {str(e)}")
            return False
    
    def delete_manager(self, username):
        """Delete a manager user"""
        try:
            result = self.users.delete_one({'username': username, 'role': 'manager'})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error deleting manager: {str(e)}")
            return False
    
    def assign_lead_to_manager(self, lead_id, manager_username):
        """Assign a lead to a specific manager"""
        try:
            # Check if lead exists first
            lead = self.leads.find_one({'_id': ObjectId(lead_id)})
            if not lead:
                logger.error(f"Lead not found with ID: {lead_id}")
                return False
            
            result = self.leads.update_one(
                {'_id': ObjectId(lead_id)},
                {'$set': {
                    'assigned_to': manager_username,
                    'assigned_at': datetime.now()
                }}
            )
            # Return True if matched (even if not modified, means already assigned)
            success = result.matched_count > 0
            if success:
                logger.info(f"Lead {lead_id} assigned to {manager_username}")
            return success
            
        except Exception as e:
            logger.error(f"Error assigning lead {lead_id}: {str(e)}")
            return False
    
    def get_manager_leads(self, manager_username):
        """Get all leads assigned to a specific manager"""
        try:
            leads = list(self.leads.find({'assigned_to': manager_username}).sort('created_at', DESCENDING))
            
            for lead in leads:
                lead['_id'] = str(lead['_id'])
                if 'created_at' in lead:
                    lead['timestamp'] = lead['created_at'].isoformat()
            
            return leads
            
        except Exception as e:
            logger.error(f"Error fetching manager leads: {str(e)}")
            return []

# Global database instance
db = Database()
