# -*- coding: utf-8 -*-

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from application import create_app
from application.extensions import db


app = create_app('default')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('runserver', Server(host='127.0.0.1', port=5200))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
