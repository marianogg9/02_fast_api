from animes.conftest import signup, login

def test_signup(test_client):
    response = signup(test_client)
    assert response.status_code == 200


def test_login_before_signup(test_client):
    # no signup first
    response = test_client.post("/login", json={"email": "alguna@sarasa.com"})
    assert response.status_code == 404
    assert "User does not exist" in response.json["message"]


def test_login_wrong_body(test_client):
    signup(test_client)
    response = test_client.post("/login", json={"email": "alguna@sarasa.com"})
    assert response.status_code == 201


def test_login(test_client):
    # signup first
    signup(test_client)
    response = login(test_client)
    assert response.status_code == 200


def test_get_all(test_client):
    # extract auth_token from login method
    response = test_client.get(
        "/all", headers={"Authorization": login(test_client).json["auth_token"]}
    )
    assert response.status_code == 200


def test_get_anime(test_client):
    response = test_client.get(
        "/anime/Death Note Rewrite",
        headers={"Authorization": login(test_client).json["auth_token"]},
    )
    assert response.status_code == 200
    assert response.json[0]["Members"] == 88699


def test_get_profile(test_client):
    response = test_client.get(
        "/profile", headers={"Authorization": login(test_client).json["auth_token"]}
    )
    assert response.json["data"]["email"] == "alguna@sarasa.com"


def test_get_all_while_not_authorized(test_client):
    # no auth_token
    response = test_client.get("/all")
    assert response.status_code == 401


def test_all_with_wrong_method(test_client):
    response = test_client.post(
        "/all", headers={"Authorization": login(test_client).json["auth_token"]}
    )
    assert response.status_code == 405


def test_logout(test_client):
    login(test_client)
    response = test_client.post(
        "/logout", headers={"Authorization": login(test_client).json["auth_token"]}
    )
    assert response.status_code == 200
    assert response.json["message"] == "Successfully logged out"
