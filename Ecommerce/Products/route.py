from flask import *
from Ecommerce.model import *
import requests
from flask_login import login_required
from flask_jwt_extended import jwt_required
from Ecommerce.Users.decorator import token_required
from Ecommerce.recommendation import *
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

product = Blueprint('product', __name__)


@product.route('/api/create/category', methods=['POST'])
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


@product.route('/api/categories', methods=['GET'])
def list_categories():
    category = Category.query.all()
    _schema = CategorySchema(many=True)
    result = _schema.dump(category)
    return jsonify({'Categories': result})


@product.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': product.id, 'name': product.name,
     'price': product.price} for product in products])

@product.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    brand= Brand.query.filter_by(id=product.brand_id).first()
    if brand:
        return jsonify({ 'name': product.name, 
        'price': product.price, 'description': product.description, 'brand':brand.name})
    return jsonify({ 'name': product.name, 
    'price': product.price, 'description': product.description})
    
@product.route("/api/brand/search")
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Search query parameter "q" is required'}), 400

    brands = Brand.query.filter(Brand.name.ilike(f'%{query}%'))
    results = []
    for brand in brands:
        products = Product.query.filter_by(brand_id=brand.id)
        product_list = []
        for product in products:
            product_list.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'category': {
                    'id': product.category.id,
                    'name': product.category.name
                }
            })
        results.append({
            'id': brand.id,
            'name': brand.name,
            'products': product_list
        })
    return jsonify(results)

@product.route('/brands/<int:brand_id>/products', methods=['GET'])
def get_brand_products(brand_id):
    products = Product.query.filter_by(brand_id=brand_id).all()
    return jsonify({'products': [{'name': product.name, 'price': product.price} for product in products]})


