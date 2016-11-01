# -*- coding: utf-8 -*-

from flask import Flask
from flask_cache import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route('/')
@cache.cached(timeout=300)
def index():
    print 'view hello called'
    return 'Hello World!'


@app.route('/posts')
def get_posts():
    return ', '.join(get_posts())


@app.route('/posts/<int:num>')
@cache.cached(timeout=60)
def post(num):
    print 'view post called'
    return str(num)


@app.route('/comments/<int:num>')
def get_comments(num):
    return ', '.join(get_comments(num))


@cache.cached(timeout=60, key_prefix='get_posts')
def get_posts():
    print 'method get_posts called'
    return ['a','b','c','d','e']


@cache.memoize(timeout=60)
def get_comments(num):
    print 'method get_comments called'
    return [str(i) for i in xrange(num)]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5205, debug=True)

