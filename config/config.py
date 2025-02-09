import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Configuration Variables
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "default_token")
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
GEMINI_API_KEY = os.getenv("GEMINI_API", "gemini_api_key")

# print(f"🔑 VERIFY_TOKEN: {VERIFY_TOKEN[:5]}******")  # Masking for security
# print(f"🛢️ MONGODB_URI: {MONGODB_URI}")