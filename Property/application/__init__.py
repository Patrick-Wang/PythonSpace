#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import load_config

bootstrap = Bootstrap()
db_property = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth_blueprint.user_login'


def create_app():
    # init Flask
    app = Flask(__name__)

    # init ext of Flask
    bootstrap.init_app(app)
    login_manager.init_app(app)
    db_property.init_app(app)
    mail.init_app(app)

    # Load config
    config = load_config()
    app.config.from_object(config)

    from application.views.auth.account import blueprint as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from application.views.index import blueprint as index_blueprint
    app.register_blueprint(index_blueprint)

    return app
