import logging

import telebot

from texts import get_text
from utils.discrod_bot import DiscordBot


class Messages:
    def __init__(self, telegram_bot_token, discord_bot_token):
        self.logger = logging.getLogger("messages")

        self.telegram_bot = telebot.TeleBot(telegram_bot_token, threaded=False)
        self.discord_bot = DiscordBot(discord_bot_token)

    def send_telegram(self, chat_id, text_name, *args, **kwargs):
        self.telegram_bot.send_message(chat_id=chat_id, text=get_text(text_name, *args, **kwargs))
        self.logger.debug(f"message in telegram to {chat_id} sent")

    def send_discord_channel(self, dchannel_id, text_name, *args, **kwargs):
        self.discord_bot.send_message(dchannel_id, message=get_text(text_name, *args, **kwargs))
        self.logger.debug(f"message to dchannel {dchannel_id} sent")
