import requests
from datetime import datetime
from google import genai
from config.config import GEMINI_API_KEY_2
# OLLAMA_URL = "http://localhost:11434/api/generate"

def extract_expense_details(user_text, user_id):
    print("in extract_expense_details")
    client = genai.Client(api_key=GEMINI_API_KEY_2)
    prompt = f"""
    You are an intelligent assistant for an expense tracker bot. Extract structured expense details from the given message.
    
    The response should be a JSON object matching this schema:
    {{
        "user_id": "{user_id}",
        "category": "string",  # Category
        "subcategory": "string or null",  # Subcategory (Coffee, Uber, Groceries, etc.)
        "description": "string or null",  # Short description of the expense
        "amount": float,  # Expense amount
        "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}",  # Date of expense in ISO format
    }}

    Ensure that:
    - "amount" is extracted as a number (e.g., ₹500 → 500).
    - "category" is  strictly one of the given list : ["travel", "food and dining", "shopping", "entertainment", "Utilities and Bills", "Health", "Housing and Rent", "Education", "Investments and Savings", "Miscellaneous"]
    - If "subcategory" or "description" cannot be extracted, return null.
    - Date defaults to the current timestamp if not explicitly mentioned.
    - This is the user id: {user_id}
    
    

    Example messages and expected JSON:
    
    Message: "Had a filter coffee at a local café, cost ₹50."
    Output: {{"user_id": "{user_id}", "category": "Food and Dining", "subcategory": "Coffee", "description": "Filter coffee at a café", "amount": 50, "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}"}}

    Message: "Booked a train ticket for my trip, cost ₹1200."
    Output: {{"user_id": "{user_id}", "category": "Travel", "subcategory": "Train", "description": "Train ticket", "amount": 1200, "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}"}}
    
    Message: "Bought a cold coffee from CCD for ₹180."
    Output: {{"user_id": "{user_id}", "category": "Food and Dining", "subcategory": "Coffee", "description": "Cold Coffee from CCD", "amount": 180, "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}"}}
    
    Message: "Bought snacks from Blinkit for ₹300 yesterday."
    Output: {{"user_id": "{user_id}", "category": "Food and Dining", "subcategory": "Snacks", "description": "Snacks from Blinkit", "amount": 300, "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}"}}
    
    Message: "Took an Ola to work, cost ₹250."
    Output: {{"user_id": "{user_id}", "category": "Travel", "subcategory": "Cab", "description": "Ola ride to work", "amount": 250, "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}"}}

    Message: "{user_text}"
    Output:
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        )
    print(response.text)
    return response.text

    # payload = {
    #     "model": "phi3",
    #     "prompt": prompt,
    #     "stream": False
    # }

    # try:
    #     response = requests.post(OLLAMA_URL, json=payload)
    #     response_json = response.json()
    #     extracted_data = response_json.get("response", "{}").strip()
    #     print("Extracted Expense Data:", extracted_data)
    #     print("---------------Done------------------")
    #     return extracted_data

    # except Exception as e:
    #     print("Error communicating with Ollama:", str(e))
    #     return "{}"


# data = extract_expense_details("Paid 200rs","919428305030")