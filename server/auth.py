from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from secrets import token_urlsafe
from werkzeug.security import generate_password_hash, check_password_hash

from . import app
from . import db
from . import login_manager
from .user import User


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.query.get(int(user_id))


@app.route('/')
def index():
    """Index page."""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        accept_terms = request.form['accept_terms']

        if not email or not password or not password_repeat or not accept_terms:
            flash('Please fill all the fields.')
            return redirect(url_for('register'))

        if accept_terms != 'on':
            flash('Please accept terms and conditions.')
            return redirect(url_for('register'))

        if password != password_repeat:
            flash('Passwords do not match.')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(
                email=email,
                password=generate_password_hash(password, method='sha256'),
                api_key=generate_api_key())
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('dashboard'))
        else:
            flash('User with this email already exists.')
            return redirect(url_for('register'))
    else:
        return render_template('register.html')


def generate_api_key():
    api_key = str(token_urlsafe(16))
    while api_key.startswith("-"):
        api_key = str(token_urlsafe(16))
    return api_key


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log in page."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash('Please fill all the fields.')
            return redirect(url_for('login'))

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            flash('User with this email does not exist.')
            return redirect(url_for('login'))

        if check_password_hash(existing_user.password, password):
            login_user(existing_user)
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect password.')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    """Log out page."""
    logout_user()
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    """Dashboard page."""
    if current_user.is_authenticated:
        return render_template(
            'dashboard.html',
            api_key=current_user.api_key
        )
    else:
        return redirect(url_for('login'))


@app.route('/collaboration')
def collaboration():
    """Collaboration page."""
    return render_template('collaboration.html')
