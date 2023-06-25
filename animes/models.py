from . import db
import datetime, jwt

# TODO: Add one more empty line
class Anime(db.Model):
        # TODO: I would just call it 'id'
        Anime_ID = db.Column(db.Integer,primary_key=True)
        # TODO: Is a Name unique, Can a Name be null?
        # TODO: By convention, we use lowercase for property of a class
        Name = db.Column(db.String)
        Genre = db.Column(db.String)
        Type = db.Column(db.String)
        Episodes = db.Column(db.Integer)
        Rating = db.Column(db.String)
        Members = db.Column(db.Integer)


# TODO: Add one more empty line
class User(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        email = db.Column(db.String(100),unique=True)
        # TODO: Does it mean the password are visible in the db?
        password = db.Column(db.String(100))
        name = db.Column(db.String(100))

        # TODO: Can you add docstrings for this function
        #  and typing hints for inputs and outputs?
        def encode_auth_token(self, user_id, secret):
                # TODO: Move 4 spaces to the left
                try:
                        # TODO: Move 8 spaces to the left
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
                        # TODO: 4 spaces to the left
                        #       What's the goal of catching an exception to only return it?
                        #       The exception will come back to the caller of encode_auth_token doing nothing
                        #       having a similar results
                        return e
                
        @staticmethod
        def decode_auth_token(auth_token,secret):
                try:
                        # TODO: 4 spaces to the left
                        payload = jwt.decode(auth_token,secret)
                        is_blacklisted_token = BlackListToken.check_blacklist_token(auth_token)
                        if is_blacklisted_token:
                                # TODO: 4 spaces to the left
                                return 'Token blacklisted. Login again.'
                        else:
                                # TODO: 4 spaces to the left
                                return payload['sub']
                except jwt.ExpiredSignature:
                        # TODO: 4 spaces to the left
                        return 'JWT token expired, login again'
                except jwt.InvalidTokenError:
                        # TODO: 4 spaces to the left
                        return 'Invalid token, login again'

# TODO: Add one more empty line
class BlackListToken(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        token = db.Column(db.String(500), unique=True, nullable=False)
        blacklisted_on = db.Column(db.DateTime, nullable=False)

        def __init__(self, token):
                # TODO: 4 spaces to the left
                self.token = token
                self.blacklisted_on = datetime.datetime.now()

        def __repr__(self):
                # TODO: 4 spaces to the left
                # TODO: You can use f string here
                #       f"<id: token: {self.token}"
                return '<id: token: {}'.format(self.token)

        @staticmethod
        def check_blacklist_token(auth_token):
                # TODO: You could make a oneline here
                #       You could use exists and scalar here. https://stackoverflow.com/questions/7646173/sqlalchemy-exists-for-query
                res = BlackListToken.query.filter_by(token=str(auth_token)).first()
                if res:
                        return True
                else:
                        return False

        