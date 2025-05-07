from fastapi import FastAPI, HTTPException
from database import collection
from models import Message
from init_db import init_data
from bson import ObjectId
from datetime import datetime
import redis
import json

r = redis.Redis(host="redis", port=6379, decode_responses=True)

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_data()

@app.post("/messages")
def create_message(msg: Message):
    msg_dict = msg.dict()
    msg_dict["timestamp"] = datetime.utcnow()
    result = collection.insert_one(msg_dict)

    # Инвалидируем кэш по получателю и отправителю
    r.delete(f"sender:{msg.sender}")
    r.delete(f"receiver:{msg.receiver}")

    return {"id": str(result.inserted_id)}

@app.get("/messages/sender/{sender}")
def get_by_sender(sender: str):
    key = f"sender:{sender}"
    cached = r.get(key)
    if cached:
        return json.loads(cached)

    messages = list(collection.find({"sender": sender}, {"_id": 0}))
    r.set(key, json.dumps(messages), ex=60)
    return messages

@app.get("/messages/receiver/{receiver}")
def get_by_receiver(receiver: str):
    key = f"receiver:{receiver}"
    cached = r.get(key)
    if cached:
        return json.loads(cached)

    messages = list(collection.find({"receiver": receiver}, {"_id": 0}))
    r.set(key, json.dumps(messages), ex=60)
    return messages
