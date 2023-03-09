from flask import *
import re
from operator import itemgetter
import requests
from Ecommerce.model import *
from .decorator import token_required
from Ecommerce import *
import shortuuid
import jwt
from flask_jwt_extended import unset_jwt_cookies


users = Blueprint('users', __name__)


@users.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'message': 'User already exists!'}), 409
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    public_id = str(shortuuid.uuid())
    first_name= data["first_name"]
    last_name= data["last_name"]
    gender= data["gender"]
    phone_number= data["phone_number"]
    country= data["country"]
    date_of_birth=data["date_of_birth"]
    user = User(public_id=public_id, first_name=first_name, 
    last_name=last_name, email=data['email'],
     password=hashed_password, gender=gender, 
     phone_number=phone_number, country=country, date_of_birth=date_of_birth, address = data["address"])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created!'}), 201

@users.route('/api/verify/<public_id>', methods=['PUT'])
@token_required
def verify_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'You are not authorized to perform this action!'}), 401
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'User not found!'}), 404
    user.verified = True
    db.session.commit()

    return jsonify({'message': 'User verified!'})

# user login endpoint
@users.route('/api/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Invalid login credentials!'}), 401
    user = User.query.filter_by(email=auth.username).first()
    if not user:
        return jsonify({'message': 'Invalid login credentials!'}), 401
    #if not user.verified:
        #return jsonify({'message': 'User is not verified!'}), 401
    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() +
         datetime.timedelta(hours=24)}, app.config['SECRET_KEY'], algorithm="HS256")
        logged = User.query.filter_by(public_id=user.public_id).first()
        logged.token = token
        db.session.add(logged)
        db.session.commit()
        return jsonify({'message': 'Login successful!', 'token': token}), 200

    return jsonify({'message': 'Invalid login credentials!'}), 401

# user logout endpoint
blacklist = set()

@users.route('/api/logout', methods=['POST'])
@token_required
def logout(current_user):
    token = request.headers.get('Authorization')
    blacklist.add(token)
    return jsonify({'message': 'Logout successful!'})

@app.before_request
def check_blacklist():
    token = request.headers.get('Authorization')
    if token in blacklist:
        return jsonify({'message': 'Token is invalid!'}), 401
    

