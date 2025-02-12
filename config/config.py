import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Configuration Variables
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "default_token")
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
GEMINI_API_KEY_1 = os.getenv("GEMINI_API_1", "gemini_api_key_1")
GEMINI_API_KEY_2 = os.getenv("GEMINI_API_2", "gemini_api_key_2")
GEMINI_API_KEY_3 = os.getenv("GEMINI_API_3", "gemini_api_key_3")
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "whatsapp_api_key")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "phone number id")

# print("Phone number id: ", PHONE_NUMBER_ID)

# print(f"What's app api key: {WHATSAPP_API_KEY}")

# print(f"🔑 VERIFY_TOKEN: {VERIFY_TOKEN[:5]}******")  # Masking for security
# print(f"🛢️ MONGODB_URI: {MONGODB_URI}")