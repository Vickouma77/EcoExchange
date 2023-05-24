#!/usr/bin/env python3

from flask import Flask
from auth.render import auth_blueprint

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(auth_blueprint)
# ...

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)