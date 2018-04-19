# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~
flask app manage

@author guoweikuang
"""
import os

from flask_script import Shell
from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from app import create_app, db
from app.models import User
from app.models import Role


app = create_app(os.getenv("WEIBO_CONFIG") or "default")
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """ 创建shell flask环境
    可以避免手动引入模块
    :return:
    """
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("db", MigrateCommand)
manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()