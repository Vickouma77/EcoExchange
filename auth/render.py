# auth/render.py
"""
A simple flask blueprint to handle 
the login form, signup form, forgotpassword form
"""

from flask import Blueprint, render_template, request, redirect, url_for

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle the login form submission
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate the username and password
        if username == 'admin' and password == 'password':
            # Successful login
            return redirect(url_for('dashboard'))

        # Invalid credentials, show an error message
        error_message = 'Invalid username or password'
        return render_template('login.html', error=error_message)

    # If it's a GET request, show the login form
    return render_template('login.html')