#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : account.py
#  @ time : 2016/7/19 14:08
#  @ author : Patrick Wang

from flask import Blueprint, redirect, request, url_for, flash, render_template
from ...models.auth.accounts import Accounts
from ...forms.auth.accounts import LoginForm, RegistrationForm
from flask_login import login_user, login_required, logout_user, current_user
from ... import db_property
from ...common.email import send_email

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


@blueprint.route('/register', methods=['GET', 'POST'])
def user_register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        new_user = Accounts(username=reg_form.username.data, email=reg_form.email.data,
                            password=reg_form.password.data, nickname=reg_form.nickname.data)
        db_property.session.add(new_user)
        db_property.session.commit()

        token = new_user.gen_confirm_token()
        send_email(new_user.email, 'Confirm your account', 'auth/email/confirm',
                   user=new_user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('index_blueprint.index'))
    return render_template('auth/registration.html', reg_form=reg_form)


@blueprint.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index_blueprint.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account, thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('index_blueprint.index'))


@blueprint.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.gen_confirm_token()
    send_email(current_user.email,  'Confirm your account', 'auth/email/confirm',
               user=current_user, token=token)
    flash('A confirmation email has been sent to you by email again!')
    return redirect(url_for('index_blueprint.index'))


@blueprint.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:15] != 'auth_blueprint.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth_blueprint.unconfirmed'))


@blueprint.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('index_blueprint.index'))
    return render_template('/auth/unconfirmed.html')
