from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup



def main_keyboard():
    markup = InlineKeyboardMarkup()
    # TODO:add in future
    # button1 = InlineKeyboardButton("فعالیت های آینده", callback_data="future_activities") 
    button2 = InlineKeyboardButton("فعالیت های روتین🔖", callback_data="routin_activities")
    markup.add(button2)
    return markup