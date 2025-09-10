import requests
import time
from bs4 import BeautifulSoup

# -------------------------
# CONFIG
# -------------------------
URL = "https://tickets.cafonline.com/fr"
CHECK_TEXT = "Bientôt disponible"

# Telegram
TELEGRAM_BOT_TOKEN = "8263711226:AAFhzrkQ-7C7gUMpz6sZ33rwFwLRbNhgREw"
TELEGRAM_CHANNEL = "@cafbotkams"   # canal public

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
# MAIN LOOP
# -------------------------
if __name__ == "__main__":
    while True:
        if check_site():
            # Billetterie OUVERTE
            message = (
                "🚨🚨🚨 La billetterie CAF Maroc 2025 est OUVERTE !!! 🎟️🔥\n"
                "👉 " + URL
            )
            send_telegram(message)
            print("OUVERTE 🚨 message envoyé toutes les 15s")
            time.sleep(15)  # toutes les 15 secondes
        else:
            # Encore fermée
            send_telegram("Encore fermé ⏳... Recheck dans 5 min.")
            print("Encore fermé ⏳ message envoyé, recheck dans 5 min")
            time.sleep(300)  # toutes les 5 minutes