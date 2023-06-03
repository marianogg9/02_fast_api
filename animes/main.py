from flask import Blueprint
from . import db
from .models import Anime

main = Blueprint('main', __name__)

@main.route('/profile')
def profule():
    return 'Profile'

@main.route("/")
def base():
    return  "This is a new API.\n"\
            "\n"\
            "It creates a new sqlite (local FS DB) and populates it from data/anime.csv.\n"\
            "\n"\
            "Methods: \n"\
            "/all will output first 100 animes, sorted by their anime ID.\n"\
            "/anime/[anime name] lists all [anime name]'s details.\n"\
            "/anime/add?[anime_id=str&name=str&type=str&genre=str&episodes=int&rating=str] adds a new entry if absent (and/or lists it if already present).\n"\
            "/anime/update?anime_id=int[&params] will update anime_id's params.\n"\
            "/anime/delete?anime_id=int deletes anime_id from the DB.\n"\
            "\n"\
            "Running: \n"\
            "python3 main.py"

@main.route('/all')
def all():
    listing = []
    for i in Anime.query.order_by(Anime.Anime_ID).limit(100):
        result = {
            "Anime_ID" : i.Anime_ID,
            "Name" : i.Name,
            "Genre" : i.Genre,
            "Type": i.Type,
            "Episodes": i.Episodes,
            "Rating": i.Rating,
            "Members": i.Members
        }
        listing.append(result)
        
    return listing


@main.route("/anime/<string:name>")
def list(name):
    listing = []
    look_for = '%{0}%'.format(name)
    anime = Anime.query.filter(Anime.Name.contains(look_for))
    if anime.first():
        for i in anime:
            result = {
                "Anime_ID" : i.Anime_ID,
                "Name" : i.Name,
                "Genre" : i.Genre,
                "Type": i.Type,
                "Episodes": i.Episodes,
                "Rating": i.Rating,
                "Members": i.Members
            }
            listing.append(result)
    else:
        result = 'error: Anime with Name = ' + str(name) + ' not found.'
        listing.append(result)
    
    return listing

# @app.route("/anime/add/")                                               # localhost:5000/anime/add?anime_id=9&name=What a beautiful day&type=TV&genre=Action&episodes=123
# def add():
#     listing = []

#     with engine.connect() as conn:                                      
#         anime_id = request.args.get('anime_id')
#         name = request.args.get('name')
#         genre = request.args.get('genre')
#         type = request.args.get('type')
#         episodes = request.args.get('episodes')
#         rating = request.args.get('rating')
#         members = request.args.get('members')

#         select_stmt = select(animes).where(animes.c.Name==name)
#         result = conn.execute(select_stmt)
#         if result.first() is None:                                      # only add a new row if it doesn't exist in the DB
#             print('Could not find it, adding..')
#             insert_stmt = insert(animes).values(Anime_ID=anime_id,Name=name,Genre=genre,Type=type,Episodes=episodes,Rating=rating,Members=members)
#             conn.execute(insert_stmt)
#             conn.commit()
#             message = 'Added: ' + name + '. A tip: resend the request to list the added entry.'
#             listing.append(message)
#         else:                                                           # if anime exists, skip and show its row
#             for i in conn.execute(select_stmt):
#                 print("Already exists, skipping..")
#                 listing.append(str(i))
        
#         return listing                         

# @app.route("/anime/update/")
# def update():
#     listing = []

#     with engine.connect() as conn:
#         try:
#             anime_id = request.args.get('anime_id')
#             name = request.args.get('name')
#             genre = request.args.get('genre')
#             type = request.args.get('type')
#             episodes = request.args.get('episodes')
#             rating = request.args.get('rating')
#             members = request.args.get('members') 
#         except: # tried to sanitise input - but it gets skipped.
#             listing.append('One of name, genre, type, episodes, rating or members parameter was not found in the request. Please check the parameters and try again.')
#             return listing

#         select_stmt = select(animes).where(animes.c.Anime_ID==anime_id)
#         result = conn.execute(select_stmt)
#         if anime_id:
#             if result.first() is None:
#                 message = "Anime ID: " + anime_id + " was not found. Please refer to an existing Anime ID. You can get a full list of Animes by accessing the /all endpoint"
#             else:
#                 for row in conn.execute(select_stmt): # i assume there is a better way of using non empty parameters
#                     new_name = name if name else row[1]
#                     new_genre = genre if genre else row[2]
#                     new_type = type if type else row[3]
#                     new_episodes = episodes if episodes else row[4]
#                     new_rating = rating if rating else row[5]
#                     new_members = members if members else row[6]
#                 update_stmt = animes.update().where(animes.c.Anime_ID==anime_id).values(Name=new_name,Genre=new_genre,Type=new_type,Episodes=new_episodes,Rating=new_rating,Members=new_members)      # why does update() have to be written differently than a select?
#                 conn.execute(update_stmt)
#                 conn.commit()
#                 message = 'Updated Name: ' + new_name + ', Genre: ' + new_genre + ', Type: ' + new_type + ', Episodes: ' + str(new_episodes) + ', Rating: ' + new_rating + ', Members: ' + str(new_members) + ' for Anime ID: ' + anime_id
#         else:
#             message = 'Please include anime_id in the request'
        
#         listing.append(message)
#         return listing

# @app.route("/anime/delete")
# def delete():
#     listing = []

#     with engine.connect() as conn:
#         anime_id = request.args.get('anime_id')
#         select_stmt = select(animes).where(animes.c.Anime_ID==anime_id)
#         result = conn.execute(select_stmt)
#         if result.first() is None:
#             message = "Anime ID: " + anime_id + " was not found. Please refer to an existing Anime ID. You can get a full list of Animes by accessing the /all endpoint"
#         else:
#             delete_stmt = animes.delete().where(animes.c.Anime_ID==anime_id)
#             conn.execute(delete_stmt)
#             conn.commit()
#             message = 'Deleted Anime ID: ' + anime_id
        
#         listing.append(message)
#         return listing

# if __name__== '__main__':
#     app.run()