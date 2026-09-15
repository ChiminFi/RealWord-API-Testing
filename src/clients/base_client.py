import requests
from requests import Response


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
        res = self.session.get(
            f"{self.base_url}{endpoint}",
            params=params,
            headers=headers,
            timeout=10,
        )

        return res

    def post(
        self,
        endpoint: str,
        payload: dict | None = None,
        headers: dict | None = None,
    ) -> Response:
        res = self.session.post(
            f"{self.base_url}{endpoint}",
            json=payload,
            headers=headers,
            timeout=10,
        )

        return res

    def put(
        self,
        endpoint: str,
        payload: dict | None = None,
        headers: dict | None = None,
    ) -> Response:
        res = self.session.put(
            f"{self.base_url}{endpoint}",
            json=payload,
            headers=headers,
            timeout=10,
        )

        return res

    def delete(self, endpoint: str, headers: dict | None = None) -> Response:
        res = self.session.delete(
            f"{self.base_url}{endpoint}", headers=headers, timeout=10
        )

        return res

    def close(self) -> None:
        self.session.close()
