import pytest


# TC_AUTH_004
def test_login(auth_client, registered_user):
    res = auth_client.login(
        email=registered_user["email"], password=registered_user["password"]
    )

    # print(res.json())
    data = res.json()
    assert res.status_code == 200
    assert data["user"]["token"]
    assert data["user"]["email"] == registered_user["email"]
    assert data["user"]["username"] == registered_user["username"]


def test_login_with_wrong_password(auth_client, registered_user):
    wrong_password = registered_user["password"] + "wrong"
    res = auth_client.login(
        email=registered_user["email"], password=wrong_password
    )

    assert res.status_code == 401
    assert "errors" in res.json()
    assert "user" not in res.json()


def test_get_user_with_logged_in_token(auth_client, logged_in_user):
    res = auth_client.get_current_user(token=logged_in_user["token"])
    data = res.json()

    assert res.status_code == 200
    assert data["user"]["email"] == logged_in_user["email"]
    assert data["user"]["username"] == logged_in_user["username"]
    assert data["user"]["token"]


def test_get_user_without_token(auth_client):
    res = auth_client.get_current_user()

    assert res.status_code == 401


@pytest.mark.xfail(
    reason="BUG-AUTH-001: malformed token return 500 instead of 401",
    strict=True,
)
def test_get_user_with_invalid_token(auth_client):
    invalid_token = "invalid_token_here_there_is"
    res = auth_client.get_current_user(token=invalid_token)

    assert res.status_code == 401
    # assert res.status_code == 500


def test_login_without_email(auth_client, registered_user):
    payload = {"user": {"password": registered_user["password"]}}
    res = auth_client.login_raw(payload=payload)

    assert res.status_code == 422
    assert "errors" in res.json()
    assert "user" not in res.json()
