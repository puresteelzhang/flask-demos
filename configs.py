# -*- coding: utf-8 -*-

import os

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config(object):
    # Flask config
    SECRET_KEY = '^753*&FdFS#4D'
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Email config
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    # Babel config
    BABEL_DEFAULT_LOCALE = 'zh'
    BABEL_DEFAULT_TIMEZONE = 'CST'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass

config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
