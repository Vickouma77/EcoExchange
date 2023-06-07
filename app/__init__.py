from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c54fd70c15fdcf389873a5930c6dc4a1'


DATABASE_HOST = 'localhost'
DATABASE_PORT = 3306
DATABASE_NAME = 'EcoExchange'
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'Vickouma@77'

# URL-encode the password
import urllib.parse
encoded_password = urllib.parse.quote(DATABASE_PASSWORD)

# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}:{encoded_password}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes, models