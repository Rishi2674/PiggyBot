import json
from db.init import expenses_collection
import re# Ensure expenses_collection is imported

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
        result =  expenses_collection.insert_one(expense_data)
        # print("result:",result)
        expense_data["_id"] = str(result.inserted_id)
        return {"message": "Expense recorded successfully", "data": expense_data}
    except Exception as e:
        print(f"❌ Database insertion failed: {str(e)}")
        return {"error": f"Database insertion failed: {str(e)}"}
