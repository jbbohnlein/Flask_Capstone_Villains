from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, Villain, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

# practice
@api.route('/getdata')
def getdata():
    return {'Book': 'Yes'}

# Create a new book
@api.route('/bookshelf', methods = ['POST'])    # POST means we can actually send data to the api
@token_required                             # requires the user to have a token
def add_book(current_user_token):
    villain = request.json['villain']
    title = request.json['title']
    hero = request.json['hero']     # json works in key-value pairs, so we're setting the value of 'name' = name
    desc = request.json['desc']
    user_token = current_user_token.token  

    print(f'BIG TESTER: {current_user_token.token}')

    villain_select = Villain(villain, title, hero, desc, user_token = user_token )  # Contact() comes from models.py. Looks similar but the ID will get written for us
                                                            # ^ This overwrites the default from the Contact() class 
    db.session.add(villain_select)    # adding / staging it to the database
    db.session.commit()         # committing it to the database

    response = book_schema.dump(villain_select)    # contact_schema is also from models.py which instantiates a class (we didn't write this but brought it in from marshmallow)
    return jsonify(response)

# Delete a book from the shelf
@api.route('/bookshelf/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    villain_select = Villain.query.get(id)
    db.session.delete(villain_select)
    db.session.commit()
    response = book_schema.dump(villain_select)
    return jsonify(response)

# Return the whole shelf
@api.route('/bookshelf', methods = ['GET'])
@token_required
def get_shelf(current_user_token):
    a_user = current_user_token.token
    villains = Villain.query.filter_by(user_token = a_user).all()  # This brings back all the contacts in our database
    response = books_schema.dump(villains)
    return jsonify(response)

# Return a single book using its ID
@api.route('/bookshelf/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, id):
    villain_select = Villain.query.get(id)
    response = book_schema.dump(villain_select)
    return jsonify(response)

#Update a book
@api.route('/bookshelf/<id>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    villain_select = Villain.query.get(id)
    villain_select.villain = request.json['villain']
    villain_select.title = request.json['title']     # json works in key-value pairs, so we're setting the value of 'name' = name
    villain_select.hero = request.json['hero']
    villain_select.desc = request.json['desc']

    villain_select.user_token = current_user_token.token 

    db.session.commit()
    response = book_schema.dump(villain_select)
    return jsonify(response)

#Return the token
@api.route('/bookshelf', methods = ['GET'])
@token_required
def get_token(current_user_token):
    user_token = current_user_token
    return user_token