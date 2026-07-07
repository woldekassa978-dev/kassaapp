# አንድ ሳንቲም የሚያወጣው ብር
RATE_PER_COIN = 0.05 

def get_real_value(coins):
    # ሳንቲሙን ወደ ብር ይቀይራል
    etb_value = coins * RATE_PER_COIN
    return etb_value
