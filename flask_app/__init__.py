from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # appの設定
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile('config.py')
    
    # DBの設定
    db.init_app(app)
    from flask_app import models
    
    # Blueprintの設定
    
    return app