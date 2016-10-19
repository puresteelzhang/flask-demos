# -*- coding: utf-8 -*-

from flask import Flask, render_template
from controllers import blueprints
from configs import config
from extensions import db, login_manager


def create_app(config_name=None):
    if config_name is None:
        config_name = 'default'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # db
    db.init_app(app)

    # login
    login_manager.init_app(app)

    # blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    handle_errors(app)

    return app


def handle_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def acess_forbidden_error(error):
        return render_template('403.html'), 403