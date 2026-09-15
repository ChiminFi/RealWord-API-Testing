from requests import Response

from src.clients.base_client import BaseClient


class AuthClient:
    def __init__(self, base_client: BaseClient):
        self.base_client = base_client

    def register(self, username: str, email: str, password: str) -> Response:
        payload = {
            "user": {"username": username, "email": email, "password": password}
        }

        return self.register_raw(payload=payload)

    def register_raw(self, payload: dict) -> Response:
        endpoint = "/api/users"
        res = self.base_client.post(endpoint=endpoint, payload=payload)

        return res

    def login(self, email: str, password: str) -> Response:
        payload = {"user": {"email": email, "password": password}}

        return self.login_raw(payload=payload)

    def login_raw(self, payload: dict) -> Response:
        endpoint = "/api/users/login"
        res = self.base_client.post(endpoint=endpoint, payload=payload)

        return res

    def get_current_user(self, token: str | None = None) -> Response:
        endpoint = "/api/user"
        headers = {"Authorization": f"Bearer {token}"} if token else None
        res = self.base_client.get(endpoint=endpoint, headers=headers)

        return res
