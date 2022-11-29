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

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from bs4 import BeautifulSoup
import requests
import json

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
    progress = db.Column(db.String(999), nullable=False)  # fname = username
    reps = db.Column(db.String(999), nullable=False)
    excercise = db.Column(db.String(9999), nullable=False)
    username = db.Column(db.String(999), nullable=False)

    def __init__(self, progress, reps, excercise, username):
        self.progress = progress
        self.reps = reps
        self.excercise = excercise
        self.username = username
        
class userPoints(db.Model):
    # movie id, reps, excercise, username
    __tablename__ = "points"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(999), nullable=False)
    pointsC = db.Column(db.String(999), nullable=False)
    pointsI = db.Column(db.String(999), nullable=False)
    pointsF = db.Column(db.String(999), nullable=False)
    pointsT = db.Column(db.String(999), nullable=False)

    def __init__(self, username, pointsC, pointsI, pointsF, pointsT):
        self.username = username
        self.pointsC = pointsC
        self.pointsI = pointsI
        self.pointsF = pointsF
        self.pointsT = pointsT
        


@app.route("/workouts/")
def workout():
    # page = requests.get(":5000").text
    # soup = BeautifulSoup(page, 'html.parser')
    # print(soup.prettify())
        
        
    # """this function renders the index page of the site
    # TODO: finish project"""
    
    #test data
    usrfeedback = UserFeedback(0, "In-Progress", "bicep stuff", "John Smithhh")
    
    
    #userInfo = json.loads(userInfo)
    #print(userInfo['exercise'])
    
    #print(post_id)
    
    
    #db.session.add(usrfeedback)
    #db.session.commit()
    
    
    return render_template('workouts.html')

@app.route("/workouts/<string:userInfo>", methods = ['POST'])
def workout2(userInfo):
    # """this function renders the index page of the site
    # TODO: finish project"""
    
    #test data
    #usrfeedback = UserFeedback(0, 10, "bicep stuff", "John Smithhh")
    
    userInfo = json.loads(userInfo)
    #print(userInfo['exercise'])
    
    Exercise = userInfo['exercise']
    status = "In-progress"
    username = "AdamSmith345"
    amountOfReps = "15"
    
    usrfeedback = UserFeedback(status,amountOfReps,  Exercise, username)
    usrPoints = userPoints('AdamSmith345', 1, 2, 789, 4)
    
    historyPoints = db.session.query(userPoints).filter(userPoints.username == "AdamSmith345").first()
    print(historyPoints.id)
    historyPoints01 = db.session.query(userPoints).get(historyPoints.id)
    print(historyPoints01.pointsF)

    #print(excercise)
    
    SpecificUserFeedbacks = db.session.query(UserFeedback).filter(UserFeedback.username == "AdamSmith345").all()
    #print(int(x) for x in SpecificUserFeedbacks)
    for x in SpecificUserFeedbacks:
        print(int(x.reps), x.excercise, x.progress)
        
    
    db.session.add(usrfeedback)
    #db.session.add(usrPoints)
    db.session.commit()
    
    
    historyPoints = db.session.query(userPoints).filter(userPoints.username == "AdamSmith345").first()
    
    return render_template('workouts.html', )


@app.route('/form', methods = ['GET', 'POST'])
def form():
    if request.method == 'POST':
        Exercise = request.form['Exercise']
        print(Exercise)
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

# @app.route("/workouts", methods=('GET', 'POST'))
# def process(request: Request, num: int = Form(...)):
#     if request.method == 'POST':
#         form = request.form
#         print(form['Exercise'])
#     print(num)
#     # """this function renders the index page of the site
#     # TODO: finish project"""
#     return render_template('workouts.html')


@app.route("/Cal")
def Cal():
    # """this function renders the index page of the site
    # TODO: finish project"""
    return render_template('Cal.html')

with app.app_context():
    db.create_all()

# if __name__ == "__main__":
#     app.run(debug=True) 