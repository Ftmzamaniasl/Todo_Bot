from Base.message import welcome_message
from Base.markup import main_keyboard




def handle(bot):
    @bot.message_handler(commands=["start"])
    def wellcome(message):
        bot.send_message(message.chat.id, text=welcome_message, reply_markup=main_keyboard())