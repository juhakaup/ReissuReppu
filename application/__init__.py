from flask import Flask
app = Flask(__name__)

#db
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gearlists.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

#app functionality
from application import views

from application.articles import models
from application.articles import views

from application.auth import models
from application.auth import views

from application.lists import models
from application.lists import views

#login
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Login required"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#create db if needed
db.create_all()