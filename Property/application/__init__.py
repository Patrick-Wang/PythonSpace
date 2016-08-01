#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import load_config

bootstrap = Bootstrap()
db_property = SQLAlchemy()


def create_app():
    # init Flask
    app = Flask(__name__)

    # init ext of Flask
    bootstrap.init_app(app)

    db_property.init_app(app)

    # Load config
    config = load_config()
    app.config.from_object(config)

    from application.views.account import blueprint as account_blueprint
    app.register_blueprint(account_blueprint)

    return app
