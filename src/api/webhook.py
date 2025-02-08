from flask import Blueprint, request, jsonify
# from src.llm.classifier import classify_message
from config.config import VERIFY_TOKEN

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/webhook", methods=["GET"])
def verify_webhook():
    """Handles the webhook verification process"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Forbidden", 403

@webhook_bp.route("/webhook", methods=["POST"])
def handle_message():
    """Handles incoming WhatsApp messages and classifies them"""
    data = request.json

    if data.get("object") == "whatsapp_business_account":
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                message = value.get("messages", [])[0]
                contact = value.get("contacts", [])[0]

                if message and contact:
                    user_text = message.get("text", {}).get("body", "")
                    user_id = message.get("from", "")
                    user_name = contact.get("profile", {}).get("name", "User")  # Default to "User" if no name

                    print(f"User {user_name} ({user_id}) sent: {user_text}")  # Debugging

                    # Send message to LLM for classification
                    # category = classify_message(user_text, user_name)

                    # print(f"Classified as: {category}")  # Debugging

                    # response_text = f"Hello {user_name}, your message is classified as: {category}"

                    # return jsonify({"message": response_text}), 200
                    return jsonify({"message": "success"}), 200

    return "OK", 200
