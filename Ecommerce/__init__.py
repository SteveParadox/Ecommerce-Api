import datetime
from flask import *
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from Ecommerce.config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
login_manager = LoginManager()
jwt = JWTManager()

    
def create_app(config_class=Config):
    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    from Ecommerce.Users.route import users
    from Ecommerce.Users.Seller.route import sellers
    from Ecommerce.Products.route import product
    from Ecommerce.Home.route import main
    from Ecommerce.Admin.route import admin
    from Ecommerce.Payment.route import payment
    from Ecommerce.Errors.handlers_api import errors

    app.register_blueprint(users)
    app.register_blueprint(product)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(payment)
    app.register_blueprint(errors)
    app.register_blueprint(sellers)

    return app
