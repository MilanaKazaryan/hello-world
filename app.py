from flask import Flask, render_template, url_for,redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__) 
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'secretkeyformypage'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'log_in'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(50), unique=True)
    post = db.relationship('Posts', backref='author', lazy=True)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120))
    images = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
exit()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET','POST'],)
def log_in():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def sign_up():
    form = RegistrationForm()
    return render_template('register.html', form=form)