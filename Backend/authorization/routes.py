import os
import sys
import stripe
import datetime
from flask import *
#import cloudinary as Cloud  
#import cloudinary.uploader
from Backend.models import *
from Backend import db, bcrypt
from Backend.config import Config
from flask_cors import cross_origin
from Backend.ext import token_required
from Backend.registration.decorator import check_confirmed
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

auth = Blueprint('authorization', __name__)

stripe_keys = {
    'secret_key': "sk_test_51IscUOBuSPNXczcenT31xOR1QnW6T2kPpfr0N3JKHvY7Idqb4oQUiOK245Azeac3VgUiN8nNT88vNf2VTkLIVebK00ZeQX3fm7",
    'publishable_key': 'pk_test_51IscUOBuSPNXczceSfoIKAm7bARLi4fS9QZr5SNVOMa3aF7zlmIwmarG0fnc2ijpkn1WrVnrs9obt9zCTPihKiBe00tVxBVhKf',
}
stripe.api_key = stripe_keys['secret_key']
Message= "Problem uploading to server... if error persists, send message to fordstphn@gmail.com to lay complaint"

try:
    PYTHON_VERSION = sys.version_info[0]
    if PYTHON_VERSION == 3:
        import urllib.request
        resource = urllib.request.urlopen('https://api.ipregistry.co/?key=0umiu3uyv8174l')
    else:
        import urlparse
        resource = urlparse.urlopen('https://api.ipregistry.co/?key=0umiu3uyv8174l')
        payload = resource.read().decode('utf-8')
        location = json.loads(payload)['location']['country']['name']
        country= str(location).lower()
except:
    pass

@auth.route('/config')
def get_publishable_key():
    stripe_config = {'publicKey': stripe_keys['publishable_key']}
    return jsonify(stripe_config)
    
@auth.route('/api/book/product/<int:product_id>', methods=['POST'])
@cross_origin()
@token_required
@check_confirmed
def bookProduct(current_user, product_id):
    product = Product.query.filter_by(id= product_id).first()
    if country not in product.available_in:
        return jsonify({
            "message": "Product not available in your region"
        })
    booked = Store.query.filter_by(saved=current_user).first()
    already_booked = Store.query.filter_by(saved=current_user).filter_by(stored_data=product.product_name).first()
    if already_booked:
        return jsonify({
            "message": "Product already booked by you"
        })
    if not booked:
        booked = Store(saved=current_user)
        booked.stored_data = product.product_name
        db.session.add(booked)
    booked.stored_data = product.product_name
    if not product:
        return jsonify({
            "message": "Product not found"
        })
    try:
        product.sold = True
        db.session.commit()
        return jsonify({
            "message": "Product has been booked"
            })
    except:
        return jsonify({
            "message": "Problem with our server... Try again"
        }), 500

@auth.route('/api/my/booked')
@cross_origin()
@token_required
@check_confirmed
def myBooked(current_user):
    store = Store.query.filter_by(saved=current_user).all()
    data = []
    for product_id in store:
        products = Product.query.filter_by(product_name=product_id.stored_data).filter(Product.sold == True).all()
        for product in products:
            data.append({
                        'name': product.product_name,
                        'description': product.description,
                        "category": product.category,
                        "price": product.product_price,
                        "varieties": product.varieties,
                        "expires": product.expiry_date,
                        "rate": product.rate
                         })
    return jsonify({
        "data": data,
    }), 200
        

@auth.route('/api/checkout/product', methods=['POST'])
@cross_origin()
def checkoutProduct():
    data = request.get_json()
    product = Product.query.filter_by(product_name = data['name']).first()
    if not product :
        return jsonify({
            "message": "Product not available at the moment"
        })
    if country not in product.available_in:
        return jsonify({
            "message": "Product not available in your region"
        })
    elif product.sold == True:
        return jsonify({
            "message": "Product currently unavailable"
        })
    intent = stripe.PaymentIntent.create(
            amount=product.product_price,
            currency=product.currency
    )
    try:
        return jsonify({
            'clientSecret': intent['client_secret']
            })
    except Exception as e:
        return jsonify(error=str(e)), 403


