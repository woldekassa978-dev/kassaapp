import os
import telebot
from pymongo import MongoClient

# Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")

# Initialize Bot
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
bot.polling(none_stop=True)
