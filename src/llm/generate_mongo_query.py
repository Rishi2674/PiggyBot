from datetime import datetime
from google import genai
from config.config import GEMINI_API_KEY
import re

def generate_mongo_query(user_query: str, user_id: str) -> dict:
    
    client  = genai.Client(api_key = GEMINI_API_KEY)
    
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
    
    try:
        response = client.models.generate_content(
            model = "gemini-2.0-flash",
            contents = prompt,
        )
        # print("response: ",response.text)
        cleaned_text = re.sub(r"```python|```", "", response.text).strip()
        cleaned_text = cleaned_text.replace("\n","")
        cleaned_text = cleaned_text.lstrip()
        # print("cleaned_text:",cleaned_text)
        mongo_query = eval(cleaned_text)  # Convert response string into a dictionary
        # print("mongo_query: ",mongo_query)
        # print("mongo_query type: ",type(mongo_query))
        # if "category" in mongo_query:
        #     mongo_query["category"] = {"$regex": f"^{mongo_query['category']}$", "$options": "i"}
        # if "subcategory" in mongo_query:
        #     mongo_query["subcategory"] = {"$regex": f"^{mongo_query['subcategory']}$", "$options": "i"}
        return mongo_query
    except Exception as e:
        print("Error generating MongoDB query:", e)
        return {}

# mq = generate_mongo_query( "How much have I spent this week?", "user123")
# print(mq)