# app.py
from flask import Flask
from auth.render import auth_blueprint

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(auth_blueprint)
# ...

if __name__ == '__main__':
    app.run()