import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "9236352164:AAFN3jFd3GuCp3bfmTrRF1PqbbHg5VbF2IY")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_telegram(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        data["reply_markup"] = reply_markup
    try:
        requests.post(f"{TELEGRAM_API}/sendMessage", json=data, timeout=10)
    except Exception as e:
        print(f"Telegram send error: {e}")

@app.route("/")
def home():
    return "CodeNiNE Bot is Running! - Use /telegram webhook"

@app.route("/health")
def health():
    return "OK", 200

@app.route("/telegram", methods=["POST", "GET"])
def telegram_webhook():
    if request.method == "GET":
        return "Telegram webhook is active! Use POST", 200
    
    try:
        data = request.get_json()
        print(f"Telegram update: {data}")
        
        if not data or "message" not in data:
            return "ok", 200
            
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()
        
        if text == "/start":
            keyboard = {
                "keyboard": [
                    [{"text": "🌐 Services"}, {"text": "💰 Pricing"}],
                    [{"text": "📞 Contact"}, {"text": "ℹ️ About"}]
                ],
                "resize_keyboard": True
            }
            send_telegram(chat_id, 
                "🔥 *Welcome to CodeNiNE.dev* 🔥\n\n"
                "Your digital partner for:\n"
                "• Web Development\n"
                "• Bot Automation\n"
                "• WhatsApp + Telegram Bots\n\n"
                "Choose an option below:", 
                keyboard)
        elif text == "🌐 Services" or text.lower() == "services":
            send_telegram(chat_id, "🌐 *Our Services:*\n\n✅ Websites\n✅ WhatsApp Bots\n✅ Telegram Bots\n✅ Automation\n\nType /start for menu")
        elif text == "💰 Pricing":
            send_telegram(chat_id, "💰 *Pricing:*\n\nBasic - R1500\nPro - R3500\n\nContact us for custom!")
        elif text == "📞 Contact":
            send_telegram(chat_id, "📞 *Contact:*\n\nWhatsApp: +27...\nTelegram: @CodeNINE_dev")
        else:
            send_telegram(chat_id, f"You said: {text}\n\nType /start for menu")
            
    except Exception as e:
        print(f"Error: {e}")
    
    return "ok", 200

@app.route("/webhook", methods=["GET", "POST"])
def whatsapp_webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        verify_token = os.getenv("VERIFY_TOKEN", "codenine123")
        if mode == "subscribe" and token == verify_token:
            return challenge, 200
        return "Verification failed", 403
    else:
        print(f"WhatsApp webhook: {request.get_json()}")
        return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
