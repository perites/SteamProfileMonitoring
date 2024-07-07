import sys

import logging
import requests

import time
import datetime
import json
import urllib.parse
import asyncio

import telebot
import discord

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
logging.getLogger("discord").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)


class DiscordBot:
    def __init__(self):
        self.discord_bot = None
        self.logger = logging.getLogger("discord-bot")

    async def _send_message(self, channel_id, message):
        @self.discord_bot.event
        async def on_ready():
            channel = self.discord_bot.get_channel(channel_id)
            if channel:
                await channel.send(message)
                self.logger.debug(f"message to channel {channel_id} sent")
            else:
                self.logger.error(f"Channel {channel_id} not found")

            await self.discord_bot.close()

        await self.discord_bot.start(config.DISCORD_BOT_TOKEN)
        await self.discord_bot.http._HTTPClient__session.close()

    def send_message(self, channel_id, message):
        try:
            self.discord_bot = discord.Client(intents=discord.Intents.default())
            asyncio.run(self._send_message(channel_id, message))

        except Exception as e:
            self.logger.exception(f"Error while sending message to {channel_id}")


def check_if_user_has_game(steam_id, game_id):
    request_json = urllib.parse.quote(
        json.dumps({
            "appids_filter": [game_id],
            "steamid": steam_id
        }))

    answer = None
    error_counter = 0
    while not answer:
        try:
            answer = requests.get(
                f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={config.STEAM_API_KEY}&format=json&input_json={request_json}")
        except ConnectionError as e:
            logging.exception("Error while making request to SteamAPI")
            error_counter += 1
            if error_counter >= 5:
                raise Exception("Connection error for 5 times, exiting loop")
            time.sleep(30)

    answer_json = answer.json()

    game_count = answer_json['response'].get('game_count')
    if game_count is None:
        logging.error(f"Got hollow response : '{answer_json}', waiting for 1 hour")
        time.sleep(60 * 60)

    return True if game_count == 1 else False


def main():
    logging.info("Starting main loop")

    try:
        telegram_bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN, threaded=False)
        discord_bot = DiscordBot()

        counter = 0
        soon_end_notified = False
        sale_end_notified = False
        bought_game_notified = False

    except Exception as e:
        logging.critical("error during initialization, exiting")
        logging.exception(e)
        sys.exit(1)

    try:
        while True:
            user_has_game = check_if_user_has_game(config.user_to_check, config.game_to_check)
            logging.debug(f"Fetched new info, if has game : {user_has_game}")

            if user_has_game and not bought_game_notified:
                logging.info("HAS GAME, sending messages")

                telegram_bot.send_message(chat_id=config.user_to_send_info,
                                          text="О, купив нарешті, сподіваюсь все інше вже допройшов, щоб як тільки я приїду ОДРАЗУ Ж пішли 😈")

                telegram_bot.send_message(chat_id=config.admin_to_send_info, text="ПЕРЕМОГА БУДЕ, купив купив купив")

                discord_bot.send_message(config.discord_channel_for_info,
                                         f"ПЕРЕМОГА БУДЕ, <@{config.user_to_send_info_discord}> купив секіро, мої вітання")

                logging.info("Info that user has game had been sent")

                bought_game_notified = True

            elif not user_has_game:
                counter += 1
                logging.debug(f"+1 to counter, counter now : {counter}")

                if counter > 6 * 6 or counter == 1:
                    telegram_bot.send_message(chat_id=config.admin_to_send_info, text="Ні, ще не купив ( ")
                    logging.info("Sent messages because of counter")

                    if counter > 1:
                        counter = 1

                current_datetime = datetime.datetime.now()
                if current_datetime > datetime.datetime(2024, 7, 10, 18, 00) and not soon_end_notified:
                    telegram_bot.send_message(chat_id=config.user_to_send_info,
                                              text='Скоро кінець літнього розпродажу ( менш ніж за 24 години ), а ти ще не купив Cекіро, так не піде.\n Ознайомтесь: https://store.steampowered.com/app/814380/Sekiro_Shadows_Die_Twice__GOTY_Edition/')

                    telegram_bot.send_message(chat_id=config.admin_to_send_info,
                                              text="кінець розпродажу за 24 години а він ще не купив, нагадування надіслано")

                    discord_bot.send_message(config.discord_channel_for_info,
                                             message=f"Літній розпродаж закінчується менш ніж за 24 години, саме час купувати все що відкладали (<@{config.user_to_send_info_discord}>)")

                    soon_end_notified = True

                    logging.info("Notified about sale ending in 24 hours")

                elif current_datetime > datetime.datetime(2024, 7, 11, 18, 00) and not sale_end_notified:
                    telegram_bot.send_message(chat_id=config.user_to_send_info,
                                              text='Літній розпродаж,закінчився, а ти ще не купив секіро, це зрада.\nНу що ж, тепер прийдеться купити за 2к 😈\nhttps://store.steampowered.com/app/814380/Sekiro_Shadows_Die_Twice__GOTY_Edition/')

                    telegram_bot.send_message(chat_id=config.admin_to_send_info,
                                              text="розпродаж закінчився а він ще не купив, пахне зрадою , нагадування надіслано")

                    discord_bot.send_message(config.discord_channel_for_info,
                                             message=f"Літній розпродаж закінчився, а хтось (<@{config.user_to_send_info_discord}>) так і не купив що мав купити (")

                    sale_end_notified = True

                    logging.info("Notified that sale endeded(")

            time.sleep(60 * 10)

    except Exception as e:
        logging.critical(
            f"error in main loop, exiting")
        logging.exception(e)

        telegram_bot.send_message(chat_id=config.admin_to_send_info,
                                  text=f"error in main loop : {e}\ncheck logs {config.link_to_logs}")

        logging.info("Exiting program")
        sys.exit(1)


if __name__ == '__main__':
    main()
