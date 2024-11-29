from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup



def routin_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("پاک کردن❌", callback_data="remove_routin") 
    button2 = InlineKeyboardButton("اضافه کردن📝", callback_data="add_routin")
    button3 = InlineKeyboardButton("تیک زدن✅", callback_data="set_routine_status")
    button4 = InlineKeyboardButton("مشاهده لیست", callback_data="veiw_routine_list")
    button5 = InlineKeyboardButton("برگشتن", callback_data="back_to_main") 
    markup.add(button1 ,button2).add(button3, button4).add(button5)
    return markup

 
def delete_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("خالی کردن لیست", callback_data="delet_all")
    markup.add(button1)
    return markup


def confirmation_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("بله", callback_data="Yes") 
    button2 = InlineKeyboardButton("خیر", callback_data="No")
    markup.add(button1, button2)
    return markup


def comeback_routin_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("برگشتن", callback_data="back_to_routine_menu") 
    markup.add(button1)
    return markup


def cancel_keyboard():
    markup = InlineKeyboardMarkup()
    butten = InlineKeyboardButton("انصراف", callback_data="back_to_routine_menu")
    markup.add(butten)
    return markup