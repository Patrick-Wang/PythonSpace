#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : index.py
#  @ time : 2016/8/2 13:52
#  @ author : Patrick Wang

from flask import Blueprint, render_template
from .. import db_property
from ..models.auth.accounts import Accounts
from ..models.auth.roles import Role
from flask_login import login_required

blueprint = Blueprint('index_blueprint', __name__)


@blueprint.route('/')
def index():
    return render_template('index.html')


@blueprint.route('/createDB')
def create_db():
    db_property.create_all()
    account = Accounts(username='wangxin', email='18624020715@163.com',
                       password='123456', nickname='patrick', location='shenyang', about_me='about me', confirmed=1)
    account2 = Accounts(username='wangxin2', email='wangxin229@163.com',
                       password='123456', nickname='patrick', location='shenyang', about_me='about me', confirmed=1)
    db_property.session.add(account)
    db_property.session.add(account2)
    db_property.session.commit()

    Role.insert_roles()
    return render_template('index.html')


@blueprint.route('/secret')
@login_required
def secret():
    return 'Must logged in user can view this page'
