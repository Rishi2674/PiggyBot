from pymongo import MongoClient
from config.config import MONGODB_URI

# Global variables
client = None
db = None
users_collection = None
expenses_collection = None
queries_collection = None

def init_db():
    global client, db, users_collection, expenses_collection, queries_collection

    print("🔄 Attempting to connect to MongoDB...")

    try:
        client = MongoClient(MONGODB_URI)
        db = client["Cluster0"]  

        # Debug: Check if database is correctly assigned
        if db is None:
            print("❌ Database not assigned!")
            return
        
        # Assign collections
        users_collection = db["users"]
        expenses_collection = db["expenses"]
        queries_collection = db["queries"]

        # Debugging logs
        # print(f"📌 db: {db}")
        # print(f"📌 users_collection: {users_collection}")
        # print(f"📌 expenses_collection: {expenses_collection}")
        # print(f"📌 queries_collection: {queries_collection}")

        if expenses_collection is None:
            print("❌ ERROR: expenses_collection was not assigned correctly!")

        print("✅ Successfully connected to MongoDB!")

        # Verify collections exist
        collections = db.list_collection_names()
        print(f"📁 Available collections: {collections}")

    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")

# ✅ Run function immediately when imported
init_db()
