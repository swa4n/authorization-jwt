# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(label='Enter username', validators=[DataRequired()])
    password = PasswordField(label='Enter password', validators=[DataRequired()])
