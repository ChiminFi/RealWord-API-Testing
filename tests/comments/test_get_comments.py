# COMMENT 001
def test_get_comments(comment_client, article_and_comment):
    res = comment_client.get_comments(
        slug=article_and_comment["article"]["slug"]
    )
    comment = res.json()["comments"]

    assert res.status_code == 200
    assert comment[0]["id"] == article_and_comment["comment"]["id"]
    assert comment[0]["body"] == article_and_comment["comment"]["body"]
    assert (
        comment[0]["author"]["username"]
        == article_and_comment["user_a"]["username"]
    )


# COMMENT 004
