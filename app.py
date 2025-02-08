from flask import Flask
from src.api.webhook import webhook_bp  # Import your webhook Blueprint

def create_app():
    app = Flask(__name__)  # Initialize Flask app
    
    # Load configurations (if you have more settings later)
    # app.config.from_object("config.config")  
    # print(VERIFY_TOKEN)
    
    # Register Blueprints
    print("import from src works!")
    app.register_blueprint(webhook_bp, url_prefix="/webhook")
    
    return app

app  = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
