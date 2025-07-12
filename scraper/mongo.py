from pymongo import MongoClient
import os

def get_mongo_client():
    try:
        mongo_client = MongoClient(os.getenv("MONGO_URI", "mongodb://root:123456@mongo:27017/"))
        return mongo_client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
    
def get_mongo_db(db_name: str):
    client = get_mongo_client()
    if client:
        try:
            db = client[db_name]
            return db
        except Exception as e:
            print(f"Error accessing database {db_name}: {e}")
            return None
        
def get_mongo_collection(db_name: str, collection_name: str):
    db = get_mongo_db(db_name)
    try:
        collection = db[collection_name]
        return collection
    except Exception as e:
        print(f"Error accessing collection {collection_name} in database {db_name}: {e}")
        return None

def add_record_to_collection(db_name: str, collection_name: str, record: dict):
    collection = get_mongo_collection(db_name, collection_name)
    if collection is None:
        print(f"Collection {collection_name} not found in database {db_name}.")
        return False
    try:
        result = collection.insert_one(record)
        print(f"Article added with id: {result.inserted_id}")
        return True
    except Exception as e:
        print(f"Error adding article to collection {collection_name}: {e}")
        return False
        
def close_mongo_client(client: MongoClient):
    if client:
        try:
            client.close()
            print("MongoDB client closed.")
        except Exception as e:
            print(f"Error closing MongoDB client: {e}")

