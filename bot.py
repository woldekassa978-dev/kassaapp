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
    users_col = None

# አሁን ከዚህ በታች ሌሎች ኮዶችህን መጨመር ትችላለህ
