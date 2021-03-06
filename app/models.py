# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~
models module

@author guoweikuang
"""
from datetime import datetime
from . import db
from . import login_manager

from flask_login import UserMixin
from flask_login import AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True, index=True)
    users = db.relationship("User", backref="role", lazy="dynamic")


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    is_superuser = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        """ set password is can't read """
        raise AttributeError("password is forbid to read!")

    @password.setter
    def password(self, password):
        """ using werkzeug product password hash

        :param password: user password
        :return: Encrypted password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """ verify the password if correct

        :param password: user password
        :return: True or False
        """
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        """

        :return:
        """
        if isinstance(self, AnonymousUserMixin):
            return False
        return True

    def is_administator(self):
        if not self.is_superuser:
            return False
        else:
            return True


class Content(db.Model, UserMixin):
    __tablename__ = 'content'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    pub_time = db.Column(db.String(255))
    comment_num = db.Column(db.Integer)
    like_num = db.Column(db.Integer)
    url = db.Column(db.String(255))


class opinion(db.Model, UserMixin):
    __tablename__ = 'opinion'
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(255))
    sen_word = db.Column(db.String(255))
    weibo_text = db.Column(db.String(255))
    pub_time = db.Column(db.DateTime, default=datetime.utcnow())
    comment = db.Column(db.String(255))
    like_num = db.Column(db.Integer)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
