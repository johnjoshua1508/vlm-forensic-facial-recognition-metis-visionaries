from pymongo import MongoClient
from config import Config

class MongoDB:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client.get_database()
        
        # Initialize collections
        self.subjects = self.db.subjects
        self.users = self.db.users
        self.settings = self.db.settings
        
        # Create indexes
        self._create_indexes()
        
    def _create_indexes(self):
        # Create unique index on subject ID
        self.subjects.create_index("subject_id", unique=True)
        
        # Create unique index on username
        self.users.create_index("username", unique=True)
    
    def close(self):
        self.client.close()

# Create a singleton instance
db = MongoDB()

