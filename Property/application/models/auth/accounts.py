#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : accounts.py
#  @ time : 2016/8/1 13:52
#  @ author : Patrick Wang

from ... import db_property
from ... import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class Accounts(UserMixin, db_property.Model):

    __tablename__ = 'accounts'

    id = db_property.Column(db_property.Integer, primary_key=True)
    username = db_property.Column(db_property.String(20), unique=True, index=True)
    email = db_property.Column(db_property.String(128), unique=True, index=True)
    nickname = db_property.Column(db_property.String(20))
    pwd = db_property.Column(db_property.String(128))
    confirmed = db_property.Column(db_property.Boolean, default=False)
    # role_id = db_property.Column(db_property.Integer, db_property.ForeignKey('roles.id'))
    # dept_id = db_property.Column(db_property.Integer, db_property.ForeignKey('departments.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.pwd = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pwd, password)

    def __init__(self, username, email, password, nickname=None):
        self.username = username
        self.email = email
        self.password = password
        self.nickname = nickname
        # self.dept = dept
        # self.role = role

    def __repr__(self):
        return '<Accounts %r>' % self.username

    def gen_confirm_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db_property.session.add(self)
        db_property.session.commit()
        return True


@login_manager.user_loader
def load_user(user_id):
    return Accounts.query.get(int(user_id))
