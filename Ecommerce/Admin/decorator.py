from functools import wraps
from flask import abort
from flask_jwt_extended import get_jwt_identity


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            abort(403, description='Admin privileges required')
        return func(*args, **kwargs)
    return wrapper
