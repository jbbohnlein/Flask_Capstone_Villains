from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')
                                        # ^ Tells where our template folder is located


@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'User-created')
            return redirect(url_for('site.home'))   # goes and looks for home() in site folder, route.py. After they've created their account, sends them back to home page
    except:
        raise Exception('Invalid form data. Please check your form')
    return render_template('sign_up.html', form=form)   # return the sign up.html page as long as they're here until it works

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form=UserLoginForm()
    try:     
        if request.method == 'POST' and form.validate_on_submit(): 
            email = form.email.data          
            password = form.password.data
            print(email,password)

            logged_user = User.query.filter(User.email == email).first()   # take the email data, check it against the User(), filter through all the data that meets that parameter
            # return the first account that comes up, which should be the logged user
            if logged_user and check_password_hash(logged_user.password, password):     # we pulled this up at the top from models. check_password_hash will unhash it
            # and make sure it's the correct credentials. The logged_user is checking to see if they're in the database
                login_user(logged_user)
                flash('You were successful in your initiation. Welcome to the Jedi Knights!', 'auth-success') # auth-success talks to application??
                return redirect(url_for('site.profile')) # once they sign in, it takes them to their user profile page
            else:
                flash('You have failed in your attempt to access this content.', 'auth-failed')
    except:
        raise Exception('Invalid form data. Please check your form.')
    return render_template('sign_in.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))