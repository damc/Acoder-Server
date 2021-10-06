from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from os import getenv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
app.config['SECRET_KEY'] = getenv('SECRET_KEY')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from .user import User
from .auth import *

db.create_all()
