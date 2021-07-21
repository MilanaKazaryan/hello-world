from flask import Flask
app = Flask(__name__)
@app.route('/')
@app.route('/home')
def home():
    return f'<h1 align="center"> Hello, World!!!</h1>'