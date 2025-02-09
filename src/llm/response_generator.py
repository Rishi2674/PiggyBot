from google import genai
from config.config import GEMINI_API_KEY

def generate_response(user_input, context="general"):
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
            You are an intelligent assistant for an expense tracker bot. 
            Generate a response for the given user input.
            Answer strictly in a single line.
            
            Message: "{user_input}"
            
            """
        elif context == "db-success":
            prompt = f"""
            The following expense details have been successfully added to the database.
            Generate a success message for the user!.     
            Answer strictly in a single line.    
            expense details: "{user_input}"
            
            """
        elif context == "query_response":
            prompt = """Hi """
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            )
        # print(response.text)
        return response.text
        
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm experiencing some issues, please try again later!"
        