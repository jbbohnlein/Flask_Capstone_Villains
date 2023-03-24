from flask import Flask
from config import Config
from models import login_manager, ma, db as root_db   # This has already been imported into models
from .api.routes import api
from .site.routes import site
from .authentication.routes import auth

from flask_sqlalchemy import SQLAlchemy   # At first, these can't be found because they haven't been stored in any folders. They exist but haven't been installed into app
from flask_migrate import Migrate
from flask_cors import CORS    # this will help prevent cross-site request forgery
from helpers import JSONEncoder


app = Flask(__name__)
CORS(app)

app.register_blueprint(api)
app.register_blueprint(site)
app.register_blueprint(auth)

app.json_encoder = JSONEncoder
app.config.from_object(Config)
root_db.init_app(app)   # This initiaties the app and makes the database
login_manager.init_app(app)  # this applies the things we've made into the app
ma.init_app(app)
migrate = Migrate(app, root_db)





