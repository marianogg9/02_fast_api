from . import db

class Anime(db.Model):
        Anime_ID = db.Column(db.Integer,primary_key=True)
        Name = db.Column(db.String)
        Genre = db.Column(db.String)
        Type = db.Column(db.String)
        Episodes = db.Column(db.Integer)
        Rating = db.Column(db.String)
        Members = db.Column(db.Integer)