from google import genai
from config.config import GEMINI_API_KEY
import json

def generate_response(user_input, context="general",user_name="User"):
    """
    Sends user input to Gemini API and returns a response.
    
    Args:
        user_input (str): The user's message.
        context (str): The type of response needed ('general' or 'success').

    Returns:
        str: The response from the Gemini API.
    """
    client = genai.Client(api_key = GEMINI_API_KEY)
    try:
        prompt = ""
        if context == "general":
            prompt = f"""
            You are an intelligent assistant for an expense tracker bot called "PiggyBot" . 
            Generate a response for the given user input.
            Answer as if you are PiggyBot itself.
            Sometimes the user may also text "-100 rs for today etc", and such other statements that obviously don't make sense. 
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
            
            return f"Thank you {user_name}! The following expense details have been successfully added to the database!"
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
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            )
        # print(response.text)
        return response.text
        
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm experiencing some issues, please try again later!"
        