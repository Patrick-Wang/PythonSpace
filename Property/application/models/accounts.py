#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : accounts.py
#  @ time : 2016/8/1 13:52
#  @ author : Patrick Wang

from .. import db_property
from werkzeug.security import generate_password_hash, check_password_hash


class Accounts(db_property.Model):

    __tablename__ = 'accounts'

    id = db_property.Column(db_property.Integer, primary_key=True)
    username = db_property.Column(db_property.String(20), unique=True)
    nickname = db_property.Column(db_property.String(20))

    pwd = db_property.Column(db_property.String(128))

    role = db_property.Column(db_property.String(18))
    dept = db_property.Column(db_property.String(100))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.pwd = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pwd, password)

    def __init__(self, username, password, nickname=None, role=None, dept=None):
        self.username = username
        self.password = password
        self.nickname = nickname
        self.dept = dept
        self.role = role

    def __repr__(self):
        return '<Accounts %r>' % self.username

