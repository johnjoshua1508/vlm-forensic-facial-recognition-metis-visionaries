from database import db
from bson import ObjectId
import datetime
import bcrypt
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username, password=None, role="user", _id=None):
        self._id = _id
        self.username = username
        self.password = password
        self.role = role
        self.created_at = datetime.datetime.now()
        self.last_login = None

    def get_id(self):
        return str(self._id)

    @property
    def is_active(self):
        return True
    
    def save(self):
        user_data = {
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at,
            "last_login": self.last_login
        }
        
        if self.password:
            # Hash the password before saving
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), salt)
            user_data["password"] = hashed_password
        
        if self._id:
            result = db.users.update_one(
                {"_id": self._id},
                {"$set": user_data}
            )
            return result.modified_count
        else:
            result = db.users.insert_one(user_data)
            self._id = result.inserted_id
            return self._id
    
    @classmethod
    def find_by_username(cls, username):
        user_data = db.users.find_one({"username": username})
        if not user_data:
            return None
        
        user = cls(
            username=user_data["username"],
            role=user_data["role"],
            _id=user_data["_id"]
        )
        user.password = user_data.get("password")
        user.created_at = user_data.get("created_at")
        user.last_login = user_data.get("last_login")
        
        return user
    
    @classmethod
    def find_by_id(cls, user_id):
        user_data = db.users.find_one({"_id": ObjectId(user_id)})
        if not user_data:
            return None
        
        user = cls(
            username=user_data["username"],
            role=user_data["role"],
            _id=user_data["_id"]
        )
        user.password = user_data.get("password")
        user.created_at = user_data.get("created_at")
        user.last_login = user_data.get("last_login")
        
        return user
    
    def check_password(self, password):
        if not self.password:
            return False
        
        return bcrypt.checkpw(password.encode('utf-8'), self.password)
    
    def update_last_login(self):
        self.last_login = datetime.datetime.now()
        db.users.update_one(
            {"_id": self._id},
            {"$set": {"last_login": self.last_login}}
        )

