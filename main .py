from telebot import TeleBot
import Base.handler
import Routine.handler
from config import *
import Base
import Routine


class TelBot:

    def __init__(self):
        self.token = token
        self.bot = TeleBot(self.token)


    def start(self):
        Base.handler.handle(self.bot)
        Routine.handler.handle(self.bot)
        

    def run_bot(self):
        self.start()
        self.bot.polling(none_stop=True)



if __name__ == "__main__":
    bot = TelBot()
    bot.run_bot()


