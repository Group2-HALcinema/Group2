from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_app import models, views, forms

db = SQLAlchemy()

def create_app():
    # appの設定
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile('config.py')
    
    # DBの設定
    db.init_app(app)
    Migrate(app, db)
    
    #LoginManager
    login_manager = LoginManager(app)
    login_manager.login_view = 'login' 
    
    # Blueprintの設定
    
    return app