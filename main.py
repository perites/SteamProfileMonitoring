import sys

import logging
import handlers

import time
import datetime

import telebot

import config

from user_to_check import UserToCheck
from message import Message
from discrod_bot import DiscordBot
from file_class import File

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] : %(message)s  ||[LOGGER:%(name)s] [FUNC:%(funcName)s] [FILE:%(filename)s]',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(config.PATH_TO_LOGS, mode='a', encoding='utf-8'),
        handlers.TelegramBotHandler(config.TELEGRAM_BOT_TOKEN, config.admin_telegram_id, logging.ERROR)
    ]
)

logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("discord").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)


def main():
    logging.info("Starting main loop")

    user_to_check = UserToCheck(config.user_steam_id_to_check,
                                config.user_telegram_id_to_send_info,
                                config.user_discord_id_to_send_info,
                                notified_file=File(config.PATH_TO_NOTIFIED_FILE))

    message = Message(telegram_bot=telebot.TeleBot(config.TELEGRAM_BOT_TOKEN, threaded=False), discord_bot=DiscordBot(),
                      user_telegram_id=user_to_check.telegram_id, user_discord_id=user_to_check.discord_id,
                      admin_telegram_id=config.admin_telegram_id,
                      discord_channel_id=config.discord_channel_for_info)

    sale_end_datetime = datetime.datetime(2024, 7, 7, 23, 8)
    soon_end_datetime = sale_end_datetime - datetime.timedelta(minutes=2)

    counter = 0

    while True:
        user_has_game = user_to_check.check_if_has_game(config.game_to_check)
        logging.debug(f"Fetched new info, if has game : {user_has_game}")

        if user_has_game and not user_to_check.notified_data.bought_game_notified:
            logging.info("HAS GAME, sending messages")

            message.process_event("game_bought", user_to_check.discord_id)

            logging.info("Info that user has game had been sent")

            user_to_check.notified_data.bought_game_notified = True
            user_to_check.update_notified_data()

        elif not user_has_game:
            counter += 1
            logging.debug(f"+1 to counter, counter now : {counter}")

            if counter > 6 * 6 or counter == 1:
                logging.info("Sending message because of counter")
                message.process_event("counter_message")

                if counter > 1:
                    counter = 1

            current_datetime = datetime.datetime.now()
            if current_datetime > soon_end_datetime and not user_to_check.notified_data.soon_end_notified:
                logging.info("Sale end soon, sending messages")

                message.process_event("sale_ends_soon", user_to_check.discord_id)

                user_to_check.notified_data.soon_end_notified = True
                user_to_check.update_notified_data()

                logging.info("All notified about sale ending in 24 hours")

            elif current_datetime > sale_end_datetime and not user_to_check.notified_data.sale_ended_notified:
                logging.info("Sale ended, sending messages")

                message.process_event("sale_ended", user_to_check.discord_id)

                user_to_check.notified_data.sale_ended_notified = True
                user_to_check.update_notified_data()

                logging.info("All notified that sale ended(")

        time.sleep(60 * 10)


if __name__ == '__main__':
    try:
        main()
    except Exception as main_loop_exception:
        logging.critical("Error in main(), exiting file")
        logging.exception(main_loop_exception)
