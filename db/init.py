from pymongo import MongoClient
from config.config import MONGODB_URI

# Global variables for MongoDB connection and collections
client = None
db = None
users_collection = None
expenses_collection = None
queries_collection = None

def init_db():
    global client, db, users_collection, expenses_collection, queries_collection

    print("🔄 Attempting to connect to MongoDB...")

    try:
        # Connect to MongoDB
        client = MongoClient(MONGODB_URI)
        db = client["Cluster0"]  

        # Define collections
        users_collection = db["users"]
        expenses_collection = db["expenses"]
        queries_collection = db["queries"]

        # Verify connection
        print("✅ Successfully connected to MongoDB!")

        # Insert test data to create collections if they don’t exist
        # users_collection.insert_one({"test": "user_created"})
        # expenses_collection.insert_one({"test": "expense_created"})
        # queries_collection.insert_one({"test": "query_created"})

        # print("📌 Inserted test documents to force collection creation.") 

        # Check existing collections
        collections = db.list_collection_names()
        print(f"📁 Available collections in 'Cluster0' database: {collections}")

    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")

