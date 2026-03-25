import telebot
import feedparser
import time
import threading
import os
from flask import Flask
from deep_translator import GoogleTranslator

# SOZLAMALAR - Aynan sizning kanalingiz uchun
TOKEN = "7913340578:AAH40Kx-K_5Xh-Xf_YvjY-9WvUatY3iR3X0"
CHANNEL_ID = "@goalzone_live" # Rasmdagi manzilga moslandi
RSS_URLS = [
    "https://www.skysports.com/rss/12040",
    "https://www.goal.com/feeds/en/news"
]

bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot status: Active and Running"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

posted_links = set()

def start_bot():
    global posted_links
    while True:
        for url in RSS_URLS:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:3]:
                    if entry.link not in posted_links:
                        # Tarjima qilish
                        uz_title = GoogleTranslator(source='en', target='uz').translate(entry.title)
                        msg = f"⚽️ **{uz_title}**\n\n🔗 [Batafsil o'qish]({entry.link})"
                        
                        bot.send_message(CHANNEL_ID, msg, parse_mode="Markdown")
                        posted_links.add(entry.link)
                        time.sleep(5)
            except Exception:
                continue 
        time.sleep(600) # Har 10 daqiqada yangi xabar qidiradi

if __name__ == "__main__":
    # Flaskni alohida oqimda ishga tushirish (Render o'chirib qo'ymasligi uchun)
    threading.Thread(target=run_flask).start()
    # Botni ishga tushirish
    start_bot()
