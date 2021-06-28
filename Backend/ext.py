import random
from flask import *

from Backend import *
from Backend.models import *
from flask_cors import cross_origin
from functools import wraps
import jwt



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        try:
            incoming = request.get_json()
            token = incoming['token']
        except:
            return jsonify({
                'message' : 'No Token sent, User not logged in'
            }), 401
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY)
            current_user = User.query\
                .filter_by(email = data['email']).first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401 
        
        return  f(current_user, *args, **kwargs)
   
    return decorated

