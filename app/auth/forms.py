# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~
auth form module

@author guoweikuang
"""
from flask_wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email


class LoginForm(Form):
    """
    login form to weibo
    """
    email = StringField("Email", validators=[DataRequired(), Length(1, 64)])
    password = PasswordField("Password", validators=[DataRequired(), Email()])
    remember_me = BooleanField("remember_me")
    submit = SubmitField("Submit")