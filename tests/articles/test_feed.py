def test_feed(
    article_client, logged_in_user_factory, profile_client, unique_article_data
):
    user_follower = logged_in_user_factory()
    user_followee = logged_in_user_factory()
    token_follower = user_follower["token"]
    username_followee = user_followee["username"]
    # headers_followee = {"Authorization": f"Bearer {user_followee['token']}"}
    # payload = {
    #     "article": {**unique_article_data, "tagList": ["pytest", "feed"]}
    # }

    res_follow = profile_client.follow(
        username=username_followee, token=token_follower
    )
    assert res_follow.status_code == 200

    res_article = article_client.create_article(
        title=unique_article_data["title"],
        description=unique_article_data["description"],
        body=unique_article_data["body"],
        tag_list=["pytest", "feed"],
        token=user_followee["token"],
    )
    assert res_article.status_code == 201
    slug = res_article.json()["article"]["slug"]

    res_feed = article_client.get_articles_feed(token=token_follower)
    data_feed = res_feed.json()
    assert res_feed.status_code == 200
    assert any(article["slug"] == slug for article in data_feed["articles"])
    # feed_count = data_feed["articlesCount"]

    res_unfollow = profile_client.unfollow(
        username=username_followee, token=token_follower
    )
    assert res_unfollow.status_code == 200

    res_feed_unfollowed = article_client.get_articles_feed(token=token_follower)
    assert res_feed_unfollowed.status_code == 200
    assert not any(
        article["slug"] == slug
        for article in res_feed_unfollowed.json()["articles"]
    )
