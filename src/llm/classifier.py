import ollama
# import requests
from google import genai
import time
from config.config import GEMINI_API_KEY

OLLAMA_URL = "http://localhost:11434/api/generate"


def classify_message(user_text):
    print("in classification messsages")
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
    You are an intelligent assistant for an expense tracker bot. 
    Classify the given message into one of the following categories:
    - 'Expense' if the message describes an expense (e.g., "I spent Rs.10 on coffee").
    - 'Query' if the message asks about expenses (e.g., "How much did I spend this week?").
    
    Message: "{user_text}"
    
    Respond ONLY with 'Expense' or 'Query'. NO explanations, NO extra text.
    """

    # payload = {
    #     "model": "phi3",
    #     "prompt": prompt,
    #     "stream": False,
    #     "options": {
    #         "temperature": 0,
    #         "max_tokens": 15,
    #     }
    # }
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        )
    print("classification output: ",response.text)
    return response.text.strip().split("\n")[0]

    # print(response.text)
    # response = ollama.generate(
    #     model="phi3",
    #     prompt=prompt,
    #     options={
    #         "temperature": 0,
    #         "max_tokens": 1,
    #         "num_ctx": 512,
    #         "num_gqa": 1
    #     }
    # )
    
    # return response["response"].strip().split()[0]   

    # try:
    #     response = requests.post(OLLAMA_URL, json=payload)
    #     print("response: ", response)
    #     response_json = response.json()
    #     classified_intent = response_json.get("response", "").strip()
    #     print("classified intent: ", classified_intent)
    #     print("---------------Done------------------")
    #     if classified_intent not in ["Expense", "Query"]:
    #         return "Unknown"

    #     return classified_intent

    # except Exception as e:
    #     print("Error communicating with Ollama:", str(e))
    #     return "Error"

# import time

# start = time.time()
# response = classify_message("What was my expense last week?")
# end = time.time()

# print("Response:", response)
# print("Time taken:", end - start, "seconds")