from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

# practice
@api.route('/getdata')
def getdata():
    return {'Book': 'Yes'}

# Create a new book
@api.route('/bookshelf', methods = ['POST'])    # POST means we can actually send data to the api
@token_required                             # requires the user to have a token
def add_book(current_user_token):
    key = request.json['key']
    author = request.json['author']     # json works in key-value pairs, so we're setting the value of 'name' = name
    title = request.json['title']
    year = request.json['year']
    user_token = current_user_token.token  

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(key, author, title, year, user_token = user_token )  # Contact() comes from models.py. Looks similar but the ID will get written for us
                                                            # ^ This overwrites the default from the Contact() class 
    db.session.add(book)    # adding / staging it to the database
    db.session.commit()         # committing it to the database

    response = book_schema.dump(book)    # contact_schema is also from models.py which instantiates a class (we didn't write this but brought it in from marshmallow)
    return jsonify(response)

# Delete a book from the shelf
@api.route('/bookshelf/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

# Return the whole shelf
@api.route('/bookshelf', methods = ['GET'])
@token_required
def get_shelf(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()  # This brings back all the contacts in our database
    response = books_schema.dump(books)
    return jsonify(response)

# Return a single book using its ID
@api.route('/bookshelf/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)

#Update a book
@api.route('bookshelf/<id>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id)
    book.name = request.json['name']     # json works in key-value pairs, so we're setting the value of 'name' = name
    book.distiller = request.json['distiller']
    book.type = request.json['type']
    book.country = request.json['country']
    book.user_token = current_user_token.token 

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)