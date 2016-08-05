#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : functions.py
#  @ time : 2016/8/5 10:47
#  @ author : Patrick Wang

from ...common.decorators import permission_required
from flask_login import login_required
from ...models.auth.roles import Permission
from . import blueprint


@blueprint.route('/func')
@login_required
@permission_required(Permission.READ_MODIFY)
def func():
    return 'Required a read and modify permission'

