from extensions import mongo
from datetime import datetime


def log_activity(action, data):
    mongo.db.logs.insert_one({
        "action": action,
        "data": data,
        "timestamp": datetime.utcnow()
    })