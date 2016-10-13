# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request

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
        title = _form["title"]
        movies.append(title)

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

