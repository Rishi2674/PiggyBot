import time
from google import genai
from config.config import GEMINI_API_KEY_1,GEMINI_API_KEY_2,GEMINI_API_KEY_3  # List of API keys

API_KEYS = [GEMINI_API_KEY_1,GEMINI_API_KEY_2,GEMINI_API_KEY_3]  # List of multiple API keys
KEY_INDEX = 0  # Start with the first API key

# Track API call timestamps
api_call_timestamps = []

def classify_message(user_text):
    """Classifies a user message into 'Expense', 'Query', or 'Other'."""
    
    
    global KEY_INDEX, api_call_timestamps

    print("🔍 Classifying message...")

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
            You are an intelligent assistant for an expense tracker bot. 
            Classify the given message into one of the following categories:
            - 'Expense' if the message describes an expense (e.g., "I spent Rs.10 on coffee").
            - 'Query' if the message asks about expenses (e.g., "How much did I spend this week?").
            - 'Other' in the following cases:
                1. If the message is strictly not related to expenses or queries.
                2. If the user asks to store or retrieve expenses with negative values.
                3. If the user queries something that is not possible (e.g., "How much did I spend tomorrow?").

            Message: "{user_text}"

            Respond ONLY with 'Expense', 'Query', or 'Other'. NO explanations, NO extra text.
            """

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                )

            if response.text:
                api_call_timestamps.append(time.time())  # Log request time
                classification = response.text.strip().split("\n")[0]
                print("✅ Classification output:", classification)
                return classification  

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
message = "How much was the cost of today?"
category = classify_message(message)
print(f"📌 Message category: {category}")
