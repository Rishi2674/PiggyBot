import requests
import whisper
import os
from config.config import WHATSAPP_API_KEY

# Your WhatsApp API Credentials
 # Replace with your API token

# Load Whisper Model (only once)
model = whisper.load_model("base")  # Use "tiny", "small", "medium", "large" as needed

def whatsapp_audio_to_text(media_id):
    """Takes WhatsApp media ID, downloads the audio, transcribes it, and returns the text."""
    
    # Step 1: Get media URL from WhatsApp API
    media_url_request = f"https://graph.facebook.com/v18.0/{media_id}"
    headers = {"Authorization": f"Bearer {WHATSAPP_API_KEY}"}
    
    response = requests.get(media_url_request, headers=headers)
    if response.status_code != 200:
        return "Error: Unable to fetch media URL"

    media_url = response.json().get("url")
    
    # Step 2: Download the audio file
    media_response = requests.get(media_url, headers=headers)
    if media_response.status_code != 200:
        return "Error: Unable to download audio file"

    audio_path = "temp_audio.ogg"  # Change to .mp3 or .wav if needed
    with open(audio_path, "wb") as f:
        f.write(media_response.content)
    
    # Step 3: Transcribe audio using Whisper
    result = model.transcribe(audio_path)
    transcription = result["text"]

    # Step 4: Cleanup and return text
    os.remove(audio_path)
    
    return transcription

# Example Usage
media_id = "953894806932837"  # Replace with actual media ID
transcribed_text = whatsapp_audio_to_text(media_id)
print(transcribed_text)
