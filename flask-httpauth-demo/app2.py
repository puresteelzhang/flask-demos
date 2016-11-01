# -*- coding: utf-8 -*-

from flask import Flask, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'

auth = HTTPTokenAuth(scheme='Token')

# 实例化一个签名序列化对象 serializer
serializer = Serializer(app.config['SECRET_KEY'], expires_in=1800)


users = ['John', 'Susan']

# 生成 token
for user in users:
    token = serializer.dumps({'username': user})
    print('Token for {}: {}\n'.format(user, token))

# 回调函数，对 token 进行验证
@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = serializer.loads(token)
    except:
        return False
    if 'username' in data:
        g.user = data['username']
        return True
    return False


@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % g.user


if __name__ == '__main__':
    app.run()
