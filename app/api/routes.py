from flask import Blueprint, render_template, request, jsonify
import requests
import json
from helpers import token_required
from models import db, ShelvedBook, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
def getdata():
    return {'yee': 'haw'} 

# Get results from the Open Library search

@api.route('/results', methods=['GET'])
def results():
    search = request.args.get("search")
    req = requests.get(f'https://openlibrary.org/search.json?q={search}&fields=key%20title%20author_name%20first_publish_year%20ratings_average&limit=9') 
    data = json.loads(req.content)
    data = data['docs'][:9]
    return render_template('results.html', data=data)

# Show the bookshelf

@api.route('/bookshelf', methods=['GET'])
@token_required
def view_shelf(current_user_token):
    a_user = current_user_token.token
    books = ShelvedBook.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

# Add a book to the shelf

@api.route('/bookshelf', methods = ['POST'])    # POST means we can actually send data to the api
@token_required                             # requires the user to have a token
def shelve_book(current_user_token):
    key = request.json['key']
    title = request.json['title']     # json works in key-value pairs, so we're setting the value of 'name' = name
    author = request.json['author']
    year = request.json['year']
    avg_rating = request.json['avg_rating']
    user_rating = request.json['user_rating']

    print(f'BIG TESTER: {current_user_token.token}')

    book = ShelvedBook(key, title, author, year, avg_rating, user_rating)  # Contact() comes from models.py. Looks similar but the ID will get written for us
             # user_token = user_token                                            # ^ This overwrites the default from the Contact() class 
    db.session.add(book)    # adding / staging it to the database
    db.session.commit()         # committing it to the database

    response = book_schema.dump(book)    # book_schema is also from models.py which instantiates a class (I didn't write this but brought it in from marshmallow)
    return jsonify(response)

#  Get a single book from the bookshelf

@api.route('/bookshelf/<key>', methods = ['GET'])   # This <id> is a variable that we'll be able to call and pull down into the rest of the function
@token_required
def get_book(key):              # Not sure how to do the current_token here      Possible arg: current_user_token, 
    # a_user = current_user_token.token
    book = ShelvedBook.query.get(key)   # user_token = a_user    here
    response = book_schema.dump(book)
    return jsonify(response)


# Update book

@api.route('/bookshelf/<key>', methods = ['POST', 'PUT'])    # POST means we can actually send data to the api
@token_required                             # requires the user to have a token
def update_book(current_user_token, key):
    book = ShelvedBook.query.get(key)
    book.title = request.json['title']     
    book.author = request.json['author']
    book.year = request.json['year']
    book.avg_rating = request.json['avg_rating']
    book.user_rating = request.json['user_rating']

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)


# Delete Book

@api.route('/bookshelf/<key>', methods = ['DELETE'])
@token_required
def remove_book(current_user_token, key):    # Need current_user_token here??
    book = ShelvedBook.query.get(key)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)