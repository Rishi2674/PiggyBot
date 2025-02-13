# from flask import Flask
from src.utils.webhook import handle_message 
# from db.init import db

# def create_app():
#     app = Flask(__name__)  # Initialize Flask app
    
#     # Load configurations (if you have more settings later)
#     # app.config.from_object("config.config")  
#     # print(VERIFY_TOKEN)
#     # init_db()  # Initialize MongoDB connection
    
#     # Register Blueprints
#     print("import from src works!")
#     app.register_blueprint(webhook_bp, url_prefix="/webhook")
    
#     return app

# app  = create_app()

# app.url_map.strict_slashes = False  


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

from flask import Flask, request, jsonify

app = Flask(__name__)

# Prevent Flask from auto-redirecting requests
app.url_map.strict_slashes = False  

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token == "hellopiggybot":  # Your verification token
            return challenge, 200
        else:
            return "Forbidden", 403

    elif request.method == "POST":
        # data = request.json
        # print("Received WhatsApp message:", data)
        # return jsonify({"status": "success"}), 200
        return handle_message(request)

if __name__ == "__main__":
    app.run(port=5000, debug=True,use_reloader=False)