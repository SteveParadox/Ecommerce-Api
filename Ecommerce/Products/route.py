from flask import *
from Ecommerce.model import *
import requests
from flask_login import login_required
from flask_jwt_extended import jwt_required

product = Blueprint('product', __name__)


@product.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': product.id, 'name': product.name,
     'price': product.price} for product in products])

@product.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price})
    

@product.route('/products/<int:product_id>/like', methods=['POST'])
def like_product(product_id):
    for product in products:
        if product['id'] == product_id:
            product['likes'] += 1
            return jsonify({'message': 'Product liked successfully.'})
    return jsonify({'error': 'Product not found.'}), 404


# Endpoint to add a product to cart
@product.route('/products/<int:product_id>/cart', methods=['POST'])
def add_to_cart(product_id):
    for product in products:
        if product['id'] == product_id:
            product['in_cart'] = True
            return jsonify({'message': 'Product added to cart successfully.'})
    return jsonify({'error': 'Product not found.'}), 404
    
    
    
@product.route('/api/products/liked', methods=['GET'])
@login_required
def get_liked_products():
    liked_product_ids = [like.product_id for like in Likes.query.filter_by(user_id=current_user.id)]
    liked_products = Product.query.filter(Product.id.in_(liked_product_ids)).all()
    products = [{'id': product.id, 'name': product.name,
    'description': product.description, 
    'price': product.price} for product in liked_products]
    return jsonify(products)
    
    

@product.route('/api/products/<int:product_id>/reviews', methods=['POST'])
def add_review(product_id):
    # Get the current user
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user_id = resp['sub']
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            # Get the product
            product = Product.query.get(product_id)
            if not product:
                return jsonify({'error': 'Product not found'}), 404

            # Get the review data
            data = request.get_json()
            rating = data.get('rating')
            comment = data.get('comment')

            # Create the review
            review = Review(rating=rating, comment=comment, user=user, product=product)

            # Add the review to the database
            db.session.add(review)
            db.session.commit()

            return jsonify({'message': 'Review added successfully'}), 201
        else:
            return jsonify({'error': resp}), 401
    else:
        return jsonify({'error': 'Authentication token not provided'}), 401


@product.route('/api/products/<int:product_id>/rating', methods=['POST'])
def add_rating(product_id):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user_id = resp['sub']
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            product = Product.query.get(product_id)
            if not product:
                return jsonify({'error': 'Product not found'}), 404
            data = request.get_json()
            rating = data.get('rating')
            product.num_ratings += 1
            product.total_ratings += rating
            product.avg_rating = product.total_ratings / product.num_ratings
            db.session.add(product)
            db.session.commit()
            return jsonify({'message': 'Rating added successfully'}), 201
        else:
            return jsonify({'error': resp}), 401
    else:
        return jsonify({'error': 'Authentication token not provided'}), 401


@product.route('/products/<category>')
def get_products_by_category(category):
    products = Product.query.filter_by(category=category).all()
    return jsonify([product.to_dict() for product in products])


@product.route('/api/products/most-visited-categories', methods=['GET'])
@jwt_required()
def get_products_by_most_visited_categories():
    current_user_id = get_jwt_identity()
    user_categories = Category.query.filter_by(user_id=current_user_id).order_by
    (Category.visits.desc()).limit(3)
    product_ids = []
    for category in user_categories:
        product_ids.extend([product.id for product in category.category.products])
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    product_schema = ProductSchema(many=True)
    return product_schema.dump(products)