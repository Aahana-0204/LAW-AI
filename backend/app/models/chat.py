from datetime import datetime

from pymongo import MongoClient

from ..config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()
chats_col = db["chats"]


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
    chats_col.insert_one(msg)


def get_chat_history(user_id, session_id, limit=20):
    msgs = chats_col.find(
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
    return list(chats_col.aggregate(pipeline))
