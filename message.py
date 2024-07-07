import logging
import texts


class Message:
    def __init__(self, telegram_bot, discord_bot,
                 user_telegram_id, user_discord_id,
                 admin_telegram_id,
                 discord_channel_id):
        self.logger = logging.getLogger("message")

        self.telegram_bot = telegram_bot
        self.discord_bot = discord_bot

        self.user_telegram_id = user_telegram_id
        self.user_discord_id = user_discord_id

        self.admin_telegram_id = admin_telegram_id

        self.discord_channel_id = discord_channel_id

    def send_telegram_to_user(self, message):
        self.telegram_bot.send_message(chat_id=self.user_telegram_id, text=message)
        self.logger.debug("message to user sent")

    def send_telegram_to_admin(self, message):
        self.telegram_bot.send_message(chat_id=self.admin_telegram_id, text=message)
        self.logger.debug("message to admin sent")

    def send_discord_channel(self, message):
        self.discord_bot.send_message(self.discord_channel_id, message=message)
        self.logger.debug("message to discord sent")

    def _send_message(self, text_for_user=None, text_for_admin=None, text_for_dchannel=None):
        self.logger.info(
            f"going to notify :"
            f"{'user' if text_for_user else ''} "
            f"{'admin' if text_for_admin else ''} "
            f"{'dchannel' if text_for_dchannel else ''}")

        if text_for_user:
            self.send_telegram_to_user(text_for_user)

        if text_for_admin:
            self.send_telegram_to_admin(text_for_admin)

        if text_for_dchannel:
            self.send_discord_channel(text_for_dchannel)

        self.logger.info("successfully notified")

    def process_event(self, event, *f_args, **f_kwargs):
        text = texts.get_event_text(event, *f_args, **f_kwargs)

        self._send_message(**text)
