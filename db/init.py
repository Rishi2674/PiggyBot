from pymongo import MongoClient
from config.config import MONGODB_URI

# Load MongoDB URI from environment variables


print("🔄 Attempting to connect to MongoDB...")

try:
    # Connect to MongoDB
    client = MongoClient(MONGODB_URI)
    db = client["Cluster0"] 

    # Verify connection
    print("✅ Successfully connected to MongoDB!")

    # Check available databases
    databases = client.list_database_names()
    print(f"📂 Available databases: {databases}")

    # Define collections
    users_collection = db["users"]
    expenses_collection = db["expenses"]
    queries_collection = db["queries"]

    users_collection.insert_one({"test": "user_created"})
    expenses_collection.insert_one({"test": "expense_created"})
    queries_collection.insert_one({"test": "query_created"})

    print("Inserted test documents to force collection creation.") 
    # Check existing collections
    collections = db.list_collection_names()
    print(f"📁 Available collections in 'piggybot' database: {collections}")

except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")
