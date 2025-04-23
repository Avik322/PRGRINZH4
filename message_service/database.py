from pymongo import MongoClient, ASCENDING
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
client = MongoClient(MONGO_URI)
db = client["messages_db"]
collection = db["messages"]

# индексы
collection.create_index([("sender", ASCENDING)])
collection.create_index([("receiver", ASCENDING)])
