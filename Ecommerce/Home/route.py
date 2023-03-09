from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_login import *
from Ecommerce.model import *
import random
import string
from datetime import datetime, timedelta
from Ecommerce.Users.decorator import token_required
from sqlalchemy import or_
from Ecommerce import *

main = Blueprint('main', __name__)


@main.route('/api/home')
def home():

    latest_products = Product.query.order_by(Product.uploaded_at.desc()).all()
    _schema = ProductSchema(many=True)
    result = _schema.dump(latest_products)
    return jsonify({'latest_products': result})

@main.route('/recommended/products')
@token_required
def recommended(current_user):

    return jsonify({'latest_products': "Coming soon"})


@main.route("/api/search")
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Search query parameter "q" is required'}), 400

    products = Product.query.filter(or_(Product.name.ilike(f'%{query}%'),
                                        Product.description.ilike(f'%{query}%')))
    results = []
    for product in products:
        results.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'category': {
                'id': product.category.id,
                'name': product.category.name
            }
        })
    return jsonify(results)

@main.route('/fake/data', methods=['POST'])
def fake():
    # create some dummy users
    for i in range(100):
        first_name = ''.join(random.choices(string.ascii_uppercase, k=10))
        last_name = ''.join(random.choices(string.ascii_uppercase, k=10))
        phone_number= f'{i}{i}{i}{i}{i}{i}{i}{i}{i}{i}{i}'
        country = ''.join(random.choices(string.ascii_uppercase, k=10))
        date_of_birth = f'{i}{i}/{i}{i}/{i}{i}'
        address = ''.join(random.choices(string.ascii_uppercase, k=10))
        email = f'user{i}@gmail.com'
        genders =['male', 'female', 'not defined', 'non-binary']
        gender = random.choice(genders)
        password = bcrypt.generate_password_hash(''.join(random.choices(string.ascii_uppercase + string.digits, k=8))).decode('utf-8')
        public_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        user = User( email=email, password=password, public_id=public_id,
         first_name=first_name, last_name=last_name, phone_number=phone_number, 
         country=country, gender=gender, address= address, date_of_birth=date_of_birth)
        db.session.add(user)

    # create some sellers
    for i in range(5):
        seller = Seller(user_id=i+1)
        db.session.add(seller)

    # create some categories
    categories = ['Books', 'Electronics', 'Home & Garden', 'Sports', 'Toys']
    for name in categories:
        category = Category(name=name)
        db.session.add(category)

    # create some products
    for i in range(20):
        name = ''.join(random.choices(string.ascii_uppercase, k=10))
        description = ''.join(random.choices(string.ascii_uppercase + string.digits, k=50))
        quantity = random.randint(1, 10)
        price = round(random.uniform(5.0, 50.0), 2)
        category_id = random.randint(1, len(categories))
        seller_id = random.randint(1, 5)
        product = Product(name=name, description=description, quantity=quantity, price=price, category_id=category_id, seller_id=seller_id)
        db.session.add(product)

    # create some orders
    for i in range(10):
        quantity = random.randint(1, 5)
        total_price = round(random.uniform(10.0, 200.0), 2)
        product_id = random.randint(1, 20)
        user_id = random.randint(1, 10)
        status = random.choice(['placed', 'shipped', 'delivered'])
        order = Order(quantity=quantity, total_price=total_price, product_id=product_id, user_id=user_id, status=status)
        db.session.add(order)

    # create some reviews
    for i in range(10):
        rating = random.randint(1, 5)
        comment = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        product_id = random.randint(1, 20)
        user_id = random.randint(1, 10)
        review = Review(rating=rating, comment=comment, product_id=product_id, user_id=user_id)
        db.session.add(review)

    # create some carts and cart items
    for i in range(10):
        cart = Cart(user_id=i+1)
        db.session.add(cart)
        for j in range(3):
            quantity = random.randint(1, 5)
            product_id = random.randint(1, 20)
            cart_id=  random.randint(1, 20)
            cart_item = CartItem(quantity=quantity, product_id=product_id, cart_id=cart_id)
            db.session.add(cart_item)

    # create some payments
    # create 10 payment records with random amount, user_id and order_id
    for i in range(10):
        amount = round(random.uniform(10.0, 200.0), 2)
        user_id = random.randint(1, 10)
        order_id = random.randint(1, 10)
        payment_date = datetime.datetime.utcnow() - timedelta(days=random.randint(0, 30))
        payment = Payment(amount=amount, user_id=user_id, order_id=order_id, payment_date=payment_date)
        db.session.add(payment)

    db.session.commit()
    return "done"