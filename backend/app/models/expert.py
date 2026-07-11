from datetime import datetime

from pymongo import MongoClient

from ..config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()
experts_col = db["experts"]
bookings_col = db["bookings"]


def seed_experts():
    if experts_col.count_documents({}) == 0:
        sample_experts = [
            {
                "name": "Adv. Priya Sharma",
                "specialization": "Criminal Law",
                "experience": 12,
                "rating": 4.8,
                "fee": 1500,
                "available": True,
                "bio": "Expert in IPC, CrPC and criminal defense with 12 years experience.",
                "avatar": "PS",
            },
            {
                "name": "Adv. Rajesh Kumar",
                "specialization": "Civil Law",
                "experience": 8,
                "rating": 4.6,
                "fee": 1200,
                "available": True,
                "bio": "Property disputes, contracts, and civil litigation specialist.",
                "avatar": "RK",
            },
            {
                "name": "Adv. Meera Iyer",
                "specialization": "Constitutional Law",
                "experience": 15,
                "rating": 4.9,
                "fee": 2000,
                "available": True,
                "bio": "PIL expert, fundamental rights cases and constitutional challenges.",
                "avatar": "MI",
            },
            {
                "name": "Adv. Arjun Patel",
                "specialization": "Family Law",
                "experience": 10,
                "rating": 4.7,
                "fee": 1000,
                "available": False,
                "bio": "Divorce, custody, maintenance and matrimonial disputes.",
                "avatar": "AP",
            },
            {
                "name": "Adv. Sunita Reddy",
                "specialization": "Labour Law",
                "experience": 7,
                "rating": 4.5,
                "fee": 900,
                "available": True,
                "bio": "Employment disputes, wrongful termination, POSH act compliance.",
                "avatar": "SR",
            },
            {
                "name": "Adv. Vikram Singh",
                "specialization": "Corporate Law",
                "experience": 11,
                "rating": 4.8,
                "fee": 2500,
                "available": True,
                "bio": "Company law, M&A, compliance and commercial contracts.",
                "avatar": "VS",
            },
        ]
        experts_col.insert_many(sample_experts)


def get_all_experts(domain=None):
    query = {}
    if domain:
        query["specialization"] = {"$regex": domain, "$options": "i"}
    experts = list(experts_col.find(query))
    for expert in experts:
        expert["_id"] = str(expert["_id"])
    return experts


def book_expert(user_id, expert_id, date, time_slot, query_summary):
    booking = {
        "user_id": user_id,
        "expert_id": expert_id,
        "date": date,
        "time_slot": time_slot,
        "query_summary": query_summary,
        "status": "pending",
        "created_at": datetime.utcnow(),
    }
    result = bookings_col.insert_one(booking)
    return str(result.inserted_id)
