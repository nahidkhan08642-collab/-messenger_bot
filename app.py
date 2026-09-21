import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "rifat_data_entry_token_2026"
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "EAAZa...YOUR_PAGE_TOKEN")

def send_messenger_reply(recipient_id, message_text):
    """Sends a conversational reply back to the user on Facebook Messenger."""
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print("Messenger API Response:", response.status_code, response.text)
        return response.json()
    except Exception as e:
        print("Error sending Messenger reply:", e)
        return None

@app.route("/", methods=["GET"])
def home():
    return "Messenger Bot is active and running for Rifat's Data Entry Page (Robiul Islam ID: 1237613292776083)!", 200

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
        
        if data.get("object") == "page":
            for entry in data.get("entry", []):
                for messaging_event in entry.get("messaging", []):
                    sender_id = messaging_event.get("sender", {}).get("id")
                    
                    # Handle incoming text messages
                    if messaging_event.get("message") and not messaging_event["message"].get("is_echo"):
                        message_text = messaging_event["message"].get("text", "")
                        print(f"Received message from {sender_id}: {message_text}")
                        
                        # Generate conversational multi-turn response for data entry inquiries
                        reply_text = (
                            "Hello! Welcome to Rifat's Data Entry service (Page ID: 1237613292776083). "
                            "We provide professional, accurate, and prompt data entry services. "
                            "How can I help you today? Please share your project details or requirements."
                        )
                        send_messenger_reply(sender_id, reply_text)
                        
                    # Handle postback events (get started buttons, etc.)
                    elif messaging_event.get("postback"):
                        payload_text = messaging_event["postback"].get("payload", "")
                        print(f"Received postback from {sender_id}: {payload_text}")
                        reply_text = "Welcome! Let's get started on your data entry project. Please tell me more about what you need."
                        send_messenger_reply(sender_id, reply_text)

        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
