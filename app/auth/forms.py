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
from wtforms.validators import ValidationError

from ..models import User
from app import db


class LoginForm(Form):
    """
    login form to weibo
    """
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")
    submit = SubmitField("Submit")


class AdminLoginForm(Form):
    """
    admin login form.
    """
    username = StringField(label='管理员账号邮箱', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[DataRequired()])
    submit = SubmitField('登陆')

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise ValidationError('账号不存在')

        if not user.verify_password(self.password):
            raise ValidationError('密码错误')

    def get_user(self):
        return db.session.query(User).filter_by(email=self.username).first()