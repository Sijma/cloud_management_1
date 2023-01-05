import config
import time
import pymongo
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["cm_db"]

# Check if the collection exists, and create it if it doesn't
for col in config.collections:
    if col not in db.list_collection_names():
        db.create_collection(col)


def add_to_database(topic, message):
    # Get the collection
    collection = db[topic]

    # Deserialize the message
    message_dict = json.loads(message)

    # Insert the message into the collection
    collection.update_one(message_dict, {"$setOnInsert": {}}, upsert=True)


def are_keywords_valid(keywords):
    for keyword in keywords:
        if keyword not in config.keywords:
            return False, f"Error: {keyword} is not a valid keyword"
    return True, ""


def register_user(data):
    # Check if the required keys are present in the JSON payload
    if "name" in data and "email" in data and "keywords" in data and "city" in data:
        valid, message = are_keywords_valid(data["keywords"])
        if not valid:
            return message

        users_collection = db["users"]
        user = users_collection.find_one({"email": data["email"]})

        # If the user does not exist, insert the new user document
        if not user:
            timestamp = int(time.time())
            data["timestamp"] = timestamp
            users_collection.insert_one(data)
            return "Operation Successful"
        else:
            return "Error: user with that email address already exists"
    else:
        return "Error: missing required keys"


def fetch_articles(email):
    # Find the user document in the collection with the matching email address
    users_collection = db["users"]
    user = users_collection.find_one({"email": email})

    # If the user exists, get the keywords array and use it to find all the documents in the corresponding collections
    if user:
        articles_by_source = {}
        for keyword in user["keywords"]:
            collection = db[keyword]
            docs = collection.find({}, {"_id": 0})
            for doc in docs:
                source_name = doc["source"]["name"]
                if source_name not in articles_by_source:
                    articles_by_source[source_name] = {"articles": []}
                articles_by_source[source_name]["articles"].append(doc)

        # For each source name, look up the description in the "sources_domain_name" collection and add it to the group
        sources_collection = db["sources_domain_name"]
        for source_name in articles_by_source:
            source_doc = sources_collection.find_one({"domain_name": source_name})
            if source_doc:
                description = source_doc["description"]
                articles_by_source[source_name]["Source Description"] = description

        return{"articles": articles_by_source}
    else:
        return "Error: user not found"


def update_keywords(data):
    if "email" in data and "keywords" in data:
        new_keywords = data["keywords"]
        valid, message = are_keywords_valid(new_keywords)
        if not valid:
            return message

        email = data["email"]
        users_collection = db["users"]

        # Update the user document with the new keywords
        result = users_collection.update_one(
            {"email": email},
            {"$set": {"keywords": new_keywords}}
        )

        # Check if the update was successful
        if result.modified_count == 1:
            # Return a success message
            return "Keywords updated successfully"

    # Return an error message
    return "Error: Failed to update keywords", 400


def delete_user(email):
    users_collection = db["users"]

    # Delete the user document with the given email
    result = users_collection.delete_one({"email": email})

    # Check if delete was successful
    if result.deleted_count == 1:
        # Return a success message
        return "User deleted successfully"
    else:
        # Return an error message
        return "Failed to delete user"
