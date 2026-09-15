import uuid


# ARTICLE 007
def test_update_article_body(article_client, article_with_owner):
    slug = article_with_owner["article"]["slug"]
    token = article_with_owner["user"]["token"]
    new_body = "The New One"
    res = article_client.update_article(slug=slug, token=token, body=new_body)

    assert res.status_code == 200

    res_get = article_client.get_article(slug=slug)
    data_get = res_get.json()

    assert res_get.status_code == 200
    assert (
        data_get["article"]["title"] == article_with_owner["article"]["title"]
    )
    assert data_get["article"]["body"] == new_body


# ARTICLE 008
def test_update_article_title(article_client, article_with_owner):
    slug = article_with_owner["article"]["slug"]
    token = article_with_owner["user"]["token"]
    new_title = "The New One" + article_with_owner["article"]["title"]
    res = article_client.update_article(slug=slug, token=token, title=new_title)

    assert res.status_code == 200

    new_slug = res.json()["article"]["slug"]

    res_get = article_client.get_article(slug=new_slug)
    data_get = res_get.json()

    assert res_get.status_code == 200
    assert data_get["article"]["title"] == new_title
    assert data_get["article"]["body"] == article_with_owner["article"]["body"]

    res_get_old_one = article_client.get_article(slug=slug)
    assert res_get_old_one.status_code == 404
    assert data_get["article"]["title"] == new_title
    assert data_get["article"]["body"] == article_with_owner["article"]["body"]


def test_update_article_without_ownership(
    article_client, logged_in_user_factory, unique_article_data
):
    user_A = logged_in_user_factory()
    user_B = logged_in_user_factory()

    res_owner = article_client.create_article(
        title=unique_article_data["title"],
        description=unique_article_data["description"],
        body=unique_article_data["body"],
        token=user_A["token"],
        tag_list=unique_article_data["tag_list"],
    )
    assert res_owner.status_code == 201
    slug = res_owner.json()["article"]["slug"]

    res_not_owner = article_client.update_article(
        slug=slug, token=user_B["token"], body="The New One"
    )

    assert res_not_owner.status_code == 403

    res_get = article_client.get_article(slug=slug)
    data_get = res_get.json()

    assert res_get.status_code == 200
    assert data_get["article"]["title"] == unique_article_data["title"]
    assert data_get["article"]["body"] == unique_article_data["body"]


# ARTICLE 11
def test_update_article_without_token(article_client, article_with_owner):
    slug = article_with_owner["article"]["slug"]
    payload = {"article": {"body": "The New One"}}
    res = article_client.update_article_raw(slug=slug, payload=payload)

    assert res.status_code == 401

    res_get = article_client.get_article(slug=slug)
    data_get = res_get.json()

    assert res_get.status_code == 200
    assert data_get["article"]["body"] == article_with_owner["article"]["body"]
    assert (
        data_get["article"]["title"] == article_with_owner["article"]["title"]
    )


# ARTICLE 12
def test_update_article_not_exist(
    article_client, logged_in_user, unique_article_data
):
    slug_not_exist = f"not-exist-{uuid.uuid4().hex}"
    res = article_client.update_article(
        slug=slug_not_exist,
        token=logged_in_user["token"],
        body=unique_article_data["body"],
    )

    assert res.status_code == 404
    assert "errors" in res.json()
