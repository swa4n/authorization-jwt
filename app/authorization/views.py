# coding=utf-8
from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Dima'}
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
