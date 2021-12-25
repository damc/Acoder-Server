from functools import wraps
from json import loads
from logging import exception
from typing import Dict, Tuple

from flask import request, jsonify
from flask.wrappers import Response

from solver.question import answer as solver_answer
from solver.safety import UnsafeTaskError
from solver.solve import solve as solver_solve
from solver.task import dict_to_task
from . import app
from . import cache
from . import db
from .error_codes import error_codes
from .user import User


def api_key_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key is None:
            return jsonify({'error': 'API key missing'}), 401
        user = User.query.filter_by(api_key=api_key).first()
        if user is None:
            return jsonify({'error': 'Invalid API key'}), 401
        return f(user, *args, **kwargs)
    return decorator


def rate_limiting(f):
    @wraps(f)
    def decorator(user, *args, **kwargs):
        if user.requests >= 250:
            return jsonify({'error': 'Too many requests'}), 429
        user.requests += 1
        db.session.commit()
        return f(user, *args, **kwargs)
    return decorator


@app.route('/v1/solve', methods=['POST'])
@api_key_required
@rate_limiting
def solve(user: User) -> Tuple[Response, int]:
    """Solve task"""
    body = loads(request.json)
    allow_cached = body["allow_cached"]
    task = dict_to_task(handle_old_versions(body["task"]))
    if allow_cached:
        cached_result = cache.get(str(task))
        if cached_result is not None:
            return jsonify(cached_result), 200
    try:
        changes = solver_solve(task, str(user.id))
    except UnsafeTaskError as error:
        user.unsafe_requests += 1
        db.session.commit()
        return jsonify({'error': str(error)}), error_codes[UnsafeTaskError]
    except Exception as error:
        if type(error) in error_codes:
            return jsonify({'error': str(error)}), error_codes[type(error)]
        exception("Unexpected error")
        return jsonify({'error': "Unexpected error"}), 500
    cache.set(str(task), changes, timeout=20)
    return jsonify(changes), 200


def handle_old_versions(task_dict: Dict) -> Dict:
    if 'test_commands' not in task_dict:
        task_dict['test_commands'] = []
    if 'title' in task_dict:
        task_dict.pop('title')
    return task_dict


@app.route('/v1/answer', methods=['GET'])
@api_key_required
@rate_limiting
def answer(user: User) -> Tuple[Response, int]:
    """Answer question"""
    question = request.args.get('question')
    if question is None:
        return jsonify({'error': 'Question missing'}), 400
    answer_ = solver_answer(question, str(user.id))
    return jsonify({'answer': answer_}), 200


@app.route('/<_version>/message', methods=['GET'])
def message(_version: str) -> Response:
    return jsonify(None)
