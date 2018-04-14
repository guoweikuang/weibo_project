# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~
auth package init file
    - init auth buleprint

@author guoweikuang
"""
from flask import Blueprint


auth = Blueprint("auth", __name__)

from . import views