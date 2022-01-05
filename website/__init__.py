from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from os import path
from flask_login import LoginManager, login_manager

db = SQLAlchemy()

DB_NAME = "database.db"


def create_app():
    app =   Flask(__name__)
    app.config['SECRET_KEY'] = 'HHGHGHHG SJFHJS'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)
    
    from .view import views
    from .auth import auth

    app.register_blueprint(views, url_prefix ='/')
    app.register_blueprint(auth, url_prefix ='/')
    
    from .models import User, Note

    create_datebase(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_datebase(app):
    if not path.exists('website/'+ DB_NAME):
        db.create_all(app=app)
        print('Created Database!')