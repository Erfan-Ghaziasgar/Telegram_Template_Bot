import os

import telebot
from dotenv import load_dotenv
from loguru import logger
from src.utils.io import read_json, write_json
from src.constants import KEYBOARDS
from Data import DATA_DIR


class Bot:
    def __init__(self):
        '''
        Initialize bot
        '''
        load_dotenv()
        BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)
        self.bot.message_handler(commands=['start', 'help'])(self.send_welcome)
        self.bot.message_handler(func=lambda message: True)(self.echo_all)

    def send_welcome(self, message):
        '''
        Send welcome message
        :param message: message
        '''
        self.bot.reply_to(message, "Howdy, how are you doing?")

    def echo_all(self, message):
        '''
        Echo all messages
        :param message: message
        '''
        write_json(message.json, DATA_DIR / "messages.json")
        self.bot.send_message(message.chat.id, message.text,
                              reply_markup=KEYBOARDS.main)

    def run(self):
        logger.info("Bot running...")
        self.bot.infinity_polling()


if __name__ == '__main__':
    logger.info("Bot started")
    bot = Bot()
    bot.run()
