#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : decorators.py
#  @ time : 2016/8/5 9:59
#  @ author : Patrick Wang

from functools import wraps
from flask_login import current_user
from flask import abort
from ..models.auth.roles import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTRATOR)(f)
