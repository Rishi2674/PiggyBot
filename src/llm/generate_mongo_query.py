import time
from google import genai
from config.config import GEMINI_API_KEY_1,GEMINI_API_KEY_2,GEMINI_API_KEY_3
from datetime import datetime
import re
# List of API keys

API_KEYS = [GEMINI_API_KEY_1,GEMINI_API_KEY_2,GEMINI_API_KEY_3]  # List of multiple API keys
KEY_INDEX = 0  # Start with the first API key

# Track API call timestamps
api_call_timestamps = []

def generate_mongo_query(user_query: str, user_id: str) -> dict:
    """
    Uses Gemini API to convert a natural language user query into a MongoDB query.
    Adds the current datetime for handling time-based queries and ensures the query 
    is scoped to the given user_id.
    """

    current_time = datetime.utcnow().isoformat()  # Get current UTC time in ISO format
    schema_example = {
        "user_id": user_id,
        "category": "string",
        "subcategory": "string",
        "description": "string",
        "amount": "float",
        "date": "datetime (ISO 8601 format)"
    }

    
    
    global KEY_INDEX, api_call_timestamps

    print("🔍 Generating mongo query...")

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
                Convert the following user query into a valid MongoDB query:
                "{user_query}"

                The query should be formatted as a Python dictionary and should filter results only for this user_id: "{user_id}".
                The category should be strictly one of the following:
                ["travel", "food and dining", "shopping", "entertainment", "Utilities and Bills", "Health", "Housing and Rent", "Education", "Investments and Savings", "Miscellaneous"]
                
                The MongoDB collection follows this schema:
                {schema_example}

                Use the current datetime for time-based queries: {current_time}.
                Ensure the query is valid and uses MongoDB operators like $gte, $lte for date filtering if needed.
                No need to give any explanation or import any libraries, just give the MongoDB query.
                """

            prompt2 = "Hey! How was your day today"
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                )

            if response.text:
                api_call_timestamps.append(time.time())  # Log request time
                cleaned_text = re.sub(r"```python|```", "", response.text).strip()
                cleaned_text = cleaned_text.replace("\n","")
                cleaned_text = cleaned_text.lstrip()  
                mongo_query = eval(cleaned_text)  # Convert response string into a dictionary
                return mongo_query

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
# message = "How much was the cost on travel of today?"
# mq = generate_mongo_query(message,user_id="1234")
# print(f"📌 Mongo query: {mq}")
