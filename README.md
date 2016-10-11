
Flask Demo
===

## v0.1

```
$ git checkout v0.1
```

一个最简单的 demo：

```python
# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5200, debug=True)
```


## v0.2

```
$ git checkout v0.2
```

```python
# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'some secret key'

books = ['the first book', 'the second book', 'the third book']


@app.route("/")
def index():
    render_string = '<ul>'

    for book in books:
        render_string += '<li>' + book + '</li>'

    render_string += '</ul>'

    return render_string

@app.route("/book", methods=['POST', 'GET'])
def book():
    _form = request.form

    if request.method == 'POST':
        title = _form["title"]
        books.append(title)
        return redirect(url_for('index'))

    return '''
        <form name="book" action="/book" method="post">
            <input id="title" name="title" type="text" placeholder="add book">
            <button type="submit">Submit</button>
        </form>
        '''

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5200, debug=True)
```


## v0.3

```
$ git checkout v0.3
```

加入蓝图功能，代码结构如下：

```
flask-demos
├── README.md
├── app.py
├── book
│   ├── __init__.py
│   └── book.py
├── movie
│   ├── __init__.py
│   └── movie.py
└── templates
    ├── 404.html
    ├── book.html
    ├── layout.html
    └── movie.html
```


通过 `python app.py` 运行。

## v0.4

```
$ git checkout v0.3
```

加入密码和 token 认证，只有登录成功的用户才可以提交书籍，其中，token 认证可使用命令行 curl 测试。

```shell
# 密码认证
curl -i -u ethan:6667 -d "title=mybook" -X POST http://127.0.0.1:5200/book

# token 认证
curl -i -u token:x -d "title=threee" -X POST http://127.0.0.1:5200/book
```


## v0.5

```
$ git checkout v0.5
```

采用工厂方法 `creat_app()` 创建 `app` 对象。

代码结构如下：

```
.
├── app.py
├── book
│   ├── __init__.py
│   └── book.py
├── configs.py
├── movie
│   ├── __init__.py
│   └── movie.py
├── requirements.txt
├── run.py
└── templates
    ├── 404.html
    ├── book.html
    ├── layout.html
    └── movie.html
```

运行：

```
$ python run.py
```

