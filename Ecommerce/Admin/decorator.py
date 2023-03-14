from functools import wraps
import secrets
from Ecommerce import app
from Ecommerce.model import Administrator

from flask_jwt import JWT, jwt_required, current_identity


def authenticate(email, password):
    admin = Administrator.query.filter_by(email=email).first()
    if admin and secrets.compare_digest(bcrypt.check_password_hash(admin.password, password), True):
        return admin

def identity(payload):
    admin_id = payload['identity']
    return Administrator.query.get(admin_id)

jwt = JWT(app, authenticate, identity)

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        admin = Administrator.query.filter_by(id=current_identity.id).first()
        if not admin:
            return jsonify({'error': 'Invalid admin token.'}), 401
        return f(*args, **kwargs)
    return decorated
