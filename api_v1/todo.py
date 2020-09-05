from flask import jsonify
from flask import request
from flask import session
from flask import Blueprint
from models import Todo, db, Fcuser
import requests
from . import api

@api.route('/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'POST':
        # 로그인 필요
        userid = session.get('userid', None)
        if not userid:
            return jsonify(), 401

        data = request.get_json()
        todo = Todo()
        todo.title = data.get('title')
        todo.fcuser_id = userid

        db.session.add(todo)
        db.session.commit()

        return jsonify(), 201

    elif request.method == 'GET':
        pass

    data = request.get_json()
    return jsonify(data)

@api.route('/test', methods=['POST'])
def test():
    data = request.get_json()
    return jsonify(data)
