# TODO add discord messages just to general channel
# deploy : change to send dania in YES , change to send in General

import sys

import time
import datetime

import logging
import requests

import telebot

import config

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] : %(message)s  ||[LOGGER:%(name)s] [FUNC:%(funcName)s] [FILE:%(filename)s]',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(config.PATH_TO_LOGS, mode='a', encoding='utf-8', )
    ]
)

logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.ERROR)


def get_user_games_info(steam_id):
    answer = requests.get(
        f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={config.API_KEY}&steamid={steam_id}&format=json")

    answer = answer.json()

    if not answer['response'].get("games"):
        logging.error(f'Got responce without "games" keyword : "{answer}"')

    return answer['response']


def check_if_has_game(all_user_games, game_to_check_id):
    for game_info in all_user_games:
        if game_info['appid'] == game_to_check_id:
            return True

    return False


def main():
    logging.info("Starting main loop")

    try:
        telegram_bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN, threaded=False)
        counter = 0
        soon_end_notified = False

        user_all_games_info = None
    except Exception as e:
        logging.critical("error during initialization, exiting")
        logging.exception(e)
        sys.exit(1)

    try:
        while True:
            current_datetime = datetime.datetime.now()
            user_all_games_info = get_user_games_info(config.user_to_check)
            if not user_all_games_info:
                logging.error("Responce came as None, waiting for 5 minutes")
                telegram_bot.send_message(config.admin_to_send_info,
                                          text=f"Responce came as None, waiting for 5 minutes, watch logs \n{config.link_to_logs} ")

                time.sleep(60 * 5)
                continue

            user_games_info = user_all_games_info['games']
            user_has_game = check_if_has_game(user_games_info, config.game_to_check)
            logging.debug(f"Fetched new info, if has game : {user_has_game}")

            if user_has_game:
                logging.debug("HAS GAME, sending messages")

                telegram_bot.send_message(chat_id=config.user_to_send_info,
                                          text="О, купив нарешті, сподіваюсь все інше вже допройшов, щоб як тільки я приїду ОДРАЗУ Ж пішли 😈")

                telegram_bot.send_message(chat_id=config.admin_to_send_info, text="ПЕРЕМОГА БУДЕ, купив купив купив")

                # discord.general.send ( YES!  )

                logging.info("Info that user has game had been sent, exiting main loop")
                break

            else:
                counter += 1
                logging.debug(f"+1 to counter, counter now : {counter}")

                if counter > 30 * 4 or counter == 1:
                    telegram_bot.send_message(chat_id=config.admin_to_send_info, text="Ні, ще не купив ( ")
                    logging.debug("Sent messages because of counter")

                    if counter > 1:
                        counter = 1

                    soon_end_notified = False

                if current_datetime > datetime.datetime(2024, 7, 10, 18, 00) and not soon_end_notified:
                    telegram_bot.send_message(chat_id=config.user_to_send_info,
                                              text='Скоро кінець літнього розпродажу ( менш ніж за 24 години ), а ти ще не купив Cекіро, так не піде.\n Ознайомтесь: https://store.steampowered.com/app/814380/Sekiro_Shadows_Die_Twice__GOTY_Edition/')

                    telegram_bot.send_message(chat_id=config.admin_to_send_info,
                                              text="кінець розпродажу за 24 години а він ще не купив, нагадування надіслано")

                    soon_end_notified = True

                    logging.info("Notified about sale ending in 24 hours")

                elif current_datetime > datetime.datetime(2024, 7, 11, 18, 00):
                    telegram_bot.send_message(chat_id=config.user_to_send_info,
                                              text='Літній розпродаж,закінчився, а ти ще не купив секіро, це зрада.\nНу що ж, тепер прийдеться купити за 2к 😈\nhttps://store.steampowered.com/app/814380/Sekiro_Shadows_Die_Twice__GOTY_Edition/')

                    telegram_bot.send_message(chat_id=config.admin_to_send_info,
                                              text="розпродаж закінчився а він ще не купив, пахне зрадою , нагадування надіслано")

                    logging.info("Notified that sale endeded(")

            time.sleep(60 * 2)

    except Exception as e:
        logging.critical(
            f"error in main loop, user_all_games_info : '{user_all_games_info}', exiting")
        logging.exception(e)

        telegram_bot.send_message(chat_id=config.admin_to_send_info,
                                  text=f"error in main loop, check logs {config.link_to_logs}")

    logging.info("Exiting program")
    sys.exit(1)


if __name__ == '__main__':
    main()
