# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, flash, redirect

book_bp = Blueprint(
    'book', 
    __name__,
    template_folder='../templates',
)

books = ['The Name of the Rose', 'The Historian', 'Rebecca']


@book_bp.route('/', methods=['GET'])
def index():
    return '<h1>Hello World!</h1>'


@book_bp.route('/book', methods=['GET', 'POST'])
def handle_book():
    _form = request.form

    if request.method == 'POST':
        title = _form["title"]
        books.append(title)
        flash("add book successfully!")
        return redirect(url_for('book.handle_book'))

    return render_template(
        'book.html',
        books=books
   )


@book_bp.route('/book/<name>')
def get_book_info(name):
    book = [name]
    if name not in books:
        book = []

    return render_template(
        'book.html',
        books=book
    )

