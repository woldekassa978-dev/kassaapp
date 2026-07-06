import os
import telebot
from pymongo import MongoClient

# 1. የቴሌግራም ቦት እና የዳታቤዝ ማገናኛ (Environment Variables)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
import os
# ... ሌሎች ኮዶች ...
MONGO_URI = os.getenv("MONGO_URI")
# ይህ መስመር Render ላይ ያስቀመጥነውን ሊንክ በራሱ ይወስደዋል

bot = telebot.TeleBot(BOT_TOKEN)

# ዳታቤዝ ግንኙነት መፈchecking
try:
    client = MongoClient(MONGO_URI)
    db = client['kassa_mining_db']
    users_col = db['users']
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ Database connection error: {e}")
    users_col = None

# 2. ተጠቃሚው ለመጀመሪያ ጊዜ ቦቱን ሲያስነሳ (/start)
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    username = message.from_user.username or "User"
    first_name = message.from_user.first_name or "Kassa Miner"
    
    # የግብዣ ሊንክ ተጭኖ ከሆነ የመጣበትን ID መለየት (e.g., /start r_123456)
    text_args = message.text.split()
    referrer_id = None
    
    if len(text_args) > 1 and text_args[1].startswith("r_"):
        try:
            referrer_id = int(text_args[1].replace("r_", ""))
        except ValueError:
            referrer_id = None

    if users_col is None:
        bot.reply_to(message, "⚠️ System maintenance. Please try again later.")
        return

    # ተጠቃሚው ቀድሞ በዳታቤዝ ላይ መኖሩን ማረጋገጥ
    existing_user = users_col.find_one({"user_id": user_id})
    
    if not existing_user:
        # አዲስ ተጠቃሚ ከሆነ መመዝገብ (የመጀመሪያ ስጦታ 5,000 ሳንቲም)
        new_user = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "balance": 5000,
            "referred_by": referrer_id,
            "friends_invited": 0
        }
        users_col.insert_one(new_user)
        
        # ጋባዥ (Referrer) ካለ ለጋባዡ +5,000 ሳንቲም መጨመር
        if referrer_id and referrer_id != user_id:
            referrer_user = users_col.find_one({"user_id": referrer_id})
            if referrer_user:
                users_col.update_one(
                    {"user_id": referrer_id},
                    {
                        "$inc": {"balance": 5000, "friends_invited": 1}
                    }
                )
                # ለጋባዡ የደስታ ማብሰያ መልዕክት መላክ
                try:
                    bot.send_message(referrer_id, f"🎉 Great news! {first_name} joined via your link. You earned +5,000 Kassa Coins!")
                except Exception:
                    pass

        welcome_text = (
            f"👋 Welcome {first_name} to Kassa Mining Bot!\n\n"
            f"💰 Start tapping, complete tasks, and mine your way to Web3 rewards.\n\n"
            f"🚀 Tap the button below to open the Web App and start mining now!"
        )
    else:
        welcome_text = f"👋 Welcome back, {first_name}! Ready to mine more Kassa Coins? Tap the button below to launch the app!"

    # 3. የዌብ አፑን የሚከፍት የቴሌግራም አዝራር (Inline Keyboard) ማዘጋጀት
    # ማሳሰቢያ፦ ከታች ያለውን የቪርሴል ሊንክ በአንተ እውነተኛ የቪርሴል አፕ ሊንክ ቀይረው
    web_app_url = "https://kassaapp-ten.vercel.app/" 
    
    keyboard = telebot.types.InlineKeyboardMarkup()
    web_app_button = telebot.types.InlineKeyboardButton(
        text="🎮 Play & Mine Kassa", 
        web_app=telebot.types.WebAppInfo(url=web_app_url)
    )
    keyboard.add(web_app_button)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)

# ቦቱን በቋሚነት ማሰራት
if __name__ == "__main__":
    print("🚀 Kassa Mining Backend Bot is running...")
    bot.infinity_polling()
