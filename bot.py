# አዲስ ተጠቃሚ በሪፈራል ሲመዘገብ የሚሰራ
def process_referral(referrer_id, new_user_id):
    if referrer_id and referrer_id != new_user_id:
        # ጋባዡ ሰው ላይ 5000 ሳንቲም ይጨምራል
        users_col.update_one(
            {"user_id": int(referrer_id)},
            {"$inc": {"coins": 5000}}
        )
        print(f"✅ Referral bonus added to {referrer_id}")

# /start ትዕዛዝን ማሻሻል
@bot.message_handler(commands=['start'])
def start_message(message):
    args = message.text.split()
    user_id = message.from_user.id
    
    # ሪፈራል ካለ ፈልግ
    if len(args) > 1:
        referrer_id = args[1]
        process_referral(referrer_id, user_id)
        
    # ተጠቃሚ መመዝገብ
    users_col.update_one(
        {"user_id": user_id},
        {"$setOnInsert": {"user_id": user_id, "coins": 500, "joined_at": datetime.now()}},
        upsert=True
    )
    bot.reply_to(message, "እንኳን ወደ Kassa Mining Bot በደህና መጡ! ማዕድን ማውጣት ይጀምሩ።")
