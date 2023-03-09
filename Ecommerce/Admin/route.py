from flask import *
from Ecommerce.model import *
from Ecommerce.Admin.decorator import admin_required

admin = Blueprint('admin', __name__)


@admin.route('/admin/users', methods=['GET'])
#@admin_required
def get_all_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    result = user_schema.dump(users)
    return jsonify(result)

@admin.route('/admin/users/<int:user_id>', methods=['GET'])
#@admin_required
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


@admin.route('/admin/register', methods=['POST'])
#@admin_required
def register_admin():
    data = request.get_json()
    if not all(field in data for field in ['name', 'email', 'password']):
        return jsonify({'error': 'Missing fields'}), 400
    new_admin = Admin(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'message': 'New admin registered successfully.'}), 201


# Retrieve a list of all products in the store
@admin.route('/admin/products', methods=['GET'])
@admin_required
def get_products():
    query_params = request.args.to_dict()
    products = Product.query.filter_by(**query_params).all()
    return jsonify({'products': [product.to_dict() for product in products]})

# Retrieve details for a specific product
@admin.route('/admin/products/<int:id>', methods=['GET'])
@admin_required
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({'product': product.to_dict()})

# Create a new product in the store
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

# Update an existing product in the store
@admin.route('/admin/products/<int:id>', methods=['PUT'])
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


@admin.route('/products/<int:id>', methods=['DELETE'])
@admin_required
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200


@admin.route('/orders', methods=['GET'])
@admin_required
def get_all_orders():
    orders = Order.query.all()
    if not orders:
        return jsonify({'error': 'No orders found'}), 404

    order_list = []
    for order in orders:
        products = []
        for item in order.items:
            product = {
                'id': item.product.id,
                'name': item.product.name,
                'price': item.product.price,
                'quantity': item.quantity
            }
            products.append(product)

        order_dict = {
            'id': order.id,
            'status': order.status,
            'total_price': order.total_price,
            'user_id': order.user_id,
            'products': products
        }
        order_list.append(order_dict)

    return jsonify({'orders': order_list}), 200

@admin.route('/orders/<int:id>', methods=['GET'])
@admin_required
def get_order_by_id(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    products = []
    for item in order.items:
        product = {
            'id': item.product.id,
            'name': item.product.name,
            'price': item.product.price,
            'quantity': item.quantity
        }
        products.append(product)

    order_dict = {
        'id': order.id,
        'status': order.status,
        'total_price': order.total_price,
        'user_id': order.user_id,
        'products': products
    }
    return jsonify({'order': order_dict}), 200

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


# DELETE /admin/orders/:id
@admin.route('/admin/orders/<int:order_id>', methods=['DELETE'])
@admin_required
def delete_order(current_user, order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Update inventory levels
    for item in order.items:
        product = item.product
        product.inventory += item.quantity
        db.session.add(product)
    
    # Issue refund
    if order.payment_status == 'paid':
        # Code to initiate refund through payment gateway
        order.payment_status = 'refunded'
    
    db.session.delete(order)
    db.session.commit()
    
    return jsonify({'message': 'Order deleted successfully'}), 200

# GET /admin/customers
@admin.route('/admin/customers', methods=['GET'])
@admin_required
def get_customers(current_user):
    customers = Customer.query.all()
    return jsonify([customer.serialize() for customer in customers]), 200

# GET /admin/customers/:id
@admin.route('/admin/customers/<int:customer_id>', methods=['GET'])
@admin_required
def get_customer_details(current_user, customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    orders = Order.query.filter_by(user_id=customer.id).all()
    return jsonify({
        'customer': customer.serialize(),
        'orders': [order.serialize() for order in orders]
    }), 200

# PUT /admin/customers/:id
@admin.route('/admin/customers/<int:customer_id>', methods=['PUT'])
@admin_required
def update_customer(current_user, customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    data = request.get_json()
    if 'name' in data:
        customer.name = data['name']
    if 'email' in data:
        customer.email = data['email']
    if 'address' in data:
        customer.address = data['address']
    if 'phone_number' in data:
        customer.phone_number = data['phone_number']
    
    db.session.add(customer)
    db.session.commit()
    
    return jsonify({'message': 'Customer updated successfully'}), 200

# DELETE /admin/customers/:id
@admin.route('/admin/customers/<int:customer_id>', methods=['DELETE'])
@admin_required
def delete_customer(current_user, customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    orders = Order.query.filter_by(user_id=customer.id).all()
    for order in orders:
        # Update inventory levels
        for item in order.items:
            product = item.product
            product.inventory += item.quantity
            db.session.add(product)
        
        # Issue refund
        if order.payment_status == 'paid':
            # Code to initiate refund through payment gateway
            order.payment_status = 'refunded'
        
        db.session.delete(order)
    
    db.session.delete(customer)
    db.session.commit()
    
    return jsonify({'message': 'Customer deleted successfully'}), 200

@admin.route('/brands', methods=['GET'])
def get_brands():
    brands = Brand.query.all()
    return jsonify({'brands': [brand.name for brand in brands]})