#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : index.py
#  @ time : 2016/8/2 13:52
#  @ author : Patrick Wang

from flask import Blueprint, render_template
from .. import db_property
from ..models.auth.accounts import Accounts
from flask_login import login_required

blueprint = Blueprint('index_blueprint', __name__)


@blueprint.route('/')
def index():
    return render_template('index.html')


@blueprint.route('/createDB')
def create_db():
    db_property.create_all()
    return render_template('index.html')


@blueprint.route('/secret')
@login_required
def secret():
    return 'Must logged in user can view this page'
