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

with app.app_context():
    db.create_all()

# if __name__ == "__main__":
#     app.run(debug=True)
