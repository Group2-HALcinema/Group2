from flask import Flask
from flask_app.models import *
from flask_migrate import Migrate
from flask_login import LoginManager

# appの設定
app = Flask(__name__,instance_relative_config=True)
app.config.from_pyfile('config.py')

# DBの設定
db.init_app(app)
Migrate(app, db)

#LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login' 

#Blueprintの登録
from flask_app.views.auth import auth_bp
app.register_blueprint(auth_bp)

from flask_app import views