# -*- coding: utf-8 -*-

from flask import Flask, render_template
from configs import config
from book import book_bp
from movie import movie_bp


def create_app(config_name):
    app = Flask(__name__)

    # basic config
    app.config.from_object(config[config_name])

    # blueprints
    app.register_blueprint(book_bp)
    app.register_blueprint(movie_bp)

    # error handler
    handle_errors(app)

    return app


def handle_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
