"""
MongoDB Database Configuration for Dubai Smart Investment
Handles leads, users, and website configuration storage
"""
import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        # MongoDB connection string from environment variable
        mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
        
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
            
            logger.info("MongoDB connected successfully")
            
        except Exception as e:
            logger.error(f"MongoDB connection failed: {str(e)}")
            # Fallback to local storage if MongoDB fails
            self.client = None
            self.db = None
    
    def save_lead(self, lead_data):
        """Save a new lead to database"""
        try:
            if self.leads is None:
                return self._save_lead_local(lead_data)
            
            lead_data['created_at'] = datetime.now()
            lead_data['updated_at'] = datetime.now()
            lead_data['status'] = lead_data.get('status', 'new')
            
            result = self.leads.insert_one(lead_data)
            logger.info(f"Lead saved to MongoDB: {lead_data.get('email')}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error saving lead to MongoDB: {str(e)}")
            return self._save_lead_local(lead_data)
    
    def get_all_leads(self):
        """Get all leads sorted by newest first"""
        try:
            if self.leads is None:
                return self._get_leads_local()
            
            leads = list(self.leads.find().sort('created_at', DESCENDING))
            
            # Convert ObjectId to string for JSON serialization
            for lead in leads:
                lead['_id'] = str(lead['_id'])
                if 'created_at' in lead:
                    lead['timestamp'] = lead['created_at'].isoformat()
            
            return leads
            
        except Exception as e:
            logger.error(f"Error fetching leads from MongoDB: {str(e)}")
            return self._get_leads_local()
    
    def delete_lead(self, lead_id):
        """Delete a lead by ID"""
        try:
            if self.leads is None:
                return self._delete_lead_local(lead_id)
            
            result = self.leads.delete_one({'_id': ObjectId(lead_id)})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error deleting lead from MongoDB: {str(e)}")
            return False
    
    def delete_leads_bulk(self, lead_ids):
        """Delete multiple leads"""
        try:
            if self.leads is None:
                return self._delete_leads_bulk_local(lead_ids)
            
            object_ids = [ObjectId(lid) for lid in lead_ids]
            result = self.leads.delete_many({'_id': {'$in': object_ids}})
            return result.deleted_count
            
        except Exception as e:
            logger.error(f"Error bulk deleting leads from MongoDB: {str(e)}")
            return 0
    
    def update_lead(self, lead_id, update_data):
        """Update a lead"""
        try:
            if self.leads is None:
                return False
            
            from bson.objectid import ObjectId
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
            if self.sessions is None:
                return False
            
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
            if self.sessions is None:
                return None
            
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
            if self.sessions is None:
                return False
            
            result = self.sessions.delete_one({'token': token})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error deleting session: {str(e)}")
            return False
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        try:
            if self.sessions is None:
                return
            
            self.sessions.delete_many({'expires_at': {'$lt': datetime.now()}})
            
        except Exception as e:
            logger.error(f"Error cleaning up sessions: {str(e)}")
    
    def get_website_config(self):
        """Get website configuration"""
        try:
            if self.config is None:
                return {}
            
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
            if self.config is None:
                return False
            
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
            if self.users is None:
                return False
            
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
            if self.users is None:
                return None
            
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
            if self.users is None:
                return []
            
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
            if self.users is None:
                return False
            
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
            if self.users is None:
                return False
            
            result = self.users.delete_one({'username': username, 'role': 'manager'})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error deleting manager: {str(e)}")
            return False
    
    def assign_lead_to_manager(self, lead_id, manager_username):
        """Assign a lead to a specific manager"""
        try:
            if self.leads is None:
                return False
            
            result = self.leads.update_one(
                {'_id': ObjectId(lead_id)},
                {'$set': {
                    'assigned_to': manager_username,
                    'assigned_at': datetime.now()
                }}
            )
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error assigning lead: {str(e)}")
            return False
    
    def get_manager_leads(self, manager_username):
        """Get all leads assigned to a specific manager"""
        try:
            if self.leads is None:
                return []
            
            leads = list(self.leads.find({'assigned_to': manager_username}).sort('created_at', DESCENDING))
            
            for lead in leads:
                lead['_id'] = str(lead['_id'])
                if 'created_at' in lead:
                    lead['timestamp'] = lead['created_at'].isoformat()
            
            return leads
            
        except Exception as e:
            logger.error(f"Error fetching manager leads: {str(e)}")
            return []
    
    # Fallback methods for local file storage
    def _save_lead_local(self, lead_data):
        """Fallback: Save lead to local JSON file"""
        import json
        try:
            leads_file = 'leads.json'
            leads = []
            
            if os.path.exists(leads_file):
                with open(leads_file, 'r') as f:
                    leads = json.load(f)
            
            lead_data['timestamp'] = datetime.now().isoformat()
            lead_data['id'] = str(len(leads) + 1)
            leads.append(lead_data)
            
            with open(leads_file, 'w') as f:
                json.dump(leads, f, indent=2)
            
            return lead_data['id']
            
        except Exception as e:
            logger.error(f"Error saving lead locally: {str(e)}")
            return None
    
    def _get_leads_local(self):
        """Fallback: Get leads from local JSON file"""
        import json
        try:
            leads_file = 'leads.json'
            if os.path.exists(leads_file):
                with open(leads_file, 'r') as f:
                    return json.load(f)
            return []
            
        except Exception as e:
            logger.error(f"Error reading leads locally: {str(e)}")
            return []
    
    def _delete_lead_local(self, lead_id):
        """Fallback: Delete lead from local JSON file"""
        import json
        try:
            leads_file = 'leads.json'
            if os.path.exists(leads_file):
                with open(leads_file, 'r') as f:
                    leads = json.load(f)
                
                leads = [l for l in leads if str(l.get('id')) != str(lead_id)]
                
                with open(leads_file, 'w') as f:
                    json.dump(leads, f, indent=2)
                
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error deleting lead locally: {str(e)}")
            return False
    
    def _delete_leads_bulk_local(self, lead_ids):
        """Fallback: Delete multiple leads from local JSON file"""
        import json
        try:
            leads_file = 'leads.json'
            if os.path.exists(leads_file):
                with open(leads_file, 'r') as f:
                    leads = json.load(f)
                
                initial_count = len(leads)
                leads = [l for l in leads if str(l.get('id')) not in [str(lid) for lid in lead_ids]]
                
                with open(leads_file, 'w') as f:
                    json.dump(leads, f, indent=2)
                
                return initial_count - len(leads)
            return 0
            
        except Exception as e:
            logger.error(f"Error bulk deleting leads locally: {str(e)}")
            return 0

# Global database instance
db = Database()
