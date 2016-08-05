#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : accounts.py
#  @ time : 2016/8/2 13:28
#  @ author : Patrick Wang

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ...models.auth.accounts import Accounts


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 128), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 128), Email()])
    username = StringField('User name', validators=[DataRequired(),
                                                    Length(1, 64),
                                                    Regexp('^[A-Za-z][A-Za-z0-9]*$',
                                                           message='user name must have only letters, '
                                                                   'numbers, dots and underlines')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    nickname = StringField('Nick name', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Accounts.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if Accounts.query.filter_by(username=field.data).first():
            raise ValidationError('User name already registered')


class ProfileForm(Form):
    nickname = StringField('Nick name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
