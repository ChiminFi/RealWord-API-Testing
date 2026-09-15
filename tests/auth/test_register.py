def test_register(auth_client, unique_user_data):
    res = auth_client.register(
        username=unique_user_data["username"],
        email=unique_user_data["email"],
        password=unique_user_data["password"],
    )
    data = res.json()
    # print(data)

    assert res.status_code == 201
    assert data["user"]["username"] == unique_user_data["username"]
    assert data["user"]["email"] == unique_user_data["email"]
    assert data["user"]["token"]


def test_register_with_registered_email(auth_client, unique_user_data):
    res_reg1 = auth_client.register(
        username=unique_user_data["username"],
        email=unique_user_data["email"],
        password=unique_user_data["password"],
    )
    assert res_reg1.status_code == 201

    res_reg2 = auth_client.register(
        username=unique_user_data["username"] + "qa",
        email=unique_user_data["email"],
        password=unique_user_data["password"],
    )

    assert res_reg2.status_code == 409
    assert "errors" in res_reg2.json()

    res_login = auth_client.get_current_user(
        token=res_reg1.json()["user"]["token"]
    )
    data_login = res_login.json()

    assert res_login.status_code == 200
    assert data_login["user"]["email"] == unique_user_data["email"]
    assert data_login["user"]["username"] == unique_user_data["username"]


def test_register_without_password(auth_client, unique_user_data):
    payload = {
        "user": {
            "email": unique_user_data["email"],
            "username": unique_user_data["username"],
        }
    }
    res = auth_client.register_raw(payload=payload)

    assert res.status_code == 422
    assert "errors" in res.json()

    res_login = auth_client.login(
        email=unique_user_data["email"], password=unique_user_data["password"]
    )

    assert res_login.status_code == 401
