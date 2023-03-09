from flask import *
from Ecommerce import *
from sklearn.metrics.pairwise import cosine_similarity
from .model import Product, Review
import numpy as np

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




def get_product_ratings():
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
    return product_ratings

def get_product_similarity(product_ratings):
    """
    Computes the cosine similarity between products based on their ratings.
    """
    product_ids = list(product_ratings.keys())
    num_products = len(product_ids)
    max_num_features = max(len(v) for v in product_ratings.values())
    product_similarity = np.zeros((num_products, num_products))
    for i in range(num_products):
        for j in range(num_products):
            if i == j:
                product_similarity[i, j] = 1
            else:
                ratings_i = product_ratings[product_ids[i]]
                ratings_j = product_ratings[product_ids[j]]
                # add zeros to the end of the rating vectors if necessary
                if len(ratings_i) < max_num_features:
                    ratings_i += [0] * (max_num_features - len(ratings_i))
                if len(ratings_j) < max_num_features:
                    ratings_j += [0] * (max_num_features - len(ratings_j))
                similarity = cosine_similarity([ratings_i], [ratings_j])[0][0]
                product_similarity[i, j] = similarity
    return product_similarity, product_ids


def get_top_recommended_products(product_id, product_similarity, product_ids):
    """
    Given a product id, computes the similarity between the product and all other
    products, and returns the top-rated products with the highest similarity scores.
    """
    product_ratings = {product_id: [] for product_id in product_ids}
    for review in Review.query.filter_by(product_id=product_id).all():
        user_id = review.user_id
        for review in Review.query.filter_by(user_id=user_id).all():
            product_ratings[review.product_id].append(review.rating)
    similarity_scores = []
    for i in range(len(product_ids)):
        if product_ids[i] != product_id:
            ratings_i = product_ratings[product_ids[i]]
            similarity_scores.append((product_ids[i], np.mean([product_similarity[i, j] for j in range(len(product_ids)) if product_ids[j] == product_id])))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[:10]
    recommended_products = []
    for product_id, score in similarity_scores:
        product = Product.query.get(product_id)
        recommended_products.append({'id': product.id, 'name': product.name, 'description': product.description})
    return recommended_products
