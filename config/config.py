import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Configuration Variables
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "default_token")  # Reads from .env, else uses default
# print(f"VERIFY_TOKEN: {VERIFY_TOKEN}")


