from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import hashlib

import os
import numpy as np
import pickle

# Generate a random secret key
app_secret_key = os.urandom(24)

app = Flask(__name__)
# app.config['SECRET_KEY'] = app_secret_key
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'sentiment_analysis'


# Using environment variables for MySQL connection
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'sentiment_analysis')

mysql = MySQL(app)


# Define a route for the home page
@app.route('/')
def home():
    if not session.get('loggedin', None):
        # Redirect to the login page if the user is not authenticated
        return redirect('/login')
    cur = mysql.connection.cursor()
    query = '''
        SELECT * FROM predictions;
    '''
    cur.execute(query)
    data = cur.fetchall()
    if data == []:
        data = None
    cur.close()

    return render_template('index.html', data=data)


# Define a route for processing user input
@app.route('/predict', methods=['POST'])
def predict_sentiment():
    # Get user input from the form
    if request.method == 'POST':
        user_input = [request.form['user_input']]
        prediction, confidence = predict(user_input)

        cur = mysql.connection.cursor()
        query = '''
            INSERT INTO predictions (user_input, prediction, confidence) VALUES (%s, %s, %s);
        '''
        cur.execute(query, (user_input[0], prediction[0], round(confidence, 2)))
        mysql.connection.commit()
        cur.close()

        return redirect('/')


# Define a route for deleting a prediction
@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM predictions WHERE id=%s", (id_data,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = hashlib.sha256((str(bytes(password, 'utf-8') + app_secret_key)).encode()).hexdigest()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s and password = %s", (email, hashed_password,))
        user = cur.fetchone()
        cur.close()
        if user:
            session['loggedin'] = True
            session['id'] = user[0]
            session['email'] = user[1]

            return redirect('/')
        else:
            error = "Invalid Credentials"

    return render_template('login.html', error=error)


# Logout route
@app.route('/logout')
def logout():
    if session['loggedin']:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('email', None)
    return redirect('/login')


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        email = request.form.get('email')
        password =  request.form.get('password')

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256((str(bytes(password, 'utf-8') + app_secret_key)).encode()).hexdigest()

        cur = mysql.connection.cursor()
        query = 'INSERT INTO users (email, password) VALUES (%s, %s)'
        cur.execute(query, (email, hashed_password))
        mysql.connection.commit()
        cur.close()

        return redirect('/login')

    return render_template('signup.html')


def predict(user_input: str):
    # Load the model
    with open('model/sentiment_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    # Load the TF-IDF vectorizer
    with open('model/tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
        tfidf_vectorizer = pickle.load(vectorizer_file)
    
    user_input_transformed = tfidf_vectorizer.transform(user_input)
    prediction = model.predict(user_input_transformed)
    confidence = np.max(model.predict_proba(user_input_transformed)) * 100

    return prediction, confidence

    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
