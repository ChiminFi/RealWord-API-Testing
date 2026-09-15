import pytest


# ARTICLE 13
@pytest.mark.smoke
def test_delete_article(article_client, article_with_owner):
    slug = article_with_owner["article"]["slug"]
    res = article_client.delete_article(
        slug=slug,
        token=article_with_owner["user"]["token"],
    )

    assert res.status_code == 204

    res_get = article_client.get_article(slug=slug)

    assert res_get.status_code == 404


# ARTICLE 14
def test_delete_article_without_ownership(
    article_client, article_with_owner, logged_in_user_factory
):
    user_b = logged_in_user_factory()

    slug = article_with_owner["article"]["slug"]
    res = article_client.delete_article(slug=slug, token=user_b["token"])

    assert res.status_code == 403

    res_get = article_client.get_article(slug=slug)
    data = res_get.json()

    assert res_get.status_code == 200
    assert "article" in data
    assert (
        data["article"]["author"]["username"]
        == article_with_owner["user"]["username"]
    )


# ARTICLE 15
def test_delete_article_without_token(article_client, article_with_owner):
    slug = article_with_owner["article"]["slug"]
    res = article_client.delete_article(slug=slug)

    assert res.status_code == 401

    res_get = article_client.get_article(slug=slug)

    assert res_get.status_code == 200
    assert "article" in res_get.json()


# ARTICLE 16
def test_delete_article_deleted(article_client, article_with_owner):
    res = article_client.delete_article(
        slug=article_with_owner["article"]["slug"],
        token=article_with_owner["user"]["token"],
    )

    assert res.status_code == 204

    res_del_2 = article_client.delete_article(
        slug=article_with_owner["article"]["slug"],
        token=article_with_owner["user"]["token"],
    )

    assert res_del_2.status_code == 404
