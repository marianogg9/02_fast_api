import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = b'9-/;,mM13XgQ;$X!'                              # dummy key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animes.db'

    db.init_app(app)

    from . import models

    with app.app_context():
        db.drop_all()
        db.create_all()

        with open('data/anime.csv','r',encoding="utf-8") as csvfile:            # read input data file
            csv_reader = csv.reader(csvfile,delimiter=',')
            first_line = csvfile.readline()
            for row in csv_reader:
                anime = models.Anime(Anime_ID=str(row[0]),Name=row[1],Genre=row[2],Type=row[3],Episodes=row[4],Rating=row[5],Members=row[6])
                db.session.add(anime)
            db.session.commit()

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app