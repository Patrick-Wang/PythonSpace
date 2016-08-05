#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : admin.py
#  @ time : 2016/8/5 10:43
#  @ author : Patrick Wang

from ...common.decorators import admin_required
from flask_login import login_required
from . import blueprint


@blueprint.route('/admin')
@login_required
@admin_required
def admin():
    return 'Administrator management page'
