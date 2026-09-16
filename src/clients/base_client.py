import logging

import requests
from requests import Response

from src.config.settings import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get(
        self,
        endpoint: str,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> Response:
        url = f"{self.base_url}{endpoint}"

        logger.info("GET %s", url)

        res = self.session.get(
            url=url,
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

        logger.info(
            "GET %s -> %s ",
            url,
            res.status_code,
        )

        return res

    def post(
        self,
        endpoint: str,
        payload: dict | None = None,
        headers: dict | None = None,
    ) -> Response:
        url = f"{self.base_url}{endpoint}"

        logger.info("POST %s", url)

        res = self.session.post(
            url=url,
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

        logger.info(
            "POST %s -> %s ",
            url,
            res.status_code,
        )

        return res

    def put(
        self,
        endpoint: str,
        payload: dict | None = None,
        headers: dict | None = None,
    ) -> Response:
        url = f"{self.base_url}{endpoint}"

        logger.info("PUT %s", url)

        res = self.session.put(
            url=url,
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

        logger.info(
            "PUT %s -> %s",
            url,
            res.status_code,
        )

        return res

    def delete(self, endpoint: str, headers: dict | None = None) -> Response:
        url = f"{self.base_url}{endpoint}"

        logger.info("DEL %s", url)
        res = self.session.delete(
            url=url,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

        logger.info(
            "DEL %s -> %s",
            url,
            res.status_code,
        )

        return res

    def close(self) -> None:
        self.session.close()
