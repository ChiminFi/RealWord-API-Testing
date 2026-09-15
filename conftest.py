import os

import psycopg
import pytest
from dotenv import load_dotenv

from src.clients.article_client import ArticleClient
from src.clients.auth_client import AuthClient
from src.clients.base_client import BaseClient
from src.clients.comment_client import CommentClient
from src.clients.profile_client import ProfileClient
from src.config.settings import BASE_URL
from src.utils.data_factory import (
    make_article_data,
    make_comment_data,
    make_user_data,
)

load_dotenv()


@pytest.fixture
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def base_client(base_url: str):
    client = BaseClient(base_url=base_url)
    yield client
    client.close()


@pytest.fixture
def auth_client(base_client):
    return AuthClient(base_client=base_client)


@pytest.fixture
def article_client(base_client):
    return ArticleClient(base_session=base_client)


@pytest.fixture
def comment_client(base_client):
    return CommentClient(base_session=base_client)


@pytest.fixture
def profile_client(base_client):
    return ProfileClient(base_client=base_client)


@pytest.fixture
def unique_user_data():
    return make_user_data()


@pytest.fixture
def unique_article_data():
    return make_article_data()


@pytest.fixture
def unique_comment_data():
    return make_comment_data()


@pytest.fixture
def registered_user(auth_client, unique_user_data):
    res = auth_client.register(
        username=unique_user_data["username"],
        email=unique_user_data["email"],
        password=unique_user_data["password"],
    )

    assert res.status_code == 201

    return {**unique_user_data, "token": res.json()["user"]["token"]}


# * logged account 会直接沿用 registered account
@pytest.fixture
def logged_in_user(auth_client, registered_user):
    res = auth_client.login(
        email=registered_user["email"], password=registered_user["password"]
    )
    assert res.status_code == 200

    return {**registered_user, "token": res.json()["user"]["token"]}


@pytest.fixture
def logged_in_user_factory(auth_client):
    def create_user():
        user_data = make_user_data()

        register_res = auth_client.register(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )
        assert register_res.status_code == 201

        login_res = auth_client.login(
            email=user_data["email"],
            password=user_data["password"],
        )
        assert login_res.status_code == 200

        return {**user_data, "token": login_res.json()["user"]["token"]}

    return create_user


# * 这个方法 会利用logged account
@pytest.fixture
def article_with_owner(article_client, unique_article_data, logged_in_user):
    res = article_client.create_article(
        title=unique_article_data["title"],
        description=unique_article_data["description"],
        body=unique_article_data["body"],
        token=logged_in_user["token"],
        tag_list=unique_article_data["tag_list"],
    )

    assert res.status_code == 201

    return {
        "user": logged_in_user,
        "article": {
            **unique_article_data,
            "slug": res.json()["article"]["slug"],
        },
    }


@pytest.fixture
def article_and_comment(article_client, comment_client, logged_in_user_factory):
    user_a = logged_in_user_factory()
    user_b = logged_in_user_factory()
    article_payload = {
        "article": {**make_article_data(), "tagList": ["test", "pytest"]}
    }
    comment_payload = make_comment_data()
    headers_a = {"Authorization": f"Bearer {user_a['token']}"}
    headers_b = {"Authorization": f"Bearer {user_b['token']}"}

    res_article = article_client.create_article_raw(
        payload=article_payload, headers=headers_b
    )
    assert res_article.status_code == 201

    article = {**article_payload, "slug": res_article.json()["article"]["slug"]}

    res_comment = comment_client.create_comment_raw(
        slug=article["slug"], payload=comment_payload, headers=headers_a
    )
    assert res_comment.status_code == 201
    comment = {
        "body": comment_payload["comment"]["body"],
        "id": res_comment.json()["comment"]["id"],
    }

    return {
        "article": article,
        "comment": comment,
        "user_a": user_a,
        "user_b": user_b,
    }


@pytest.fixture
def multiple_articles(article_client, logged_in_user_factory, request):
    user_a = logged_in_user_factory()
    user_b = logged_in_user_factory()
    header_a = {"Authorization": f"Bearer {user_a['token']}"}
    header_b = {"Authorization": f"Bearer {user_b['token']}"}

    article_count_a = 0
    article_count_b = 0
    article_up_to = getattr(request, "param", 3)

    while article_count_a < article_up_to:
        payload = {"article": {**make_article_data(), "tagList": ["test", "a"]}}
        res_a = article_client.create_article_raw(
            payload=payload, headers=header_a
        )
        assert res_a.status_code == 201
        article_count_a = article_count_a + 1

    while article_count_b < 2:
        payload = {"article": {**make_article_data(), "tagList": ["test", "b"]}}
        res_b = article_client.create_article_raw(
            payload=payload, headers=header_b
        )

        assert res_b.status_code == 201
        article_count_b = article_count_b + 1

    return {
        "user_a": {**user_a, "count": article_count_a},
        "user_b": {**user_b, "count": article_count_b},
    }


@pytest.fixture
def db_connection():
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    yield conn
    conn.close()
