from functools import wraps
from Backend.ext import token_required
from flask import jsonify



def check_confirmed(func):
    @token_required
    @wraps(func)
    def decorated_function(current_user, *args, **kwargs):
        if current_user.confirmed is False:
            return jsonify({
                "message": 'Please confirm your account!'
            })
        return func(*args, **kwargs)

    return decorated_function
