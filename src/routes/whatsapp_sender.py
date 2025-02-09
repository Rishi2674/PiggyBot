import requests
import os
from config.config import WHATSAPP_API_KEY,PHONE_NUMBER_ID


# Load from environment variables or replace with your actual credentials# Your WhatsApp Business phone number ID

def send_whatsapp_text_message(recipient_phone_number, message_text):
    """
    Sends a text message to a user's WhatsApp number using the WhatsApp Cloud API.

    Args:
        recipient_phone_number (str): The recipient's WhatsApp number in international format (e.g., "919428305030").
        message_text (str): The text message content to send.

    Returns:
        dict: The API response as a JSON dictionary.
    """
    url = f"https://graph.facebook.com/v13.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_phone_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("✅ Message sent successfully!")
    else:
        print(f"❌ Failed to send message: {response.status_code} - {response.text}")

    return response.json()


