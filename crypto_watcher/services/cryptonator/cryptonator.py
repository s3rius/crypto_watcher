from decimal import Decimal
from typing import Dict
from urllib.parse import urljoin

import requests

from crypto_watcher.services.cryptonator.models import ExchangeRate, Ticker
from crypto_watcher.settings import Settings


class CryptonatorService:
    """Class for converting cryptocurrency to currency."""

    def __init__(self, settings: Settings) -> None:
        self.base_url = "https://api.cryptonator.com/"
        self.target_currency = settings.local_currency
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "CryptonatorApi/1"})

    def convert(  # noqa: WPS210
        self,
        cryptos: Dict[str, float],
    ) -> Dict[str, ExchangeRate]:
        """
        Conver a dict of creyptocurrencys with current exchange rate.

        This function gets results from cryptonator and converts
        given amounts to target currency.

        :param cryptos: Dict of cryptos values. key - crypto name, value - amount.
        :return: Dict of converted exchange rates.
        """
        rates = {}
        for name, amount in cryptos.items():
            response = self.session.get(
                urljoin(self.base_url, f"/api/ticker/{name}-{self.target_currency}"),
            )
            if not response.ok:
                continue
            ticker = Ticker(**response.json()["ticker"])
            price = Decimal(ticker.price) * Decimal(amount)
            rates[name] = ExchangeRate(
                **ticker.dict(),
                rate="{0:,.2f}".format(float(price)),
            )
        return rates
