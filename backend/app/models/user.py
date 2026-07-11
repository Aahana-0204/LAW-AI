from datetime import datetime

import bcrypt
from pymongo import MongoClient

from ..config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()
users_col = db["users"]


def create_user(name, email, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = {
        "name": name,
        "email": email,
        "password": hashed,
        "created_at": datetime.utcnow(),
        "plan": "free",
    }
    result = users_col.insert_one(user)
    return str(result.inserted_id)


def find_user_by_email(email):
    return users_col.find_one({"email": email})


def verify_password(plain, hashed):
    return bcrypt.checkpw(plain.encode(), hashed.encode())
