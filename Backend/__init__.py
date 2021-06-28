import datetime
from flask import *
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from Backend.config import Config
from flask_profiler import Profiler

app= Flask(__name__)
app.config.from_object(Config)
app.config['DEBUG'] = True
app.config['flask_profiler']={
	"enabled":app.config['DEBUG'],
	"storage":{
		"engine": "sqlite"	
	},
	"basicAuth":{
	"enabled": True,
	"username": "admin",
	"password": "admin"
	}
}

bcrypt= Bcrypt()
jwt= JWTManager()
mail = Mail()
ma = Marshmallow()
db = SQLAlchemy()
io = SocketIO()
profiler = Profiler()


def create_app(config_class=Config):
    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    io.init_app(app)
    jwt.init_app(app)
    profiler.init_app(app)


    from Backend.authorization.routes import auth
    from Backend.product.routes import product
    from Backend.registration.routes import reg

    app.register_blueprint(auth)
    app.register_blueprint(product)
    app.register_blueprint(reg)

    @app.cli.command()
    def routes():
        """'Display registered routes"""
        rules = []
        for rule in app.url_map.iter_rules():
            methods = ','.join(sorted(rule.methods))
            rules.append((rule.endpoint, methods, str(rule)))

        sort_by_rule = operator.itemgetter(2)
        for endpoint, methods, rule in sorted(rules, key=sort_by_rule):
            route = '{:50s} {:25s} {}'.format(endpoint, methods, rule)
            print(route)
        

    return app





