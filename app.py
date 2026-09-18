import os
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "rifat_data_entry_token_2026"

@app.route("/", methods=["GET"])
def home():
    return "Messenger Bot is running live and permanent for Rifat!", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403

    elif request.method == "POST":
        data = request.json
        print("Incoming Webhook Data:", data)
        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
