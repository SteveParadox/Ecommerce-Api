from flask import *
from Ecommerce.model import *
from flask_login import *

sellers = Blueprint('sellers', __name__)


@sellers.route('/api/sellers/products', methods=['POST'])
@login_required
def add_product():
    if current_user.is_seller:
        name = request.json.get('name')
        description = request.json.get('description')
        price = request.json.get('price')
        quantity = request.json.get('quantity')
        seller_id = current_user.id

        product = Product(name=name, description=description, price=price, 
        quantity=quantity, seller_id=seller_id)

        db.session.add(product)
        db.session.commit()

        return jsonify({'message': 'Product added successfully!'}), 201
    else:
        return jsonify({'message': 'Only sellers can add products!'}), 401

# Endpoint to get all products of a seller
@sellers.route('/api/sellers/products', methods=['GET'])
@login_required
def get_seller_products():
    if current_user.is_seller:
        seller_id = current_user.id
        products = Product.query.filter_by(seller_id=seller_id).all()

        products_list = []
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'quantity': product.quantity,
                'seller_id': product.seller_id
            }
            products_list.append(product_data)

        return jsonify({'products': products_list}), 200
    else:
        return jsonify({'message': 'Only sellers can access their products!'}), 401

# Endpoint to update a product for sellers
@sellers.route('/api/sellers/products/<int:id>', methods=['PUT'])
@login_required
def update_product(id):
    if current_user.is_seller:
        product = Product.query.filter_by(id=id, seller_id=current_user.id).first()

        if not product:
            return jsonify({'message': 'Product not found!'}), 404

        product.name = request.json.get('name', product.name)
        product.description = request.json.get('description', product.description)
        product.price = request.json.get('price', product.price)
        product.quantity = request.json.get('quantity', product.quantity)

        db.session.commit()

        return jsonify({'message': 'Product updated successfully!'}), 200
    else:
        return jsonify({'message': 'Only sellers can update their products!'}), 401

# Endpoint to delete a product for sellers
@sellers.route('/api/sellers/products/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id):
    if current_user.is_seller:
        product = Product.query.filter_by(id=id, seller_id=current_user.id).first()

        if not product:
            return jsonify({'message': 'Product not found!'}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({'message': 'Product deleted successfully!'}), 200
    else:
        return jsonify({'message': 'Only sellers can delete their products!'}), 401