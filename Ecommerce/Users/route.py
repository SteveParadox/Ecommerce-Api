from flask import *
import re
from operator import itemgetter
from flask_bcrypt import *
from flask_jwt_extended import *
import requests
from Ecommerce.model import *
from .decorator import token_required


users = Blueprint('users', __name__)


@users.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'message': 'User already exists!'}), 409
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    public_id = str(shortuuid.uuid())
    user = User(public_id=public_id, name=data['name'], email=data['email'], password=hashed_password)
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
    if not user.verified:
        return jsonify({'message': 'User is not verified!'}), 401
    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() +
         datetime.timedelta(hours=24)}, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'message': 'Login successful!', 'token': token}), 200

    return jsonify({'message': 'Invalid login credentials!'}), 401

# user logout endpoint
@users.route('/api/logout', methods=['POST'])
@token_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful!'})

@users.route('/api/orders', methods=['POST'])
@token_required
def place_order(current_user):
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')
    if not product_id or not quantity:
        return jsonify({'error': 'Missing required fields'}), 400
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    if quantity <= 0:
        return jsonify({'error': 'Invalid quantity'}), 400
    order = Order(product_id=product_id, quantity=quantity, total_price=product.price * quantity, user_id=current_user.id)
    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'Order placed successfully'}), 201