@product.route('/api/products/<int:product_id>/like', methods=['POST'])
@token_required
def like_product(current_user, product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({'error': 'Product not found!'}), 404

    if product.likes.filter_by(user_id=current_user.id).first():
        return jsonify({'error': 'Product already liked!'}), 400

    like = Like(user_id=current_user.id, product_id=product_id)
    db.session.add(like)
    product.like += 1
    db.session.commit()

    return jsonify({'message': 'Product liked successfully!'}), 200



@product.route('/products/<int:product_id>/dislike', methods=['POST'])
@token_required
def dislike_product(product_id):
    for product in products:
        if product['id'] == product_id:
            product['dislikes'] += 1
            db.session.add(product)
            db.session.commit()
            return jsonify({'message': 'Product disliked successfully.'})
    return jsonify({'error': 'Product not found.'}), 404

# Endpoint to add a product to cart
@product.route('/products/cart/add', methods=['POST'])
@token_required
def add_to_cart(current_user):
    data = request.get_json()
    product_id = data["product_id"]
    quantity = data["quantity"]
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found.'}), 404
    #if not product.is_available:
        #return jsonify({'error': 'Product not available for purchase.'}), 400

    if quantity > product.quantity:
        return jsonify({'error': 'Not enough product availavle.'}), 400
    
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        pass
    else:
        cart = Cart(user_id = current_user.id)
        db.session.add(cart)
    cart_item = CartItem.query.filter_by(product_id= product_id).first()
    if cart_item:
        cart_item.quantity += quantity
        cart_id = cart.id
    else:
        cart_item = CartItem(product_id=product_id, quantity=quantity, cart_id=cart.id)
        db.session.add(cart_item)
    db.session.commit()

    return jsonify({'message': 'Product added to cart successsfully.'}), 200
    
    

@product.route('/products/cart', methods=['GET'])
@token_required
def view_cart(current_user):
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        return jsonify({'message': 'Cart is empty.'}), 200
    cart_items = []
    for item in cart.items:
        product = Product.query.get(item.product_id)
        cart_item = {
            'id': item.id,
            'product_id': item.product_id,
            'product_name': product.name,
            'quantity': item.quantity,
            'price': product.price
        }
        cart_items.append(cart_item)
    return jsonify({'cart_items': cart_items}), 200

    

@product.route('/api/products/<int:product_id>/reviews', methods=['POST'])
@token_required
def add_review(current_user, product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    data = request.get_json()
    rating = data['rating']
    comment = data['comment']
    review = Review(rating=rating, comment=comment, user_id=current_user.id, product_id=product.id)
    db.session.add(review)
    db.session.commit()

    return jsonify({'message': 'Review added successfully'}), 201


@product.route('/products/<category>')
def get_products_by_category(category):
    category_name = Category.query.filter_by(name=category).first()
    if not category_name:
        return jsonify({'error': 'Category not found'}), 404

    products = Product.query.filter_by(category_id=category_name.id).all()
    response = {
        'category': category_name.name,
        'products': [product.to_dict() for product in products]
    }

    return jsonify(response)


@product.route('/api/place/order', methods=['POST'])
@token_required
def place_order(current_user):
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        return jsonify({'error': 'No items in cart'}), 400
    
    orders = Order.query.filter_by(user_id=current_user.id).first()
  
    product_ids = [item.product_id for item in cart.items]
    quantities = [item.quantity for item in cart.items]
    
    if not product_ids or not quantities or len(product_ids) != len(quantities):
        return jsonify({'error': 'Missing or invalid required fields'}), 400
    
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    if len(products) != len(product_ids):
        return jsonify({'error': 'One or more products not found'}), 404
    
    invalid_quantities = [i for i, q in enumerate(quantities) if q <= 0]
    if invalid_quantities:
        return jsonify({'error': f'Invalid quantity for product {product_ids[invalid_quantities[0]]}'}), 400
    
    orders = []
    for i, product in enumerate(products):
        order = Order(product_id=product.id, quantity=quantities[i], total_price=product.price * quantities[i], user_id=current_user.id)
        orders.append(order)
    db.session.add_all(orders)
    db.session.commit()
    
    # Clear cart
    #cart.items = []
    db.session.commit()
    
    return jsonify({'message': 'Orders placed successfully'}), 201 


@product.route('/api/orders', methods=['GET'])
@token_required
def get_orders(current_user):
    orders = Order.query.filter_by(user_id=current_user.id).all()
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

@product.route('/api/orders/<int:order_id>/update', methods=['PUT'])
@token_required
def update_order(current_user, order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    data = request.get_json()
    
    if 'product_id' in data:
        product = Product.query.filter_by(id=data['product_id']).first()
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        order.product_id = product.id
        
    if 'quantity' in data:
        quantity = data['quantity']
        if quantity <= 0:
            return jsonify({'error': 'Invalid quantity'}), 400
        order.quantity = quantity
        order.total_price = quantity * product.price
        
    db.session.commit()
    
    return jsonify({'message': 'Order updated successfully'}), 200


@product.route('/product/<int:product_id>/review')
def get_rating(product_id):
    reviews = Review.query.filter_by().first()
    _schema = ReviewSchema()
    result = _schema.dump(reviews)
    return jsonify({'review': result})




@app.route('/product/ratings')
def get_ratings():
    """
    Returns a dictionary containing the ratings for each product
    keyed by product id.
    """
    product_ratings = {}
    reviews = Review.query.all()
    for review in reviews:
        product_id = review.product_id
        rating = review.rating
        if product_id not in product_ratings:
            product_ratings[product_id] = []
        product_ratings[product_id].append(rating)
    return jsonify(product_ratings)

@app.route('/product_similarity/<int:product_id>')
def get_product_similarity(product_id):
    """
    Computes the cosine similarity between a product and all other products based on their ratings.
    """
    product_ids = Product.query.filter_by(id=product_id).first()
    num_products = len(product_ids)
    product_similarity = np.zeros((num_products, num_products))
    for i in range(num_products):
        for j in range(num_products):
            if i == j:
                product_similarity[i, j] = 1
            else:
                ratings_i = product_ratings[product_ids[i]]
                ratings_j = product_ratings[product_ids[j]]
                similarity = cosine_similarity([ratings_i], [ratings_j.T])[0][0]
                product_similarity[i, j] = similarity
    return product_similarity, product_ids


@product.route('/recommendations')
@token_required
def get_recommendations(current_user):
    """
    Given a user id, computes the similarity between the products they have rated
    and all other products, and returns the top-rated products with the highest
    similarity scores.
    """
    user_reviews = Review.query.filter_by(user_id=current_user.id).all()
    rated_product_ids = set(review.product_id for review in user_reviews)
    product_ratings = {product.id: [] for product in Product.query.all()}
    for review in user_reviews:
        product_ratings[review.product_id].append(review.rating)
    product_similarity, product_ids = get_product_similarity(product_ratings)
    recommended_products = get_top_recommended_products(current_user, product_similarity, product_ids)
    return jsonify(recommended_products)

