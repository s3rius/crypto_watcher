import hashlib
import hmac
import re
import time
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlencode, urljoin

import requests
from requests.structures import CaseInsensitiveDict

from crypto_watcher.services.binance.models import BinanceStatus
from crypto_watcher.settings import Settings


class BinanceService:
    """Service to load data from binance."""

    def __init__(self, settings: Settings) -> None:
        self.base_url = settings.binance_api.rstrip("/") + "/"  # noqa: WPS336
        self.api_key = settings.binance_api_key
        self.secret_key = settings.binance_secret_key
        self.user_name = settings.binance_user_name
        self.algo = settings.binance_algo
        self._session = requests.Session()
        self._next_query_time: Optional[datetime] = None

    def create_signature(self, unsafe_data: str) -> str:
        """
        Build a binance signature.

        :param unsafe_data: Data to encrypt.
        :returns: Encrypted data.
        """
        return hmac.new(
            self.secret_key.encode(),
            unsafe_data.encode(),
            hashlib.sha256,
        ).hexdigest()

    def set_next_safe_time(self, headers: CaseInsensitiveDict) -> None:  # type: ignore
        """
        Parse returned headers to get weight.

        The binance API has weights on endpoints and that value differs
        for different users. This function parses headers and gets the weight value.

        :param headers: API response headers.
        """
        weight_regex = re.compile(
            r"X-SAPI-USED-IP-WEIGHT-(?P<num>\d+)(?P<period>[SMHD])",
        )
        period_mapping = {"S": "seconds", "M": "minutes", "H": "hours", "D": "days"}
        for header_name in headers.keys():
            match = weight_regex.match(header_name)
            if match:
                delta_param = {
                    period_mapping[match.group("period")]: int(match.group("num")),
                }
                self._next_query_time = datetime.now() + timedelta(**delta_param)
                return

    def get_status(self, algorithm: str) -> BinanceStatus:
        """
        Get current current mining status.

        This function returns recent payments.
        To help you check current earnings.

        :param algorithm: mining algorithm.
        :returns: earnings status.
        """
        query = {
            "algo": algorithm,
            "userName": self.user_name,
            "timestamp": int(time.time()) * 1000,
            "recvWindow": 50000,
        }
        if self._next_query_time and self._next_query_time > datetime.now():
            return None
        signature = self.create_signature(urlencode(query))
        query["signature"] = signature
        response = self._session.get(
            urljoin(self.base_url, "/sapi/v1/mining/statistics/user/status"),
            params=query,
            headers={
                "X-MBX-APIKEY": self.api_key,
            },
        )
        response_json = response.json()
        if response_json["code"] != 0:
            return None
        self.set_next_safe_time(response.headers)
        return BinanceStatus(**response_json["data"])
