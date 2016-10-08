# -*- coding: utf-8 -*-

from app import create_app


if __name__ == '__main__':
    app = create_app('default')
    app.run(host='127.0.0.1', port=5200, debug=True)
