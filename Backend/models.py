from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from marshmallow_sqlalchemy import ModelSchema
from Backend import db, jwt, app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    country = db.Column(db.String(60), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    product = db.relationship('Product', backref='author', lazy=True)
    logged_in = db.Column(db.Integer, default=0)
    save_ = db.relationship('Store', backref='saved', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id, 'user_email': self.email}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.company_name}','{self.email}'),'{self.confirmed}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(25), nullable=False)
    category = db.Column(db.String(25), nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(150), unique=True, nullable=False)
    currency = db.Column(db.String(5),  default='usd')
    varieties = db.Column(db.Integer, nullable=False, default=1)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    sold = db.Column(db.Boolean, nullable=False, default=False)
    faulty = db.Column(db.Boolean, default=False)
    expiry_date = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rate = db.Column(db.Integer, default=0)
    comment = db.relationship('Comment', backref='thought', lazy=True)
    customer = db.relationship('Customer', backref='location', lazy=True)
    available_in = db.Column(db.JSON)
    

    def __repr__(self):
        return f"Product('{self.product_name}', '{self.description}'), '{self.sold}')"

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


class Authorization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stored_data = db.Column(db.String(100))
    time_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
 

 
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(100))
    time_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


class UserSchema(ModelSchema):
    class Meta:
        model = User

class CommentSchema(ModelSchema):
    class Meta:
        model = Comment

class ProductSchema(ModelSchema):
    class Meta:
        model = Product


class StoreSchema(ModelSchema):
    class Meta:
        model = Store