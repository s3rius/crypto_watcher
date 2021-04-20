from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from pathlib import Path


def parse_args() -> Namespace:
    """Parse args from CLI.

    :returns: parsed namespace.
    """
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-b",
        "--binance_api",
        default="https://api.binance.com/",
        type=str,
        help="Binance base API URL",
        dest="binance_api",
    )
    parser.add_argument(
        "-n",
        "--nbminer_api",
        default="http://localhost:22333/",
        type=str,
        help="NBMiner base API URL",
        dest="nbminer_api",
    )
    parser.add_argument(
        "-s",
        "--secret-file",
        default="~/.binance_secrets",
        type=lambda path: Path(path).expanduser(),
        help="Path to the file with binance keys.",
        dest="secret",
    )
    parser.add_argument(
        "-c",
        "--currency",
        default="USD",
        type=str,
        help="Your local currency to convert cryptocurrency values.",
        dest="local_currency",
    )
    return parser.parse_args()
