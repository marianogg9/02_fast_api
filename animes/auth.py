from flask import Blueprint, redirect, url_for, request, make_response
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from . import db
from flask_login import login_required,logout_user
import os

auth = Blueprint('auth', __name__)
secret = os.environ['FLASK_SECRET_KEY']

@auth.route('/signup')
def signup():
    '''
    Signup method description (text)
    '''
    return "Signup: curl -XPOST -d '\"email\":\"your_email\",\"password\":\"your_password\"}' -H 'Content-Type: application/json' server_address:port/signup"

@auth.route('/signup', methods = ['POST'])
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
            #print(response_object)
            return make_response(response_object), 201
        except Exception:
            #logging.exception('some error')
            response_object = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(response_object), 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in'
        }
        return make_response(response_object), 202

@auth.route('/login')
def login():
    '''
    Login method description (text)
    '''
    return "Login: curl -XPOST -d '\"email\":\"your_email\",\"password\":\"your_password\"}' -H 'Content-Type: application/json' server_address:port/login"

@auth.route('/login', methods=['POST'])
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
        return make_response(response_object), 500

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))