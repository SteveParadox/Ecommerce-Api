from flask import jsonify
from Ecommerce.model import *
from Ecommerce.Admin.decorator import admin_required
from Ecommerce import *
import jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


admin = Blueprint('admin', __name__)

@admin.route('/admin/register', methods=['POST'])
def register_admin():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Name, email, and password are required.'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    admin = Administrator(name=name, email=email, password=hashed_password)
    db.session.add(admin)
    db.session.commit()

    return jsonify({'message': 'Admin created!'}), 201



@admin.route('/admin/login', methods=['POST'])
def admin_login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    admin = Administrator.query.filter_by(email=email).first()
    if not admin:
        return jsonify({'error': 'Invalid email or password'}), 401
    if not bcrypt.check_password_hash(admin.password, password):
        return jsonify({'error': 'Invalid email or password'}), 401
    access_token = create_access_token(identity=admin.id)
    
    return jsonify({'message': 'Login successful', 'access_token': access_token}), 200



@admin.route('/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    result = user_schema.dump(users)
    return jsonify(result)

@admin.route('/admin/user/<int:user_id>', methods=['GET'])
@admin_required
def get_user_by_id(user_id):
    user = User.query.get_or_404(user_id)
    user_schema = UserSchema()
    result = user_schema.dump(user)
    return jsonify(result)

@admin.route('/admin/users/<int:user_id>/status', methods=['PUT'])
@admin_required
def update_user_status(user_id):
    user = User.query.get_or_404(user_id)
    new_status = request.json.get('status')
    user.is_seller = new_status
    db.session.commit()
    return jsonify({'message': f'Successfully updated user {user_id} status to {new_status}.'})


@admin.route('/admin/users/<int:user_id>/delete', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'Successfully deleted user {user_id}.'})



@admin.route('/admin/products', methods=['GET'])
@admin_required
def get_products():
    products = Product.query.all()
    return jsonify({'products': [product.to_dict() for product in products]})

# Retrieve details for a specific product
@admin.route('/admin/products/<int:id>', methods=['GET'])
@admin_required
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({'product': product.to_dict()})

@admin.route('/admin/products', methods=['POST'])
@admin_required
def create_product():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input data'}), 400
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return jsonify({'product': product.to_dict()}), 201

@admin.route('/admin/products/<int:id>/update', methods=['PUT'])
@admin_required
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input data'}), 400
    for key, value in data.items():
        setattr(product, key, value)
    db.session.commit()
    return jsonify({'product': product.to_dict()})


@admin.route('/admin/products/<int:id>/delete', methods=['DELETE'])
@admin_required
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200


@admin.route('/admin/orders', methods=['GET'])
@admin_required
def get_all_orders():
    orders = Order.query.all()
    if not orders:
        return jsonify({'error': 'No orders found'}), 404

    order_list = []
    for order in orders:
        product = Product.query.filter_by(id=order.product_id).first()
        user = User.query.filter_by(id=order.user_id).first()
        products = []
        for item in order.items:
            product = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': item.quantity
            }
            products.append(product)

        order_dict = {
            'id': order.id,
            'status': order.status,
            'total_price': order.total_price,
            'user_id': f"{user.first_name} {user.last_name}",
            'products': products
        }
        order_list.append(order_dict)

    return jsonify({'orders': order_list}), 200





@admin.route('/admin/brands', methods=['GET'])
@admin_required
def get_brands():
    brands = Brand.query.all()
    return jsonify({'brands': [brand.name for brand in brands]})


@admin.route('/admin/create/category', methods=['POST'])
@admin_required
def categories():
    if request.method == 'GET':
        categories = Category.query.all()
        return jsonify([{'id': c.id, 'name': c.name} for c in categories])
    elif request.method == 'POST':
        data = request.get_json()
        for i in data['name']:
            category = Category(name=i)
            db.session.add(category)
            db.session.commit()
        return jsonify({'id': category.id, 'name': category.name}), 201
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@admin.route('/api/categories', methods=['GET'])
@admin_required
def list_admin_categories():
    category = Category.query.all()
    _schema = CategorySchema(many=True)
    result = _schema.dump(category)
    return jsonify({'Categories': result})


@admin.route('/admin/orders/all', methods=['GET'])
@admin_required
def get_orders():
    orders = Order.query.filter_by().all()
    if not orders:
        return jsonify({'message': 'No orders found'}), 404
    
    order_data = []
    for order in orders:
        product = Product.query.get(order.product_id)
        order_dict = {
            'id': order.id,
            'product': product.name,
            'quantity': order.quantity,
            'total_price': order.total_price
        }
        order_data.append(order_dict)
    
    return jsonify({'orders': order_data}), 200

@admin.route('/admin/orders/<int:order_id>', methods=['GET'])
@admin_required
def get_admin_orders(order_id):
    orders = Order.query.filter_by(id=order_id).first()
    if not orders:
        return jsonify({'message': 'No orders found'}), 404
    
    product = Product.query.get(order.product_id)
    order_dict = {
        'id': order.id,
        'description': product.description,
        'image': product.image_url,
        'product': product.name,
        'quantity': order.quantity,
        'total_price': order.total_price
    }

    return jsonify({'orders': order_dict}), 200

@admin.route('/admin/orders/<int:order_id>/status', methods=['GET'])
@admin_required
def get_admin_orders_status(order_id):
    data =request.get_json()
    status = data["status"]
    if status != "delivered" or status != "shipped" or status != "placed":
        return jsonify({'error': 'No such status'}), 404
    orders = Order.query.filter_by(id=order_id).first()
    if not orders:
        return jsonify({'message': 'No orders found'}), 404
    
    return jsonify({'orders': order_dict}), 200

@admin.route('/admin/orders/<int:order_id>', methods=['DELETE'])
@admin_required
def delete_order(current_user, order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    for item in order.items:
        product = item.product
        product.quantity += item.quantity
        db.session.add(product)
    
    # Issue refund
    if order.payment_status == 'placed':
        # Code to initiate refund through payment gateway
        order.payment_status = 'refunded'
    db.session.delete(order)
    db.session.commit()
    
    return jsonify({'message': 'Order deleted successfully'}), 200


@admin.route('/orders/<int:id>', methods=['PUT'])
@admin_required
def update_order_status(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    request_data = request.get_json()
    if not request_data or 'status' not in request_data:
        return jsonify({'error': 'Invalid or missing request body'}), 400

    status = request_data['status']
    if not status or not isinstance(status, str):
        return jsonify({'error': 'Invalid status value'}), 400

    order.status = status
    db.session.commit()
    return jsonify({'message': 'Order status updated successfully'}), 200
