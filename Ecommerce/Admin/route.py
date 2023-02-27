from flask import *
from Ecommerce.model import *

admin = Blueprint('admin', __name__)


@admin.route('/admin/users', methods=['GET'])
#@admin_required
def get_all_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    result = user_schema.dump(users)
    return jsonify(result)

@admin.route('/admin/users/<int:user_id>', methods=['GET'])
#@admin_required
def get_user_by_id(user_id):
    user = User.query.get_or_404(user_id)
    user_schema = UserSchema()
    result = user_schema.dump(user)
    return jsonify(result)

@admin.route('/admin/users/<int:user_id>/status', methods=['PUT'])
#@admin_required
def update_user_status(user_id):
    user = User.query.get_or_404(user_id)
    new_status = request.json.get('status')
    user.status = new_status
    db.session.commit()
    return jsonify({'message': f'Successfully updated user {user_id} status to {new_status}.'})


@admin.route('/admin/users/<int:user_id>', methods=['DELETE'])
#@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'Successfully deleted user {user_id}.'})


@app.route('/admin/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    if not all(field in data for field in ['name', 'email', 'password']):
        return jsonify({'error': 'Missing fields'}), 400
    new_admin = Admin(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'message': 'New admin registered successfully.'}), 201