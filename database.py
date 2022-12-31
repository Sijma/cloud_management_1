import config
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["cm_db"]

# Create the keyword collections, returns existing object instead of error if they already exist
for keyword in config.keywords:
    db.create_collection(keyword)

