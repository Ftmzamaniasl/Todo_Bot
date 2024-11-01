from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("فعالیت های آینده", callback_data="future_activities") 
    button2 = InlineKeyboardButton("فعالیت های روتین🔖", callback_data="routin_activities")
    markup.add(button2).add(button1)
    return markup

def routin_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("پاک کردن❌", callback_data="remove_routin") 
    button2 = InlineKeyboardButton("اضافه کردن📝", callback_data="add_routin")
    button3 = InlineKeyboardButton("تیک زدن✅", callback_data="set_routine_status")
    button4 = InlineKeyboardButton("مشاهده لیست", callback_data="veiw_routine_list")
    button5 = InlineKeyboardButton("برگشتن", callback_data="back_to_main") 
    markup.add(button1 ,button2).add(button3, button4).add(button5)
    return markup


def comeback_routin_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("برگشتن", callback_data="back_to_routine_menu") 
    markup.add(button1)
    return markup
