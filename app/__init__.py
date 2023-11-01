from flask import Flask

# New imports
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os


# force loading of environment variables
load_dotenv('.flaskenv')

DB_NAME = os.environ.get('SQLITE_DB')
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csc33O'

# Specify the connection parameters/credentials for the database
DB_CONFIG_STR = 'sqlite:///' + os.path.join(basedir, DB_NAME)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True


# Create database connection and associate it with the Flask application
db = SQLAlchemy(app)

login = LoginManager(app)

# enables @login_required
login.login_view = 'login'

# Add models
from app import routes, models
from app.models import User

# Create DB schema
db.create_all()

# Create admin and basic user account
user = User.query.filter_by(username='admin').first()
if user is None:
    user_admin = User(username='admin', role='admin')
    user_admin.set_password('csc330')
    db.session.add(user_admin)
    db.session.commit()

user = User.query.filter_by(username='user').first()
if user is None:
    reg_user = User(username='user', role = 'user')
    reg_user.set_password('csc330')
    db.session.add(reg_user)
    db.session.commit()
