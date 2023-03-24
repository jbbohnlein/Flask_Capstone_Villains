from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

# bookshelf = {}

@login_manager.user_loader

def load_user(user_id):
   return User.query.get(user_id) 


class User(db.Model, UserMixin):       # This whole class is for users to create accounts and login and what data is associated with that account
    id = db.Column(db.String, primary_key=True)
    # username = db.Column(db.String(150), nullable=False, default='') # username can't be empty to sign up
    email = db.Column(db.String(150), nullable=False)     # email can't be empty to sign up
    password = db.Column(db.String, nullable=False, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True) # Want to be able to see/gatekeep who is accessing our stuff
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # when the user creates an account, we'll know what date it was

    def __init__(self, email, password='', token='', g_auth_verify=False):     # username=''
        self.id = self.set_id()
        # self.username = username
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

# Create a class of books with the info that I actually want to store. 
# So, when a user wants to update their shelf, they can

class ShelvedBook(db.Model):
    key = db.Column(db.String, primary_key=True)  # Maybe not needed?
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    # cover = db.Column(db.Image)
    year = db.Column(db.Integer)
    avg_rating = db.Column(db.Float(1, 1))
    user_rating = db.Column(db.Integer)

# all these db.s come from ^ where I set variables for class instantiation 
# and set db = SQLAlchemy. This is how data gets put into SQLAlchemy

    def __init__(self,key,title,author,year,avg_rating,user_rating):
        self.key = key
        self.title = title
        self.author = author
        self.year = year
        self.avg_rating = avg_rating
        self.user_rating = user_rating

    def __repr__(self):
        return f'{self.title} has been added to your shelf'

# Need to deal with creating a network and how the data interacts with one another
        # deals with connecting the dots and how things relate to one another:
class BookSchema(ma.Schema):
    class Meta:
        fields = ['key', 'title', 'author', 'year', 'avg_rating', 'user_rating']

book_schema = BookSchema()
books_schema = BookSchema(many=True)