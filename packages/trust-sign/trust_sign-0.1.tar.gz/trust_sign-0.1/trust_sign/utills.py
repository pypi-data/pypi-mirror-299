from functools import wraps
from flask import request, jsonify

def require_api_key(api_key):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request_api_key = request.headers.get('X-API-KEY')
            if request_api_key != api_key:
                return jsonify({'error': 'Unauthorized'}), 401
            return f(*args, **kwargs)
        return wrapper
    return decorator
