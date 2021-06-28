import datetime
import os
from flask import *
from Backend.models import *
from Backend import db, bcrypt
from flask_cors import cross_origin
import cloudinary as Cloud  
import cloudinary.uploader
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Backend.config import Config
from Backend.ext import token_required
from Backend.registration.decorator import check_confirmed

product = Blueprint('product', __name__)

Message= "Problem uploading to server... If error persists, Send message to fordstphn@gmail.com to lay complaint"


@product.route('/api/register/product', methods=['POST'])
@cross_origin()
@token_required
@check_confirmed
def regProduct(current_user):
    data = request.get_json()
    name = str(data['product_name']).lower()
    category = str(data['category']).lower()
    price = int(data['price'])
    desc = data['description']
    variety = int(data['variety'])
    expiry_date = data['expiry_date']
    currency = str(data['currency']).lower()
    available_in = data['available_in']
    try:
        product = Product(author=current_user)
        product.product_name = name
        product.category = str(category).lower()
        product.description = desc
        product.product_price = price
        product.description = desc
        product.varieties = variety
        product.expiry_date = expiry_date
        product.currency = currency
        product.available_in = available_in
        db.session.add(product)
        db.session.commit()
        return jsonify({
            "message": "Product added successfully"
        })
    except:
            return jsonify({
                "message": Message
            })


@product.route('/api/products', methods=['GET'])
@cross_origin()
def displayProducts():
    product =Product.query.all()
    product_schema = ProductSchema(many=True)
    result = product_schema.dump(product)
    return jsonify({
        "data": result
    }), 200


@product.route('/api/my/products', methods=['GET'])
@cross_origin()
@token_required
@check_confirmed
def myProducts(current_user):
    product =Product.query.filter_by(author=current_user).all()
    product_schema = ProductSchema(many=True)
    result = product_schema.dump(product)
    return jsonify({
        "data": result,
    }), 200


@product.route('/api/get/product/<int:id>', methods=['GET'])
@cross_origin()
def getProduct(id):
    product = Product.query.get_or_404(id)
    product_schema = ProductSchema()
    result = product_schema.dump(product)
    return jsonify({
        "data": result,
    }), 200

@product.route("/api/product/category", methods=['GET'])
@cross_origin()
def category():
    data = request.get_json()
    ctg = data['category']
    category= str(ctg).lower()
    product = Product.query.filter_by(category=category).all()
    product_schema = ProductSchema(many=True)
    result = product_schema.dump(product)
    return jsonify({
        "data": result
    }), 200

@product.route('/api/search/product')
@cross_origin()
def search():
    data = request.get_json()
    pass

@product.route("/api/product/country", methods=['GET'])
@cross_origin()
def searchCountry():
    try:
        data = request.get_json()
        countries=[]
        ctg = str(data['country']).lower()
        country= str(ctg.lower())
        product = Product.query.all()
    except:
        return jsonify({
            "message": "Not receiving data 'country' "
        })
    try:
        for i in product:
            if country in i.available_in:
                countries.append({
                    "name":i.product_name,
                    "price":str(i.currency).upper() +' '+ str(i.product_price),
                    "category": i.category,
                    "description": i.description,
                    "available_in": i.available_in,
                    "company name":i.author.company_name
                })
        return jsonify({
            "data": countries
        }), 200
    except:
        return jsonify({
            "message": Message
        })

@product.route("/api/delete/product/<int:id>", methods=['POST'])
@cross_origin()
@token_required
@check_confirmed
def delProduct(current_user, id):
    product = Product.query.get_or_404(id)
    if not product:
        return jsonify({
            "message": "Product does not exist currently"
        })
    if product.author != current_user:
        abort(403)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({
            "message": 'Product has been deleted!'
        })
    except:
        return jsonify({
            "message": Message
        })

@product.route("/api/delete/products", methods=['POST'])
@cross_origin()
@token_required
@check_confirmed
def delAllProduct(current_user):
    product = Product.query.filter_by(author = current_user).all()
    try:
        for i in product:
            if i.author != current_user:
                abort(403)
            db.session.delete(i)
        db.session.commit()
        return jsonify({
            "message": 'Products has been deleted!'
        })
    except:
        return jsonify({
            "message": Message
        })
 

@product.route("/api/product/<int:id>/update", methods=['POST'])
@cross_origin()
@token_required
@check_confirmed
def updateProduct(current_user, id):
    data= request.get_json()
    product = Product.query.get_or_404(id)
    if not product:
        return jsonify({
            "message": "Product currently unavailable"
        })
    if product.author != current_user:
        abort(403)
    if product.sold != True:
        for i in range(0, len(data)):
            print(data)
        db.session.commit()
        return jsonify(
            {"message":'Your product has been updated!'}
            )
    return jsonify({
        "message": "Product already sold or not available currently"
    })



@product.route("/api/product/update", methods=['POST'])
@cross_origin()
@token_required
@check_confirmed
def updateAllProduct(current_user):
    data= request.get_json()
    product = Product.query.filter_by(author=current_user).all()
    if product.author != current_user:
        abort(403)
    for i in product:
        if i.sold != True:
            i.product_name = data['product_name']
            i.price= data['price']
            i.category = data['category']
            i.description = data['description']
            i.varieties = data['variety']
            db.session.commit()
            return jsonify(
                {"message":'Your product has been updated!'}
                )
        return jsonify({
            "message": "Error"
        })


