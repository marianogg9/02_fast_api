from flask import Blueprint, redirect, url_for, request, make_response, g, abort
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
                return {'status':'fail', 'message':resp}, 402
        else:
            return {'status':'fail','message':'Provide a valid token'}, 401
        return f(*args, **kwargs)
    return decorated_function


@auth.route('/signup')
def signup():
    return "Signup: curl -XPOST -d '\"email\":\"your_email\",\"password\":\"your_password\"}' -H 'Content-Type: application/json' server_address:port/signup"

@auth.route('/signup', methods = ['POST'])
@swag_from('apidocs/signup.yaml')
def signup_post():
    post_data = request.get_json()
    user = User.query.filter_by(email=post_data.get('email')).first()
    if not user:
        try:
            new_user = User(email=post_data.get('email'),name=post_data.get('name'),password=generate_password_hash(post_data.get('password'),method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            auth_token = new_user.encode_auth_token(new_user.id, secret)
            return {'status':'success','message':'Successfully registered','auth_token':auth_token.decode("utf-8")}, 200
        except Exception:
            return {'status':'fail','message':'Some error ocurred, please try again'}, 201
    else:
        return {'status':'fail','message':'User already exists, please log in instead'}, 202

@auth.route('/login')
def login():
    return "Login: curl -XPOST -d '\"email\":\"your_email\",\"password\":\"your_password\"}' -H 'Content-Type: application/json' server_address:port/login"

@auth.route('/login', methods=['POST'])
@swag_from('apidocs/login.yaml')
def login_post():
    post_data = request.get_json()
    try:
        user = User.query.filter_by(email=post_data.get('email')).first()
        if user and check_password_hash(user.password,post_data.get('password')):
            auth_token = user.encode_auth_token(user.id,secret)
            if auth_token:
                return {'status':'success','message':'Successfully logged in.','auth_token':auth_token.decode("utf-8")}, 200
        else:
            # return {'status':'fail','message':'User does not exist, try with a different user'}, 404
            abort(404,description='User does not exist, try with a different user')
    except Exception as e:
        return {'status':'fail','message':e}, 201

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

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
                return {'status':'success','message':'Successfully logged out'}, 200
            except Exception as e:
                return {'status':'fail','message':e}, 201
        else:
            return {'status':'fail','message':resp}, 401
    else:
        return {'status':'fail','message':'Please provide a valid token'}, 401