import pytest


def test_article_list_author_filter(multiple_articles, article_client):
    auth_a = multiple_articles["user_a"]["username"]
    res = article_client.list_articles(auth=auth_a)
    data = res.json()

    assert res.status_code == 200
    assert len(data["articles"]) == multiple_articles["user_a"]["count"]
    assert data["articlesCount"] == multiple_articles["user_a"]["count"]
    assert all(
        article["author"]["username"] == auth_a for article in data["articles"]
    )


@pytest.mark.parametrize("multiple_articles", [5], indirect=True)
def test_articles_limit_offset(multiple_articles, article_client):
    auth_a = multiple_articles["user_a"]["username"]
    res = article_client.list_articles(auth=auth_a, limit=2, offset=2)
    data = res.json()

    assert res.status_code == 200
    assert len(data["articles"]) == 2
    assert data["articlesCount"] == multiple_articles["user_a"]["count"]

    res_check = article_client.list_articles(auth=auth_a)
    data_check = res_check.json()

    assert res_check.status_code == 200
    assert data["articles"] == data_check["articles"][2:4]


@pytest.mark.parametrize("multiple_articles", [5], indirect=True)
def test_articles_last_partial_page(multiple_articles, article_client):
    auth_a = multiple_articles["user_a"]["username"]
    res = article_client.list_articles(auth=auth_a, limit=3, offset=3)
    data = res.json()
    print(data)

    assert res.status_code == 200
    assert len(data["articles"]) == 2
    assert data["articlesCount"] == multiple_articles["user_a"]["count"]
