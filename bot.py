# ይህ ተግባር የሪፈራል ቦነስን በሰርቨር ደረጃ ይፈጽማል
def process_referral(referrer_id, new_user_id):
    try:
        # ጋባዡ ሰው እና አዲሱ ተጠቃሚ አንድ አይነት መሆን የለባቸውም
        if str(referrer_id) != str(new_user_id):
            # ለጋባዡ ሰው 5,000 ሳንቲም ይጨምራል
            result = users_col.update_one(
                {"user_id": int(referrer_id)},
                {"$inc": {"coins": 5000}}
            )
            if result.modified_count > 0:
                print(f"✅ Referral bonus of 5000 added to {referrer_id}")
    except Exception as e:
        print(f"Error processing referral: {e}")

# /start ትዕዛዝን ሙሉ በሙሉ በዚህ መልክ ያዘምኑ
@bot.message_handler(commands=['start'])
def start_message(message):
    args = message.text.split()
    user_id = message.from_user.id
    username = message.from_user.username
    
    # 1. አዲስ ተጠቃሚ ከሆነ እና ሪፈራል ካለው ቦነስ አድርግ
    if len(args) > 1:
        referrer_id = args[1]
        process_referral(referrer_id, user_id)
        
    # 2. ተጠቃሚውን መዝግብ (አልተመዘገበ ከሆነ)
    users_col.update_one(
        {"user_id": user_id},
        {"$setOnInsert": {"user_id": user_id, "username": username, "coins": 500}}, 
        upsert=True
    )
    
    bot.reply_to(message, "እንኳን ወደ Kassa Mining Bot በደህና መጡ! ማዕድን ማውጣት ይጀምሩ።")
