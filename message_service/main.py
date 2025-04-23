from fastapi import FastAPI, HTTPException
from database import collection
from models import Message
from init_db import init_data
from bson import ObjectId
from datetime import datetime

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_data()

@app.post("/messages")
def create_message(msg: Message):
    msg_dict = msg.dict()
    msg_dict["timestamp"] = datetime.utcnow()
    result = collection.insert_one(msg_dict)
    return {"id": str(result.inserted_id)}

@app.get("/messages/sender/{sender}")
def get_by_sender(sender: str):
    return list(collection.find({"sender": sender}, {"_id": 0}))

@app.get("/messages/receiver/{receiver}")
def get_by_receiver(receiver: str):
    return list(collection.find({"receiver": receiver}, {"_id": 0}))
