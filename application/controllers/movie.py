# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, abort, redirect, url_for
from flask_login import current_user

movie_bp = Blueprint(
    'movie', 
    __name__,
    template_folder='../templates',
)

movies = ['The Name of the Rose', 'The Historian', 'Rebecca']


@movie_bp.route('/movie', methods=['GET', 'POST'])
def index():
    _form = request.form

    if request.method == 'POST':
        if not current_user.is_authenticated:
            abort(403)
        title = _form["title"]
        movies.append(title)
        return redirect(url_for('.index'))

    return render_template(
        'movie.html',
        movies=movies
    )


@movie_bp.route('/movie/<name>')
def info(name):
    movie = [name]
    if name not in movies:
        movie = []

    return render_template(
        'movie.html',
        movies=movie
    )
