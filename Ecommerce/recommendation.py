from flask import *
from Ecommerce import *

def get_user_categories(user_id):
    user = User.query.get(user_id)
    categories = [category.name for category in user.category]
    return categories

# Get the top N most popular products for each category
def get_top_products_for_categories(categories, n):
    top_products = []
    for category in categories:
        category_obj = Category.query.filter_by(name=category).first()
        if category_obj:
            products = Product.query.filter_by(category_id=category_obj.id).order_by(Product.popularity.desc()).limit(n).all()
            top_products.extend(products)
    return top_products

# Generate product suggestions for the user
def generate_product_suggestions(user_id, num_suggestions):
    categories = get_user_categories(user_id)
    top_products = get_top_products_for_categories(categories, num_suggestions)
    return top_products

def get_top_selling_products(num_products):
    products = Product.query.all()
    products.sort(key=lambda x: len(x.orders), reverse=True)
    return products[:num_products]

def get_most_popular_categories(num_categories):
    categories = Category.query.all()
    categories.sort(key=lambda x: x.number_of_visits, reverse=True)
    return categories[:num_categories]

def get_product_revenue(product_id):
    product = Product.query.get(product_id)
    if not product:
        return None
    revenue = 0
    for order in product.orders:
        revenue += order.total_price
    return revenue

def get_orders_for_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return None
    orders = user.orders.all()
    return orders
