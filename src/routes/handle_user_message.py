from src.llm.response_generator import generate_response
from src.routes.whatsapp_sender import send_whatsapp_text_message
from src.llm.generate_mongo_query import generate_mongo_query
from src.llm.classifier import classify_message
from src.llm.expense_extraction import extract_expense_details
from db.operations import store_expense, execute_mongo_query
from flask import jsonify

def handle_user_message(user_text, user_id,user_name="User"):
    category = classify_message(user_text)  # Assuming this function returns "expense", "query", or "none"
    
    if category.lower() == "expense":
        expense_data = extract_expense_details(user_text, user_id)
        
        if not expense_data:
            return jsonify({"error": "Failed to extract expense details"}), 400
        
        result = store_expense(expense_data)
        
        if "message" in result:
            response_text = generate_response(user_input=user_text, context="db-success",user_name=user_name)
        else:
            response_text = "Failed to store expense details. Please try again."
            return jsonify({"error": response_text}), 400
        
        send_whatsapp_text_message(user_id, response_text)
        return jsonify({"message": response_text}), 200
    
    elif category.lower() == "query":
        print("🟢 Query detected")
        
        mongo_db_query = generate_mongo_query(user_query=user_text, user_id=user_id)
        print("Generated MongoDB Query:", mongo_db_query)
        
        if not mongo_db_query:
            response_text = "I couldn't understand your query. Please rephrase."
            send_whatsapp_text_message(user_id, response_text)
            return jsonify({"error": response_text}), 400
        
        results = execute_mongo_query(user_id=user_id, mongo_query=mongo_db_query)
        # print("Query Results:", results)
        
        response_text = generate_response(user_input=results, context="query_response",user_name=user_name)
        send_whatsapp_text_message(user_id, response_text)
        return jsonify({"message": "Success"}), 200
    
    else:  # Handles "none" or any unclassified messages
        response_text = generate_response(user_input=user_text, context="general",user_name=user_name)
        send_whatsapp_text_message(user_id, response_text)
        return jsonify({"message": "Normal message sent"}), 200
    
    return jsonify({"error": "Unhandled Category"}), 400
