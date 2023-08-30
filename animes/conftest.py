import csv, os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flasgger import Swagger
import pytest

db = SQLAlchemy()

def create_app():
    """
    Flask app initialization and DB population (from input CSV)
    """
    app = Flask(__name__)
    swagger = Swagger(app)

    app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]  # dummy key
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test-animes.db"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from . import models

    with app.app_context():
        db.drop_all()
        db.create_all()

        with open(
            "../data/anime.csv", "r", encoding="utf-8"
        ) as csvfile:  # read input data file
            csv_reader = csv.reader(csvfile, delimiter=",")
            first_line = csvfile.readline()
            for row in csv_reader:
                anime = models.Anime(
                    Anime_ID=str(row[0]),
                    Name=row[1],
                    Genre=row[2],
                    Type=row[3],
                    Episodes=row[4],
                    Rating=row[5],
                    Members=row[6],
                )
                db.session.add(anime)
            db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app

@pytest.fixture()
def app():
    app = create_app()
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
