import logging

import telebot


class TelegramBotHandler(logging.Handler):
    def __init__(self, bot_token, chat_id_to_sent_logs, min_level):
        super().__init__()
        self.bot = telebot.TeleBot(bot_token, threaded=False)
        self.chat_id = chat_id_to_sent_logs
        self.min_level = min_level

    def emit(self, record):
        if record.levelno >= self.min_level:
            log_entry = self.format(record)
            self.send_log(log_entry)

    def send_log(self, log_entry):
        self.bot.send_message(self.chat_id, log_entry)
