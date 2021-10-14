from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    api_key = db.Column(db.String(100), unique=True)
    requests = db.Column(db.Integer, default=0)
    unsafe_requests = db.Column(db.Integer, default=0)
