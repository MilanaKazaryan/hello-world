from flask import Flask, render_template, url_for,redirect, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, PostsForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'secretkeyformypage'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET','POST'],)
def log_in():
    if current_user.is_authenticated:
        return redirect(url_for('post'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))
        flash('Invalid email or password!', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('log_in'))    
    return render_template('register.html', form=form)

@app.route('/newposts', methods=['POST', 'GET'])
@login_required
def new_posts():
    post = PostsForm()
    if post.validate_on_submit():
        posts = Posts(text=post.text.data, author=current_user)
        db.session.add(posts)
        db.session.commit()
        return redirect('/posts')
    return render_template('newposts.html', post=post, name=current_user.username)

@app.route('/posts', methods=['GET', 'POST'])
@login_required
def post():
    posts = Posts.query.all()
    return render_template('posts.html', posts=posts)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))