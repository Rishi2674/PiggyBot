from flask import Blueprint, request, jsonify,Response
from config.config import VERIFY_TOKEN
from src.routes.handle_user_message import handle_user_message
from db.operations import get_or_create_user


PROCESSED_MESSAGES = set()

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/", methods=["GET"])
def verify_webhook():
    """Handles the webhook verification process"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    print("Verification Token: ", VERIFY_TOKEN)
    print("Received Token: ", token)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Forbidden", 403

@webhook_bp.route("/", methods=["POST"])
def handle_message():
    """Handles incoming WhatsApp messages (Text & Audio)."""
    data = request.get_json()
    
    print("Received WhatsApp Message:", data)
    message = data["entry"][0]["changes"][0]["value"].get("messages", [None])[0]
    if not message:
        return jsonify({"status": "no_message"}), 200
    
    message_id = message["id"]
    if message_id in PROCESSED_MESSAGES:
        print("ℹ️ Message already processed, skipping.")
        return jsonify({"status": "duplicate"}), 200

    PROCESSED_MESSAGES.add(message_id)
    response = jsonify({"status": "success"})
    response.status_code = 200
    
    if data.get("object") == "whatsapp_business_account":
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})

                if "statuses" in value:
                    print("ℹ️ Status update received, no processing needed.")
                    return jsonify({"message": "Status update received"}), 200

                if "messages" in value:
                    message = value["messages"][0]
                    contact = value.get("contacts", [{}])[0]
                    user_id = message.get("from", "")
                    user_name = contact.get("profile", {}).get("name", "User")
                    
                    user_text = None  # Default None for text-based input
                    
                    # **Handle TEXT Messages**
                    if message["type"] == "text":
                        user_text = message.get("text", {}).get("body", "")
                        print(f"📩 User {user_name} ({user_id}) sent: {user_text}")
                    
                    # **Handle AUDIO Messages (Voice Notes)**
                    elif message["type"] == "audio":
                        media_id = message["audio"]["id"]  # Get media ID
                        print(f"🎙️ User {user_name} ({user_id}) sent a voice message.")
                        print("media id: ", media_id)
                        # user_text = convert_voice_to_text(media_id)  # Convert to text
                        # print(f"📝 Transcribed text: {user_text}")

                    if not user_text or not user_id:
                        print("⚠️ Invalid message format received!")
                        return jsonify({"error": "Invalid request"}), 400
                    
                    # Process text message (from text or voice)
                    user = get_or_create_user(user_id=user_id, name=user_name)
                    results = handle_user_message(user_text=user_text, user_id=user_id, user_name=user_name)

                    if isinstance(results, Response):
                        return results  # Directly return Flask Response objects
                    else:
                        return jsonify({"message": str(results)}), 200
    
    return response



