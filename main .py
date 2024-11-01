from telebot import TeleBot
from config import *


class TelBot:

    def __init__(self):
        self.token = token
        self.bot = TeleBot(self.token)
        # self.handler = HandlerMain(self.bot)


    def start(self):
        self.handler.handle()


    def run_bot(self):
        self.start()
        self.bot.polling(none_stop=True)



if __name__ == "__main__":
    bot = TelBot()
    bot.run_bot()


