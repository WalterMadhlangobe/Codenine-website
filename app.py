from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# WhatsApp Config - you will fill these from Meta
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "codenine123")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


@app.route('/')
def home():
    return render_template('index.html')


# === WHATSAPP WEBHOOK ===
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    # Meta verification
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403


@app.route('/webhook', methods=['POST'])
def handle_message():
    data = request.get_json()
    print("Incoming:", data)

    try:
        # Extract message
        if data['object'] == 'whatsapp_business_account':
            for entry in data['entry']:
                for change in entry['changes']:
                    value = change['value']
                    if 'messages' in value:
                        message = value['messages'][0]
                        from_number = message['from']
                        msg_body = message['text']['body'].lower()

                        # BOT LOGIC FOR CODENINE
                        reply = get_bot_reply(msg_body)
                        send_whatsapp_message(from_number, reply)
    except Exception as e:
        print(f"Error: {e}")

    return "OK", 200


def get_bot_reply(msg):
    if "hi" in msg or "hello" in msg or "hey" in msg:
        return "🚀 Welcome to CodeNine.dev! I'm CodeNine Bot.\n\nWhat do you need?\n1️⃣ New Website\n2️⃣ E-commerce Store\n3️⃣ Website Redesign\n4️⃣ Talk to Walter\n\nReply with number (1-4)"
    elif "1" in msg:
        return "🔥 NEW WEBSITE — Let's go!\nWe build fast, modern sites from R2500.\nWhat's your business name & budget? (e.g. 'Salon, R4000')"
    elif "2" in msg or "shop" in msg:
        return "🛒 E-COMMERCE — We got you!\nShopify / Custom store with payments.\nFrom R5500. Send your products list!"
    elif "3" in msg:
        return "🎨 REDESIGN — We make old sites sexy again!\nSend me your current link and I'll audit free!"
    elif "price" in msg or "cost" in msg:
        return "💰 CodeNine Pricing:\n• Starter Site: R2500\n• Business Pro: R4500\n• E-commerce: R5500+\n\nAll include hosting setup + domain help.\nWant a custom quote? Type your business type!"
    else:
        return "Got it! 👊 Walter will reply soon.\nIn meantime, see our work: https://codenine-website.onrender.com\n\nType 'Hi' to restart bot."


def send_whatsapp_message(to, text):
    if not WHATSAPP_TOKEN:
        print("No token set - skipping send")
        return
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    r = requests.post(url, headers=headers, json=payload)
    print(f"Sent: {r.status_code} - {r.text}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))