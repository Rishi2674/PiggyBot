import time
from openai import OpenAI
from datetime import datetime
import re
from config.config import OPENAI_API_KEY  # Single OpenAI API Key

# Track API call timestamps
api_call_timestamps = []

def generate_mongo_query(user_query: str, user_id: str) -> dict:
    """
    Uses OpenAI's GPT to convert a natural language user query into a MongoDB query.
    Adds the current datetime for handling time-based queries and ensures the query
    is scoped to the given user_id.
    """
    current_time = datetime.utcnow().isoformat()  # Get current UTC time in ISO format
    schema_example = {
        "user_id": user_id,
        "category": "string",
        "description": "string",
        "amount": "float",
        "date": "datetime (ISO 8601 format)"
    }
    
    output1 = {"description": {"$regex": "starbucks", "$options": "i"}, "user_id": user_id}
    
    global api_call_timestamps
    print("🔍 Generating Mongo query...")
    
    # Clean up old timestamps (keep only requests in the last 60 sec)
    current_time_unix = time.time()
    api_call_timestamps = [t for t in api_call_timestamps if current_time_unix - t < 60]
    
    # If we've hit the 10 requests/min limit, wait
    if len(api_call_timestamps) >= 10:
        wait_time = 60 - (current_time_unix - api_call_timestamps[0])
        print(f"🚨 Rate limit exceeded! Waiting {int(wait_time)} seconds...")
        time.sleep(wait_time)
    
    prompt = f'''
    Convert the following user query into a valid MongoDB query:
    "{user_query}"

    The query should be formatted as a Python dictionary and should filter results only for this user_id: "{user_id}".
    The category should be strictly one of the following:
    ["travel", "food and dining", "shopping", "entertainment", "Utilities and Bills", "Health", "Housing and Rent", "Education", "Investments and Savings", "Miscellaneous"]

    The MongoDB collection follows this schema:
    {schema_example}

    Use the current datetime for time-based queries: {current_time}.
    User id is: {user_id}

    ### **Query Requirements:**
    1. **For category-based filtering** → Use direct matching (`"category": "<category_name>"`).
    2. **For description-based filtering** → Use `$regex` with case-insensitive matching (`$options: "i"`).
    3. **For time-based filtering** → Use `$gte` and `$lte` for date ranges when applicable.
    4. **For multiple conditions**, intelligently use:
       - `$or` when querying multiple keywords in descriptions (e.g., "uber" or "ola").
       - `$and` when combining filters (e.g., category + date range + keyword in description).
    5. **Ensure the query is syntactically correct** and uses MongoDB operators properly.
    6. Always use lowercase for queries, because data is stored in lowercase itself.
    7. **No need to give any explanation or import any libraries**, just return the MongoDB query.

    ### **Example Queries and Expected Output:**
    - **"How much did I spend on Starbucks?"**
      Output: {output1}
    '''
    
    try:
        # print("in try block")
        client = OpenAI(
            api_key = OPENAI_API_KEY
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            )
        # print(response)
        # print(response.choices)
        if response and hasattr(response,'choices') and len(response.choices) > 0:
            query_text = response.choices[0].message.content.strip()
            cleaned_text = re.sub(r"```python|```", "", query_text).strip().replace("\n", "").lstrip()
            mongo_query = eval(cleaned_text)  # Convert response string into a dictionary
            api_call_timestamps.append(time.time())  # Log request time
            return mongo_query

    except OpenAI.error.OpenAIError as e:
        print(f"❌ OpenAI API Error: {str(e)}")
        return "OpenAI error"
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return "Other"

    return "Other"

# Example Usage
message = "How much did I spend on buying a new vest?"
mq = generate_mongo_query(message, user_id="919428305030")
print(f"📌 Mongo query: {mq}")