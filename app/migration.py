from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_script import Manager

from app import app, db

# Initializing Flask-Migrate
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', Migrate)

if __name__ == '__main__':
    manager.run()