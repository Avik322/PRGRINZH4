from database import collection
from datetime import datetime

def init_data():
    if collection.count_documents({}) == 0:
        collection.insert_many([
            {"sender": "alice", "receiver": "bob", "content": "Hello Bob!", "timestamp": datetime.utcnow()},
            {"sender": "bob", "receiver": "alice", "content": "Hi Alice!", "timestamp": datetime.utcnow()},
        ])
