import pytest
from . import create_app

authorization = "some API token"

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

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_signup(client):
    response = client.post("/signup",json={"email":"alguna@sarasa.com","password":"1234"})
    assert response.status_code == 200

def test_login(client):
    response = client.post("/login",json={"email":"alguna@sarasa.com","password":"1234"})
    assert response.status_code == 200

def test_all(client):
    response = client.get("/all",headers={"Authorization": authorization})
    assert response.status_code == 401 or response.status_code == 402
    assert response.json["status"] == "fail"

def test_anime(client):
    response = client.get("/anime/Death Note Rewrite",headers={"Authorization": authorization})
    assert response.status_code == 200
    assert response.json[0]["Members"] == 88699

def test_profile(client):
    response = client.get("/profile",headers={"Authorization": authorization})
    assert response.json["data"]["email"] == "alguna@sarasa.com"