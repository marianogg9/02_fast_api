import csv
from flask import Flask
from sqlalchemy import create_engine, select, Table, Column, Integer, MetaData, String

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
    return 'This is a new API'

@app.route("/all")
def all():
    listado = []

    with engine.connect() as conn:                                      # show an ordered set of rows
        stmt = select(animes).limit(100).order_by(animes.c.Anime_ID)
        for i in conn.execute(stmt):
            # print(i)
            listado.append(str(i))                                      # this has to be JSON serialisable, so sqlalchemy result object (of type = row) won't work for Flask, hence a list
        
        return listado                                                  

@app.route("/animes/<string:name>")
def querying_animes(name):
    listado = []

    with engine.connect() as conn:                                  
        stmt = select(animes).limit(100).order_by(animes.c.Anime_ID).where(animes.c.Name==name)
        for i in conn.execute(stmt):
            # print(i)
            listado.append(str(i))
        
        return listado                                                  

@app.route("/anime/add/<string:name>")
def querying(name):
    listado = []

    with engine.connect() as conn:                                      
        stmt = select(animes).limit(100).order_by(animes.c.Anime_ID).where(animes.c.Name==name)
        for i in conn.execute(stmt):
            # print(i)
            listado.append(str(i))
        
        return listado                                                 

if __name__== '__main__':
    app.run()