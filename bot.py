def daily_mining_update(user_id):
    # ተጠቃሚው በየቀኑ በራሱ ጊዜ የሚያገኘው የሳንቲም ቦነስ
    daily_bonus = 50 
    users_col.update_one(
        {"user_id": user_id},
        {"$inc": {"coins": daily_bonus}}
    )
