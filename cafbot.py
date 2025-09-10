import requests
import time
from bs4 import BeautifulSoup
from threading import Thread
from flask import Flask
import os 
# -------------------------
# CONFIG
# -------------------------
URL = "https://tickets.cafonline.com/fr"
CHECK_TEXT = "Bientôt disponible"

# Telegram
TELEGRAM_BOT_TOKEN = "8263711226:AAFhzrkQ-7C7gUMpz6sZ33rwFwLRbNhgREw"
TELEGRAM_CHANNEL = "@cafbotkams"

# Flask app
app = Flask(__name__)
status = "Encore fermé ⏳"

# -------------------------
# NOTIFICATION TELEGRAM
# -------------------------
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHANNEL, "text": msg}
    try:
        r = requests.post(url, data=data)
        if r.status_code == 200:
            print("[TELEGRAM] ✅ Message envoyé :", msg[:50])
        else:
            print("[TELEGRAM] ❌ Erreur :", r.text)
    except Exception as e:
        print("[TELEGRAM] Erreur :", e)

# -------------------------
# CHECK SITE
# -------------------------
def check_site():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text()
        return CHECK_TEXT not in page_text
    except Exception as e:
        print("[CHECK] Erreur :", e)
        return False

# -------------------------
# BOT LOOP
# -------------------------
def bot_loop():
    global status
    while True:
        if check_site():
            status = "🚨🚨🚨 La billetterie CAF Maroc 2025 est OUVERTE !!! 🎟️🔥"
            send_telegram(status + "\n👉 " + URL)
            print("OUVERTE 🚨 message envoyé toutes les 15s")
            time.sleep(15)  # spam toutes les 15 sec
        else:
            status = "Encore fermé ⏳"
            send_telegram("Encore fermé ⏳... Recheck dans 5 min.")
            print("Encore fermé ⏳ message envoyé, recheck dans 5 min")
            time.sleep(300)  # toutes les 5 min

# -------------------------
# FLASK ROUTES
# -------------------------
@app.route("/")
def index():
    return f"<h1>{status}</h1>"

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    # Lance le bot en thread parallèle
    Thread(target=bot_loop, daemon=True).start()
    # Render fournit un port via la variable d'environnement PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)