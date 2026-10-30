import os
import requests
from flask import Flask, request

app = Flask(__name__)

# === CONFIG ===
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "codenine123")

# === MENU ===
MENU = (
    "Sawubona! 👋 Welcome to CodeNiNE\n"
    "Built to Complete\n\n"
    "1️⃣ Website Packages\n"
    "2️⃣ Bot Packages\n"
    "3️⃣ E-Commerce Packages\n"
    "4️⃣ Custom Trading Bot\n"
    "5️⃣ Full CodeNiNE Catalog\n"
    "6️⃣ Talk to Founder Walter\n\n"
    "Reply with number (1-6) or type MENU"
)


def get_bot_reply(msg):
    if not msg:
        return MENU
    m = msg.lower().strip()

    if m in ["hi", "hello", "hey", "menu", "/start", "start", "sawubona"]:
        return MENU

    if m == "1":
        return (
            "🌐 WEBSITE CATALOG\n"
            "STARTER R1,500 - Gallery + WhatsApp button\n"
            "STANDARD R2,800 - MOST POPULAR ⭐ - E-commerce + Cart\n"
            "FLEET R4,500+ - Full company site\n\n"
            "Add: Logo R750, Domain R500/yr"
        )

    if m == "2":
        return (
            "🤖 BOT CATALOG\n"
            "STARTER R1,200 - Auto Reply Bot\n"
            "STANDARD R2,800 - MOST POPULAR - AI Business Bot\n"
            "PRO R5,000+ - Trading Bot MT4/MT5\n\n"
            "Works on WhatsApp, Telegram, Instagram"
        )

    if m == "3":
        return (
            "🛒 E-COMMERCE CATALOG\n"
            "STARTER R4,800 - Small shop\n"
            "BUSINESS R7,500 - MOST POPULAR\n"
            "PRO R10,200 - Fleet store + Fleet\n"
            "PayFast + Stock + WhatsApp orders"
        )

    if m == "4":
        return (
            "📈 CUSTOM TRADING BOT\n"
            "Send your strategy PDF/video/vix code\n"
            "MT4/MT5/TradingView -> Auto trading\n"
            "From R3,000 - Quote in 2hrs\n"
            "Telegram signal bot included"
        )

    if m == "5":
        return (
            "📦 FULL NINE CATALOG\n"
            "Websites + Bots + E-com + Booking Systems\n"
            "Fleet: www.codenine.dev\n"
            "Built to Complete - Founder Walter"
        )

    if m == "6":
        return (
            "👨‍💻 Connecting you to Walter...\n"
            "Send your question here, he replies in 10 mins\n"
            "Or email: walter@codenine.dev\n"
            "WhatsApp direct: +27 XX XXX XXXX"
        )

    if "price" in m or "cost" in m or "how much" in m:
        return (
            "💰 CodeNiNE Pricing:\n"
            "Starter Site: R2,500\n"
            "Business Pro: R4,500\n"
            "E-commerce: R5,500+\n"
            "All include hosting setup"
        )

    return MENU


# === SENDERS ===
def send_whatsapp_message(to, text):
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print("Missing WA tokens")
        return
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
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


# === ROUTES ===
@app.route("/")
def home():
    return "CodeNiNE Bot Live ✅ - Telegram + WhatsApp"


@app.route("/webhook", methods=["GET", "POST"])
def whatsapp_webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed", 403

    data = request.get_json()
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            msg_obj = entry['messages'][0]
            from_num = msg_obj['from']
            text = msg_obj.get('text', {}).get('body', '')
            reply = get_bot_reply(text)
            send_whatsapp_message(from_num, reply)
    except Exception as e:
        print(f"WA Error: {e}")
    return "ok", 200


@app.route(f"/telegram/{BOT_TOKEN}", methods=["POST"])
@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    try:
        message = data.get('message') or data.get('edited_message')
        if not message:
            return "ok", 200
        chat_id = message['chat']['id']
        text = message.get('text', '')
        reply = get_bot_reply(text)
        send_telegram_message(chat_id, reply)
    except Exception as e:
        print(f"TG Error: {e}")
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))