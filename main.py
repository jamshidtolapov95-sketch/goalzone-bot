
import telebot
import feedparser
from deep_translator import GoogleTranslator
import time
from flask import Flask
import threading

# SOZLAMALAR
TOKEN = "7913340578:AAH40Kx-K_5Xh-Xf_YvjY-9WvUatY3iR3X0"
CHANNEL_ID = "@goalzone_uz" # Kanal manzili
RSS_URLS = [
    "https://www.skysports.com/rss/12040", # Sky Sports
    "https://www.goal.com/feeds/en/news"    # Goal.com
]

bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

posted_links = set()

def get_news():
    global posted_links
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            if entry.link not in posted_links:
                try:
                    title_uz = GoogleTranslator(source='en', target='uz').translate(entry.title)
                    text = f"⚡️ **{title_uz}**\n\n🔗 [Batafsil]({entry.link})"
                    bot.send_message(CHANNEL_ID, text, parse_mode="Markdown")
                    posted_links.add(entry.link)
                    time.sleep(2)
                except Exception as e:
                    print(f"Xato: {e}")

def main_loop():
    while True:
        get_news()
        time.sleep(300) # 5 daqiqa dam oladi

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("Bot ishga tushdi...")
    main_loop()
