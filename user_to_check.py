import logging
import requests

import json
import time
import urllib.parse
from dataclasses import dataclass

import constants
import utils.json_file as file


@dataclass
class NotifiedData:
    bought_game_notified: bool = None
    sale_soon_ends_notified: bool = None
    sale_ended_notified: bool = None


@dataclass
class UserToCheck:
    steam_id: str
    telegram_id: str
    discord_id: int

    path_to_notified_file: str
    notified_file: file.File = None
    notified_data: NotifiedData = None

    logger: logging.Logger = None

    def __post_init__(self):
        self.notified_file = file.File(self.path_to_notified_file)
        self.notified_data = NotifiedData(**self.notified_file.read_data())
        self.logger = logging.getLogger(f"user-{self.steam_id}")

    def check_if_has_game(self, game_id):
        request_json = urllib.parse.quote(
            json.dumps({
                "appids_filter": [game_id],
                "steamid": self.steam_id
            }))

        answer = self._send_request(request_json).json()

        game_count = answer['response'].get('game_count')
        if game_count is None:
            self.logger.error(f"Got hollow response : '{answer}', waiting for 1 hour")
            time.sleep(60 * 60)

        return True if game_count == 1 else False

    def _send_request(self, request_json):
        max_retries = 5
        retry_delay = 30

        for _ in range(max_retries):
            try:
                answer = requests.get(
                    f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={constants.STEAM_API_KEY}&format=json&input_json={request_json}")
                return answer

            except Exception:
                self.logger.exception("Error while making request to SteamAPI")
                time.sleep(retry_delay)

        raise Exception("Connection error for 5 times, exiting loop")

    def update_notified_file(self):
        self.notified_file.write_data(self.notified_data.__dict__)
