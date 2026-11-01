import os
import requests
from flask import Flask, request
app = Flask(__name__)
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "codenine123")
MENU = """👋 Welcome to CodeNiNE!\n1️⃣ Website Packages\n2️⃣ Bot Packages\n3️⃣ E-Commerce\n4️⃣ Trading Bots\n5️⃣ Full Catalog\n6️⃣ Talk to Walter\nReply 1-6"""
def get_bot_reply(msg):
    if not msg: return MENU
    m=msg.lower().strip()
    if m in ["hi","hello","hey","menu","/start","start","sawubona","dumela"]: return MENU
    if m=="1": return "🌐 WEBSITE: STARTER R1500, STANDARD R2500, FLEET R6500 - Type MENU"
    if m=="2": return "🤖 BOTS: STARTER R1500, STANDARD R2800, PRO R5000 - Type MENU"
    if m=="3": return "🛒 E-COMMERCE: Basic R2500, Pro R4500, Fleet R6500 - Type MENU"
    if m=="4": return "⚙️ TRADING BOTS: MT4/5 R5000+ Crypto R5000+ - Type MENU"
    if m=="5": return "📂 FULL CATALOG: Websites, Bots, E-Com, Trading, Logos - Type MENU"
    if m=="6": return "📞 Walter: +27 81 211 6710 | @CodeNINE_dev | walter@codenine.dev - Type MENU"
    return f"You said: {msg}\n\n{MENU}"
def send_whatsapp_message(to,text):
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID: return
    url=f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers={"Authorization":f"Bearer {WHATSAPP_TOKEN}"}
    payload={"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":text}}
    requests.post(url,headers=headers,json=payload)
def send_telegram_message(chat_id,text):
    if not BOT_TOKEN: return
    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url,json={"chat_id":chat_id,"text":text})
@app.route("/")
def home(): return "CodeNiNE Bot Live - ACTIVE"
@app.route("/privacy-policy")
def privacy_policy():
    return """<html><head><title>Privacy Policy - CodeNiNE</title></head><body style="font-family:Arial;padding:40px;max-width:800px;margin:auto;"><h1>Privacy Policy - CodeNiNE</h1><p><b>Effective Date:</b> Nov 2026</p><p>CodeNiNE respects privacy. We collect phone number, name, messages to provide bot services.</p><h2>Use</h2><p>To reply inquiries, provide catalog, connect to founder Walter.</p><h2>No Sharing</h2><p>We don't sell/share data. Data stays on Render secure servers.</p><h2>Contact</h2><p>Email: walter@codenine.dev | WhatsApp: +27 81 211 6710</p><p>© 2026 CodeNiNE</p></body></html>""",200
@app.route("/telegram",methods=["GET","POST"])
def telegram_webhook():
    if request.method=="GET": return "Telegram webhook ACTIVE",200
    data=request.get_json()
    try:
        if data and "message" in data:
            chat_id=data["message"]["chat"]["id"]
            text=data["message"].get("text","")
            reply=get_bot_reply(text)
            send_telegram_message(chat_id,reply)
    except Exception as e: print(e)
    return "ok",200
@app.route("/webhook",methods=["GET","POST"])
def whatsapp_webhook():
    if request.method=="GET":
        mode=request.args.get("hub.mode")
        token=request.args.get("hub.verify_token")
        challenge=request.args.get("hub.challenge")
        if mode=="subscribe" and token==VERIFY_TOKEN: return challenge,200
        return "Verification failed",403
    data=request.get_json()
    try:
        if data and "entry" in data:
            entry=data["entry"][0]["changes"][0]["value"]
            if "messages" in entry:
                from_num=entry["messages"][0]["from"]
                text=entry["messages"][0].get("text",{}).get("body","")
                reply=get_bot_reply(text)
                send_whatsapp_message(from_num,reply)
    except Exception as e: print(e)
    return "ok",200
if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
