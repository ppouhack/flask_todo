from flask import jsonify
from flask import request
from flask import session
from flask import Blueprint
from models import Todo, db, Fcuser
import requests
from . import api

@api.route('/todos/done', methods=['PUT'])
def todos_done():
    userid = session.get('userid', 1)
    if not userid:
        return jsonify(), 401

    data = request.get_json()
    todo_id = data.get('todo_id')

    todo = Todo.query.filter_by(id=todo_id).first()
    fcuser = Fcuser.query.filter_by(userid=userid).first()

    if todo.fcuser_id != fcuser.id:
        return jsonify(), 400

    todo.status = 1

    db.session.commit()

    return jsonify()

@api.route('/todos', methods=['GET', 'POST', 'DELETE'])
def todos():
    # 로그인 필요
    userid = session.get('userid', 1)
    if not userid:
        return jsonify(), 401

    if request.method == 'POST':
        data = request.get_json()
        todo = Todo()
        todo.title = data.get('title')

        fcuser = Fcuser.query.filter_by(userid=userid).first()
        todo.fcuser_id = fcuser.id

        todo.due = data.get('due')
        todo.status = 0

        db.session.add(todo)
        db.session.commit()

        return jsonify(), 201

    elif request.method == 'GET':
        todos = Todo.query.filter_by(fcuser_id=userid)
        return jsonify([t.serialize for t in todos]), 201

    elif request.method == 'DELETE':
        data = request.get_json()
        todo_id = data.get('todo_id')
        todo = Todo.query.filter_by(id=todo_id).first()

        db.session.delete(todo)
        db.session.commit()

        return jsonify(), 203

    return jsonify()

@api.route('/test', methods=['POST'])
def test():
    data = request.get_json()
    return jsonify(data)
