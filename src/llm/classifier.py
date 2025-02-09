import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def classify_message(user_text):
    

    prompt = f"""
    You are an intelligent assistant for an expense tracker bot. 
    Classify the given message into one of the following categories:
    - 'Expense' if the message describes an expense (e.g., "I spent Rs.10 on coffee").
    - 'Query' if the message asks about expenses (e.g., "How much did I spend this week?").
    
    Message: "{user_text}"
    
    Respond strictly with one word either 'Expense' or 'Query'. No further explanation is needed, just one word.
    """

    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response_json = response.json()
        classified_intent = response_json.get("response", "").strip()
        print("classified intent: ", classified_intent)
        print("---------------Done------------------")
        if classified_intent not in ["Expense", "Query"]:
            return "Unknown"

        return classified_intent

    except Exception as e:
        print("Error communicating with Ollama:", str(e))
        return "Error"

print(classify_message("Spent 1000 on coffee."))