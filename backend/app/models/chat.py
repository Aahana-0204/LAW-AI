from datetime import datetime

from pymongo import MongoClient

from ..config import Config

_client = None
_db = None


def _get_db():
    global _client, _db
    if _db is not None:
        return _db
    _client = MongoClient(
        Config.MONGO_URI,
        serverSelectionTimeoutMS=8000,
        connectTimeoutMS=8000,
        socketTimeoutMS=8000,
        maxPoolSize=1,
    )
    uri = Config.MONGO_URI or ""
    db_name = "lawai"
    if "/" in uri:
        part = uri.split("/")[-1].split("?")[0]
        if part:
            db_name = part
    _db = _client[db_name]
    return _db


def _chats():
    return _get_db()["chats"]


def save_message(user_id, session_id, role, content, sources=None, domain=None):
    msg = {
        "user_id": user_id,
        "session_id": session_id,
        "role": role,
        "content": content,
        "sources": sources or [],
        "domain": domain,
        "timestamp": datetime.utcnow(),
    }
    _chats().insert_one(msg)


def get_chat_history(user_id, session_id, limit=20):
    msgs = _chats().find(
        {"user_id": user_id, "session_id": session_id},
        sort=[("timestamp", 1)],
    ).limit(limit)
    result = []
    for msg in msgs:
        msg["_id"] = str(msg["_id"])
        result.append(msg)
    return result


def get_sessions(user_id):
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$sort": {"timestamp": -1}},
        {
            "$group": {
                "_id": "$session_id",
                "last_msg": {"$first": "$content"},
                "domain": {"$first": "$domain"},
                "ts": {"$first": "$timestamp"},
            }
        },
        {"$sort": {"ts": -1}},
        {"$limit": 20},
    ]
    return list(_chats().aggregate(pipeline))
