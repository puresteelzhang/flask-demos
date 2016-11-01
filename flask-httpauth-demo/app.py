# -*- coding: utf-8 -*-

from flask import Flask, url_for, render_template, request, flash, \
    redirect, make_response, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'

auth = HTTPBasicAuth()

# 模拟数据库
books = ['The Name of the Rose', 'The Historian', 'Rebecca']
users = [
    {'username': 'ethan', 'password': generate_password_hash('6666')},
    {'username': 'peter', 'password': generate_password_hash('4567')}
]


@auth.verify_password
def verify_password_or_token(username_or_token, password):
    # first try to authenticate by token
    user = verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        if not verify_password(username_or_token, password):
            return False

    return True


def generate_auth_token(username, expiration):
    serializer = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    user = filter(lambda user: user['username'] == username, users)

    token = serializer.dumps({'username': username}) if user else None
    return token


def verify_password(username, password):
    user = filter(lambda user: user['username'] == username, users)

    if user and check_password_hash(user[0]['password'], password):
        g.user = username
        return True
    return False


def verify_auth_token(token):
    g.user = None
    serializer = Serializer(app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token)
    except SignatureExpired:
        return None    # valid token, but expired
    except BadSignature:
        return None    # invalid token

    g.user = data['username']
    return g.user


@app.route('/token')
@auth.login_required
def get_auth_token():
    username = g.user
    token = generate_auth_token(username, 60)
    return jsonify({'token': token.decode('ascii'), 'duration': 60})


@app.route('/', methods=['GET'])
def index():
    return render_template(
        'book.html',
        books=books
    )


@app.route('/', methods=['POST'])
@auth.login_required
def add_book():
    _form = request.form
    title = _form["title"]
    if not title:
        return '<h1>invalid request</h1>'

    books.append(title)
    flash("add book successfully!")
    return redirect(url_for('index'))


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5206, debug=True)
