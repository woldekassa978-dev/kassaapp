import os
import telebot
import time
import threading
from pymongo import MongoClient
from datetime import datetime

# Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")

bot = telebot.TeleBot(BOT_TOKEN)

try:
    client = MongoClient(MONGO_URI)
    db = client['kassa_mining_db']
    users_col = db['users']
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ Database connection error: {e}")

# የ ETB ስሌት ተግባር
def get_user_balance_text(user_id):
    user = users_col.find_one({"user_id": user_id})
    if not user: return "ተጠቃሚ አልተገኘም!"
    coins = user.get("coins", 0)
    etb_value = coins * 0.05  # 1 ሳንቲም = 0.05 ብር
    return f"💰 የሳንቲም መጠን፦ {coins:,.2f}\n💵 አጠቃላይ ዋጋ፦ {etb_value:,.2f} ETB"

# Auto-compounding ተግባር (በየ 24 ሰዓቱ የሚሰራ)
def daily_auto_compound():
    while True:
        # በየ 24 ሰዓቱ (86400 ሰከንድ) ይጠብቃል
        time.sleep(86400) 
        interest_rate = 0.009  # 0.9%
        users_col.update_many(
            {},
            {"$inc": {"coins": {"$multiply": ["$coins", interest_rate]}}}
        )
        print("📈 Daily auto-compound completed.")

# የ Scheduler ሪን (Background Thread) መጀመር
threading.Thread(target=daily_auto_compound, daemon=True).start()

# /start ትዕዛዝ
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    # ተጠቃሚ መመዝገብ
    users_col.update_one(
        {"user_id": user_id},
        {"$setOnInsert": {"user_id": user_id, "username": username, "coins": 0}},
        upsert=True
    )
    bot.reply_to(message, f"ሰላም! ወደ Kassa Mining Bot እንኳን ደህና መጡ።\n\n{get_user_balance_text(user_id)}")

# ዋና ሉፕ
print("🚀 Bot is running...")
bot.polling(none_stop=True)
