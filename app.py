from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to PiggyBot!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification Step for WhatsApp API
        verify_token = "your_verify_token"
        challenge = request.args.get("hub.challenge")
        token = request.args.get("hub.verify_token")

        if token == verify_token:
            return challenge
        return "Verification failed", 403

    elif request.method == 'POST':
        # Handling incoming WhatsApp messages
        data = request.get_json()
        print("Received WhatsApp Message:", data)
        return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
