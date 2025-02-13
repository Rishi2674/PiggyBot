import time
from openai import OpenAI
from config.config import OPENAI_API_KEY  # Import your single OpenAI API key

# Set OpenAI API ke 

# Track API call timestamps
api_call_timestamps = []


def classify_message(user_text):
    """Classifies a user message into 'Expense', 'Query', or 'Other' using OpenAI's API."""

    global api_call_timestamps

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
        try:
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

            client = OpenAI(
                api_key = OPENAI_API_KEY
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}],
                )

            if response and hasattr(response,'choices') and len(response.choices) > 0:
                print("in response")
                api_call_timestamps.append(time.time())  # Log request time
                classification = response.choices[0].message.content.strip()
                classification = classification.split("\n")[0]                

                if classification not in ["Expense", "Query", "Other"]:
                    print("⚠️ Unexpected response, defaulting to 'Other'.")
                    return "Other"

                print("✅ Classification output:", classification)
                return classification

        except OpenAI.error.RateLimitError:
            print("⚠️ Rate limit hit. Waiting before retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:
            print(f"❌ Error: {e}")
            return "Other"

    print("❌ Max retries reached. Returning 'Other'.")
    return "Other"


# Example Usage
message = "How much was the cost of today?"
category = classify_message(message)
print(f"📌 Message category: {category}")
