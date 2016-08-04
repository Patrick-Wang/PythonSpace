#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : default.py
#  @ time : 2016/7/21 0:40
#  @ author : Patrick Wang

import os


class DefaultConfig(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this word is hard to guess'

    # sqlalchemy config
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/property'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = False

    # email config
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    PROPERTY_MAIL_SUBJECT_PREFIX = '[PROPERTY]'
    PROPERTY_MAIL_SENDER = 'Property Admin <property@example.com>'
    PROPERTY_ADMIN = os.environ.get('PROPERTY_ADMIN')

