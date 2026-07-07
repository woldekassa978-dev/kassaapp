import os
import telebot
from pymongo import MongoClient
from datetime import datetime

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

# ደረጃ 2፡ የ register_user ተግባር
def register_user(user_id, username):
    user_data = {
        "user_id": user_id,
        "username": username,
        "coins": 0,                    
        "joined_at": datetime.now(),   
        "last_updated": datetime.now() 
    }
    users_col.update_one(
        {"user_id": user_id}, 
        {"$setOnInsert": user_data}, 
        upsert=True
    )

# ደረጃ 4፡ ሳንቲም ሲያገኙ ማዘመን
def update_coins_with_timestamp(user_id, amount):
    users_col.update_one(
        {"user_id": user_id},
        {
            "$inc": {"coins": amount},            
            "$set": {"last_updated": datetime.now()} 
        }
    )

# ደረጃ 3፡ የ /start ትዕዛዝ
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    register_user(user_id, username)
    bot.reply_to(message, "ሰላም! ወደ Kassa Mining Bot እንኳን ደህና መጡ። ማዕድን ማውጣት ይጀምሩ!")

# ለሙከራ: ተጠቃሚው ሲጫን ሳንቲም እንዲጨምር
@bot.message_handler(func=lambda message: message.text == "💰 ማዕድን ማውጣት")
def tap_mining(message):
    user_id = message.from_user.id
    update_coins_with_timestamp(user_id, 10) # 10 ኮይን ይጨምራል
    bot.reply_to(message, "10 ኮይን አግኝተዋል!")

print("🚀 Bot is running...")
bot.polling(none_stop=True)
