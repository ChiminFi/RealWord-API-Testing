import pytest


def test_unfavorite_favorite_unfavorite(
    article_client, logged_in_user_factory, article_with_owner
):  # noqa: E501
    favoriter = logged_in_user_factory()["token"]
    favorited_slug = article_with_owner["article"]["slug"]

    res_init = article_client.get_article(slug=favorited_slug, token=favoriter)
    assert res_init.status_code == 200
    favoritesCount = res_init.json()["article"]["favoritesCount"]

    res_F2T = article_client.favorite_article(
        slug=favorited_slug, token=favoriter
    )

    assert res_F2T.status_code == 200

    res_F2T_check = article_client.get_article(
        slug=favorited_slug, token=favoriter
    )
    data_F2T_check = res_F2T_check.json()

    assert res_F2T_check.status_code == 200
    assert data_F2T_check["article"]["favorited"]
    assert data_F2T_check["article"]["favoritesCount"] == favoritesCount + 1

    res_T2F = article_client.unfavorite_article(
        slug=favorited_slug, token=favoriter
    )

    assert res_T2F.status_code == 200

    res_T2F_check = article_client.get_article(
        slug=favorited_slug, token=favoriter
    )
    data_T2F_check = res_T2F_check.json()

    assert res_T2F_check.status_code == 200
    assert not data_T2F_check["article"]["favorited"]
    assert data_T2F_check["article"]["favoritesCount"] == favoritesCount


@pytest.mark.xfail(reason="Twice favorite bug")
def test_favorite_twice(
    article_client, article_with_owner, logged_in_user_factory
):  # noqa: E501
    favoriter = logged_in_user_factory()["token"]
    favorited_slug = article_with_owner["article"]["slug"]

    res_init = article_client.get_article(slug=favorited_slug, token=favoriter)
    assert res_init.status_code == 200

    favoritesCount = res_init.json()["article"]["favoritesCount"]

    res_F2T = article_client.favorite_article(
        slug=favorited_slug, token=favoriter
    )

    assert res_F2T.status_code == 200

    res_F2T_check = article_client.get_article(
        slug=favorited_slug, token=favoriter
    )
    assert res_F2T_check.status_code == 200
    assert (
        res_F2T_check.json()["article"]["favoritesCount"] == favoritesCount + 1
    )

    res_T2T = article_client.favorite_article(
        slug=favorited_slug, token=favoriter
    )
    assert res_T2T.status_code == 200
    # assert res_T2T.status_code == 500

    # res_T2T_check = article_client.get_article(
    #     slug=favorited_slug, token=favoriter
    # )
    # assert res_T2T_check.status_code == 200
