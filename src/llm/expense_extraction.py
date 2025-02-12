import time
from google import genai
from datetime import datetime
from config.config import GEMINI_API_KEY_1,GEMINI_API_KEY_2,GEMINI_API_KEY_3  # List of API keys

API_KEYS = [GEMINI_API_KEY_1,GEMINI_API_KEY_2,GEMINI_API_KEY_3]  # List of multiple API keys
KEY_INDEX = 0  # Start with the first API key

# Track API call timestamps
api_call_timestamps = []

def extract_expense_details(user_text, user_id):
    """Classifies a user message into 'Expense', 'Query', or 'Other'."""
    
    
    global KEY_INDEX, api_call_timestamps

    print("🔍 extracting expense Details...")

    # Clean up old timestamps (keep only requests in the last 60 sec)
    current_time = time.time()
    api_call_timestamps = [t for t in api_call_timestamps if current_time - t < 60]

    # If we've hit the 10 requests/min limit, wait
    if len(api_call_timestamps) >= 10:
        wait_time = 60 - (current_time - api_call_timestamps[0])
        print(f"🚨 Rate limit exceeded! Waiting {int(wait_time)} seconds...")
        time.sleep(wait_time)

    retries = 3
    for attempt in range(retries):
        api_key = API_KEYS[KEY_INDEX]
        client = genai.Client(api_key = api_key)

        try:
            # client = genai.GenerativeModel("gemini-2.0-flash")
            
            prompt = f"""
                You are an intelligent assistant for an expense tracker bot. Extract structured expense details from the given message.
                
                The response should be a JSON object matching this schema:
                {{
                    "user_id": "{user_id}",
                    "category": "string",  # Category
                    "subcategory": "string or None",  # Subcategory (Coffee, Uber, Groceries, etc.)
                    "description": "string or None",  # Short description of the expense
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
                
            prompt2 = "Hi! How are you doing?"

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                )

            if response.text:
                api_call_timestamps.append(time.time())  # Log request time
                # classification = response.text.strip().split("\n")[0]
                print("✅ Extracted Details:", response.text)
                return response.text  

        except Exception as e:
            error_message = str(e)
            print(f"❌ Error: {error_message}")

            if "RESOURCE_EXHAUSTED" in error_message:
                print("⚠️ Rate limit hit. Switching API keys or waiting...")
                KEY_INDEX = (KEY_INDEX + 1) % len(API_KEYS)

                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print("❌ All API keys exhausted. Try again later.")
                    return "Other"
            else:
                return "Other"

    return "Other"

# Example Usage
# message = "Spend 200 on Rent!"
# data = extract_expense_details(message,"user123")
# print(f"📌 Message category: {category}")
