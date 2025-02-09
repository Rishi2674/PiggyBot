from flask import Blueprint, request, jsonify
from src.llm.classifier import classify_message
from src.llm.expense_extraction import extract_expense_details
from db.operations import store_expense
from config.config import VERIFY_TOKEN
from db.init import db 
import datetime

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/", methods=["GET"])
def verify_webhook():
    """Handles the webhook verification process"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    print("Verification Token: ", VERIFY_TOKEN )
    print("Received Token: ", token)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Forbidden", 403

@webhook_bp.route("/", methods=["POST"])
def handle_message():
    """Handles incoming WhatsApp messages and classifies them"""
    # print("hello from handle_messages()")
    # user_text = "I spent Rs. 500 on coffee"  # Debugging
    # user_id = "919876543210"
    data = request.get_json()
    print("Received WhatsApp Message:", data)
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

                      # Debugginggi
                    if not user_text or not user_id:
                        return jsonify({"error": "Invalid request"}), 400
                    
                    # existing_user = db.users_collection.find_one({"user_id": user_id})
                    # if not existing_user:
                    #     user_data = {
                    #         "user_id": user_id,
                    #         "user_name": user_name or "Unknown",
                    #         "created_at": datetime.utcnow(),
                    #         }
                    #     db.users_collection.insert_one(user_data)
                    #     print("New user added to the database")
                    
                    print(f"User {user_name} ({user_id}) sent: {user_text}")  # Debugging
                    
                    

                    category = classify_message(user_text=user_text)
                    response_text = f"Hello {user_name}, your message is classified as: {category}"

                    if category.lower() == "expense":   # Case-insensitive check
                        expense_data = extract_expense_details(user_text, user_id)  
                        print(expense_data)
                        if expense_data:
                            result = store_expense(expense_data)  # Call the new function
                            return jsonify(result), 201 if "message" in result else 500  # 500 for DB errors
                        else:
                            return jsonify({"error": "Failed to extract expense details"}), 400  # 400 for extraction failure

                    
                    elif category == 'Query' or category == 'query':
                        print("Query detected")
                        
                    return jsonify({"message": response_text}), 200

    return "OK", 200
