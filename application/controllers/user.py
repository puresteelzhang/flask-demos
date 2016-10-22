# -*- coding: utf-8 -*-

import re
from datetime import datetime

from flask import Blueprint, render_template
from flask import redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user

from application.models import User
from application.extensions import db


user_bp = Blueprint(
    'user',
    __name__,
    template_folder='../templates'
)

alphanumeric = re.compile(r'^[0-9a-zA-Z_]*$')
email_address = re.compile(r'[a-zA-z0-9\.]+@[a-zA-Z0-9]+\.+[a-zA-Z]')


@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template(
            'signup.html',
            title=u'注册',
            form=None
        )
    elif request.method == 'POST':
        _form = request.form
        username = _form['username']
        email = _form['email']
        password = _form['password']
        password2 = _form['password2']

        message_e, message_u, message_p = "", "", ""

        # Check username is valid or not.
        if not username:
            message_u = u'用户名不能为空'
        elif not alphanumeric.match(username):
            message_u = u'用户名必须为字母、数字和下划线'
        elif User.query.filter_by(username=username).first():
            message_u = u'用户名已经存在'

        # Check email is valid or not.
        if not email:
            message_e = u'邮箱不能为空'
        elif not email_address.match(email):
            message_e = u'邮箱无效'
        elif User.query.filter_by(email=email).first():
            message_e = u'邮箱已经存在'

        # Check the password is valid or not.
        if password != password2:
            message_p = u'密码不对'
        elif password == "" or password2 == "":
            message_p = u'密码不能为空'

        if message_u or message_p or message_e:
            return render_template(
                "signup.html",
                form=_form,
                title=u'注册',
                message_u=message_u,
                message_p=message_p,
                message_e=message_e
            )

        # A valid register info, save the info into db.
        else:
            reg_user = User(username=username, email=email, password=password)
            db.session.add(reg_user)
            db.session.commit()
            login_user(reg_user)

            return redirect(url_for('user.signin'))


@user_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(request.args.get('next') or url_for("book.index"))
        return render_template(
            'signin.html',
            title=u'登录',
            form=None
        )
    elif request.method == 'POST':
        _form = request.form
        u = User.query.filter_by(email=_form['email']).first()
        if u and u.verify_password(_form['password']):
            login_user(u)
            u.last_login = datetime.now()
            db.session.commit()
            return redirect(request.args.get('next') or url_for('book.index'))
        else:
            message = u'无效的用户名或密码'

            return render_template(
                'signin.html',
                title=u'用户登录',
                form=_form,
                message=message
            )


@user_bp.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('book.index'))
