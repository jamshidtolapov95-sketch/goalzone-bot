import telebot
import feedparser
import time
from googletrans import Translator
from flask import Flask
from threading import Thread

# --- RENDER O'CHIB QOLMASLIGI UCHUN ---
app = Flask('')
@app.route('/')
def home():
    return "Bot ishlayapti!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- SOZLAMALAR ---
API_TOKEN = '8783318642:AAHe-cHu7C5IRxoKg68wD2ARM91n_Q8rkeo'
CHANNEL_ID = '@goalzone_live'

SOURCES = [
    {'url': 'https://www.sports.ru/rss/all_news.xml', 'lang': 'ru'},
    {'url': 'https://feeds.bbci.co.uk/sport/football/rss.xml', 'lang': 'en'}
]

AD_TEXT = "\n\n💰 **DAROMAD:** [Bonusni olish](https://t.me/goalzone_live)"

bot = telebot.TeleBot(API_TOKEN)
translator = Translator()
posted_links = []

def check_and_post():
    for source in SOURCES:
        try:
            feed = feedparser.parse(source['url'])
            if feed.entries:
                latest = feed.entries[0]
                if latest.link not in posted_links:
                    translation = translator.translate(latest.title, src=source['lang'], dest='uz')
                    flag = "🇷🇺" if source['lang'] == 'ru' else "🇬🇧"
                    msg = f"⚡️ **TEZKOR {flag}**\n\n{translation.text}\n\n👉 [Batafsil]({latest.link}){AD_TEXT}\n\n⚽️ {CHANNEL_ID}"
                    bot.send_message(CHANNEL_ID, msg, parse_mode="Markdown")
                    posted_links.append(latest.link)
                    if len(posted_links) > 50: posted_links.pop(0)
        except Exception as e:
            print(f"Xato: {e}")

if __name__ == "__main__":
    keep_alive() # Web serverni yoqish
    print("Global Bot Render-da ishga tushdi...")
    while True:
        check_and_post()
        time.sleep(120) # 2 daqiqa kutish
