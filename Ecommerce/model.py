from datetime import datetime
from flask import *
from Ecommerce import db, login_manager, app
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, ModelSchema



class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(100), nullable=False)
    last_name=db.Column(db.String(100), nullable=False)
    middle_name=db.Column(db.String(100), nullable=True)
    phone_number=db.Column(db.String(100), nullable=False)
    additional_phone_number=db.Column(db.String(100), nullable=True)
    country=db.Column(db.String(100), nullable=False)
    gender=db.Column(db.String(100), nullable=False)
    date_of_birth=db.Column(db.String(100), nullable=False)
    address=db.Column(db.String(100), nullable=True)
    second_address = db.Column(db.String(100), nullable=True)
    email=db.Column(db.String(100), nullable=False, unique=True)
    public_id=db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(100), nullable=False)
    token=db.Column(db.String(10000))
    is_confirmed=db.Column(db.Boolean, nullable=False, default=False)
    is_seller=db.Column(db.Boolean, nullable=False, default=False)
    categories=db.relationship('Category', backref='user', lazy=True)
    likes=db.relationship('Like', backref='user', lazy=True)



class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products = db.relationship('Product', backref='seller', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number_of_visits = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    products = db.relationship('Product', backref='category', lazy=True)

order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.PrimaryKeyConstraint('order_id', 'product_id')
)

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False) #add Unique=True
    products = db.relationship('Product', backref='brand', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100000))
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    likes = db.Column(db.Integer, nullable=False, default=0)
    dislikes = db.Column(db.Integer, nullable=False, default=0)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    orders = db.relationship('Order', backref='products', lazy=True)
    likes = db.relationship('Like', backref='product', lazy=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=True)
    
    def to_dict(self):
            return {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'price': self.price,
                'category': self.category.name,
            }


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='placed')
    shipping_address = db.relationship('ShippingAddress', backref='order', uselist=False)
    #products = db.relationship('Product', secondary=order_product, backref=db.backref('orders_', lazy='dynamic'))

    __table_args__ = (
        db.ForeignKeyConstraint(['product_id'], ['product.id']),
    )


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

class ShippingAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)

    
class AdminSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Admin
        load_instance = True

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class SellerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Seller
        load_instance = True

class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True

class ProductSchema(ModelSchema):
    class Meta:
        model = Product
        load_instance = True

class OrderSchema(ModelSchema):
    class Meta:
        model = Order
        load_instance = True

class ShippingAddressSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ShippingAddress
        load_instance = True

class ReviewSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        load_instance = True

class CartSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cart
        load_instance = True

class CartItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CartItem
        load_instance = True

class PaymentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
        load_instance = True