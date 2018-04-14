# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~
auth module

@author guoweikuang
"""
from flask import flash
from flask import url_for
from flask import request
from flask import redirect
from flask import render_template

from flask_login import login_user

from . import auth
from .forms import LoginForm

from ..models import User


@auth.route('/login', methods=["GET", "POST"])
def login():
    """ login module
    verify username and password.
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash("user login success!")
            return redirect(request.args.get("next") or url_for('weibo.index'))
        flash("invalid username or password!")

    return render_template("auth/login.html", form=form)
