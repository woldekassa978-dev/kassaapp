# አዲስ ስራን ለመመዝገብ (ለምሳሌ: ቻናል መቀላቀል)
def complete_task(user_id, task_name, reward):
    # ተጠቃሚው ስራውን ሰርቶ ከሆነ አትድገም
    result = users_col.update_one(
        {"user_id": user_id, "completed_tasks": {"$ne": task_name}},
        {
            "$inc": {"coins": reward},
            "$push": {"completed_tasks": task_name}
        }
    )
    return result.modified_count > 0 # ስራው በተሳካ ሁኔታ ከተጠናቀቀ True ይመልሳል

# በቴሌግራም ላይ Task አዝራር ሲነካ
@bot.callback_query_handler(func=lambda call: call.data.startswith("task_"))
def handle_task_callback(call):
    user_id = call.from_user.id
    task_name = call.data  # ለምሳሌ: task_join_channel
    reward = 1000 # ለዚህ ስራ የሚሰጠው ሳንቲም
    
    if complete_task(user_id, task_name, reward):
        bot.answer_callback_query(call.id, f"✅ እንኳን ደስ አለዎት! {reward} ሳንቲም አግኝተዋል።")
    else:
        bot.answer_callback_query(call.id, "❌ ስራው ቀድሞ ተጠናቋል ወይም ስህተት ተፈጥሯል።")
