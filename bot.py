import os
import telebot
import threading
import time
import json
from pymongo import MongoClient
from datetime import datetime

# Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")

bot = telebot.TeleBot(BOT_TOKEN)
client = MongoClient(MONGO_URI)
db = client['kassa_mining_db']
users_col = db['users']

# 1. Auto-compounding (በየ 24 ሰዓቱ 0.9% ይጨምራል)
def daily_auto_compound():
    while True:
        time.sleep(86400) 
        users_col.update_many({}, {"$inc": {"coins": {"$multiply": ["$coins", 0.009]}}})
        print("📈 Auto-compound applied.")

threading.Thread(target=daily_auto_compound, daemon=True).start()

# 2. Task Completion (ስራ ሲጠናቀቅ ሳንቲም ይጨምራል)
def complete_task(user_id, task_name, reward):
    result = users_col.update_one(
        {"user_id": user_id, "completed_tasks": {"$ne": task_name}},
        {"$inc": {"coins": reward}, "$push": {"completed_tasks": task_name}},
        upsert=True
    )
    return result.modified_count > 0

# /start ትዕዛዝ
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    users_col.update_one(
        {"user_id": user_id},
        {"$setOnInsert": {"user_id": user_id, "coins": 500, "completed_tasks": []}},
        upsert=True
    )
    bot.reply_to(message, "እንኳን ደህና መጡ! ማዕድን ማውጣት ይጀምሩ።")

# 3. Web App Data (ከ Mini App የሚላክ መረጃን መቀበል)
@bot.message_handler(content_types=['web_app_data'])
def handle_webapp_data(message):
    data = json.loads(message.web_app_data.data)
    user_id = message.from_user.id
    
    if data.get('action') == "task_completed":
        task_name = data.get('task')
        if complete_task(user_id, task_name, 1000):
            bot.send_message(user_id, "✅ ስራው ተጠናቀቀ! 1000 ሳንቲም አግኝተዋል።")
        else:
            bot.send_message(user_id, "❌ ስራው ቀድሞ ተጠናቋል!")

bot.polling(none_stop=True)
