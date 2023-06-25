# TODO: For imports usually we sort in the alphabetical order depending on their source
#   First we import python built-in modules
#   Then, we import third parties modules
#   Finally, we import local modules/projects
#   You can use isort to sort automatically imports for you

from flask import Blueprint, request, render_template, make_response
from . import db
from .models import Anime, User
import os
from flasgger import swag_from
from .auth import login_required

main = Blueprint('main', __name__)
secret = os.environ['FLASK_SECRET_KEY']

@main.route('/profile')
@swag_from('apidocs/profile.yaml')
@login_required
def profile():
    auth_header = request.headers.get('Authorization')

    # TODO: If there is no auth header, should be abort the request directly
    #   Instead of passing a empty string for the header?
    if auth_header:
        # TODO: In production code, we use logging library instead of print
        print(auth_header.split(" ")[0])
        auth_token = auth_header.split(" ")[0]
    else:
        auth_token = ''
        # TODO: Usually it is good to raise an exception as soon as possible
        #   If no auth header i would return 401 directly

    if auth_token:
        resp = User.decode_auth_token(auth_token,secret)
        # TODO: Usually it is good to raise an exception as soon as possible
        #   If invalid token i would return 401 directly
        if not isinstance(resp,str):
            user = User.query.filter_by(id=resp).first()
            response_object = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email
                }
            }
            return make_response(response_object), 200
        response_object = {
            'status': 'fail',
            'message': resp
        }
        return make_response(response_object), 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid token'
        }
        return make_response(response_object), 401

@main.route('/')
@swag_from('apidocs/base.yaml')
def index():
    '''
    Show a minimal API documentation page
    '''
    return render_template('base.html')

@main.route('/all')
@swag_from('apidocs/all.yaml')
@login_required
# TODO: all => movies
def all():
    '''
    List first 100 animes per anime id

    Request headers:
        
        Authorization (JWT token from signup/login)::string
    
    Input:

        none

    Output:

        JSON list
    '''
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
    return make_response(listing), 200


@main.route('/anime/<string:name>')
@swag_from('apidocs/get_anime.yaml')
@login_required
def list(name):
    '''
    Get information about a given anime by its name

    Request headers:
        
        Authorization (JWT token from signup/login)::string

    Input: 

        name::string (required)

    Output: 

        JSON object:
            anime_id::int
            name::string
            genre::string
            type::string
            episodes::int
            rating::string
            members::int
    '''
    listing = []
    look_for = '%{0}%'.format(name)
    anime = Anime.query.filter(Anime.Name.contains(look_for))
    if anime.first():
        for i in anime:
            output = {
                "Anime_ID" : i.Anime_ID,
                "Name" : i.Name,
                "Genre" : i.Genre,
                "Type": i.Type,
                "Episodes": i.Episodes,
                "Rating": i.Rating,
                "Members": i.Members
            }
            listing.append(output)
    else:
        output = 'error: Anime with Name = ' + str(name) + ' not found.'
        listing.append(output)
        return make_response(listing), 404
    
    return make_response(listing), 200

@main.route('/anime/add/<int:anime_id>', methods=['POST'])
@swag_from('apidocs/add_anime.yaml')
@login_required
def add(anime_id):
    '''
    Add a new anime

    Request headers:
        
        Authorization (JWT token from signup/login)::string

    Input:

        Querystring:

            anime_id::int (required)
            name::string (optional)
            genre::string (optional)
            type::string (optional)
            episodes::int (optional)
            rating::string (optional)
            members::int (optional)
    
    Output:

        JSON:

            confirmation message::string
    '''
    listing = []

    # TODO: I don't think the client have to enter a animeid to create an anime
    #   The backend is responsible to generate a new anime id
    if anime_id is None:
        listing.append('Please enter an Anime ID')
        return listing

    # TODO: Here you can use Pydantic to validate the data
    name = request.args.get('name')
    genre = request.args.get('genre')
    type = request.args.get('type')
    episodes = request.args.get('episodes')
    rating = request.args.get('rating')
    members = request.args.get('members')

    # TODO: I would put this call to SQLAlchemy in a utils function called get_movie_by_id
    result = Anime.query.filter_by(Anime_ID=anime_id).first()

    if result:
        print('already exists')
        message = 'Anime with Anime_ID: ' + str(anime_id) + ' already exists.'
        listing.append(message)
        return make_response(listing), 201
    else:
        # TODO: This logic can be put in another file called utils
        #   it will keep things clear in the view and will isolate your code in a new file called utils
        #   this file will contain a function called create_anime
        #   as a result it will become simpler to test the creation of anime as well
        new_anime = Anime(Anime_ID=anime_id,Name=name,Genre=genre,Type=type,Episodes=episodes,Rating=rating,Members=members)
        db.session.add(new_anime)
        db.session.commit()

        # TODO: Instead of querying back the anime could you just use new_anime?
        new_result = Anime.query.filter_by(Anime_ID=anime_id).first()
        output = {
                "Anime_ID" : new_result.Anime_ID,
                "Name" : new_result.Name,
                "Genre" : new_result.Genre,
                "Type": new_result.Type,
                "Episodes": new_result.Episodes,
                "Rating": new_result.Rating,
                "Members": new_result.Members
        }
        listing.append(output)
    
    return make_response(listing), 200

