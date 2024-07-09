import sys

import logging
from utils.logging_handlers import TelegramBotHandler

import time
import datetime

from utils.discrod_bot import DiscordBot
from utils.telegram_bot import TelegramBot

import constants
from config import RUN_CONFIG as config

import user_to_check as utch
import texts

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] : %(message)s  ||[LOGGER:%(name)s] [FUNC:%(funcName)s] [FILE:%(filename)s]',
    datefmt='%d-%m-%y %H:%M:%S',
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(constants.PATH_TO_LOGS, mode='a', encoding='utf-8'),
        TelegramBotHandler(constants.TELEGRAM_BOT_TOKEN, constants.ADMIN_TELEGRAM_ID, logging.ERROR)
    ]
)

logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("discord").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)


def main():
    logging.info("Starting main loop")

    user_to_check = utch.UserToCheck(config.user_steam_id_to_check,
                                     config.user_telegram_id_to_send_info,
                                     config.user_discord_id_to_send_info,
                                     path_to_notified_file=constants.PATH_TO_NOTIFIED_FILE)

    telegram_bot = TelegramBot(constants.TELEGRAM_BOT_TOKEN)
    discord_bot = DiscordBot(constants.DISCORD_BOT_TOKEN)

    def notify_all(event):
        telegram_bot.send_message(user_to_check.telegram_id, message=texts.get_text(f"{event}_user"))

        telegram_bot.send_message(constants.ADMIN_TELEGRAM_ID, message=texts.get_text(f"{event}_admin"))

        discord_bot.send_message_to_channel(config.discord_channel_for_info, message=texts.get_text(f"{event}_dchannel",
                                                                                                    user_to_check.discord_id))

    counter = 0

    while True:
        user_has_game = user_to_check.check_if_has_game(constants.GAME_ID_TO_CHECK)
        logging.debug(f"Fetched new info, if has game: {user_has_game}")

        if user_has_game:
            if user_to_check.notified_data.bought_game_notified:
                logging.debug("User bought game, already notified")
                telegram_bot.send_message(constants.ADMIN_TELEGRAM_ID,
                                          texts.get_text("already_notified_game_bought_admin"))
                time.sleep(config.if_has_game_request_interval_s)
                continue

            logging.info("User bought game")

            notify_all("game_bought")
            user_to_check.notified_data.bought_game_notified = True
            user_to_check.update_notified_file()

            logging.info("Info that user bought game sent")

        elif not user_has_game:
            counter += 1
            logging.debug(f"Counter +1, counter now: {counter}")

            if counter > config.counter_value_to_send or counter == 1:
                logging.info("Sending message because of counter")

                telegram_bot.send_message(constants.ADMIN_TELEGRAM_ID, message=texts.get_text("counter_message_admin"))
                if counter > 1:
                    counter = 1

            current_datetime = datetime.datetime.now()
            if current_datetime > config.sale_soon_ends_datetime and not user_to_check.notified_data.sale_soon_ends_notified:
                logging.info("Sale ends soon, sending messages")

                notify_all("sale_ends_soon")
                user_to_check.notified_data.sale_soon_ends_notified = True
                user_to_check.update_notified_file()

                logging.info("All notified about sale ends soon")

            elif current_datetime > config.sale_end_datetime and not user_to_check.notified_data.sale_ended_notified:
                logging.info("Sale ended, sending messages")

                notify_all("sale_ended")
                user_to_check.notified_data.sale_ended_notified = True
                user_to_check.update_notified_file()

                logging.info("All notified about sale ended(")

        time.sleep(config.if_has_game_request_interval_s)


if __name__ == '__main__':
    try:
        main()
    except Exception as main_loop_exception:
        logging.critical("Error in main(), exiting file")
        logging.exception(main_loop_exception)
