from flask import Blueprint, redirect, url_for, request, make_response, g
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User, BlackListToken
from . import db
from flask_login import login_required,logout_user
import os
from flasgger import swag_from
from functools import wraps

auth = Blueprint('auth', __name__)
secret = os.environ['FLASK_SECRET_KEY']


def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            print(auth_header.split(" ")[0])
            auth_token = auth_header.split(" ")[0]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token,secret)
            if isinstance(resp,str):
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(response_object), 402
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid token'
            }
            return make_response(response_object), 401
        return f(*args, **kwargs)
    return decorated_function


# TODO: Is it still needed?
@auth.route('/signup')
def signup():
    '''
    Signup method description (text)
    '''
    return "Signup: curl -XPOST -d '\"email\":\"your_email\",\"password\":\"your_password\"}' -H 'Content-Type: application/json' server_address:port/signup"

@auth.route('/signup', methods = ['POST'])
@swag_from('apidocs/signup.yaml')
def signup_post():
    '''
    Signup

    Input:

        JSON object:
            
            email::string
            password::string

    Output:

        JSON object:

            auth_token::string
            message::string
            status::string
    '''
    post_data = request.get_json()
    user = User.query.filter_by(email=post_data.get('email')).first()
    if not user:
        try:
            new_user = User(email=post_data.get('email'),name=post_data.get('name'),password=generate_password_hash(post_data.get('password'),method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            auth_token = new_user.encode_auth_token(new_user.id, secret)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode("utf-8")
            }
            return make_response(response_object), 200
        except Exception:
            response_object = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(response_object), 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in'
        }
        return make_response(response_object), 202


# TODO: Is it still needed?
@auth.route('/login')
def login():
    '''
    Login method description (text)
    '''
    return "Login: curl -XPOST -d '\"email\":\"your_email\",\"password\":\"your_password\"}' -H 'Content-Type: application/json' server_address:port/login"

# TODO: An other way would be to have a uri "/tokens/" when you make a POST Request you are logging in.
@auth.route('/login', methods=['POST'])
@swag_from('apidocs/login.yaml')
def login_post():
    '''
    Login

    Input:

        JSON object:
            
            email::string
            password::string

    Output:

        JSON object:

            auth_token::string
            message::string
            status::string
    '''
    post_data = request.get_json()
    try:
        # TODO: This logic could be in the utils file in a function called get_user_by_email
        user = User.query.filter_by(email=post_data.get('email')).first()
        if user and check_password_hash(user.password,post_data.get('password')):
            auth_token = user.encode_auth_token(user.id,secret)
            if auth_token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode("utf-8")
                }
                return make_response(response_object), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(response_object), 404
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Try again.'
        }
        return make_response(response_object), 201

# TODO: Still needed?
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# TODO: Still needed?
@auth.route('/logout', methods = ['POST'])
@swag_from('apidocs/logout.yaml')
@login_required
def logout_post():

    auth_header = request.headers.get('Authorization')
    if auth_header:
        print(auth_header.split(" ")[0])
        auth_token = auth_header.split(" ")[0]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token,secret)
        if not isinstance(resp,str):
            blacklist_token = BlackListToken(token=auth_token)
            try:
                db.session.add(blacklist_token)
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return make_response(response_object), 200
            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': e
                }
                return make_response(response_object), 201
        else:
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