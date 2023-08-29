import pytest
from . import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True})

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def signup(client):
    response = client.post(
        "/signup", json={"email": "alguna@sarasa.com", "password": "1234"}
    )
    return response


def login(client):
    signup(client)
    response = client.post(
        "/login", json={"email": "alguna@sarasa.com", "password": "1234"}
    )
    return response


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
