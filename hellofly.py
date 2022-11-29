import os
#import flask, render_template
from flask import Flask, render_template
import flask_sqlalchemy
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, \
    current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import find_dotenv, load_dotenv

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:QO3ze345PPfRfaJ@localhost:5432"
app.config["SECRET_KEY"] = "super secret key"

db = SQLAlchemy(app)

#login_manager = LoginManager()
#login_manager.init_app(app)


class UserFeedback(db.Model):
    # movie id, reps, excercise, username
    __tablename__ = "userfeedback"
    id = db.Column(db.Integer, primary_key=True)
    progress = db.Column(db.Integer, nullable=False)  # fname = username
    reps = db.Column(db.Integer, nullable=False)
    excercise = db.Column(db.String(9999), nullable=False)
    username = db.Column(db.String(999), nullable=False)

    def __init__(self, progress, reps, excercise, username):
        self.progress = progress
        self.reps = reps
        self.excercise = excercise
        self.username = username



@app.route("/workouts")
def workout():
    # """this function renders the index page of the site
    # TODO: finish project"""
    
    #test data
    usrfeedback = UserFeedback(0, 10, "bicep stuff", "John Smithhh")
    
    
    db.session.add(usrfeedback)
    db.session.commit()
    
    
    return render_template('workouts.html')

@app.route("/")
def index():
    # """this function renders the index page of the site
    # TODO: finish project"""
    return render_template('dashboard.html')

@app.route("/trending")
def trending():
    # """this function renders the index page of the site
    # TODO: finish project"""
    return render_template('trending.html')


@app.route("/Cal")
def Cal():
    # """this function renders the index page of the site
    # TODO: finish project"""
    return render_template('Cal.html')

with app.app_context():
    db.create_all()

# if __name__ == "__main__":
#     app.run(debug=True) 