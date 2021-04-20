from pydantic import BaseSettings


class Settings(BaseSettings):
    """Main watcher settings."""

    binance_api: str
    nbminer_api: str

    binance_api_key: str
    binance_secret_key: str
    binance_user_name: str
    binance_algo: str

    local_currency: str
