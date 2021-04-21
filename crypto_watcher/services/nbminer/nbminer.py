from typing import Optional
from urllib.parse import urljoin

import requests
from requests.exceptions import ConnectionError, ConnectTimeout

from crypto_watcher.services.nbminer.models import NBMinerStatus
from crypto_watcher.settings import Settings


class NBMinerService:
    """Service for parsing current NBminer status."""

    def __init__(self, settings: Settings):
        self.base_url = settings.nbminer_api.rstrip("/") + "/"  # noqa: WPS336
        self.session = requests.Session()

    def get_status(self) -> Optional[NBMinerStatus]:
        """
        Get actual nbminer status.

        :return: current status
        """
        try:
            response = self.session.get(
                urljoin(self.base_url, "/api/v1/status"),
                timeout=2,
            )
        except (ConnectionError, ConnectTimeout):
            return None
        if not response.ok:
            return None
        return NBMinerStatus(**response.json())
