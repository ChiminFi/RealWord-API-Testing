from requests import Response

from src.clients.base_client import BaseClient


class ProfileClient:
    def __init__(self, base_client: BaseClient):
        self.base_client = base_client

    def get_profile(self, username: str, token: str | None = None):
        endpoint = f"/api/profiles/{username}"
        headers = {"Authorization": f"Bearer {token}"} if token else None
        res = self.base_client.get(endpoint=endpoint, headers=headers)

        return res

    def follow(self, username: str, token: str | None = None):
        endpoint = f"/api/profiles/{username}/follow"
        headers = {"Authorization": f"Bearer {token}"} if token else None

        res = self.base_client.post(endpoint=endpoint, headers=headers)

        return res

    def unfollow(self, username: str, token: str | None = None):
        endpoint = f"/api/profiles/{username}/follow"
        headers = {"Authorization": f"Bearer {token}"} if token else None

        res = self.base_client.delete(endpoint=endpoint, headers=headers)

        return res
