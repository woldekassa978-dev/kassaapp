import os
import telebot
from pymongo import MongoClient
from urllib.parse import quote_plus

# 1. Environment Variables ን ከ Render ማንበብ
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")

# 2. ቦቱን ማስጀመር
if not BOT_TOKEN:
    print("❌ BOT_TOKEN አልተገኘም!")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)

# 3. ዳታቤዝ መገናኘቱን ማረጋገጥ
try:
    client = MongoClient(MONGO_URI)
    db = client['kassa_mining_db']
    users_col = db['users']
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ Database connection error: {e}")

# 4. የ /start ትዕዛዝ
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "ሰላም! ቦቱ በአሁኑ ሰዓት እየሰራ ነው።")

print("🚀 Bot is running...")
bot.polling(none_stop=True)
