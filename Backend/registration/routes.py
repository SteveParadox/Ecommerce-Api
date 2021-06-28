import datetime
import os
import jwt
import json
from flask import *
from Backend.models import User,UserSchema,Product,ProductSchema
from Backend import db, bcrypt
from flask_cors import cross_origin
import cloudinary as Cloud  
import cloudinary.uploader
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Backend.config import Config

from Backend.registration.decorator import check_confirmed
from Backend.registration.email import send_email
from Backend.registration.token import generate_confirmation_token, confirm_token
from Backend.registration.utils import send_reset_email
from Backend.ext import token_required

reg = Blueprint('registration', __name__)
  


@reg.route('/home')
def home():
    return jsonify({
	"message":"Trash"
    })
   

@reg.route('/user')
def allUsers():
    user= User.query.all()
    user_schema = UserSchema(many=True)
    result = user_schema.dump(user)
    return jsonify({
        "data": result,
    }), 200

@reg.route('/test')
@token_required
#@check_confirmed
def test(current_user):

    return jsonify({
        "message": "verified"
    })



@reg.route('/confirm/token/<current_user>')
@cross_origin()
def confirm_email(current_user):
    token= current_user
    try:
        email = confirm_token(token)
    except: 
        return jsonify({"message":'The confirmation link is invalid or has expired.'})
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        return jsonify({"message": 'Account already confirmed. Please login.'})
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": 'Your account has been confirmed. Thanks!'})

@reg.route('/api/register/brand', methods=['POST'])
@cross_origin()
def regBrand():
    data = request.get_json()
    name = data['company_name']
    email = data['email']
    password = data['password']
    country = str(data['country']).lower()
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({
                "message" : 'This email is already taken by another user, Please try another one.'
                })
    try:
        user = User()
        user.company_name = str(name[0]).upper()+name[1:]
        user.email = str(email).lower()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.password = hashed_password
        user.country= country
        user.confirmed = False
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify({
            "message": "Problem adding information to database, if such error persists, send message to fordstphn@gmail.com to lay complaint"
        })
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('registration.confirm_email', current_user=token, _external=True)
    html = render_template('confirm_url.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(user.email, subject, html)
    
    return jsonify({
        "status ": "success",
        "message": "User added successfully, Please Verify Account",
        "token": token,
        "url": confirm_url,
        "verify Mail": 'A confirmation email has been sent via email.'
    
}), 201
    
@reg.route('/api/login/account', methods=['POST'])
@cross_origin()
def logInAccount(expires_sec=30):
    data = request.get_json()
    try:
        email = data['email']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            user.logged_in =  user.logged_in + 1
            db.session.commit()
            payload= {
                    "id": user.id,  
                    "name": user.company_name,
                    'exp' : datetime.datetime.now() + datetime.timedelta(minutes = 1),
                    "email": user.email
                }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
            data = jwt.decode(token, Config.SECRET_KEY, algorithms="HS256")
            return jsonify({'token' : token.decode('UTF-8'),
            "name":data['name'], "email": data['email'], "expires": data['exp']} ), 201
        return jsonify({
            "message":
                'Could not verify user'}, 401)
                
    except:
        return jsonify({
            "message": 'Sorry there is error on our end'},
                500)
   