from flask_login import UserMixin
from . import db

class Anime(db.Model):
        Anime_ID = db.Column(db.Integer,primary_key=True)
        Name = db.Column(db.String)
        Genre = db.Column(db.String)
        Type = db.Column(db.String)
        Episodes = db.Column(db.Integer)
        Rating = db.Column(db.String)
        Members = db.Column(db.Integer)

class User(UserMixin, db.Model):
        id = db.Column(db.Integer,primary_key=True)
        email = db.Column(db.String(100),unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(100))