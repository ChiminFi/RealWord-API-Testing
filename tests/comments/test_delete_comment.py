import random


# COMMENT 007
def test_delete_comment(comment_client, article_and_comment):
    slug = article_and_comment["article"]["slug"]
    comment_id = article_and_comment["comment"]["id"]
    comment_token = article_and_comment["user_a"]["token"]

    res = comment_client.delete_comment(
        slug=slug, comment_id=comment_id, token=comment_token
    )

    assert res.status_code == 204

    res_get = comment_client.get_comments(slug=slug)

    assert res_get.status_code == 200
    assert len(res_get.json()["comments"]) == 0


def test_delete_comment_without_ownership(
    comment_client, article_and_comment, logged_in_user_factory
):
    slug = article_and_comment["article"]["slug"]
    comment_id = article_and_comment["comment"]["id"]
    user_delete = logged_in_user_factory()
    comment_body = article_and_comment["comment"]["body"]

    res = comment_client.delete_comment(
        slug=slug, comment_id=comment_id, token=user_delete["token"]
    )

    assert res.status_code == 403

    res_get = comment_client.get_comments(slug=slug)
    data = res_get.json()

    assert res_get.status_code == 200
    assert data["comments"][0]["body"] == comment_body


def test_comment_not_exist(comment_client, logged_in_user, article_with_owner):
    comment_id = random.randint(100000, 999999999)

    slug = article_with_owner["article"]["slug"]
    token = logged_in_user["token"]
    res = comment_client.delete_comment(
        slug=slug, comment_id=comment_id, token=token
    )

    assert res.status_code == 404
