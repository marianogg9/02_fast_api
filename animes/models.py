from . import db
import datetime, jwt

class Anime(db.Model):
        Anime_ID = db.Column(db.Integer,primary_key=True)
        Name = db.Column(db.String)
        Genre = db.Column(db.String)
        Type = db.Column(db.String)
        Episodes = db.Column(db.Integer)
        Rating = db.Column(db.String)
        Members = db.Column(db.Integer)

class User(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        email = db.Column(db.String(100),unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(100))

        def encode_auth_token(self, user_id, secret):
                try:
                        payload = {
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,seconds=300),
                                'iat': datetime.datetime.utcnow(),
                                'sub': user_id
                        }
                        return jwt.encode(
                                payload,
                                secret,
                                algorithm='HS256'
                        )
                except Exception as e:
                        return e
                
        @staticmethod
        def decode_auth_token(auth_token,secret):
                try:
                        payload = jwt.decode(auth_token,secret)
                        is_blacklisted_token = BlackListToken.check_blacklist_token(auth_token)
                        if is_blacklisted_token:
                                return 'Token blacklisted. Login again.'
                        else:
                                return payload['sub']
                except jwt.ExpiredSignature:
                        return 'JWT token expired, login again'
                except jwt.InvalidTokenError:
                        return 'Invalid token, login again'

class BlackListToken(db.Model):
        id = db.Column(db.Integer,primary_key=True, autoincrement = True)
        token = db.Column(db.String(500), unique = True, nullable = False)
        blacklisted_on = db.Column(db.DateTime, nullable = False)

        def __init__(self, token):
                self.token = token
                self.blacklisted_on = datetime.datetime.now()

        def __repr__(self):
                return '<id: token: {}'.format(self.token)

        @staticmethod
        def check_blacklist_token(auth_token):
                res = BlackListToken.query.filter_by(token=str(auth_token)).first()
                if res:
                        return True
                else:
                        return False

        