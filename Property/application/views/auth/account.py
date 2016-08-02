#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : account.py
#  @ time : 2016/7/19 14:08
#  @ author : Patrick Wang

from flask import Blueprint, redirect, request, url_for, flash, render_template
from ...models.auth.accounts import Accounts
from ...forms.auth.accounts import LoginForm
from flask_login import login_user, login_required, logout_user

blueprint = Blueprint('auth_blueprint', __name__)


@blueprint.route('/login', methods=['GET', 'POST'])
def user_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        account = Accounts.query.filter_by(email=login_form.email.data).first()
        if account is not None and account.verify_password(login_form.password.data):
            login_user(account, login_form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index_blueprint.index'))
        flash('Invalid user name or password!')
    return render_template('auth/login.html', login_form=login_form)


@blueprint.route('/logout')
@login_required
def user_logout():
    logout_user()
    flash('You have logged out!')
    return redirect(url_for('index_blueprint.index'))

