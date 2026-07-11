from datetime import datetime

import bcrypt
from pymongo import MongoClient

from ..config import Config

# Lazy connection — only connects on first use (fixes Vercel cold start timeout)
_client = None
_db = None


def _get_db():
    global _client, _db
    if _db is not None:
        return _db
    _client = MongoClient(
        Config.MONGO_URI,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
        socketTimeoutMS=15000,
        maxPoolSize=1,       # Serverless: keep pool small
        tls=True,
        tlsAllowInvalidCertificates=True,   # Bypass SSL cert check (Vercel ↔ Atlas)
        retryWrites=True,
    )
    # Extract database name from URI or default to "lawai"
    uri = Config.MONGO_URI or ""
    db_name = "lawai"
    if "/" in uri:
        part = uri.split("/")[-1].split("?")[0]
        if part:
            db_name = part
    _db = _client[db_name]
    return _db


def _users():
    return _get_db()["users"]


def create_user(name, email, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=10)).decode()
    user = {
        "name": name,
        "email": email,
        "password": hashed,
        "created_at": datetime.utcnow(),
        "plan": "free",
    }
    result = _users().insert_one(user)
    return str(result.inserted_id)


def find_user_by_email(email):
    return _users().find_one({"email": email})


def verify_password(plain, hashed):
    return bcrypt.checkpw(plain.encode(), hashed.encode())
