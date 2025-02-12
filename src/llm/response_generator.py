import time
from google import genai
from config.config import GEMINI_API_KEY_1,GEMINI_API_KEY_2,GEMINI_API_KEY_3  # List of API keys

API_KEYS = [GEMINI_API_KEY_1,GEMINI_API_KEY_2,GEMINI_API_KEY_3]  # List of multiple API keys
KEY_INDEX = 0  # Start with the first API key

# Track API call timestamps
api_call_timestamps = []

def generate_response(user_input, context="general",user_name="User"):
    """
    Sends user input to Gemini API and returns a response.
    
    Args:
        user_input (str): The user's message.
        context (str): The type of response needed ('general' or 'success').

    Returns:
        str: The response from the Gemini API.
    """

    
    
    global KEY_INDEX, api_call_timestamps

    print("🔍 Generating response...")

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
            prompt = ""
            if context == "general":
                prompt = f"""
                You are an intelligent assistant for an expense tracker bot called "PiggyBot" . 
                Generate a response for the given user input.
                Answer as if you are PiggyBot itself.
                Sometimes the user may also text "100 rs for tomorrow ", "-100 rs on clothes" and such other statements that obviously don't make sense. 
                Answer accordingly to these inputs!
                Answer strictly in a single line.
                
                Message: "{user_input}"
                User_Name: "{user_name}"
                
                """
            elif context == "db-success":
                # prompt = f"""
                # The following expense details have been successfully added to the database.
                # Generate a success message for the user!.     
                # Answer strictly in a single line.    
                # expense details: "{user_input}"
                
                
                # """
                
                return f"Thank you {user_name}! The following expense details have been successfully recorded!"
            elif context == "query_response":
                
                user_input = str(user_input)
                print(type(user_input))
                prompt = f"""
                    You are an AI assistant that converts structured MongoDB query results into a natural language summary for a user. 

                    Input:
                    You will receive an array of expense records in JSON format. Each record has the following fields:
                    - category (string) → The main category of the expense (e.g., "Food", "Transport").
                    - subcategory (optional string) → A more specific type within the category (e.g., "Pizza", "Taxi").
                    - description (optional string) → Additional details about the expense.
                    - amount (float) → The amount spent.
                    - date (ISO datetime) → The date when the expense was recorded.
                    - user_id (string) → The user’s ID (not needed in the response).

                    Task:
                    Convert the structured data into a **clear, friendly, and concise natural language response** for the user.  
                    Follow these **guidelines**:
                    1. Summarize the results in a conversational tone.
                    2. Group similar expenses together if applicable.
                    3. Show totals when possible (e.g., "You spent ₹800 on Food in January").
                    4. Use bullet points for readability if multiple expenses exist.
                    5. Make it time-aware (e.g., "Yesterday", "Last month", "On January 15").
                    6. Also, when user asks for only total amount spent, provide the total amount spent by the user.

                    
                User_Name = "{user_name}"
                Query result : 
                {user_input}
                """
                prompt2 = "Hey! how are you doing? how is your day?"
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                )
            # print(response.text)
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
                    return "API limit exhausted, please try again later!"
            else:
                return "Other"

    return "Other"

# Example Usage
# message = "What is piggybot?"
# response = generate_response(message,context="db-success",user_name="User")
# print(f"📌 Message response: {response}")
