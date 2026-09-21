import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "rifat_data_entry_token_2026"
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "EAAfml573upUBSpY4Kj59caZAuwBesXlqVTMk42O2THBvZAh3940bEwL4OstudvyqmAcZAICXgJec48Cd7ovTQdmhgubdP0hPib8XjVtN2uzYBSvSAwtLA94IHaXVgnoZCslflHxczs0TZBiZBnXQkL5YclQIRmRFVLcZB3LDVIZB7XZBC2xsx0WzElS0dVRuePlrT7yFbmyBUU1fCS1REkO246OgwvNuWYmKuNwh5k7Pnr11o8JWphv4fkM30ZCmnN4C9GB9MyFZBJsRZBFxZB2gmZAe0N7hXP")

def send_messenger_reply(recipient_id, message_text):
    """Sends an engaging, client-focused conversational reply for Data Entry jobs."""
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, params=params, json=payload, headers=headers, timeout=10)
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
                    
                    if messaging_event.get("message") and not messaging_event["message"].get("is_echo"):
                        message_text = messaging_event["message"].get("text", "")
                        print(f"Received message from {sender_id}: {message_text}")
                        
                        # Client hunting & Job-taking response: inviting clients to assign data entry work
                        reply_text = (
                            "Hello! Thanks for reaching out to Rifat's Data Entry service (Page: Robiul Islam). "
                            "We are ready to take your data entry projects, Excel spreadsheets, copy-paste tasks, and data processing work with 100% accuracy and fast delivery. "
                            "Please share your project details, file samples, or budget so we can start right away!"
                        )
                        send_messenger_reply(sender_id, reply_text)
                        
                    elif messaging_event.get("postback"):
                        payload_text = messaging_event["postback"].get("payload", "")
                        print(f"Received postback from {sender_id}: {payload_text}")
                        reply_text = "Welcome! We are ready to take your data entry projects. Tell us what tasks you need completed!"
                        send_messenger_reply(sender_id, reply_text)

        return "EVENT_REGISTERED", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
