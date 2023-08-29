import pytest
from . import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def signup(client):
    response = client.post("/signup",json={"email":"alguna@sarasa.com","password":"1234"})
    return response

def login(client):
    signup(client)
    response = client.post("/login",json={"email":"alguna@sarasa.com","password":"1234"})
    return response

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_signup(client):
    response = signup(client)
    assert response.status_code == 200

def test_login_before_signup(client):
    # no signup first
    response = client.post("/login",json={"email":"alguna@sarasa.com"})
    assert response.status_code == 404
    assert "User does not exist" in response.json["message"]

def test_login_wrong_body(client):
    signup(client)
    response = client.post("/login",json={"email":"alguna@sarasa.com"})
    assert response.status_code == 201

def test_login(client):
    # signup first
    signup(client)
    response = login(client)
    assert response.status_code == 200

def test_get_all(client):
    # extract auth_token from login method
    response = client.get("/all",headers={"Authorization": login(client).json["auth_token"]})
    assert response.status_code == 200

def test_get_anime(client):
    response = client.get("/anime/Death Note Rewrite",headers={"Authorization": login(client).json["auth_token"]})
    assert response.status_code == 200
    assert response.json[0]["Members"] == 88699

def test_get_profile(client):
    response = client.get("/profile",headers={"Authorization": login(client).json["auth_token"]})
    assert response.json["data"]["email"] == "alguna@sarasa.com"

def test_get_all_while_not_authorized(client):
    # no auth_token
    response = client.get("/all")
    assert response.status_code == 401

def test_all_with_wrong_method(client):
    response = client.post("/all",headers={"Authorization": login(client).json["auth_token"]})
    assert response.status_code == 405

def test_logout(client):
    login(client)
    response = client.post("/logout",headers={"Authorization": login(client).json["auth_token"]})
    assert response.status_code == 200
    assert response.json["message"] == "Successfully logged out"