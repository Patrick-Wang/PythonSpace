#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : account.py
#  @ time : 2016/7/19 14:08
#  @ author : Patrick Wang

from flask import Blueprint
from ..models.accounts import Accounts
from .. import db_property

blueprint = Blueprint('account_blueprint', __name__)


@blueprint.route('/login', methods=['GET', 'POST'])
def user_login():
    account = Accounts.query.filter_by(username='wangxin').first()
    if account.verify_password('123456'):
        return 'successful'
    else:
        return 'failed'


@blueprint.route('/addaccount', methods=['GET', 'POST'])
def user_add():
    account = Accounts('wangxin', '123456')
    db_property.session.add(account)
    db_property.session.commit()
    return 'add successful'

