#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : roles.py
#  @ time : 2016/8/4 14:35
#  @ author : Patrick Wang

from ... import db_property


class Permission:
    ONLY_READ = 0x01
    READ_MODIFY = 0x02
    ADMINISTRATOR = 0xff


class Role(db_property.Model):
    __tablename__ = 'roles'

    id = db_property.Column(db_property.Integer, primary_key=True)
    name = db_property.Column(db_property.String(20), unique=True)
    default = db_property.Column(db_property.Boolean)
    permissions = db_property.Column(db_property.Integer)
    users = db_property.relationship('Accounts', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.READ_MODIFY | Permission.ONLY_READ, True),
            'Admin': (Permission.ONLY_READ | Permission.READ_MODIFY | Permission.ADMINISTRATOR, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db_property.session.add(role)
        db_property.session.commit()
