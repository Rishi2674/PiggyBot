from db.init import db  # Import MongoDB client

def store_expense(expense_data):
    """Inserts the extracted expense data into the MongoDB expenses collection."""
    if not expense_data:
        return {"error": "Invalid expense data"}
    
    try:
        db.expenses_collection.insert_one(expense_data)
        return {"message": "Expense recorded successfully", "data": expense_data}
    except Exception as e:
        return {"error": f"Database insertion failed: {str(e)}"}

