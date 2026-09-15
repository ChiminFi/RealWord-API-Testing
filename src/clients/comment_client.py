from requests import Response

from src.clients.base_client import BaseClient


class CommentClient:
    def __init__(self, base_session: BaseClient):
        self.base_session = base_session

    def get_comments(self, slug: str) -> Response:
        endpoint = f"/api/articles/{slug}/comments"
        res = self.base_session.get(endpoint=endpoint)

        return res

    def create_comment(self, slug: str, body: str, token: str):
        payload = {"comment": {"body": body}}
        headers = {"Authorization": f"Bearer {token}"}

        return self.create_comment_raw(
            slug=slug, payload=payload, headers=headers
        )

    def create_comment_raw(
        self,
        slug: str | None = None,
        payload: dict | None = None,
        headers: dict | None = None,
    ):
        endpoint = f"/api/articles/{slug}/comments"
        res = self.base_session.post(
            endpoint=endpoint, payload=payload, headers=headers
        )

        return res

    def delete_comment(
        self, slug: str, comment_id: str, token: str | None = None
    ):
        endpoint = f"/api/articles/{slug}/comments/{comment_id}"
        headers = {"Authorization": f"Bearer {token}"} if token else None

        res = self.base_session.delete(endpoint=endpoint, headers=headers)

        return res
