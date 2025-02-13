import requests
import whisper
import os
from config.config import WHATSAPP_API_KEY

# Load Whisper Model (only once)
model = whisper.load_model("base")  # Use "tiny", "small", "medium", "large" as needed

def whatsapp_audio_to_text(media_id):
    """Takes WhatsApp media ID, downloads the audio, transcribes it, and returns the text with detailed error logging."""
    
    # Step 1: Get media URL from WhatsApp API
    media_url_request = f"https://graph.facebook.com/v18.0/{media_id}"
    headers = {"Authorization": f"Bearer {WHATSAPP_API_KEY}"}
    
    response = requests.get(media_url_request, headers=headers)
    
    # Logging API response
    if response.status_code != 200:
        error_message = f"Error: Unable to fetch media URL. Status Code: {response.status_code}, Response: {response.text}"
        print(error_message)
        return error_message

    media_url = response.json().get("url")
    if not media_url:
        error_message = "Error: Media URL is missing in the API response."
        print("API Response:", response.json())  # Log full API response
        return error_message

    # Step 2: Download the audio file
    media_response = requests.get(media_url, headers=headers)
    
    if media_response.status_code != 200:
        error_message = f"Error: Unable to download audio file. Status Code: {media_response.status_code}, Response: {media_response.text}"
        print(error_message)
        return error_message

    audio_path = "temp_audio.ogg"  # Change to .mp3 or .wav if needed
    try:
        with open(audio_path, "wb") as f:
            f.write(media_response.content)
    except Exception as e:
        error_message = f"Error: Failed to save audio file. Exception: {str(e)}"
        print(error_message)
        return error_message
    
    # Step 3: Transcribe audio using Whisper
    try:
        result = model.transcribe(audio_path)
        transcription = result["text"]
    except Exception as e:
        error_message = f"Error: Whisper transcription failed. Exception: {str(e)}"
        print(error_message)
        return error_message
    finally:
        # Cleanup audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)
    
    return transcription

# Example Usage
# media_id = "1008559431331694"  # Replace with actual media ID
# transcribed_text = whatsapp_audio_to_text(media_id)
# print("Transcription:", transcribed_text)
