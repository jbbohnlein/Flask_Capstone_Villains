from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid    # for unique ids in primary keys
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow # helps with moving data back and forth
import secrets 

# set variables for class insantiation

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader   # like writing a route where the user
# getting looked for will get loaded

def load_user(user_id):
   return User.query.get(user_id) 

class User(db.Model, UserMixin):       # This whole class is for users to create accounts and login and what data is associated with that account
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(150), nullable=False)     # email can't be empty to sign up
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True) # Want to be able to see/gatekeep who is accessing our stuff
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # when the user creates an account, we'll know what date it was

    def __init__(self, email, password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)   # going to send back a token hex for token which is 24 characters long

    def set_id(self):
        return str(uuid.uuid4())   # when we run this function it will generate a uuid for user and have a primary key that it's own entity

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash    # when they make their password, it'll take their password and hash it, and this pw_hash is the only way to unhash it

    def __repr__(self):
        return f'User {self.email} has been added to the database'

# TODO: Figure out how to make these nullable entries actually nullable without giving me a 500 error

class Villain(db.Model):
    id = db.Column(db.String, primary_key = True)
    villain = db.Column(db.String(200))
    title = db.Column(db.String(200), nullable=False)
    hero = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, villain, title, hero, desc, user_token, id = ''):
        self.id = self.set_id()
        self.villain = villain
        self.title = title
        self.hero = hero
        self.desc = desc
        self.user_token = user_token


    def __repr__(self):
        return f'The following villain has been added to the database: {self.villain} from {self.title}'

    def set_id(self):
        return (secrets.token_urlsafe())

class BookSchema(ma.Schema):
    class Meta:
        fields = ['id','villain', 'title', 'hero', 'desc']

book_schema = BookSchema()
books_schema = BookSchema(many=True)
