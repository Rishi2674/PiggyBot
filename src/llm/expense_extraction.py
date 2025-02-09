import requests
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"

def extract_expense_details(user_text, user_id):
    prompt = f"""
    You are an intelligent assistant for an expense tracker bot. Extract structured expense details from the given message.
    
    The response should be a JSON object matching this schema:
    {{
        "user_id": "{user_id}",
        "category": "string",  # Category (Food, Travel, Shopping, etc.)
        "subcategory": "string or null",  # Subcategory (Coffee, Uber, Groceries, etc.)
        "description": "string or null",  # Short description of the expense
        "amount": float,  # Expense amount
        "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}",  # Date of expense in ISO format
    }}

    Ensure that:
    - "amount" is extracted as a number (e.g., ₹500 → 500).
    - "category" is one of Food, Travel, Shopping, Groceries, etc.
    - If "subcategory" or "description" cannot be extracted, return null.
    - Date defaults to the current timestamp if not explicitly mentioned.

    Example messages and expected JSON:
    
    Message: "Had a filter coffee at a local café, cost ₹50."
    Output: {{"user_id": "{user_id}", "category": "Food", "subcategory": "Coffee", "description": "Filter coffee at a café", "amount": 50, "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}"}}

    Message: "Booked a train ticket for my trip, cost ₹1200."
    Output: {{"user_id": "{user_id}", "category": "Travel", "subcategory": "Train", "description": "Train ticket", "amount": 1200, "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}"}}
    
    Message: "Bought a cold coffee from CCD for ₹180."
    Output: {{"user_id": "{user_id}", "category": "Food", "subcategory": "Coffee", "description": "Cold Coffee from CCD", "amount": 180, "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}"}}
    
    Message: "Bought snacks from Blinkit for ₹300 yesterday."
    Output: {{"user_id": "{user_id}", "category": "Food", "subcategory": "Snacks", "description": "Snacks from Blinkit", "amount": 300, "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}"}}
    
    Message: "Took an Ola to work, cost ₹250."
    Output: {{"user_id": "{user_id}", "category": "Travel", "subcategory": "Cab", "description": "Ola ride to work", "amount": 250, "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}"}}

    Message: "{user_text}"
    Output:
    """

    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response_json = response.json()
        extracted_data = response_json.get("response", "{}").strip()
        print("Extracted Expense Data:", extracted_data)
        print("---------------Done------------------")
        return extracted_data

    except Exception as e:
        print("Error communicating with Ollama:", str(e))
        return "{}"

