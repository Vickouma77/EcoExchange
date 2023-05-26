from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)
