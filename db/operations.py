import json
from db.init import expenses_collection,users_collection
from db.schemas import UserSchema
import re
from db.init import db

def store_expense(expense_data):
    """Inserts the extracted expense data into the MongoDB expenses collection."""
    
    # ✅ Convert JSON string to dictionary if necessary
    cleaned_text = re.sub(r"```json|```", "", expense_data).strip()
    cleaned_text = cleaned_text.replace("\n","")
    cleaned_text = cleaned_text.lstrip()
    print("cleaned_text:",cleaned_text)
    if isinstance(cleaned_text, str):  
        try:
            expense_data = json.loads(cleaned_text)  
        except json.JSONDecodeError as e:
            print(f"❌ ERROR: Failed to decode JSON string: {e}")
            return {"error": "Invalid JSON format"}

    # print(f"📌 Type after conversion: {type(expense_data)}")  # Should be <class 'dict'>

    if not isinstance(expense_data, dict):
        return {"error": "Expense data must be a dictionary"}

    if expenses_collection is None:
        print("❌ ERROR: expenses_collection is None! Check MongoDB connection.")
        return {"error": "Database not initialized"}

    try:
        # print("in try")
        expense_data["category"] = (expense_data["category"].lower() if expense_data["category"] is not None else "miscellaneous")

        # expense_data["subcategory"] = (expense_data["subcategory"].lower() if expense_data["subcategory"] is not None else "miscellaneous")
        expense_data["description"] = (expense_data["description"].lower() if expense_data["description"] is not None else "miscellaneous")

        result =  expenses_collection.insert_one(expense_data)
        # print("result:",result)
        expense_data["_id"] = str(result.inserted_id)
        print("Data stored successfully")
        return {"message": "Expense recorded successfully", "data": expense_data}
    except Exception as e:
        print(f"❌ Database insertion failed: {str(e)}")
        return {"error": f"Database insertion failed: {str(e)}"}

  

def execute_mongo_query(user_id: str, mongo_query: dict):
    """
    Executes a MongoDB query for the given user_id and prints the output.
    
    Args:
        user_id (str): The user's ID to ensure query is user-specific.
        mongo_query (dict): The generated MongoDB query.
    
    Returns:
        list: List of matching expense records.
    """
    try:
        # Ensure the query includes the user_id for filtering
        mongo_query["user_id"] = user_id

        # Query the database
        results = list(expenses_collection.find(mongo_query, {"_id": 0}))  # Exclude MongoDB's internal _id field

        if results:
            print("Query Results:", results)
        else:
            print("No matching records found.")
        
        return results
    except Exception as e:
        print("Error executing MongoDB query:", e)
        return []


def get_or_create_user(user_id: str, name = "User"):
    """Checks if a user exists; if not, creates a new user entry."""
    
    user = users_collection.find_one({"user_id": user_id})
    
    if user:
        print(f"✅ User {user_id} exists.")
        return user  # Return existing user
    
    # Create a new user entry
    new_user = UserSchema(user_id=user_id, name=name).model_dump()
    users_collection.insert_one(new_user)
    print(f"🆕 New user {user_id} added to the database.")
    
    return new_user  # Return newly inserted user

# def test():
#     print("🔍 Fetching all expenses for user 919428305030...")
#     all_expenses = list(expenses_collection.find({"user_id": "919428305030"}))
#     for expense in all_expenses:
#         print(expense)

#     query = {"user_id": "919428305030", "category": "food", "subcategory": "chocolate"}
#     results = list(expenses_collection.find(query))
#     print("🔍 Query Results:", results)

# test()

# user = get_or_create_user("929428305030","Rishi Upadhyay")