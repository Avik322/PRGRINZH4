"""
Message Command API (CQRS)
Producer: receives HTTP commands and publishes a JSON event to Kafka.
Cache: invalidates Redis keys so that read model stays fresh.
"""

from datetime import datetime
import json
import os

from fastapi import FastAPI, HTTPException
import redis
from confluent_kafka import Producer

# ---------- Redis -------------
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True,
)

# ---------- Kafka -------------
producer = Producer(
    {"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")}
)
TOPIC = "messages"

# ---------- FastAPI -----------
app = FastAPI(title="Message Command API (ASCII only)")

# ---------- Pydantic model ----
from pydantic import BaseModel


class Message(BaseModel):
    sender: str
    receiver: str
    text: str


# ---------- Endpoints ---------
@app.post("/messages", status_code=202)
def create_message(msg: Message):
    """Publish a message event to Kafka and invalidate cache."""
    payload = msg.dict()
    payload["timestamp"] = datetime.utcnow().isoformat()

    try:
        producer.produce(TOPIC, json.dumps(payload).encode())
        producer.flush()
    except BufferError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    # invalidate cache keys
    redis_client.delete(f"sender:{msg.sender}")
    redis_client.delete(f"receiver:{msg.receiver}")

    return {"status": "queued"}


@app.get("/messages/sender/{sender}")
def get_by_sender(sender: str):
    key = f"sender:{sender}"
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)

    # Lazy import to avoid Mongo requirement when only posting
    from database import collection

    messages = list(collection.find({"sender": sender}, {"_id": 0}))
    redis_client.set(key, json.dumps(messages), ex=60)
    return messages


@app.get("/messages/receiver/{receiver}")
def get_by_receiver(receiver: str):
    key = f"receiver:{receiver}"
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)

    from database import collection

    messages = list(collection.find({"receiver": receiver}, {"_id": 0}))
    redis_client.set(key, json.dumps(messages), ex=60)
    return messages
