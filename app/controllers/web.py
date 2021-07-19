import logging
import time

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

from app.models.todo import Todo
from utils.utils import TIME_FORMAT
from conf import config

logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../../static',
            template_folder='../../templates')


def run():
    app.run(host=config.web_ip, port=config.web_port)


@app.route('/')
def index():
    return render_template('./index.html')


@app.teardown_appcontext
def remove_session(ex=None):
    from app.models.base import Session
    Session.remove()


@app.route('/todo', methods=['GET', 'PUT', 'POST', 'DELETE'])
def todo_api():
    if request.method == 'GET':
        logger.info('access by GET')

        todo_list = Todo.get_all()

        if todo_list is None:
            return jsonify({'todo': None}), 200

        return jsonify({'todo': [todo.values for todo in todo_list]}), 200

    if request.method == 'POST':
        logger.info('access by POST')

        response_json = request.json
        logger.info(f'json data -> {response_json}')

        contents = response_json['contents']
        priority = response_json['priority']

        timestamp = time.strftime(TIME_FORMAT)
        status = Todo.create(timestamp=timestamp,
                             contents=contents, priority=priority)
        if status:
            return jsonify({'timestamp': timestamp}), 200
        elif not status:
            return jsonify({'error': 'Data Created Error!!'}), 400

    if request.method == 'PUT':
        logger.info('access by PUT')

        response_json = request.json
        logger.info(f'json data -> {response_json}')

        timestamp = response_json['timestamp']
        contents = response_json['contents']
        priority = response_json['priority']

        status = Todo.update(timestamp=timestamp,
                             contents=contents, priority=priority)
        if status:
            return jsonify({'message': 'Update complete'}), 200
        elif not status:
            return jsonify({'error': 'Updata error'}), 400

    if request.method == 'DELETE':
        logger.info('access by DELETE')

        response_json = request.json
        logger.info(f'json data -> {response_json}')

        timestamp = response_json['timestamp']

        status = Todo.delete(timestamp=timestamp)

        if status:
            return jsonify({'message': 'Delete complete'}), 200
        elif not status:
            return jsonify({'error': 'Delete error'}), 400
