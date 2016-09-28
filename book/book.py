# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, flash, \
    redirect, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth


book_bp = Blueprint(
    'book', 
    __name__,
    template_folder='../templates',
)

auth = HTTPBasicAuth()

books = ['The Name of the Rose', 'The Historian', 'Rebecca']
users = [
    {'username': 'ethan', 'password': generate_password_hash('6689')},
    {'username': 'peter', 'password': generate_password_hash('4567')}
]

@auth.verify_password
def verify_password(username, password):
    for user in users:
        if user['username'] == username:
            if check_password_hash(user['password'], password):
                return True
    return False


@book_bp.route('/', methods=['GET'])
def index():
    return '<h1>Hello World!</h1>'


@book_bp.route('/book', methods=['GET'])
def get_books():
    return render_template(
        'book.html',
        books=books
    )


@book_bp.route('/book', methods=['POST'])
@auth.login_required
def add_book():
    _form = request.form
    title = _form["title"]
    if not title:
        return '<h1>invalid request</h1>'

    books.append(title)
    flash("add book successfully!")
    return redirect(url_for('book.get_books'))


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@book_bp.route('/book/<name>')
def get_book_info(name):
    book = [name]
    if name not in books:
        book = []

    return render_template(
        'book.html',
        books=book
    )
