from flask import Blueprint, render_template

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/results')
def results():
    return render_template('results.html')

# @site.route('/rateit')
# def rate_book():
#     return render_template('rating.html')

@site.route('/bookshelf')
def show_shelf():
    return render_template('bookshelf.html')


@site.route('/profile')
def profile():
    return render_template('profile.html')


#  need a call in here that pulls user token