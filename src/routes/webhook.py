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
    """Handles incoming WhatsApp messages and classifies them"""
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
                
                # Handle message status updates (sent, delivered, read, etc.)
                if "statuses" in value:
                    print("ℹ️ Status update received, no processing needed.")
                    return jsonify({"message": "Status update received"}), 200
                
                # Handle incoming messages
                if "messages" in value:
                    message = value["messages"][0]
                    contact = value.get("contacts", [{}])[0]
                    
                    user_text = message.get("text", {}).get("body", "")
                    user_id = message.get("from", "")
                    user_name = contact.get("profile", {}).get("name", "User")
                    
                    if not user_text or not user_id:
                        print("⚠️ Invalid message format received!")
                        return jsonify({"error": "Invalid request"}), 400
                    
                    
                    
                    print(f"📩 User {user_name} ({user_id}) sent: {user_text}")
                    
                    user = get_or_create_user(user_id=user_id, name=user_name)
                    
                    results = handle_user_message(user_text=user_text, user_id=user_id, user_name=user_name)
                    
                    # category = classify_message(user_text=user_text)
                    # response_text = f"Hello {user_name}, your message is classified as: {category}"
                    
                    # if category.lower() == "expense":
                    #     expense_data = extract_expense_details(user_text, user_id)
                        
                    #     if expense_data:
                    #         result = store_expense(expense_data)
                            
                    #         if "message" in result:
                    #             response_text = generate_response(user_input=user_text, context="db-success")
                    #             send_whatsapp_text_message(recipient_phone_number=user_id, message_text=response_text)
                    #             return jsonify({"message": response_text}), 200
                    #         else:
                    #             return jsonify({"error": "Failed to store expense details"}), 400
                    #     else:
                    #         return jsonify({"error": "Failed to extract expense details"}), 400
                    
                    # elif category.lower() == "query":
                    #     print("🟢 Query detected")
                    #     mongo_db_query = generate_mongo_query(user_query=user_text, user_id=user_id)
                    #     print("mongo_db_query: ",mongo_db_query)
                    #     if mongo_db_query:
                    #         results = execute_mongo_query(user_id=user_id, mongo_query=mongo_db_query)
                    #         print("results: ",results)
                    #         response_text = generate_response(user_input=results, context="query_response")
                    #         send_whatsapp_text_message(recipient_phone_number=user_id, message_text=response_text)
                    #         # return jsonify({"message": "Sucesss"}), 200
                    #         return 200
                    
                    # elif category.lower() == "none":
                    #     response_text = generate_response(user_input=user_text, context="general")
                    #     send_whatsapp_text_message(recipient_phone_number=user_id, message_text=response_text)
                    #     return jsonify({"message": "random message sent"}), 200
                    
                    if isinstance(results, Response):
                        return results  # Directly return Flask Response objects
                    else:
                        return jsonify({"message": str(results)}), 200
    
    return response


