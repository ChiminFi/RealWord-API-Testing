# ARTICLE 003
def test_create_article(article_client, logged_in_user, unique_article_data):
    res = article_client.create_article(
        title=unique_article_data["title"],
        description=unique_article_data["description"],
        body=unique_article_data["body"],
        token=logged_in_user["token"],
        tag_list=unique_article_data["tag_list"],
    )
    data = res.json()
    slug1 = data["article"]["slug"]

    assert res.status_code == 201
    assert "article" in data
    assert data["article"]["title"] == unique_article_data["title"]

    res_created_article = article_client.get_article(slug=slug1)

    assert res_created_article.status_code == 200
    assert (
        res_created_article.json()["article"]["description"]
        == unique_article_data["description"]
    )


# ARTICLE 004
def test_create_article_without_token(article_client, unique_article_data):
    payload = {
        "article": {
            **unique_article_data,
            "tagList": unique_article_data["tag_list"],
        }
    }
    res = article_client.create_article_raw(payload=payload)

    assert res.status_code == 401
    assert "article" not in res.json()


# ARTICLE 005
def test_article_without_title(
    article_client, logged_in_user, unique_article_data
):
    payload = {
        "article": {
            "description": unique_article_data["description"],
            "body": unique_article_data["body"],
            "tagList": unique_article_data["tag_list"],
        }
    }
    headers = {"Authorization": f"Bearer {logged_in_user['token']}"}
    res = article_client.create_article_raw(payload=payload, headers=headers)

    assert res.status_code == 422
    assert "article" not in res.json()
