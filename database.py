import config
import pymongo
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["cm_db"]

# Check if the collection exists, and create it if it doesn't
for keyword in config.keywords:
    if keyword not in db.list_collection_names():
        db.create_collection(keyword)


def add_to_database(topic, message):
    # Get the collection
    collection = db[topic]

    # Deserialize the message
    message_dict = json.loads(message)

    # Insert the message into the collection
    collection.update_one(message_dict, {"$setOnInsert": {"key": "value"}}, upsert=True)
