from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_login import *
from Ecommerce.model import *

main = Blueprint('main', __name__)

@main.route('/')
def x():
    return render_template('index.html', title='My Website', message='Welcome to my website!')



@main.route('/home')
def home():
    user_id = request.headers.get('user_id') or session.get('user_id')
    user_interests = User.query.get_or_404(user_id)
    recommended_products = recommendation_engine.get_recommendations(user_interests)
    latest_products = Product.query.order_by(Product)
    return jsonify({'recommended_products': recommended_products, 
    'latest_products': latest_products})