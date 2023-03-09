from flask import *
from Ecommerce.model import *
from flask_login import *
from Ecommerce.Users.decorator import token_required
from Ecommerce import db, app
sellers = Blueprint('sellers', __name__)

@sellers.route('/api/sellers/register', methods=['POST'])
@token_required
def register_seller(current_user):
    current_user.is_seller = True
    db.session.add(current_user)
    seller = Seller(user_id=current_user.id)
    db.session.add(seller)
    db.session.commit()
    return jsonify({'message': 'Congratulations, You are now a seller'})


@sellers.route('/api/sellers/products', methods=['POST'])
@token_required
def add_product(current_user):
    if current_user.is_seller:
        name = request.json.get('name')
        description = request.json.get('description')
        price = request.json.get('price')
        quantity = request.json.get('quantity')
        seller_id = current_user.id
        category = Category.query.filter_by(name=request.json.get('category')).first()
        if category:
            product = Product(name=name, description=description, price=price, 
             seller_id=seller_id,quantity = quantity, category_id=category.id) 
            db.session.add(product)
            db.session.commit()
            return jsonify({'message': 'Product added successfully!'}), 201
        else:
             return jsonify({'message': 'Category not found'}), 404
    else:
        return jsonify({'message': 'Only sellers can add products!'}), 401

# Endpoint to get all products of a seller
@sellers.route('/api/sellers/products', methods=['GET'])
@token_required
def get_seller_products(current_user):
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
@sellers.route('/api/seller/products/<int:id>/update', methods=['PUT'])
@token_required
def update_product(current_user, id):
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
@sellers.route('/api/seller/products/<int:id>/delete', methods=['DELETE'])
@token_required
def delete_product(current_user, id):
    if current_user.is_seller:
        product = Product.query.filter_by(id=id, seller_id=current_user.id).first()

        if not product:
            return jsonify({'message': 'Product not found!'}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({'message': 'Product deleted successfully!'}), 200
    else:
        return jsonify({'message': 'Only sellers can delete their products!'}), 401


@sellers.route('/brand/create', methods=['POST'])
@token_required
def create_brand(current_user):
    if not current_user.is_seller:
        return jsonify({'message': 'Unauthorized access'}), 401
        
    data = request.get_json()
    name = data.get('name')
    brand = Brand(name=name)
    db.session.add(brand)
    db.session.commit()
    return jsonify({'message': 'Brand created successfully', 'brand': brand.name})

@sellers.route('/brand/<int:brand_id>/update', methods=['PUT'])
@token_required
def update_brand(current_user, brand_id):
    if current_user.is_seller:
        brand = Brand.query.get_or_404(brand_id)
        data = request.get_json()
        name = data.get('name')
        if name:
            brand.name = name
        db.session.commit()
        return jsonify({'message': 'Brand updated successfully', 'brand': brand.name})

    # if user is not a seller, return an error response
    return jsonify({'error': 'You are not authorized to update a brand.'}), 401


@sellers.route('/brand/<int:brand_id>/delete', methods=['DELETE'])
@token_required
def delete_brand(current_user ,brand_id):
    if current_user.is_seller:
        brand = Brand.query.get_or_404(brand_id)
        db.session.delete(brand)
        db.session.commit()
        return jsonify({'message': 'Brand deleted successfully'})

    # if user is not a seller, return an error response
    return jsonify({'error': 'You are not authorized to delete a brand.'}), 401


@sellers.route('/brand/<int:brand_id>/add/product', methods=['POST'])
@token_required
def create_product(current_user, brand_id):
    if not current_user.is_seller:
        return jsonify({'message': 'Unauthorized access'}), 401
        
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    description = data.get("description")
    quantity = data.get("quantity")
    category_name= data.get("category")
    category = Category.query.filter_by(name=category_name).first()
    if category:
        product = Product(name=name, price=price, brand_id=brand_id,
        quantity=quantity, description=description, 
        category=category, seller_id=current_user.id)
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product created successfully', 'product': {'name': product.name, 'price': product.price}})
    return jsonify({"error": "Category not found"})

@sellers.route('/products/sold', methods=['GET'])
@token_required
def view_sold_products(current_user):
    if current_user.is_seller:
        sold_products = Product.query.join(Order).filter(Order.user_id == current_user.id).all()
        sold_products_data = [{'id': p.id, 'name': p.name, 'price': p.price} for p in sold_products]

        return jsonify({'sold_products': sold_products_data})



@sellers.route('/payment_ledger', methods=['GET'])
@token_required
def payment_ledger(current_user):
    if current_user.is_seller:
        orders = Order.query.filter_by(user_id=current_user.id).all()
        payment_data = []
        for order in orders:
            product = Product.query.filter_by(id=order.product_id).first()
            user = User.query.filter_by(id=order.user_id).first()
            payment_data.append({
                'order_id': order.id,
                'customer_name': f"{user.first_name} {user.last_name}",
                'product_name': product.name,
                'product_quantity': order.quantity,
                'payment_amount': order.total_price,
                'payment_status': order.status
            })

        return jsonify({'payment_ledger': payment_data})
    else:
        abort(403)
