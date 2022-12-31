import config
import pymongo

keywords = ["current", "breaking", "world", "political", "business", "sports", "entertainment", "technology"]

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["cm_db"]

# Create the keyword collections, returns existing object instead of error if they already exist
for keyword in keywords:
    db.create_collection(keyword)

