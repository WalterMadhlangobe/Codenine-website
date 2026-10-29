from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# WhatsApp Config
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "codenine123")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "EAAUsgVV5ZAiMBS9D3rBie1N6qFsspjoIielMuL9tZCnkvslKrhZCokBuQQ2sagdIlopIYGXculWAob02ZAbLZBzUNXAacmx89AWigPC9LImMucMNBZBZAouYoSNttk436d3lpwzDYIRxIPqJDUWlftA5r6ZB5hIdTA2C6vv8rRpeZBsHA4x8SAZCVbPwW38MYRdZA3qrLUXEmAi271Vbzv6ChmZBfGZAqYiTiLx5sa028sQonJEtNpY1qdKf6Rvvkkt8DdsNEeJJ6Xj2055KEVy3TZCI68pcMb")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "1447454081781641")

@app.route('/')
def home():
    return render_template('index.html')

# === VERIFY WEBHOOK (GET) ===
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

# === RECEIVE MESSAGES (POST) - ONLY ONE POST! ===
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Incoming:", data)
    try:
        if data.get('object') == 'whatsapp_business_account':
            for entry in data['entry']:
                for change in entry['changes']:
                    value = change['value']
                    if 'messages' in value:
                        msg = value['messages'][0]
                        from_number = msg['from']
                        msg_body = msg.get('text', {}).get('body', '').lower()

                        reply = get_bot_reply(msg_body)
                        send_whatsapp_message(from_number, reply)
    except Exception as e:
        print(f"Error: {e}")
    return "OK", 200

# === BOT LOGIC ===
def get_bot_reply(msg):
    MENU = """👋 Welcome to CodeNiNE - Built to Complete
www.codenine.dev | Founder Walter

Reply with number:
1️⃣ Website Prices
2️⃣ Bot Prices
3️⃣ E-commerce
4️⃣ Custom Trading Bot
5️⃣ See ALL Catalogs
6️⃣ Talk to Human"""

    if "hi" in msg or "hello" in msg or "hey" in msg or "menu" in msg:
        return MENU
    elif msg.strip() == "1":
        return "🌐 WEBSITE CATALOG\nSTARTER R1,500\nSTANDARD R3,500 ⭐ MOST POPULAR\nPRO R5,500\nFLEET R8,500+\nE-COM R10,000+\n\nReply ORDER + your business name"
    elif msg.strip() == "2":
        return "🤖 BOT CATALOG\nStarter R1,800\nStandard R3,800 ⭐\nPro R6,500\nFleet R9,500+\nE-comm AI R12,000+\n\nReply ORDER BOT"
    elif msg.strip() == "3":
        return "🛒 E-COMMERCE\nStarter R4,500\nBusiness R7,500 ⭐\nPro R10,000+\nCart + PayFast + WhatsApp Orders"
    elif msg.strip() == "4":
        return "🛠️ CUSTOM TRADING BOT\nSend strategy PDF/video\nWe code MT4/MT5/TradingView\nFrom R3,000\nQuote in 2hrs"
    elif msg.strip() == "5":
        return "📚 FULL CODE NINE CATALOG\nWebsites + Bots + E-com + Booking Systems + Fleet\nwww.codenine.dev\nBuilt to Complete"
    elif msg.strip() == "6":
        return "👨‍💻 Connecting you to Walter... Send your question, he replies in 10 mins.\nOr email: walter@codenine.dev"
    elif "price" in msg or "cost" in msg:
        return "💰 CodeNine Pricing:\n• Starter Site: R2,500\n• Business Pro: R4,500\n• E-commerce: R5,500+\n\nAll include hosting setup + domain help.\n" + MENU
    else:
        return MENU

# === SEND MESSAGE ===
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