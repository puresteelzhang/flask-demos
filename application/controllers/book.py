# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, abort, redirect, url_for
from flask_login import login_required, current_user
from application.models import Book
from application.extensions import db

book_bp = Blueprint(
    'book',
    __name__,
    template_folder='../templates',
)


@book_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@book_bp.route('/book', methods=['GET', 'POST'])
def show_book():
    books = Book.query.all()

    if request.method == 'POST':
        if not current_user.is_authenticated:
            abort(403)

        title = request.form["title"]
        book = Book(title=title)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('.show_book'))

    return render_template(
        'book.html',
        books=books
    )
