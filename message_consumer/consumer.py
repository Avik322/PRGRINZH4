# -*- coding: utf-8 -*-
import os
import json
import time
import signal
import sys
import logging
import redis
from pymongo import MongoClient
from confluent_kafka import Consumer, KafkaError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

# ---------- окружение ----------
BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
GROUP_ID  = os.getenv("KAFKA_GROUP_ID", "msg-consumer")
TOPIC     = "messages"

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
client    = MongoClient(MONGO_URI)
collection = client.messages_db.messages

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True,
)

conf = {
    "bootstrap.servers": BOOTSTRAP,
    "group.id": GROUP_ID,
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
}

consumer = Consumer(conf)
consumer.subscribe([TOPIC])

def shutdown(*_):
    logging.info("Stopping consumer...")
    consumer.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

logging.info("Message Consumer started")
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() != KafkaError._PARTITION_EOF:
            logging.error(msg.error())
        continue

    try:
        payload = json.loads(msg.value().decode())
        collection.insert_one(payload)

        # сброс кешей, св€занных с участниками
        r.delete(f"sender:{payload['sender']}")
        r.delete(f"receiver:{payload['receiver']}")

        consumer.commit(msg)
        logging.info(
            "Stored message from '%s' to '%s'",
            payload["sender"],
            payload["receiver"],
        )
    except Exception as exc:
        logging.exception("Failed to consume: %s", exc)
