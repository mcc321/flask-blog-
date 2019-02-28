# -*- coding: utf-8 -*-
from flask import Flask , render_template,jsonify
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import sys , os
from flask_login import LoginManager 

mail=Mail()
moment=Moment()
db=SQLAlchemy()
login_manager=LoginManager()
login_manager.session_protection = 'strong'#设置验证密码强度


from .func import *
def create_app():
    #蓝图注册
    from . import auth , main
    
    app = Flask(__name__)
    app.register_blueprint(main.main , url_prefix='/main')
    app.register_blueprint(auth.auth , url_prefix='/auth')
    




    #配置模块
    dir_path = os.path.abspath(os.path.dirname(__file__))
    os.environ['mcc_config'] = os.path.join(dir_path , 'config\\development.py')
    # instance_path = os.path.join(dir_path , 'instance/config.py')
    app.config.from_envvar('mcc_config')
    # app.config.from_pyfile(instance_path)
    app.config.from_pyfile("config\\production.py")


    #模型初始化
    mail.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    

    #数据库初始化
    with app.app_context():
        db.create_all()
        from .models import Role
        Role.insert_roles()
        dic=dict()
        dic['name']='root'
        dic['password']='root'
        dic['email']=None
        dic['confirmed']=True
        dic['pri']=2
        db_user_push(dic)
    return app

    from .models import Role
    Role.insert_roles()











