def test_unfollow_to_follow(profile_client, logged_in_user_factory):
    follower = logged_in_user_factory()
    followee = logged_in_user_factory()

    res = profile_client.follow(
        username=followee["username"], token=follower["token"]
    )

    assert res.status_code == 200

    res_get = profile_client.get_profile(
        username=followee["username"], token=follower["token"]
    )

    assert res_get.status_code == 200
    assert res_get.json()["profile"]["following"]


def test_follow_to_unfollow(profile_client, logged_in_user_factory):
    follower = logged_in_user_factory()
    followee = logged_in_user_factory()

    res_F2T = profile_client.follow(
        username=followee["username"], token=follower["token"]
    )
    assert res_F2T.status_code == 200

    res_F2T_check = profile_client.get_profile(
        username=followee["username"], token=follower["token"]
    )
    assert res_F2T_check.status_code == 200
    assert res_F2T_check.json()["profile"]["following"]

    res_T2F = profile_client.unfollow(
        username=followee["username"], token=follower["token"]
    )
    assert res_T2F.status_code == 200

    res_T2F_check = profile_client.get_profile(
        username=followee["username"], token=follower["token"]
    )

    assert res_T2F_check.status_code == 200
    assert not res_T2F_check.json()["profile"]["following"]
