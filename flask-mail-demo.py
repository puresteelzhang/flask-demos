# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_mail import Mail, Message
from threading import Thread
import os

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or 'me@example.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or '666666'

mail = Mail(app)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# 最基本的发送邮件方式
@app.route('/')
def index():
    msg = Message('Hello', sender=('ethan', 'me@example.com'), recipients=['other@example.com'])
    # msg.body = 'The first email!'
    msg.html = '<b>Hello Web</b>'
    mail.send(msg)

    return '<h1>OK!</h1>'


# 异步发送邮件
@app.route('/sync')
def send_email():
    msg = Message('Hello', sender=('ethan', 'me@example.com'), recipients=['other@example.com'])
    msg.html = '<b>send email asynchronously</b>'
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return 'send successfully'


# 邮件带附件
@app.route('/attach')
def add_attchments():
    msg = Message('Hello', sender=('ethan', 'me@example.com'), recipients=['other@example.com'])
    msg.html = '<b>Hello Web</b>'

    with app.open_resource("/Users/ethan/Documents/pixels.jpg") as fp:
        msg.attach("photo.jpg", "image/jpeg", fp.read())

    mail.send(msg)
    return '<h1>OK!</h1>'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6234, debug=True)

