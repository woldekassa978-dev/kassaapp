import os
import telebot
from pymongo import MongoClient

# Environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")

# Bot initialization
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables!")

bot = telebot.TeleBot(BOT_TOKEN)

# Database connection
try:
    client = MongoClient(MONGO_URI)
    db = client['kassa_mining_db']
    users_col = db['users']
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ Database connection error: {e}")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "ሰላም! ቦቱ እየሰራ ነው።")

print("🚀 Bot is running...")
bot.polling()
