from telebot import TeleBot
from config import text_1
from markup import main_keyboard




class StartHandler:

    def __init__(self, bot) -> None:
        self.bot = bot
    
    def start(self):
        @self.bot.message_handler(commands=["start"])
        def wellcome(message):
            self.bot.send_message(message.chat.id, text=text_1, reply_markup=main_keyboard())