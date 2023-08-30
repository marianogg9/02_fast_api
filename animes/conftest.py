import csv, os, pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flasgger import Swagger
from animes import create_app

db = SQLAlchemy()
dbname = "test-db-animes"

@pytest.fixture()
def app():
    app = create_app(dbname)
    app.config.update({"TESTING": True})

    yield app


@pytest.fixture()
def test_client(app):
    return app.test_client()


def signup(test_client):
    response = test_client.post(
        "/signup", json={"email": "alguna@sarasa.com", "password": "1234"}
    )
    return response


def login(test_client):
    signup(test_client)
    response = test_client.post(
        "/login", json={"email": "alguna@sarasa.com", "password": "1234"}
    )
    return response


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
