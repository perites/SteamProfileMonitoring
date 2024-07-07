import logging
import requests

import json
import time
import urllib.parse
from dataclasses import dataclass

import config


class UserToCheck:
    def __init__(self, steam_id, telegram_id, discord_id, notified_file):
        self.logger = logging.getLogger("user-check")

        self.steam_id = steam_id
        self.telegram_id = telegram_id
        self.discord_id = discord_id

        self.notified_file = notified_file
        self.notified_data = None
        self.get_notified_data()

    def check_if_has_game(self, game_id):
        request_json = urllib.parse.quote(
            json.dumps({
                "appids_filter": [game_id],
                "steamid": self.steam_id
            }))

        answer = None
        error_counter = 0
        while not answer:
            try:
                answer = requests.get(
                    f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={config.STEAM_API_KEY}&format=json&input_json={request_json}")
            except ConnectionError:
                self.logger.exception("Error while making request to SteamAPI")
                error_counter += 1
                if error_counter >= 5:
                    raise Exception("Connection error for 5 times, exiting loop")

                time.sleep(30)

        answer_json = answer.json()

        game_count = answer_json['response'].get('game_count')
        if game_count is None:
            self.logger.error(f"Got hollow response : '{answer_json}', waiting for 1 hour")
            time.sleep(60 * 60)

        return True if game_count == 1 else False

    def get_notified_data(self):
        raw_notified_data = self.notified_file.read_data()
        self.notified_data = NotifiedData(**raw_notified_data)

    def update_notified_data(self):
        self.notified_file.write_data(self.notified_data.__dict__)


@dataclass
class NotifiedData:
    bought_game_notified: bool
    soon_end_notified: bool
    sale_ended_notified: bool
