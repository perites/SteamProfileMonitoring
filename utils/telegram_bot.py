import logging

import telebot


class TelegramBot:
    def __init__(self, telegram_bot_token):
        self.bot = telebot.TeleBot(telegram_bot_token, threaded=False)

        self.logger = logging.getLogger("telegram-bot")

    def send_message(self, chat_id, message):
        self.bot.send_message(chat_id, message)
        self.logger.debug(f"Message to {chat_id} sent")
