from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# this is secret key for extra protection)
app.secret_key = 'your secret key'

# database connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vickouma@77'
app.config['MYSQL_DB'] = 'EcoExchange'

# Intialize MySQL
mysql = MySQL(app)

#the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something is wrong
    msg = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # variables for access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))

        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # redirecting to home page
            return redirect(url_for('home'))
        else:
    
            msg = 'Incorrect username or password!'
    
    return render_template('index.html', msg=msg)

#the logout page
@app.route('/logout')
def logout():
    #loging the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

#the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something is wrong
    msg = ''

    #variables with default values
    username = ''
    password = ''
    email = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
         #variables with form data
         username = request.form['username']
         password = request.form['password']
         email = request.form['email']
    elif request.method == 'POST':
         # if form is empty
         msg = 'Please fill out the form!'

    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
    account = cursor.fetchone()
    # If account exists show error and validation checks
    if account:
        msg = 'Account already exists!'
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        msg = 'Invalid email address!'
    elif not re.match(r'[A-Za-z0-9]+', username):
        msg = 'Username must contain only characters and numbers!'
    elif not username or not password or not email:
         msg = 'Please fill out the form!'
    else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
        cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
        mysql.connection.commit()
        msg = 'You have successfully registered!'

    return render_template('register.html', msg=msg, username=username, password=password , email=email)

#the home page
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:

        return render_template('home.html', username=session['username'])
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#the profile page
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # account information
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    
    return redirect(url_for('login'))

#the product page
@app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        #processing the form data
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        image = request.files['image']

        # Saving the image to a desired location
        image.save('<desired_location>/<filename>')

        # Insert the product details into the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO products (title, description, price, user_id, image_url) VALUES (%s, %s, %s, %s, %s)', (title, description, price, session['id'], '<path_to_saved_image>'))
        mysql.connection.commit()

        # Redirect to the products page or display a success message
        return redirect(url_for('product'))
    else:
        # Fetch and display the user's products
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM products WHERE user_id = %s', [session['id']])
        products = cursor.fetchall()

        return render_template('product.html', products=products)
