from requests import Response

from src.clients.base_client import BaseClient


class ArticleClient:
    def __init__(self, base_session: BaseClient):
        self.base_session = base_session

    def create_article(
        self,
        title: str,
        description: str,
        body: str,
        token: str,
        tag_list: list | None = None,
    ) -> Response:
        payload = {
            "article": {
                "title": title,
                "description": description,
                "body": body,
                "tagList": tag_list if tag_list else [],
            }
        }
        headers = {"Authorization": f"Bearer {token}"}

        return self.create_article_raw(payload=payload, headers=headers)

    def create_article_raw(
        self, payload: dict | None = None, headers: dict | None = None
    ) -> Response:
        endpoint = "/api/articles"
        res = self.base_session.post(
            endpoint=endpoint, payload=payload, headers=headers
        )

        return res

    def get_article(self, slug: str, token: str | None = None) -> Response:
        endpoint = f"/api/articles/{slug}"
        headers = {"Authorization": f"Bearer {token}"} if token else None
        res = self.base_session.get(endpoint=endpoint, headers=headers)

        return res

    def update_article(
        self,
        slug: str,
        token: str,
        title: str | None = None,
        description: str | None = None,
        body: str | None = None,
        tag_list: list | None = None,
    ) -> Response:
        article = {}

        if title is not None:
            article["title"] = title
        if description is not None:
            article["description"] = description
        if body is not None:
            article["body"] = body
        if tag_list is not None:
            article["tagList"] = tag_list

        payload = {"article": article}
        headers = {"Authorization": f"Bearer {token}"}

        return self.update_article_raw(
            slug=slug, payload=payload, headers=headers
        )

    def update_article_raw(
        self,
        slug: str,
        payload: dict | None = None,
        headers: dict | None = None,
    ) -> Response:
        endpoint = f"/api/articles/{slug}"
        res = self.base_session.put(
            endpoint=endpoint, payload=payload, headers=headers
        )

        return res

    def delete_article(self, slug: str, token: str | None = None) -> Response:
        endpoint = f"/api/articles/{slug}"
        headers = {"Authorization": f"Bearer {token}"} if token else None
        res = self.base_session.delete(endpoint=endpoint, headers=headers)

        return res

    def favorite_article(self, slug, token) -> Response:
        endpoint = f"/api/articles/{slug}/favorite"
        headers = {"Authorization": f"Bearer {token}"} if token else None

        res = self.base_session.post(endpoint=endpoint, headers=headers)

        return res

    def unfavorite_article(self, slug, token) -> Response:
        endpoint = f"/api/articles/{slug}/favorite"
        headers = {"Authorization": f"Bearer {token}"} if token else None

        res = self.base_session.delete(endpoint=endpoint, headers=headers)

        return res

    def list_articles(
        self,
        tag: str | None = None,
        auth: str | None = None,
        favorited: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        token: str | None = None,
    ) -> Response:
        params = {
            "tag": tag,
            "author": auth,
            "favorited": favorited,
            "limit": limit,
            "offset": offset,
        }

        params = {
            key: value for key, value in params.items() if value is not None
        }
        headers = {"Authorization": f"Bearer {token}"} if token else None
        endpoint = "/api/articles"

        res = self.base_session.get(
            endpoint=endpoint, params=params, headers=headers
        )

        return res

    def get_articles_feed(
        self,
        limit: int | None = None,
        offset: int | None = None,
        token: str | None = None,
    ) -> Response:
        params = {"limit": limit, "offset": offset}

        params = {
            key: value for key, value in params.items() if value is not None
        }
        endpoint = "/api/articles/feed"
        headers = {"Authorization": f"Bearer {token}"} if token else None

        res = self.base_session.get(
            endpoint=endpoint, params=params, headers=headers
        )

        return res
