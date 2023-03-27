# Our Helpers file will essentially create an extra function to check tokens for rightful access to data, 
# and create an encoder for our JSON content.

from functools import wraps    # functools comes with python
import secrets
from flask import request, jsonify, json        
import decimal

from models import User

# we could pull in our Contact class as well, but we'll not use that here, as we don't need it for this particular project 
# - just know we could eventually pull that in and give it a token as well.

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

# we are checking to see if 'x-access-token' is in our headers for our API calls - we will see what this looks like when we start 
# actually digging in and posting and getting data - but this process will help us modify the token into such a way that we can 
# use the token and authenticate it.  It allows us to either modify the token or send back specific errors detailing what's 
# gone wrong if we make a faulty API call. 


        if 'x-access-token' in request.headers:         # This request.headers is in Insomnia, or at least that's where I can set it.                     

            token = request.headers['x-access-token'].split(' ')[1]   # headers is setup to be a dictionary. x-access-token is the key
                            # Therefore, we want the 1st index, not the 0th, because the 0th is the word "Bearer"

        if not token:
            return jsonify({'message': 'Token is missing.'}), 401 #error. Trying to give our code directions for knowing and telling us what's wrong

# Check to see if token is in the database:
        try:
            current_user_token = User.query.filter_by(token = token).first() # going to userclass, filter by token, and take first thing
            print(token)                                # QUESTION: Why not just say token? Why does it have to =token?
            print(current_user_token)
        except:
            owner=User.query.filter_by(token=token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):   # from secrets import
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated
    # Note also that the function returns itself - this is unusual, but part of the checking process. 
    # This means it will continue running as long as we're asking for it. That token will stay in place

    #  *args, **kwargs - as many tokens as we add, we want it to be able to take that data

    # The *args and **kwargs (and the decorated getting returned) are allowing us to continue 
    # adding more and more data to the process as long as we run the function.


# This checks that the instances of json are decimals, and then changes them into strings that we can use later:
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):   # checking to see if the object is a certain data type
            return str(obj)
        return super(JSONEncoder,self).default(obj)