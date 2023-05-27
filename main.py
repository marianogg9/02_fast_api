import csv
from flask import Flask,request
from sqlalchemy import create_engine, select, insert, Table, Column, Integer, MetaData, String

engine = create_engine("sqlite+pysqlite:///local.db", echo=True)        # create a file based DB
metadata = MetaData()
animes = Table('Anime',
            metadata,
                Column('Anime_ID',Integer),
                Column('Name',String),
                Column('Genre',String),
                Column('Type',String),
                Column('Episodes',Integer),
                Column('Rating',String),
                Column('Members',Integer)
                )
metadata.create_all(engine)                                             # create the table
insert_query = animes.insert()

with open('data/anime.csv','r',encoding="utf-8") as csvfile:            # read input data file
    csv_reader = csv.reader(csvfile,delimiter=',')
    first_line = csvfile.readline()
    with engine.connect() as conn:                                      # open a connection to the DB
        conn.execute(
            insert_query,
            [{"Anime_ID":row[0],"Name":row[1],"Genre":row[2],"Type":row[3],"Episodes":row[4],"Rating":row[5],"Members":row[6]} 
            for row in csv_reader]
        )
        conn.commit()                                                   # commit the changes

app = Flask(__name__)

@app.route("/")
def base():
    return  "This is a new API.\n"\
            "\n"\
            "It creates a new sqlite in memory DB and populates it from data/anime.csv.\n"\
            "\n"\
            "Methods: \n"\
            "/all will output first 100 animes, sorted by their anime ID.\n"\
            "/anime/anime_name lists all anime_name details.\n"\
            "/anime/add?anime_id=str&name=str&type=str&genre=str&episodes=int&rating=float adds a new entry if absent (and/or lists it if already present).\n"\
            "\n"\
            "Running: \n"\
            "python3 main.py"

@app.route("/all")
def all():
    listing = []

    with engine.connect() as conn:                                      # show an ordered set of rows
        stmt = select(animes).limit(100).order_by(animes.c.Anime_ID)
        for i in conn.execute(stmt):
            # print(i)
            listing.append(str(i))                                      # this has to be JSON serialisable, so sqlalchemy result object (of type = row) won't work for Flask, hence a list
        
        return listing                                                  

@app.route("/anime/<string:name>")
def querying_animes(name):
    listing = []

    with engine.connect() as conn:                                  
        stmt = select(animes).limit(100).order_by(animes.c.Anime_ID).where(animes.c.Name==name)
        result = conn.execute(stmt)
        if result.first() is None:
            messagge = 'Anime: "' + name + '" not found'
            listing.append(messagge)
        else:
            for i in conn.execute(stmt):                                # kinda weird, not sure why I cannot use 'result' again (it throws as 'qlalchemy.exc.ResourceClosedError: This result object is closed' error)
                listing.append(str(i))
        
        return listing                                                  

@app.route("/anime/add/")                                               # localhost:5000/anime/add?anime_id=9&name=What a beautiful day&type=TV&genre=Action&episodes=123
def add():
    listing = []

    with engine.connect() as conn:                                      
        anime_id = request.args.get('anime_id')
        name = request.args.get('name')
        genre = request.args.get('genre')
        type = request.args.get('type')
        episodes = request.args.get('episodes')
        rating = request.args.get('rating')
        members = request.args.get('members')

        select_stmt = select(animes).where(animes.c.Name==name)
        result = conn.execute(select_stmt)
        if result.first() is None:                                      # only add a new row if it doesn't exist in the DB
            print('Could not find it, adding..')
            insert_stmt = insert(animes).values(Anime_ID=anime_id,Name=name,Genre=genre,Type=type,Episodes=episodes,Rating=rating,Members=members)
            conn.execute(insert_stmt)
            conn.commit()
            message = 'Added: ' + name + '. A tip: resend the request to list the added entry.'
            listing.append(message)
        else:                                                           # if anime exists, skip and show its row
            for i in conn.execute(select_stmt):
                print("Already exists, skipping..")
                listing.append(str(i))
        
        return listing                                                 

if __name__== '__main__':
    app.run()