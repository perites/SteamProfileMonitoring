import argparse
import logging

import constants
from configs import CONFIGS
from utils.json_file import File

logger = logging.getLogger("args-parser")
parser = argparse.ArgumentParser(prog="SteamProfileMonitoring",
                                 description="Program that tracks a specified Steam profile to detect game purchase")

parser.add_argument("config_name", type=str, choices=CONFIGS.keys())
parser.add_argument("--deploy", action="store_true")

parser.add_argument("--reset_notified", action="store_true")


def parse_args():
    args = parser.parse_args()

    maybe_config = CONFIGS[args.config_name]

    if maybe_config.config_type == "deploy" and not args.deploy:
        raise Exception("Cant run deploy type config without --deploy flag enabled")

    if maybe_config.config_type != "deploy" and args.deploy:
        raise Exception("Cant run other than deploy type config with --deploy flag enabled")

    if args.reset_notified:
        if args.deploy:
            logger.warning("Ignoring --reset_notified flag because of --deploy flag")
        else:
            File(constants.PATH_TO_NOTIFIED_FILE).write_data(
                {
                    "bought_game_notified": False,
                    "sale_soon_ends_notified": False,
                    "sale_ended_notified": False
                }
            )

    logger.info(f"Running {args.config_name} config of type {maybe_config.config_type}")
    return CONFIGS[args.config_name]
