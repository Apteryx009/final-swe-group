import os
import flask
import datetime
from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, \
    current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.secret_key = os.getenv('FLASK_SECRET_KEY')
db = SQLAlchemy(app)

# login manager stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

@login_manager.user_loader
def load_user(user_id):
    return endUser.query.get(int(user_id))

class endUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    passwordHash = db.Column(db.String(500), nullable=False)

    def __init__(self, username, password_hash):
        self.username = username
        self.passwordHash = password_hash

class discussion_posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime_posted = db.Column(db.DateTime, default=datetime.datetime.now)
    content = db.Column(db.Text)
    author = db.Column(db.String(255))

class discussion_posts_form(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")

def createUser(new_user, password):
    """this function creates a new user"""
    user = endUser(new_user, generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

@app.route("/discussion", methods=['GET', 'POST'])
def discussion():
    form = discussion_posts_form()

    if form.validate_on_submit():
        post = discussion_posts(title=form.title.data, content=form.content.data)
        form.title.data = ""
        form.content.data = ""

        db.session.add(post)
        db.session.commit()

        flash("Post added successfully!")
        
    return render_template('discussion.html', form=form)

@app.route("/workouts")
def workout():
    """this function renders the index page of the site
    """
    return render_template('workouts.html')

@app.route("/")
@login_required
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

        print("username:" + username)
        print("password:" + password)

        user = endUser.query.filter_by(username=username).first()
        print("user = ")
        print(user)
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
def signup():
    if flask.request.method == 'GET':
        return render_template('signup.html')
    else:
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        createUser(username, password)

        flask.flash(f"Successfully created new user {username}")
        flask.redirect(flask.url_for('login_page'))



with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

