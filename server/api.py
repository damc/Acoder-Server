from flask import request, jsonify
from flask.wrappers import Response

from solver.task import json_to_task

from . import app
from .user import User
from solver import solve as solver_solve


def api_key_required(f):
    def decorator(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key is None:
            return jsonify({'error': 'api key is missing'}), 401
        user = User.query.filter_by(api_key=api_key).first()
        if user is None:
            return jsonify({'error': 'invalid api key'}), 401
        return f(user, *args, **kwargs)
    return decorator


@app.route('/solve', methods=['POST'])
@api_key_required
def solve(user: User) -> Response:
    """Solve task"""
    json = request.json
    task = json_to_task(json)
    return jsonify(solver_solve(task, str(user.id)))
