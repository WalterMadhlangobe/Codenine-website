import os
import requests
from flask import Flask, request

app = Flask(__name__)

# ================= CONFIG =================
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "codenine123")

# ================= MENU =================
MENU = """👋 Welcome to CodeNiNE!
Built to Complete/style

1️⃣ Website Packages
2️⃣ Bot Packages  
3️⃣ E-Commerce Packages
4️⃣ Custom Trading Bots
5️⃣ Full CodeNiNE Catalog
6️⃣ Talk to Founder Walter

Reply with number (1-6) or type MENU"""

def get_bot_reply(msg):
    if not msg:
        return MENU
    m = msg.lower().strip()
    if m in ["hi", "hello", "hey", "menu", "/start", "start", "sawubona", "dumela"]:
        return MENU
    if m == "1":
        return "🌐 *WEBSITE CATALOG:*\n\nSTARTER R1,500 - Gallery + Whatsapp button\nSTANDARD R2,500 - MOST POPULAR - E-commerce + Cart + Pay\nFLEET R6,500 - Full company site + Fleet management\n\nADD: Logo R750, Domain R500/yr, Hosting R300/yr\n\nType MENU"
    if m == "2":
        return "🤖 *BOT CATALOG:*\n\nSTARTER R1,500 - Auto Reply Bot\nSTANDARD R2,800 - MOST POPULAR - AI Business Bot\nPRO R5,000 - Trading Bot R7K/R15K\n\nWorks on Whatsapp, Telegram, Instagram, Website\n\nType MENU"
    if m == "3":
        return "🛒 *E-COMMERCE CATALOG:*\n\nBasic Shop R2,500 - Products + Cart + Whatsapp Order\nPro Shop R4,500 - Payment Gateway + Inventory\nFLEET R6,500 - Full management\n\nType MENU"
    if m == "4":
        return "⚙️ *CUSTOM TRADING BOTS:*\n\nMetaTrader 4/5 Bots - R5,000+\nCrypto Bots - R5,000+\nForex Automation\n\nTalk to Walter for custom quote\n\nType MENU"
    if m == "5":
        return "📂 *FULL CODENINE CATALOG:*\n\nWe build:\n• Websites\n• Whatsapp/Telegram Bots\n• E-Commerce\n• Trading Bots\n• Company Logos\n\nVisit: codenine.dev\n\nType MENU"
    if m == "6":
        return "📞 *TALK TO FOUNDER:*\n\nWalter Mashlangobe\nWhatsApp: +27 81 211 6710\nTelegram: @CodeNINE_dev\nEmail: walter@codenine.dev\n\nType MENU"
    return f"You said: {msg}\n\n{MENU}"

# ================= SEND FUNCTIONS =================
def send_whatsapp_message(to, text):
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print("No WA TOKEN")
        return
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    r = requests.post(url, headers=headers, json=payload)
    print(f"WA -> {r.status_code}")

def send_telegram_message(chat_id, text):
    if not BOT_TOKEN:
        print("No BOT_TOKEN")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload)
    print(f"TG -> {r.status_code} {r.text[:100]}")

# ================= ROUTES =================
@app.route("/")
def home():
    return "CodeNiNE Bot Live - Telegram + Whatsapp - ACTIVE"

# --- THIS WAS MISSING - NOW FIXED! ---
@app.route("/privacy-policy")
def privacy_policy():
    return """
    <html><head><title>Privacy Policy - CodeNiNE</title></head>
    <body style="font-family:Arial; padding:40px; max-width:800px; margin:auto;">
    <h1>Privacy Policy - CodeNiNE</h1>
    <p><b>Effective Date:</b> November 1, 2026</p>
    <p>CodeNiNE ("we", "us") respects your privacy. This policy explains how we handle data for our WhatsApp and Telegram bots.</p>
    <h2>1. Information We Collect</h2>
    <p>We only collect your phone number, name, and messages you send to our bot to provide services.</p>
    <h2>2. How We Use It</h2>
    <p>To reply to your inquiries, provide catalog information, and connect you to our founder Walter.</p>
    <h2>3. No Sharing</h2>
    <p>We do not sell or share your data with third parties. Data stays on our secure servers (Render).</p>
    <h2>4. Contact</h2>
    <p>Email: walter@codenine.dev | WhatsApp: +27 81 211 6710</p>
    <p>© 2026 CodeNiNE - Built to Complete</p>
    </body></html>
    """, 200

@app.route("/telegram", methods=["GET", "POST"])
def telegram_webhook():
    if request.method == "GET":
        return "Telegram webhook is ACTIVE! Go send /start in Telegram", 200
    data = request.get_json()
    print(f"Telegram incoming: {data}")
    try:
        if data and "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")
            reply = get_bot_reply(text)
            send_telegram_message(chat_id, reply)
    except Exception as e:
        print(f"Telegram Error: {e}")
    return "ok", 200

@app.route("/webhook", methods=["GET", "POST"])
def whatsapp_webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification failed", 403
    data = request.get_json()
    print(f"WhatsApp incoming: {data}")
    try:
        if data and "entry" in data:
            entry = data["entry"][0]["changes"][0]["value"]
            if "messages" in entry:
                msg_obj = entry["messages"][0]
                from_num = msg_obj["from"]
                text = msg_obj.get("text", {}).get("body", "")
                reply = get_bot_reply(text)
                send_whatsapp_message(from_num, reply)
    except Exception as e:
        print(f"WA Error: {e}")
    return "ok", 200

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
