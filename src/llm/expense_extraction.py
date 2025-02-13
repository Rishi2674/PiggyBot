import time
from openai import OpenAI
from datetime import datetime
from config.config import OPENAI_API_KEY  # Your OpenAI API Key

# Track API call timestamps for rate limiting
api_call_timestamps = []

def extract_expense_details(user_text, user_id):
    """Classifies a user message into structured expense details."""
    
    schema = {
        "user_id": user_id,
        "category": "string",  # Strictly one of the predefined categories
        "description": "string",  # Key details about the expense
        "amount": float,  # Extracted numerical value of expense
        "date": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')  # ISO format date
    }
    
    print("🔍 Extracting expense details...")
    
    # Clean up old timestamps (keep only requests in the last 60 sec)
    current_time = time.time()
    global api_call_timestamps
    api_call_timestamps = [t for t in api_call_timestamps if current_time - t < 60]

    # If we've hit the rate limit, wait
    if len(api_call_timestamps) >= 10:
        wait_time = 60 - (current_time - api_call_timestamps[0])
        print(f"🚨 Rate limit exceeded! Waiting {int(wait_time)} seconds...")
        time.sleep(wait_time)

    prompt = f"""
        You are an intelligent assistant for an expense tracker bot. Extract structured expense details from the given message.

        ### Expected JSON Schema:
        {schema}

        ### Constraints:
        - Extract the "amount" as a number (₹500 → 500).
        - "Category" must be one of: ["travel", "food and dining", "shopping", "entertainment", "Utilities and Bills", "Health", "Housing and Rent", "Education", "Investments and Savings", "Miscellaneous"].
        - "Description" should summarize key details (e.g., "Starbucks coffee", "Train ticket").
        - If the date is missing, default to the current timestamp.
        - Extract brand/store names if mentioned.
        - User ID: {user_id}

        ### Examples:

        1. **Input:** "Had a filter coffee at a local café, cost ₹50."
        **Output:** {{"user_id": "{user_id}", "category": "Food and Dining", "description": "Filter coffee at local café", "amount": 50, "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}"}}

        2. **Input:** "Took an Ola to work, cost ₹250."
        **Output:** {{"user_id": "{user_id}", "category": "Travel", "description": "Ola ride to work", "amount": 250, "date": "{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}"}}

        **Now process this message:**
        "{user_text}"
    """

    try:
        print("in try block")
        client = OpenAI(
            api_key = OPENAI_API_KEY
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            )
        print(response)
        print(response.choices)
        if response and hasattr(response,'choices') and len(response.choices) > 0:
            print("in response")
            api_call_timestamps.append(time.time())  # Log request time
            extracted_details = response.choices[0].message.content.strip()
            print("✅ Extracted Details:", extracted_details)
            return extracted_details

    except OpenAI.error.OpenAIError as e:
        print(f"❌ OpenAI API Error: {str(e)}")
        return "OpenAI error"
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return "Other"

    return "Hello"

# Example Usage
# message = "Spent 200 on Pani Puri!"
# data = extract_expense_details(message, "user123")
# print(f"📌 Message details: {data}")