@main.route('/anime/update/<int:anime_id>', methods=['PATCH'])
@swag_from('apidocs/update_anime.yaml')
@login_required
def update(anime_id):
    '''
    Update an existing anime

    Request headers:
        
        Authorization (JWT token from signup/login)::string

    Input:

        Querystring:

            anime_id::int (required)
            name::string (optional)
            genre::string (optional)
            type::string (optional)
            episodes::int (optional)
            rating::string (optional)
            members::int (optional)
    
    Output:

        JSON object:

            anime_id::int
            name::string
            genre::string
            type::string
            episodes::int
            rating::string
            members::int
    '''
    listing = []
    # anime_id = request.args.get('anime_id')

    # TODO: If parameter is missing you can return a 400 Bad syntax error with this message
    if anime_id is None:
        listing.append('Please enter an Anime ID')
        return listing

    # TODO: Here you can use Pydantic to validate the data
    name = request.args.get('name')
    genre = request.args.get('genre')
    type = request.args.get('type')
    episodes = request.args.get('episodes')
    rating = request.args.get('rating')
    members = request.args.get('members')

    result = Anime.query.filter_by(Anime_ID=anime_id).first()

    if result:
        result.Name = (name if name is not None else result.Name)
        result.Genre = (genre if genre is not None else result.Genre)
        result.Type = (type if type is not None else result.Type)
        result.Episodes = (episodes if episodes is not None else result.Episodes)
        result.Rating = (rating if rating is not None else result.Rating)
        result.Members = (members if members is not None else result.Members)

        db.session.commit()

        new_result = Anime.query.filter_by(Anime_ID=anime_id).first()
        # TODO: Pydantic should allow you to serialize data to prepare the response
        output = {
                "Anime_ID" : new_result.Anime_ID,
                "Name" : new_result.Name,
                "Genre" : new_result.Genre,
                "Type": new_result.Type,
                "Episodes": new_result.Episodes,
                "Rating": new_result.Rating,
                "Members": new_result.Members
        }
        listing.append(output)
    else:
        message = 'Anime with Anime ID: ' + str(anime_id) + ' does not exist. Please include an existing Anime ID.'
        listing.append(message)
        return make_response(listing), 201

    return make_response(listing), 200

@main.route('/anime/delete/<int:anime_id>', methods=['DELETE'])
@swag_from('apidocs/delete_anime.yaml')
@login_required
def delete(anime_id):
    '''
    Delete an exsiting anime

    Request headers:
        
        Authorization (JWT token from signup/login)::string

    Input:

        Querystring:

            anime_id::int (required)
    
    Output:

        JSON:

            confirmation message::string
    '''
    listing = []

    # TODO: If parameter is missing you can return a 400 Bad syntax error with this message
    if anime_id is None:
        listing.append('Please enter an Anime ID')
        return listing
    
    result = Anime.query.filter_by(Anime_ID=anime_id).first()

    if result:
        db.session.delete(result)
        db.session.commit()
        message = 'Anime with Anime ID: ' + str(anime_id) + ' has been deleted from the DB.'
        listing.append(message)
    else:
        message = 'Anime with Anime ID: ' + str(anime_id) + ' does not exist. Please include an existing Anime ID.'
        listing.append(message)
        return make_response(listing), 201

    return make_response(listing), 200