import pytest


# COMMENT 004
@pytest.mark.smoke
def test_create_comment(
    article_with_owner,
    logged_in_user_factory,
    comment_client,
    unique_comment_data,
):
    user_comment = logged_in_user_factory()
    slug = article_with_owner["article"]["slug"]
    comment_body = unique_comment_data["comment"]["body"]

    res = comment_client.create_comment(
        slug=slug,
        body=comment_body,
        token=user_comment["token"],
    )

    assert res.status_code == 201

    created_comment = res.json()["comment"]
    comment_id = created_comment["id"]

    res_get = comment_client.get_comments(slug=slug)

    comments = res_get.json()["comments"]
    comment = next(
        comment for comment in comments if comment["id"] == comment_id
    )

    assert res_get.status_code == 200
    assert "id" in comment
    assert comment["body"] == comment_body
    assert comment["author"]["username"] == user_comment["username"]


def test_create_comment_without_token(
    comment_client, article_with_owner, unique_comment_data
):
    slug = article_with_owner["article"]["slug"]
    res = comment_client.create_comment_raw(
        slug=slug, payload=unique_comment_data
    )

    assert res.status_code == 401

    res_get = comment_client.get_comments(slug=slug)
    data = res_get.json()
    # print(data)

    assert res_get.status_code == 200
    assert len(data["comments"]) == 0
