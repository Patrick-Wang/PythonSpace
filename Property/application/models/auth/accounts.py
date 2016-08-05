#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : accounts.py
#  @ time : 2016/8/1 13:52
#  @ author : Patrick Wang

from .roles import Role, Permission
from ... import db_property
from ... import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime


class Accounts(UserMixin, db_property.Model):

    __tablename__ = 'accounts'

    id = db_property.Column(db_property.Integer, primary_key=True)
    username = db_property.Column(db_property.String(20), unique=True, index=True)
    email = db_property.Column(db_property.String(128), unique=True, index=True)
    nickname = db_property.Column(db_property.String(20))
    pwd = db_property.Column(db_property.String(128))
    confirmed = db_property.Column(db_property.Boolean, default=False)
    location = db_property.Column(db_property.String(64))
    about_me = db_property.Column(db_property.Text())
    member_since = db_property.Column(db_property.DateTime(), default=datetime.utcnow)
    last_seen = db_property.Column(db_property.DateTime(), default=datetime.utcnow)
    role_id = db_property.Column(db_property.Integer, db_property.ForeignKey('roles.id'))
    # dept_id = db_property.Column(db_property.Integer, db_property.ForeignKey('departments.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.pwd = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pwd, password)

    def __init__(self, **kwargs):
        super(Accounts, self).__init__(**kwargs)
        if self.role is None:
            if self.email == '18624020715@163.com':
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

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

    def can(self, permissions):
        return self.role.permissions is not None and \
               (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTRATOR)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db_property.session.add(self)
        db_property.session.commit()


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_admin(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    return Accounts.query.get(int(user_id))
