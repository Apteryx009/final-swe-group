import os
import flask
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

##DuckWorth
load_dotenv(find_dotenv())
##
print( os.environ.get('SQLALCHEMY_DATABASE_URI'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
db = SQLAlchemy(app)



###DuckWorth

# login manager stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'
##
###########DuckWorth
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

def createUser(new_user, password):
    """this function creates a new user"""
    user = endUser(new_user, generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
################


class keepUsr:
    def __init__(self, usrStr):
        self.usrStr = usrStr

usrName = keepUsr("blank")

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
    SpecificUserFeedbacks = db.session.query(UserFeedback).filter(UserFeedback.username == usrName.usrStr).all()
        
    # """this function renders the index page of the site
    # TODO: finish project"""
    
    #test data
    usrfeedback = UserFeedback(0, "In-Progress", "bicep stuff", usrName.usrStr)
    
    print("ayyyyyy")
    
    #userInfo = json.loads(userInfo)
    #print(userInfo['exercise'])
    
    #print(post_id)
    
    
    #db.session.add(usrfeedback)
    #db.session.commit()
    
    
    return render_template('workouts.html', SpecificUserFeedbacks=SpecificUserFeedbacks)


##Duckworth
@app.route("/blog1")
@login_required
def blog1():
    return render_template('blog1.html')

@app.route("/blog2")
@login_required
def blog2():
    return render_template('blog2.html')

@app.route("/blog3")
@login_required
def blog3():
    return render_template('blog3.html')

@app.route("/blog4")
def blog4():
    return render_template('blog4.html')
###########




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
    username = usrName.usrStr
    amountOfReps = userInfo['Reps']
    
    usrfeedback = UserFeedback(status,amountOfReps,  Exercise, username)
    usrPoints = userPoints(usrName.usrStr, 1, 2, 789, 4)
    
    #historyPoints = db.session.query(userPoints).filter(userPoints.username == username).first()
    #print(historyPoints.id)
    #historyPoints01 = db.session.query(userPoints).get(historyPoints.id)
    #print(historyPoints01.pointsF)

    #print(excercise)
    
    SpecificUserFeedbacks = db.session.query(UserFeedback).filter(UserFeedback.username == username).all()
    #print(int(x) for x in SpecificUserFeedbacks)
    #for x in SpecificUserFeedbacks:
    #    print(int(x.reps), x.excercise, x.progress, x.username)
    
     
        
    print(SpecificUserFeedbacks)
    db.session.add(usrfeedback)
    #db.session.add(usrPoints)
    db.session.commit()
    
    
    historyPoints = db.session.query(userPoints).filter(userPoints.username == usrName.usrStr).first()
    
    return render_template('workouts.html', SpecificUserFeedbacks=SpecificUserFeedbacks )

@app.route("/workouts/<int:row2Del>", methods = ['POST'])
def delete(row2Del):
    # """this function renders the index page of the site
    # TODO: finish project"""
   
    
    #userInfo = json.loads(userInfo)
    print(row2Del)
    StrRow2Del = str(row2Del)
    
    if row2Del < 0:
        print("negative num is ", row2Del)

    SpecificUserFeedbacks = db.session.query(UserFeedback).get(row2Del)
    print(SpecificUserFeedbacks, " Delete this")
   
    db.session.delete(SpecificUserFeedbacks)
    #db.session.query(UserFeedback).filter(UserFeedback.id == row2Del).delete()
    
    #db.session.add(usrPoints)
    db.session.commit()
    
    
    
    return render_template('workouts.html')

@app.route("/workouts3/<int:row2Del>", methods = ['GET', 'POST'])
def finished(row2Del):
    # """this function renders the index page of the site
    # TODO: finish project"""
   
    #don't worry about naming convention
   
    print("hi there", row2Del)
    
    #SpecificUserFeedbacks = db.session.query(UserFeedback).filter(UserFeedback.id == str(row2Del)).with_for_update().one()
    SpecificUserFeedbacks = db.session.query(UserFeedback).filter(UserFeedback.username == usrName.usrStr).all()

    print(row2Del -1)
    print(SpecificUserFeedbacks[row2Del -1].username)
    SpecificUserFeedbacks[row2Del -1].progress = "Finished1"
    #print(SpecificUserFeedbacks.progress)
  
    db.session.commit()
    
    
    
    return render_template('/workouts3/<int:row2Del>',SpecificUserFeedbacks=SpecificUserFeedbacks )
    
@app.route("/workouts3/", methods = ['GET', 'POST'])
def finished3():
    
    return render_template('workouts3.html', SpecificUserFeedbacks=SpecificUserFeedbacks)







@app.route('/form', methods = ['GET', 'POST'])
def form():
    if request.method == 'POST':
        Exercise = request.form['Exercise']
        Reps = request.form['Reps']
        print(Exercise)
        return render_template('workouts.html')


@app.route("/")
@login_required
def index():
    return render_template('dashboard.html')

@app.route("/trending")
@login_required
def trending():
    # """this function renders the index page of the site
    # TODO: finish project"""
    
    
    arrInProgress = []
    arrCompleted = []
    arrTotal = []
    
    listOfInProgressRows = db.session.query(UserFeedback).filter(UserFeedback.username == usrName.usrStr,UserFeedback.progress == "In-progress").all()
    listOfInCompletedRows = db.session.query(UserFeedback).filter(UserFeedback.username == usrName.usrStr,UserFeedback.progress == "Finished1").all()
    ListarrTotal = db.session.query(UserFeedback).filter(UserFeedback.username == usrName.usrStr).all()
    print(listOfInProgressRows, listOfInCompletedRows, arrTotal)
    
    #working correctly!
    print(len(listOfInProgressRows))
    
    for index in range(len(listOfInProgressRows)):
        arrInProgress.append(int(listOfInProgressRows[index].reps))
    for index in range(len(listOfInCompletedRows)):
        arrCompleted.append(int(listOfInCompletedRows[index].reps))
    for index in range(len(ListarrTotal)):
        arrTotal.append(int(ListarrTotal[index].reps))
    
    
    print(arrTotal)
    
    return render_template('trending.html',arrInProgress=arrInProgress,arrCompleted=arrCompleted,arrTotal=arrTotal)


@app.route("/account")
def account():
    #stuff
    username01 = usrName.usrStr
    return render_template('account.html',username01=username01 )

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
@login_required
def Cal():
    # """this function renders the index page of the site
    # TODO: finish project"""
    print(usrName.usrStr)
    return render_template('Cal.html')

############################DuckWorth
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
        
        persistUserName = username
        usrName.usrStr = persistUserName

        print("username:" + username)
        print("password:" + password)

        user = endUser.query.filter_by(username=username).first()
        print("user = ")
        print(user)
        if user:
            if check_password_hash(user.passwordHash, password):
                login_user(user)
                flask.flash("Login successful.")
                return flask.redirect(flask.url_for('index', persistUserName=persistUserName))
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
        persistUserName = username

        flask.flash(f"Successfully created new user {username}")
        flask.redirect(flask.url_for('login_page'))



with app.app_context():
    db.create_all()

