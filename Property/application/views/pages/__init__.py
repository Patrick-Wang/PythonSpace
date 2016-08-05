#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : __init__.py.py
#  @ time : 2016/8/5 15:53
#  @ author : Patrick Wang

from flask import Blueprint

blueprint = Blueprint('pages_blueprint', __name__)

from . import admin, functions, profile