@auth.route('/api/add/to/cart/<int:product_id>', methods=['POST'])
@cross_origin()
@token_required
@check_confirmed
def addToCart(current_user, product_id):
    product = Product.query.filter_by(id= product_id).first()
    if not product:
        return jsonify({
            "message": "Product is not available at the moment"
        })
    if country not in product.available_in:
        return jsonify({
            "message": "Product not available in your region"
        })
    cart = Store.query.filter_by(saved=current_user).first()
    already_booked = Store.query.filter_by(saved=current_user).filter_by(stored_data=product.product_name).first()
    if already_booked:
        return jsonify({
            "message": "Product already in your cart"
        })
    try:
        if not cart:
            cart = Store(saved=current_user)
            cart.stored_data = product.product_name
            db.session.add(cart)
        cart.stored_data = product.product_name
        db.session.commit()
        return jsonify({
            "message": "Product successfully add to cart"
        })
    except:
        return jsonify({
            "message": Message
        })

@auth.route('/api/my/cart')
@cross_origin()
@token_required
@check_confirmed
def myStore(current_user):
    store = Store.query.filter_by(saved=current_user).all()
    data = []
    for product_id in store:
        products = Product.query.filter_by(product_name=product_id.stored_data).all()
        for product in products:
            data.append({'name': product.product_name,
                         'description': product.description,
                         "category": product.category,
                         "price": product.product_price,
                         "varieties": product.varieties,
                         "expires": product.expiry_date,
                         "rate": product.rate,
                         "currency": product.currency
                         })
    return jsonify({
        "data": data,
    }), 200


@auth.route('/api/remove/from/cart/<int:product_id>', methods=['POST'])
@cross_origin()
@token_required
@check_confirmed
def removeFromCart(current_user, product_id):
    product = Product.query.filter_by(id= product_id).first()
    if not product:
        return jsonify({
                "message": "Product is not available at the moment"
            })
    store = Store.query.filter_by(saved=current_user).filter_by(stored_data=product.product_name).first()
    if not store:
        return jsonify({
            "message": "product not in your cart"
        })
    try:
        db.session.delete(store)
        db.session.commit()
        return jsonify({
            "message": "Product successfully removed from cart"
        })
    except:
        return jsonify({
            "message": Message
        })



@auth.route('/api/rate/product/<int:product_id>', methods=['POST'])
@cross_origin()
def rate(product_id):
    data = request.get_json()
    product = Product.query.filter_by(id= product_id).first()
    if not product:
        return jsonify({
            "message": "product not available"
        })
    try:
        product.rate =product.rate + int(data['rate'])
        db.session.commit()
        return jsonify({
            "message": "Product has been rated"
        })
    except:
        return jsonify({
            "message": Message
        })

@auth.route('/api/add/comment/product/<int:product_id>', methods=['POST'])
@cross_origin()
@token_required
@check_confirmed
def addComment(current_user, product_id):
    data = request.get_json()
    product = Product.query.filter_by(id= product_id).first()
    if not product:
        return jsonify({
            "message": "product not available"
        })
    try:
        comment = Comment(thought=product)
        comment.post = data['post']
        db.session.add(comment)
        db.session.commit()

        return jsonify({
            "message": "Comment on product has been posted "
        })
    except:
        return jsonify({
            "message": Message
        })

@auth.route('/api/comments/product/<int:product_id>')
@cross_origin()
def comments(product_id):
    product = Product.query.filter_by(id= product_id).first()
    comment = Comment.query.filter_by(thought=product).all()
    comment_schema = CommentSchema(many=True)
    result = comment_schema.dump(comment)
    return jsonify({
            "data": result
        }), 200


    
