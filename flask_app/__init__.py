from flask import Flask
from flask_app.models import *
from flask_migrate import Migrate
from flask_login import LoginManager
    
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
    
    return app