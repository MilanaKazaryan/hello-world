from flask import Flask, render_template, url_for,redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm
app = Flask(__name__) 
app.config['SECRET_KEY'] = 'secretkeyformypage'
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def log_in():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register')
def sign_up():
    form = RegistrationForm()
    return render_template('register.html', form=form)