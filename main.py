import sys

import time

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
        logging.FileHandler("main.log", mode='w', encoding='utf-8', )
    ]
)

logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.ERROR)


def get_user_games_info(steam_id):
    answer = requests.get(
        f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={config.API_KEY}&steamid={steam_id}&format=json")
    answer = answer.json()['response']

    return answer


def check_if_has_game(all_user_games, game_to_check_id):
    for game_info in all_user_games:
        if game_info['appid'] == game_to_check_id:
            return True

    return False


def main_cycle():
    logging.info("Starting main loop")

    try:
        bot = telebot.TeleBot(config.BOT_TOKEN, threaded=False)
        counter = 0
    except Exception as e:
        logging.exception("error during initialization")

    while True:
        try:
            user_has_game = check_if_has_game(get_user_games_info(config.user_to_check)['games'], config.game_to_check)
            logging.debug(f"Fetched new info, if has game : {user_has_game}")
            if user_has_game:
                logging.debug("HAS GAME, sending messages")
                bot.send_message(chat_id=config.telegram_ids['perite'],
                                 text="Купив нарешті, сподіваюсь все інше вже допройшовб, щоб як тільки я приїду ОДРАЗУ Ж пішли")

                bot.send_message(chat_id=config.telegram_ids['perite'], text="ПЕРЕМОГА БУДЕ, купив купив купив")
                # discord.send ( YES!  )
                # discord.dm.send( YES! )
                logging.info("Info that user has game had been sent, exiting main loop")
                break
            else:
                counter += 1
                logging.debug(f"+1 to counter, counter now : {counter}")

            if counter > 60 * 4 or counter == 1:
                bot.send_message(chat_id=config.telegram_ids['perite'], text="Ні, ще не купив ( ")
                logging.debug("Sent messages because of counter")

            time.sleep(60)
        except Exception as e:
            logging.exception("error in main loop, program still running")
            bot.send_message(chat_id=config.telegram_ids['perite'],
                             text=f"error in main loop, check logs {config.link_to_logs}")

    logging.info("Exiting program")


main_cycle()
