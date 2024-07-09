import datetime
from dataclasses import dataclass, field

from constants import STEAM_IDS, TELEGRAM_IDS, DISCORD_IDS, DISCORD_CHANNEL_IDS


@dataclass
class Config:
    config_type: str

    user_steam_id_to_check: str
    user_telegram_id_to_send_info: str
    user_discord_id_to_send_info: str

    discord_channel_for_info: int

    if_has_game_request_interval_s: int
    counter_send_every: tuple[float, str]

    sale_end_datetime: datetime.datetime
    sale_soon_ends_diff: datetime.timedelta
    sale_soon_ends_datetime: datetime.datetime = None

    counter_value_to_send: int = None

    periods: dict[str, int] = field(default_factory=lambda: {"hours": (60 * 60), "minutes": 60, "seconds": 1})

    def __post_init__(self):
        self.sale_soon_ends_datetime = self.sale_end_datetime - self.sale_soon_ends_diff

        self.counter_value_to_send = int(
            self._interval_repeats_per(self.counter_send_every[1]) * self.counter_send_every[0])

    def _interval_repeats_per(self, period_name):
        period_time = self.periods[period_name]
        interval_per_period = period_time / self.if_has_game_request_interval_s
        return interval_per_period


has_game_TEST_config = Config(
    config_type="test",

    user_steam_id_to_check=STEAM_IDS['perite'],
    user_telegram_id_to_send_info=TELEGRAM_IDS['perite'],
    user_discord_id_to_send_info=DISCORD_IDS['perite'],
    discord_channel_for_info=DISCORD_CHANNEL_IDS['fake_general'],

    if_has_game_request_interval_s=20,
    counter_send_every=(0.5, "minutes"),

    sale_end_datetime=datetime.datetime.now() + datetime.timedelta(minutes=4),
    sale_soon_ends_diff=datetime.timedelta(minutes=2),

)

no_game_TEST_config = Config(
    config_type="test",

    user_steam_id_to_check=STEAM_IDS['azuma'],
    user_telegram_id_to_send_info=TELEGRAM_IDS['perite'],
    user_discord_id_to_send_info=DISCORD_IDS['perite'],
    discord_channel_for_info=DISCORD_CHANNEL_IDS['fake_general'],

    if_has_game_request_interval_s=10,
    counter_send_every=(30, "seconds"),

    sale_end_datetime=datetime.datetime.now() + datetime.timedelta(minutes=2),
    sale_soon_ends_diff=datetime.timedelta(minutes=1),

)

deploy_config = Config(
    config_type="deploy",

    user_steam_id_to_check=STEAM_IDS['paradise'],
    user_telegram_id_to_send_info=TELEGRAM_IDS['paradise'],
    user_discord_id_to_send_info=DISCORD_IDS['paradise'],
    discord_channel_for_info=DISCORD_CHANNEL_IDS['real_general'],

    if_has_game_request_interval_s=60 * 10,
    counter_send_every=(6, "hours"),

    sale_end_datetime=datetime.datetime(2024, 7, 11, 18, 00),
    sale_soon_ends_diff=datetime.timedelta(hours=24))
