#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : profile.py
#  @ time : 2016/8/5 15:50
#  @ author : Patrick Wang

from . import blueprint
from flask import render_template, flash, redirect, url_for
from ...models.auth.accounts import Accounts
from flask_login import login_required, current_user
from ...forms.auth.accounts import ProfileForm
from ... import db_property


@blueprint.route('/profile/<username>')
def account_profile(username):
    account = Accounts.query.filter_by(username=username).first()
    if account is not None:
        return render_template('pages/profile.html', account=account)


@blueprint.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db_property.session.add(current_user)
        db_property.session.commit()
        flash('Your profile has been changed!')
        return redirect(url_for('.account_profile', username=current_user.username))
    form.nickname.data = current_user.nickname
    form.about_me.data = current_user.about_me
    form.location.data = current_user.location
    return render_template('pages/profile_edit.html', edit_form=form)
