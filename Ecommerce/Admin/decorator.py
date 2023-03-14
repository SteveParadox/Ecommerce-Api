from functools import wraps
from Ecommerce import app
from Ecommerce.model import Administrator
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity


def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        admin_id = get_jwt_identity()
        admin = Administrator.query.get(admin_id)
        if not admin:
            return jsonify({'error': 'Invalid admin token.'}), 401
        return f(*args, **kwargs)
    return decorated
