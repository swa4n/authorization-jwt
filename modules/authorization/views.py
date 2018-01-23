# coding=utf-8
import datetime
from functools import wraps

import jwt
from flask import render_template, request, redirect, flash, jsonify, session, g
from jwt import ExpiredSignatureError

from modules import app
from modules.authorization.forms import LoginForm

users = {
    "Dima": "Dima",
    "Olha": "Olha",
    "Oleg": "Oleg"
}


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')

        if not token:
            # return jsonify({'message': 'Token is required'}), 403
            token = session.get("token")

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            g.user = data.get('user')
        except ExpiredSignatureError:
            return jsonify({'message': 'Token is invalid'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'This is available only for people with valid token'})


@app.route('/')
@app.route('/index')
@token_required
def index():
    user = {'name': g.user}
    title = "Login"
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title=title, user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users and password == users[username]:
            token = jwt.encode(
                {'user': username,
                 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
                app.config['SECRET_KEY'])
            session["token"] = token
            flash('token=' + token)
            return redirect('/index')
    return render_template('login.html',
                           title='Log In',
                           form=form)
