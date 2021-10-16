from logging import exception
from typing import Tuple

from flask import request, jsonify
from flask.wrappers import Response

from solver import solve as solver_solve, UnsafeTaskError
from solver.task import json_to_task
from . import app
from . import db
from .error_codes import error_codes
from .user import User


def api_key_required(f):
    def decorator(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key is None:
            return jsonify({'error': 'Api key is missing'}), 401
        user = User.query.filter_by(api_key=api_key).first()
        if user is None:
            return jsonify({'error': 'Invalid api key'}), 401
        return f(user, *args, **kwargs)
    return decorator


def limit_number_of_requests(f):
    def decorator(user, *args, **kwargs):
        if user.requests >= 250:
            return jsonify({'error': 'Too many requests'}), 429
        user.requests += 1
        db.session.commit()
        return f(user, *args, **kwargs)
    return decorator


@app.route('/solve', methods=['POST'])
@api_key_required
@limit_number_of_requests
def solve(user: User) -> Tuple[Response, int]:
    """Solve task"""
    json = request.json
    task = json_to_task(json)
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
    return jsonify(changes), 200
