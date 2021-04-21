import json
import time

from rich.live import Live

from crypto_watcher.arg_parser import parse_args
from crypto_watcher.renderer import get_layout
from crypto_watcher.services.binance import BinanceService
from crypto_watcher.services.cryptonator import CryptonatorService
from crypto_watcher.services.nbminer import NBMinerService
from crypto_watcher.settings import Settings


def start_watcher(settings: Settings) -> None:  # noqa: WPS210
    """
    Gather all info from services and renders it to terminal.

    :param settings: current application settings.
    """
    binance_status = None
    profit_today = {}
    profit_yesterday = {}
    nb_service = NBMinerService(settings)
    binance_service = BinanceService(settings)
    cryptonator_service = CryptonatorService(settings)
    with Live("Waiting for data...", screen=True) as term:
        while True:  # noqa: WPS457
            nb_status = nb_service.get_status()
            algorithm = settings.binance_algo
            if nb_status:
                algorithm = nb_status.stratum.algorithm
            new_bin_status = binance_service.get_status(algorithm)
            if new_bin_status:
                binance_status = new_bin_status
                profit_today = cryptonator_service.convert(binance_status.profit_today)
                profit_yesterday = cryptonator_service.convert(
                    binance_status.profit_yesterday,
                )
            term.update(
                get_layout(
                    nb_status,
                    binance_status,
                    profit_today,
                    profit_yesterday,
                ),
            )
            time.sleep(2)


def main() -> None:  # noqa: WPS210
    """
    Main function.

    :raises ValueError: if secret file wasn't found.
    """
    cli_args = parse_args()
    if not cli_args.secret.exists():
        raise ValueError("Secret file doesn't exist!")

    with open(str(cli_args.secret), "r") as secret_file:
        secret_json = json.load(secret_file)
        api_key = secret_json["api_key"]
        secret_key = secret_json["secret_key"]
        user_name = secret_json["user_name"]
        algo = secret_json["algorithm"]

    settings = Settings(
        binance_api=cli_args.binance_api,
        nbminer_api=cli_args.nbminer_api,
        binance_api_key=api_key,
        binance_secret_key=secret_key,
        binance_user_name=user_name,
        binance_algo=algo,
        local_currency=cli_args.local_currency,
    )
    try:
        start_watcher(settings)
    except KeyboardInterrupt:
        print("Have a good day!")  # noqa: WPS421
