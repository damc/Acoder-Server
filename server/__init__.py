from logging import basicConfig, DEBUG
from os import getenv
from sys import stdout

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


basicConfig(stream=stdout, level=DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app, engine_options={'pool_pre_ping': True})
login_manager = LoginManager()
login_manager.init_app(app)

from .user import User
from .auth import *
from .api import *

db.create_all()
