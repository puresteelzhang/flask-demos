# -*- coding: utf-8 -*-

from flask import Flask
from flask_mongoengine import MongoEngine
from datetime import datetime


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'test',
    'host': '127.0.0.1',
    'port': 27017
}

db = MongoEngine(app)


class Todo(db.Document):
    meta = {
        'collection': 'todo',
        'ordering': ['-create_at'],
        'strict': False,
    }

    task = db.StringField()
    create_at = db.DateTimeField(default=datetime.now)
    is_completed = db.BooleanField(default=False)

    def to_dict(self):
        return {
            'id': str(self.id),
            'task': self.task,
            'create_at': self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
            'is_completed': self.is_completed
        }


@app.route('/', methods=['GET'])
def index():
    content = '<ul>'

    todos = Todo.objects().all()   # 查询所有数据
    if not todos:
        return "<p>No todos exist! <a href='/addtodo'>Add todo first.</a></p>"

    for todo in todos:
        create_at = todo.create_at.strftime("%Y-%m-%d %H:%M:%S")
        content += '<li>' + todo.task + ', ' + create_at + ', ' + str(todo.is_completed)

    content += '</ul>'
    content += "<p><a href='/filter'>filter</a></p>"
    content += "<p><a href='/sort'>sort</a></p>"
    content += "<p><a href='/update'>update</a></p>"
    content += "<p><a href='/upsert'>upsert</a></p>"
    content += "<p><a href='/pagination'>pagination</a></p>"
    content += "<p><a href='/delete'>delete</a></p>"

    return content


@app.route('/addtodo')
def add_todo():
    todo1 = Todo(task='task 1', is_completed=False)
    todo2 = Todo(task='task 2', is_completed=False)
    todo3 = Todo(task='task 3', is_completed=False)
    todo4 = Todo(task='task 4', is_completed=False)
    todo5 = Todo(task='task 5', is_completed=False)

    # 使用 save() 方法添加数据
    todo1.save()
    todo2.save()
    todo3.save()
    todo4.save()
    todo5.save()

    return "<p>add succssfully! <a href='/'>Home</a></p>"


@app.route('/filter')
def filter():
    task = 'task 1'
    todo = Todo.objects(task=task).first()

    return '<p>' + todo.task + ', ' + todo.create_at.strftime("%Y-%m-%d %H:%M:%S") + '</p>'


@app.route('/sort')
def sort():
    content = '<ul>'

    todos = Todo.objects().order_by('create_at')
    for todo in todos:
        create_at = todo.create_at.strftime("%Y-%m-%d %H:%M:%S")
        content += '<li>' + todo.task + ', ' + create_at + ', ' + str(todo.is_completed)

    content += '</ul>'
    return content


@app.route('/update')
def update():
    task = 'task 1'
    todo = Todo.objects(task=task).first()  # 先查找
    if not todo:
        return "the task doesn't exist!"

    todo.update(is_completed=True)   # 再更新

    return "<p>update succssfully! <a href='/'>Home</a></p>"


@app.route('/upsert')
def upsert():
    # if not exists then insert
    task = 'task 7'
    Todo.objects(task=task).update(upsert=True, task=task)

    return "<p>upsert succssfully! <a href='/'>Home</a></p>"


@app.route('/pagination')
def paginate():
    content = '<ul>'
    skip_nums = 1
    limit = 3

    todos = Todo.objects().order_by(
        '-create_at'
    ).skip(
        skip_nums
    ).limit(
        limit
    )

    for todo in todos:
        create_at = todo.create_at.strftime("%Y-%m-%d %H:%M:%S")
        content += '<li>' + todo.task + ', ' + create_at + ', ' + str(todo.is_completed)

    content += '</ul>'
    return content


@app.route('/delete')
def delete():
    task = 'task 6'
    todo = Todo.objects(task=task).first()  # 先查找
    if not todo:
        return "the task doesn't exist!"

    todo.delete()   # 再删除

    return "<p>delete succssfully! <a href='/'>Home</a></p>"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5204, debug=True)
