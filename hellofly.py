import os
import flask
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, \
    current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

#login_manager = LoginManager()
#login_manager.init_app(app)

class endUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    passwordHash = db.Column(db.String(500), nullable=False)

    def __init__(self, username, password_hash):
        self.username = username
        self.passwordHash = password_hash

def createUser(new_user, password):
    """this function creates a new user"""
    user = endUser(new_user, generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

@app.route("/workouts")
def workout():
    """this function renders the index page of the site
    """
    return render_template('workouts.html')

@app.route("/")
def index():
    """this function renders the index page of the site
    """
    return render_template('dashboard.html')

@app.route("/trending")
def trending():
    # """this function renders the index page of the site
    # """
    return render_template('trending.html')


@app.route("/Cal")
def Cal():
    # """this function renders the index page of the site
    # """
    return render_template('Cal.html')

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if flask.request.method == 'GET':
        # if method == GET, render login page
        return render_template('login.html')
    else:
        # else, process login
        # retrieve username and password from form fields
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        user = endUser.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.passwordHash, password):
                login_user(user)
                flask.flash("Login successful.")
                return flask.redirect(flask.url_for('index'))
            else:
                flask.flash("Incorrect password")
        else:
            flask.flash("User ID does not exist in database.")
    username=""
    password=""

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def create_an_account():
    if flask.request.method == 'GET':
        return render_template('signup.html')
    else:
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        createUser(username, password)



with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

