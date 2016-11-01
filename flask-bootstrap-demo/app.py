# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/book')
def book():
    books = ['the first book', 'the second book']
    return render_template('index.html', books=books)


@app.route('/movie')
def movie():
    movies = ['the first movie', 'the second movie']
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5200, debug=True)
