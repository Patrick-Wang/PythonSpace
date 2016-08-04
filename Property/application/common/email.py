#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @ file : email.py
#  @ time : 2016/8/3 16:25
#  @ author : Patrick Wang

from .. import mail
from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['PROPERTY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['PROPERTY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
