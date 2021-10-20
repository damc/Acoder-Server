from logging import basicConfig, DEBUG
from os import getenv
from sys import stdout

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

basicConfig(stream=stdout, level=DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, engine_options={'pool_pre_ping': True})

cache = Cache(app, config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': getenv('REDIS_URL')
})

login_manager = LoginManager()
login_manager.init_app(app)

from .user import User
from .auth import *
from .api import *

db.create_all()
